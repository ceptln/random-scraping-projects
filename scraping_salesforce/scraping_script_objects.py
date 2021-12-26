# -*- coding: utf-8 -*-

"""
Created on Dec 28 08:02:41 2019
@author: ceptln
"""

# Python frameworks imports
import pandas as pd
import json
import requests
from lxml import html

## All I do here is to load the “html_content“ variable with the html content of the first - it works

# Extract the page content and parsing the json content

url = "https://developer.salesforce.com/docs/get_document/atlas.en-us.api.meta"
response = requests.get(url)
parsed = json.loads(response.content)

# Get the list of the Standard Objects dictionnaries

std_obj_list = parsed['toc'][1]['children'][1]['children']

# Create the list of all the Standard Objects url and a list of all the get_content pages

url_list = []
getcontent_url_list = []

for i in range(len(std_obj_list)):
    url_end = std_obj_list[i]['a_attr']['href']
    
    url = 'https://developer.salesforce.com/docs/atlas.en-us.api.meta/api/'+url_end
    url_list.append(url)
    
    getcontent_url = 'https://developer.salesforce.com/docs/get_document_content/api/'+url_end+'/en-us/228.0'
    getcontent_url_list.append(getcontent_url)

error_url = []
df_objects = pd.DataFrame(columns=['ObjectName', 'Summary', 'Supported Calls','Special Access Rules','Usage','Associated Objects','Additional Considerations and Related Objects'])

for url in getcontent_url_list:
    # Try operator to avoid IndexError that'd raise if an object page doesn't render
    try :
        gc_content = requests.get(url)
        json_content = json.loads(gc_content.content)
        html_content = json_content['content']

        ## Cleane the html code
        # Removed the span[@class='keyword parmname'] because wouldn't get “Comment“ in the Description of the Field Name “Response“
        # Removed the <samp class="codeph nolang"> because wouldn't get the Supported Calls otherwise
        html_content_1 = html_content.replace('<span class="keyword parmname">', "")
        html_content_2 = html_content_1.replace('</span>', "")
        html_content_3 = html_content_2.replace('\n            ', " ")
        html_content_4 = html_content_3.replace('<samp class="codeph nolang">','')
        html_content_5 = html_content_4.replace('</samp>','')
        html_content_6 = html_content_5.replace('\n   ','')
        html_content_7 = html_content_6.replace('       ','')
        html_content_8 = html_content_7.replace('\t','')
        html_content_9 = html_content_8.replace('\n',' ')
        html_content_clean = html_content_9.replace('\n           ',' ')


        # Import lxml and creating a tree
        from lxml import html
        tree = html.fromstring(html_content_clean)

        # Extract the name of the standard object
        object_name_list = tree.xpath('//span[@id="topic-title"]/text()')
        # Try different xpaths to match all patterns found in the html code
        if len(object_name_list) > 0:
            object_name = object_name_list[0]
        else: 
            object_name_list = tree.xpath('//h1[@class="helpHead1"]/text()')
            object_name = object_name_list[0]

        # Extract the description of the standard object
        summary_list = tree.xpath('//span[@id="summary"]/text()')
        # Try different xpaths to match all patterns found in the html code
        if len(summary_list) > 0:
            summary = summary_list[0]
        else:
            summary_list = tree.xpath('//span[@id="summary"]/span/text()')
            summary = summary_list[0]

        # Extract the Supported Calls of the standard object
        supported_calls_list = tree.xpath('//div[@class="section" and ./h2/text()="Supported Calls"]/p/text()')
        # Try different xpaths to match all patterns found in the html code
        if len(supported_calls_list)>0: 
            supported_calls = supported_calls_list[0]
        else: supported_calls = None


        # Extract the Special Access Rules of the standard object
        special_access_rules_list = tree.xpath('//div[@class="section" and ./h2/text()="Special Access Rules"]/p/text()')
        # Try different xpaths to match all patterns found in the html code
        if len(special_access_rules_list)>0: 
            special_access_rules = special_access_rules_list[0]
        else: 
            special_access_rules_list = tree.xpath('//div[@class="section" and ./h2/text()="Special Access\nRules"]/p/text()')
            if len(special_access_rules_list)>0:
                special_access_rules = special_access_rules_list[0]
            else: special_access_rules = None

        # Extract the Usage of the standard object
        usage_list = tree.xpath('//div[@class="section" and ./h2/text()="Usage"]/p/text()')
        if len(usage_list)>0: 
            usage = usage_list[0]
        else: 
            usage_list = tree.xpath('//div[@class="section" and ./h2/text()=" Usage"]/p/text()')
            if len(usage_list)>0:
                usage = usage_list[0]
            else : 
                usage_list = tree.xpath('//div[@class="section" and ./h2/text()="Usage"]/div/text()')
                if len(usage_list)>0:
                    usage = usage_list[0]
                else : usage = None
            

        # Extract the Associated Objects of the standard object
        associated_objects_list = tree.xpath('//div[@class="section" and ./h2/text()="Associated Objects"]/p/text()')
        if len(associated_objects_list)>0: 
            associated_objects = associated_objects_list[0]
        else: associated_objects = None

        # Extract the Additional Considerations and Related Objects of the standard object
        additional_considerations_list = tree.xpath('//div[@class="section" and ./h2/text()="Additional Considerations and Related Objects"]/p/text()')
        if len(additional_considerations_list)>0: 
            additional_considerations = additional_considerations_list[0]
        else: additional_considerations = None

        # Creat a dictionnary with all the scraped elements
        info_dict = {'ObjectName':object_name,'Summary':summary,'Supported Calls':supported_calls,'Special Access Rules':special_access_rules,'Usage':usage,'Associated Objects':associated_objects,'Additional Considerations and Related Objects':additional_considerations}
        # Add a new row to the “Objects dataframe“. 
        df_objects = df_objects.append(info_dict, ignore_index=True)
       
    # Keep all the error url to come back to them later
    except IndexError :
        error_url.append(url)
        


