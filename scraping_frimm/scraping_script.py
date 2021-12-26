# -*- coding: utf-8 -*-

"""
Created on Feb 3 09:58:31 2020

@author: ceptln
"""

# Importing recquired packages
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import pandas as pd

# Locating the driver
driver_location = "/Users/camilleepitalon/chromedriver"
driver = webdriver.Chrome(driver_location)

# Activating the driver on frimm landing page
driver.get('https://www.frimm.com/index.php?ac=frimm_cerca_agenzia_immobiliare')

# Creating the list of cities 
cities_list = ['Roma', 'Milano', 'Napoli', 'Torino', 'Palermo','Bologna, BO']

df = pd.DataFrame(columns=['Title','Agency_ID','Street','Zip_Code','City','Zone','Phone','Email','Website'])

for city in cities_list:

    # Starting research
    driver.find_element_by_xpath("//input[@class='search__input pac-target-input']").clear()
    driver.find_element_by_xpath("//input[@class='search__input pac-target-input']").send_keys(city,Keys.ENTER)
    time.sleep(3)

    
    # Getting the number of results pages
    number_of_pages_text = driver.find_element_by_xpath("//span[@id='totale_risultati_1']").text
    number_of_pages = int(number_of_pages_text[-1])
    
    # Getting all results of the research
    for i in range(number_of_pages-1):
        driver.find_element_by_xpath("//a[text()='Mostra ulteriori risultati']").click()
        time.sleep(2)
    
    # Extracting all boxes
    boxes_list = driver.find_elements_by_xpath('//div[@class="media-body"]')

    for box in boxes_list:
        text = box.text
        text_splited = text.split('\n')

        # Agency name and ID
        title = text_splited[0]
        agency_id = int(text_splited[1].replace('ID:',''))

        #Address elements
        address_list = text_splited[2].split(' | ')
        street = address_list[0]
        if len(address_list) == 4:
            zip_code = address_list[1]
            city = address_list[2]
            zone = address_list[3][6:]
        elif len(address_list) == 2:
            zip_code = None
            city = address_list[1]
            zone = None

        # Agency contact elements
        contact_list = text_splited[3].split('  ')
        if len(contact_list) == 3:
            phone = contact_list[0][1:]
            email = contact_list[1]
            website = contact_list[2]
        elif len(contact_list) == 2:
            phone = contact_list[0][1:]
            if '@' in contact_list[1]:
                email = contact_list[1]
                website = None
            elif 'www' in contact_list[1]:
                email = None
                website = contact_list[1]
            else :
                email = None
                website = None

        box_dict = {'Title':title,'Agency_ID':agency_id,'Street':street,'Zip_Code':zip_code,'City':city,'Zone':zone,'Phone':phone,'Email':email,'Website':website}
        df = df.append(box_dict, ignore_index=True)
        
df.to_csv(r'/Users/camilleepitalon/Documents/Work/scraping/frimm_data.csv', index = False)