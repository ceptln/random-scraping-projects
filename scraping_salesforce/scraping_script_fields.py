# -*- coding: utf-8 -*-

"""
Created on Dec 26 10:23:00 2019
@author: ceptln
"""


# Load first page content
url = 'https://developer.salesforce.com/docs/atlas.en-us.220.0.api.meta/api/sforce_api_objects_acceptedeventrelation.htm'
emplacement_du_driver="/Users/macbook16decamille/chromedriver"
driver = webdriver.Chrome(emplacement_du_driver)
driver.get(url)

# Accept cookies and closing footer
time.sleep(4)
driver.find_element_by_css_selector("button#onetrust-accept-btn-handler").click()
time.sleep(2)
driver.find_element_by_css_selector("img.close-icon").click()

# Get the list of all the pages of the current version
liste_of_url_key=[]
for el in driver.find_elements_by_css_selector("span.ng-binding.ng-scope") :
    liste_of_url_key.append(el.text)

# Create the list of all the url to scrape
idx=liste_of_url_key.index("AcceptedEventRelation")
idx2=liste_of_url_key.index("WorkTypeGroupMember")
liste_of_url_key=liste_of_url_key[idx:idx2]
for idx,url in enumerate(liste_of_url_key) : 
    liste_of_url_key[idx]=url.lower()

# Create the 'Fields' dataframe
df_fields = pd.DataFrame(columns=['ObjectName', 'FieldName', 'Type','Properties','Description'])
error_list = []

# For loop to go through the url list
for url_key in liste_of_url_key[0:10]:
    url = "https://developer.salesforce.com/docs/atlas.en-us.220.0.object_reference.meta/object_reference/sforce_api_objects_"+url_key+".htm"
    driver.get(url)
    time.sleep(2)
    soup = BeautifulSoup(driver.page_source, 'lxml')
    try :
        # Extract Object Name
        object_name_html = soup.select('span[id="topic-title"]')
        if len(object_name_html)>0:
            object_name = object_name_html[0].text
        else : 
            object_name_html = soup.select('h1[class="helpHead1"]') 
            object_name = object_name_html[0].text

        # Extract the fields' names 
        field_names_html = soup.select('tr > td[data-title="Field Name"]')
        if len(field_names_html) == 0 : field_names_html = soup.select('tr > td[data-title="Field"]')
        if len(field_names_html) == 0 : field_names_html = soup.select('tr > td[data-title="Name"]')
        field_names_list = []
        for i in range(len(field_names_html)):
            field_names = field_names_html[i].text
            field_names_clean = field_names.replace('\n','')
            field_names_list.append(field_names_clean)

        # Extract the details and create a dictionnary for each field
        field_details_html = soup.select('tr > td[data-title="Details"]')
        field_details_list = []
        for i in range(len(field_details_html)):
            field_details = field_details_html[i].text
            field_details.replace('\n','')
            if 'Type' in field_details and 'Properties'in field_details and 'Description'in field_details: 
                # Split and join the elements together
                field_split = field_details.split()
                type_index = field_split.index('Type')+1
                properties_index = field_split.index('Properties')+1
                description_index = field_split.index('Description')+1
                field_type = ' '.join(field_split[type_index:properties_index-1])
                field_properties = ' '.join(field_split[properties_index:description_index-1])
                field_description = ' '.join(field_split[description_index:])
                # Create a dictionnary with each field elements
                details_dict = {'ObjectName':object_name,'FieldName':field_names_list[i],'Type':field_type,'Properties':field_properties,'Description':field_description}
            else:
                details_dict = {'ObjectName':object_name,'FieldName':field_names_list[i],'Type':None,'Properties':None,'Description':None}
            field_details_list.append(details_dict) 

        df_fields = df_fields.append(field_details_list, ignore_index=True)
    except IndexError :
        error_list.append(url)