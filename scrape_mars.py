# Declare Dependencies 
from bs4 import BeautifulSoup as bs
from splinter import Browser
import pandas as pd
import GetOldTweets3 as got
import os
import time
import requests
import warnings
warnings.filterwarnings('ignore')

def init_browser():
    executable_path = {"executable_path": "chromedriver"}
    return Browser("chrome", **executable_path, headless=False)

# Create Mission to Mars global dictionary that can be imported into Mongo
mars_info = {}

# NASA MARS NEWS
def scrape_mars_news():

            # Initialize browser 
        browser = init_browser()

        url = 'https://mars.nasa.gov/news/'
        
        browser.visit(url)

        time.sleep(5)

        html = browser.html

        soup = bs(html, 'lxml')

        list_text = soup.find('div', class_='list_text')

        news_title = list_text.find('div', class_='content_title').text

        news_p = soup.find('div', class_='article_teaser_body').text

        mars_info['News_Title'] = news_title

        mars_info['News_Paragraph'] = news_p

        return mars_info

        browser.quit()
        




# FEATURED IMAGE
def scrape_mars_image():

            # Initialize browser 
        browser = init_browser()

        url2 = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
        browser.visit(url2)

        time.sleep(5)

        html2 = browser.html

        soup = bs(html2, 'lxml')

        find_url = soup.find('div', class_ = 'carousel_items')

        url_ending  = find_url.find('article')['style'].replace('background-image: url(','')
        url_ending2 = url_ending.replace(');', '')[1:-1]

        
        url3 = "https://www.jpl.nasa.gov"

        featured_image_url = url3 + url_ending2

        featured_image_url

        mars_info['Featured_URL'] = featured_image_url

        

        
        return mars_info

        browser.quit()

        

        

# Mars Weather 
def scrape_mars_weather():

        # Initialize browser 
        ##browser = init_browser()

        #browser.is_element_present_by_css("div", wait_time=1)
        text_query = 'InSight: sol 549'
        count = 10

        tweetCriteria = got.manager.TweetCriteria().setQuerySearch(text_query)\
                                                    .setMaxTweets(count)

        tweets = got.manager.TweetManager.getTweets(tweetCriteria)

        text_tweets = [[tweet.date, tweet.text] for tweet in tweets]

        # Creation of dataframe from tweets
        tweets_df = pd.DataFrame(text_tweets, columns = ['Datetime', 'Text'])

        marsw=tweets_df['Text'].iloc[3]

        mars_info['mars_weather'] = marsw

        

        return mars_info

        browser.quit()
        
# Mars Facts
def scrape_mars_facts():

        # Initialize browser 
        browser = init_browser()



        url5 = 'https://space-facts.com/mars/'

        browser.visit(url5)

        time.sleep(5)


        data = pd.read_html(url5)

        df = data[0]

        df.rename(columns={0: 'Parameter', 1: 'Value'}, inplace=True)

        table_html = df.to_html()

        table_html2 = table_html.replace('\n', '')

        mars_info['Mars_Facts'] = table_html2

        return mars_info

        browser.quit()

# Mars Hemisphere

def scrape_mars_hemispheres():

        # Initialize browser 
        browser = init_browser()

        url5 = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
        browser.visit(url5)

        time.sleep(5)

        html4 = browser.html

        soup = bs(html4,'lxml')

        objects = soup.find_all('div', class_='item')

        img_url_ending = []

        hemisphere_image_urls = []

        url6 ='https://astrogeology.usgs.gov'

        for object in objects:
            img_url_ending = object.find('a', class_='itemLink product-item')['href']
            title=object.find('h3').text
            img_url = url6 + img_url_ending
            browser.visit(img_url)
            html5 = browser.html
            soup = bs(html5, 'lxml')
            hemisphere_image_urls.append({"title" : title, "img_url" : img_url})

        mars_info['Hemisphere_Image_URLs'] = hemisphere_image_urls
            
         

        return mars_info

        browser.quit()