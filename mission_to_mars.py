#!/usr/bin/env python
# coding: utf-8

# In[1]:


from bs4 import BeautifulSoup
import pandas as pd
from splinter import Browser
import time


# In[2]:


executable_path = {
    'executable_path': '/Users/2fresh/Desktop/Working Repo & Notes/1) Homework Working Repo/Unit 12/Instructions/chromedriver'}
browser = Browser('chrome', **executable_path, headless=False)


# In[3]:


# Mars scraping for top title article with title and paragraph
url_mars = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'
browser.visit(url_mars)
browser.is_element_present_by_tag('div', wait_time=2)


# In[4]:


html_mars = browser.html


# In[5]:


soup_mars = BeautifulSoup(html_mars, 'lxml')


# In[6]:


news_title = soup_mars.find('div', class_='content_title').text
news_title


# In[7]:


news_paragraph = soup_mars.find('div', class_='article_teaser_body').text
news_paragraph


# In[8]:


# JPL scraping for featured Mars image
url_jpl = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
browser.visit(url_jpl)
browser.is_text_present('FULL IMAGE', wait_time=2)
browser.click_link_by_partial_text('FULL IMAGE')
browser.is_element_present_by_css('fancybox-image', wait_time=2)


# In[9]:


html_jpl = browser.html


# In[10]:


soup_jpl = BeautifulSoup(html_jpl, 'lxml')


# In[11]:


image_location = soup_jpl.find('img', class_='fancybox-image')['src'].strip()
image_location


# In[12]:


featured_image_url = 'https://www.jpl.nasa.gov' + image_location
featured_image_url


# In[13]:


# Scrape weather for Mars from their twitter account
url_mars_weather = 'https://twitter.com/marswxreport?lang=en'
browser.visit(url_mars_weather)
browser.is_element_present_by_tag('p', wait_time=2)


# In[14]:


html_mars_weather = browser.html


# In[15]:


soup_mars_weather = BeautifulSoup(html_mars_weather, 'lxml')


# In[16]:


tweets = soup_mars_weather.find_all(
    'p', class_='TweetTextSize TweetTextSize--normal js-tweet-text tweet-text')


# In[17]:


for tweet in tweets:
    try:
        mars_weather = tweet.text.replace('\n', '').split("pic")[0]
        if "InSight" in mars_weather:
            break
    except:
        pass

mars_weather


# In[18]:


# Scrape Mars Facts page using Pandas
url_facts = 'https://space-facts.com/mars/'


# In[19]:


tables = pd.read_html(url_facts)
tables


# In[20]:


df = tables[0]
df.columns = ['title', 'value']


# In[21]:


df.head()


# In[22]:


html_facts = df.to_html()
html_facts


# In[23]:


html_facts = html_facts.replace('\n', '')


# In[24]:


html_facts


# In[25]:


# Scrape Mars Astrogeology Science Center for images
url_mars_weather = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
browser.visit(url_mars_weather)
browser.is_element_present_by_tag('div', wait_time=2)


# In[26]:


html_mars_hemisphere = browser.html


# In[27]:


soup_mars_hemisphere = BeautifulSoup(html_mars_hemisphere, 'lxml')


# In[28]:


# Scrape Mars Astrogeology Science Center for images

hemisphere_image_urls = []
hemisphere_titles = soup_mars_hemisphere.find_all('div', class_='item')

for x in hemisphere_titles:
    url_mars_weather = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url_mars_weather)
    html_mars_hemisphere = browser.html
    soup_mars_hemisphere = BeautifulSoup(html_mars_hemisphere, 'lxml')
    browser.is_text_present('Hemisphere Enhanced', wait_time=2)
    title = x.find('h3').text
#     assert browser.find_link_by_partial_text('Hemisphere Enhanced')
#     browser.click_link_by_partial_text('Hemisphere Enhanced')
    browser.click_link_by_partial_text(title)
    browser.is_text_present('Hemisphere Enhanced', wait_time=2)

    html_mars_hemisphere = browser.html
    soup_mars_hemisphere = BeautifulSoup(html_mars_hemisphere, 'lxml')

    partial_img = soup_mars_hemisphere.find('img', class_="wide-image")['src']
    img = 'https://astrogeology.usgs.gov' + partial_img

    hemisphere_image_urls.append({"title": title, "img_url": img})


#     hemisphere_image_urls_test["image"] = soup_mars_hemisphere.find('div', class_="downloads").img['src'].strip()
#     hemisphere_image_urls_test["title"] = soup_mars_hemisphere.find('h2', class_="title").text
#     hemisphere_image_urls_test.update(hemisphere_image_urls_test)

hemisphere_image_urls


# In[29]:


browser.quit()

# add variables and existing dictionary into one dictionary

mars_scraped_data = [
    {"news_title": news_title,
     "news_paragraph": news_paragraph,
     "featured_image_url": featured_image_url,
     "mars_weather": mars_weather,
     "mars_facts": html_facts,
     }
]

# combine all data into one list with dictionary format
mars_scraped_final = mars_scraped_data + hemisphere_image_urls
