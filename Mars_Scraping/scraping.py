# Import Splinter, BeautifulSoup and Pandas
from splinter import Browser
from bs4 import BeautifulSoup as soup
import pandas as pd
import datetime as dt

def scrape_all():
    # Initiate headless driver for deployment
    browser = Browser("chrome", executable_path="chromedriver", headless=True)
    # Set news title and paragraph variables
    news_title, news_paragraph = mars_news(browser)

    # Running all scraping functions and storing results in dictionary
    data = {
        "news_title": news_title,
        "news_paragraph": news_paragraph,
        "featured_image": featured_image(browser),
        "cerberus_image": cerberus_image(browser),
        "facts": mars_facts(),
        "last_modified": dt.datetime.now()
    }

    # Stop webdriver and return data
    browser.quit()
    return data
    
    # Path to chromedriver
    # get_ipython().system('which chromedriver')
    # Set the executable path and initialize the chrome browser in splinter
    # executable_path = {'executable_path': 'chromedriver'}
    # browser = Browser('chrome', **executable_path)

# Creating function
def mars_news(browser):
    # Scraping Mars News
    # Assign url and instruct the browser to visit it
    url = 'http://mars.nasa.gov/news/'
    browser.visit(url)
    
    # Optional delay for loading the page
    browser.is_element_present_by_css("ul.item_list li.slide", wait_time=1)
    
    # Setting up html parser
    html = browser.html
    news_soup = soup(html, 'html.parser')
    
    # Using try/except for error handling
    try:
        slide_elem = news_soup.select_one('ul.item_list li.slide')
        # Setting up scrape for title
        news_title = slide_elem.find("div", class_="content_title").get_text()
        # Setting up scrape for article summary
        news_p = slide_elem.find('div', class_="article_teaser_body").get_text()
    
    except AttributeError:
        return None, None
    
    return news_title, news_p

# Featured Images

def featured_image(browser):

    # Visit URL
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)
    
    # Find and click the full image button
    full_image_elem = browser.find_by_id('full_image')
    full_image_elem.click()
    
    # Find the more info button and click that
    browser.is_element_present_by_text('more info', wait_time=1)
    more_info_elem = browser.links.find_by_partial_text('more info')
    more_info_elem.click()
    
    # Parse the resulting html with soup
    html = browser.html
    img_soup = soup(html, 'html.parser')
    
    # Add try/except for error handling
    try:
        # Find the relative image url
        img_url_rel = img_soup.select_one('figure.lede a img').get("src")

    except AttributeError:
        return None
    
    # Use the base URL to create an absolute URL
    img_url = f'https://www.jpl.nasa.gov{img_url_rel}'
    
    return img_url

# Cerberus Image
def cerberus_image(browser):

    # Visit URL for Cerberus Hemisphere
    #urlc = 'https://astropedia.astrologeology.usgs.gov/download/Mars/Viking/cerberus_enhanced.tif/full.jpg'
    urlc = 'https://astrology.usgs.gov/search/map/Mars/Viking/cerberus_enhanced'
    browser.visit(urlc)

    # Find and click the full image button
    #full_image_cerberus = browser.find_by_id('wide-image-toggle')
    # full_image_cerberus = browser.find_by_id('wide-image-toggle')[0]
    # full_image_cerberus.click()

    # browser.is_element_present_by_text('Sample', wait_time=1)
    # more_info_elem = browser.links.find_by_partial_text('Sample')
    # more_info_elem.click()

    # Parse the resulting image with soup 
    html = browser.html
    img_cerb = soup(html, 'html.parser')

    # Add try/except for error handling
    try:
        # Find the relative image urlc
        img_url_relc = img_cerb.select_one('div.downloads img').get("src")
    
    except AttributeError:
        return None
    
    # Use the base URL to create an absolute URL
    #img_urlc = f'https://astrology.usgs.gov{img_url_relc}'

    return img_url_relc


# Mars Facts
def mars_facts():
    # Adding try and except block for error handling
    try:
        # Using 'read_html' to scrape the facts table into a dataframe
        df = pd.read_html('http://space-facts.com/mars/')[0]
    
    except BaseException:
        return None

    # Assigning columns and setting index of the dataframe
    df.columns=['Description', 'Mars']
    df.set_index('Description', inplace=True)

    # Converting dataframe into HTML format, add bootstrap
    return df.to_html(classes="table table-striped")

if __name__ == "__main__":

    # If running as script, print scraped data
    print(scrape_all())
