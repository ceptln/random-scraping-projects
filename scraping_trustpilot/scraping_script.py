# -*- coding: utf-8 -*-

"""
Created on Jun 14 11:30:12 2020
@author: ceptln
"""

# Import recquired packages
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import pandas as pd

# Locate the driver
driver_location = "/Users/macbook16decamille/Documents/Python/chromedriver"
driver = webdriver.Chrome(driver_location)

# Activate the driver on frimm landing page
driver.get('https://www.trustpilot.com/review/papernest.es')
time.sleep(3)

# Close the cookies pop-up banner
driver.find_element_by_xpath("//button[text()='I accept']").click()

# Create lists to store scraped data
name_list = []
date_list = []
location_list = []
rate_list = []
title_list = []
review_list = []

# Scrap reviewers' name
name_elements = driver.find_elements_by_xpath('//div[@class="consumer-information__name"]')
for name in name_elements:
    name_list.append(name.text)

# Scrap date of review
date_elements = driver.find_elements_by_xpath('//time')
for date in date_elements:
    date_list.append(date.get_attribute('datetime'))
    
# Scrap reviewers' location
location_elements = driver.find_elements_by_xpath('//div[@class="consumer-information__location"]/span')
for loc in location_elements:
    location_list.append(loc.text)

# Scrap rate/score
rate_elements = driver.find_elements_by_xpath('//div[@class="star-rating star-rating--medium"]/img')
for rate in rate_elements:
    rate_list.append(rate.get_attribute('alt'))

# Scrap the review itself
content_elements = driver.find_elements_by_xpath("//div[@class='review-content__body']")
for content in content_elements:
    text = content.text
    split_text = text.split('\n')
    if len(split_text)<2 :
        title = split_text[0]
        review = '-'
    else :
        title = split_text[0]
        review = ''.join(split_text[1:]) 
    title_list.append(title)
    review_list.append(review)

# Merge the results in a dictionary
dict = {'Date' : date_list, 'Location' : location_list, 'Reviewer': name_list, 'Score': rate_list, 'Title': title_list, 'Review' : review_list}

# Turn the dictionary into a dataframe
df = pd.DataFrame(dict)

df.to_csv(r'/Users/camilleepitalon/Documents/scraping/trustpilot_esp_data.csv', index = False)
