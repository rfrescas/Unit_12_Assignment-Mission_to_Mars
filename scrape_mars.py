from bs4 import BeautifulSoup
import pandas as pd
from splinter import Browser
import time


def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {
        'executable_path': '/Users/2fresh/Desktop/Working Repo & Notes/1) Homework Working Repo/Unit 12/Instructions/chromedriver'}
    return Browser('chrome', **executable_path, headless=False)


def scrape():
    browser = init_browser()
    mars_scraped_final = {}

    # Mars scraping for top title article with title and paragraph
    url_mars = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'
    browser.visit(url_mars)
    browser.is_element_present_by_tag('div', wait_time=2)
    html_mars = browser.html
    soup_mars = BeautifulSoup(html_mars, 'lxml')
    news_title = soup_mars.find('div', class_='content_title').text
    news_paragraph = soup_mars.find('div', class_='article_teaser_body').text
    mars_scraped_final['news_title'] = news_title
    mars_scraped_final['news_paragraph'] = news_paragraph

    # JPL scraping for featured Mars image
    url_jpl = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url_jpl)
    browser.is_text_present('FULL IMAGE', wait_time=2)
    browser.click_link_by_partial_text('FULL IMAGE')
    browser.is_element_present_by_css('fancybox-image', wait_time=2)
    html_jpl = browser.html
    soup_jpl = BeautifulSoup(html_jpl, 'lxml')
    image_location = soup_jpl.find(
        'img', class_='fancybox-image')['src'].strip()
    featured_image_url = 'https://www.jpl.nasa.gov' + image_location
    mars_scraped_final['featured_image_url'] = featured_image_url

    # Scrape weather for Mars from their twitter account
    url_mars_weather = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(url_mars_weather)
    browser.is_element_present_by_tag('p', wait_time=2)
    html_mars_weather = browser.html
    soup_mars_weather = BeautifulSoup(html_mars_weather, 'lxml')
    tweets = soup_mars_weather.find_all(
        'p', class_='TweetTextSize TweetTextSize--normal js-tweet-text tweet-text')
    for tweet in tweets:
        try:
            mars_weather = tweet.text.replace('\n', '').split("pic")[0]
            if "InSight" in mars_weather:
                break
        except:
            pass
    mars_scraped_final["mars_weather"] = mars_weather

    # Scrape Mars Facts page using Pandas
    url_facts = 'https://space-facts.com/mars/'
    tables = pd.read_html(url_facts)
    df = tables[0]
    df.columns = ['title', 'value']
    html_facts = df.to_html()
    html_facts = html_facts.replace('\n', '')
    mars_scraped_final['mars_facts'] = html_facts

    # Scrape Mars Astrogeology Science Center for images
    url_mars_weather = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url_mars_weather)
    browser.is_element_present_by_tag('div', wait_time=2)
    html_mars_hemisphere = browser.html
    soup_mars_hemisphere = BeautifulSoup(html_mars_hemisphere, 'lxml')

    hemisphere_image_urls = []
    hemisphere_titles = soup_mars_hemisphere.find_all('div', class_='item')

    for x in hemisphere_titles:
        url_mars_weather = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
        browser.visit(url_mars_weather)
        html_mars_hemisphere = browser.html
        soup_mars_hemisphere = BeautifulSoup(html_mars_hemisphere, 'lxml')
        browser.is_text_present('Hemisphere Enhanced', wait_time=2)
        title = x.find('h3').text

        browser.click_link_by_partial_text(title)
        browser.is_text_present('Hemisphere Enhanced', wait_time=2)

        html_mars_hemisphere = browser.html
        soup_mars_hemisphere = BeautifulSoup(html_mars_hemisphere, 'lxml')

        partial_img = soup_mars_hemisphere.find(
            'img', class_="wide-image")['src']
        img = 'https://astrogeology.usgs.gov' + partial_img

        hemisphere_image_urls.append({"title": title, "img_url": img})

    # add the final piece of data to input into Mongo
    mars_scraped_final['hemisphere_title_url'] = hemisphere_image_urls

    # scraping is done so closing out the connection
    browser.quit()

    return mars_scraped_final


if __name__ == "__main__":
    mars_scraped_final = scrape()
    print(mars_scraped_final)
