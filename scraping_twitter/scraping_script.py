# -*- coding: utf-8 -*-

"""
Created on Oct 21 14:05:46 2020
@author: ceptln
"""

# Import recquired packages
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import pandas as pd

# Locate the driver
# You need to download it first: https://chromedriver.chromium.org/downloads
driver_location = "/Users/macbook16decamille/chromedriver"
driver = webdriver.Chrome(driver_location)

# Activate the driver on filtered twitter research page
# To find the url you want enter your parameters there (https://twitter.com/search-advanced?lang=en) and press OK
driver.get('https://twitter.com/search?lang=en&q=(%23pregnancy)%20until%3A2021-09-29%20since%3A2021-09-01&src=typed_query')
time.sleep(2)

# Create the empty dataframe
df = pd.DataFrame(columns=['name', 'pseudo', 'date', 'tweet', 'interaction'])

for j in range(0,50):
    
    # Scroll manually the results page (otherwise only scraps 8-10 results - ça clc)
    driver.execute_script("window.scrollTo(0,"+str(2000*j)+")")
    time.sleep(3)
    
    # Create a list with the different Selenium objects (= tweets) that we'll parse
    all_tweets = driver.find_elements_by_xpath("//div[@aria-label='Timeline: Search timeline']/div/div")
    
    # Loop over each element to parse it
    for tweet in all_tweets :
        
        # Condition to avoid shit elements which are not tweets ("See more", blabla)
        if len(tweet.text) > 10 : 
            
            # Create an empty list which we'll append to df (adding 1 more row)
            tweet_row = []
            
            # Split the text we get to separate main elements (name, pseudo, blabla)
            split_list = tweet.text.splitlines()
            
            name = split_list[0]
            tweet_row.append(name)
            
            pseudo = split_list[1]
            tweet_row.append(pseudo)
            
            date = split_list[3]
            tweet_row.append(date)
            
            content = " | ".join([i for i in split_list[4:] if len(i)>6])
            tweet_row.append(content)
            
            tweet_row.append(str(sum([int(i) for i in split_list[-3:] if i > "0" and i < '99999999' and len(i)<6]+ [0])))
            
            # Exclude the tweet badly scraped (no content for instance)
            if len(tweet_row)==5 : 
                
                # Appending the new tweet to the dataframe df
                df.loc[len(df)]=tweet_row

# Remove the duplicates (as the scrolling tips I used is not really precise)
df.drop_duplicates()

# Extract the data to a CSV file
df.to_csv(r'/Users/camilleepitalon/Documents/scraping/twitter_pregnancy_data.csv', index = False)