# Import Dependencies
from splinter import Browser
from bs4 import BeautifulSoup as bs
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import pymongo
import time
import requests

# This is for debugging

def savetofile(filename,contents):
    file = open(filename,"w",encoding="utf-8")
    file.write(contents)
    file.close()


def scrape():
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    # NASA Mars News

    url = 'https://mars.nasa.gov/news/'

    browser.visit(url)
    time.sleep(3)

    html = browser.html
    soup = bs(html, 'html.parser')

    slides = soup.find_all('li', class_='slide')

    html = browser.html
    soup = bs(html, "html.parser")

    content_title = slides[0].find('div', class_ = 'content_title')
    news_title = content_title.text.strip()

    article_teaser_body = slides[0].find('div', class_ = 'article_teaser_body')
    news_p = article_teaser_body.text.strip()

    # JPL Mars Space Images

    base_url = 'https://www.jpl.nasa.gov'
    url = base_url + '/spaceimages/?search=&category=Mars'

    browser.visit(url)
    time.sleep(1)
    html = browser.html
    soup = bs(html, 'html.parser')  

    featured_image_url = base_url + soup.find('a',class_='button fancybox')['data-fancybox-href']

    # Mars facts
    # try: 
    url = 'https://space-facts.com/mars/'
    browser.visit(url)
    table = pd.read_html(url)
    # except BaseException:
    #     return None

    df = table[0]
    df.columns = ['Mars Facts', 'Value']
    df.set_index('Mars Facts', inplace=True)
    # df = df.to_html()

    # Mars Hemispheres

    base_url = 'https://astrogeology.usgs.gov'
    url = base_url + '/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'

    browser.visit(url)
    html = browser.html
    soup = bs(html, 'html.parser')

    items = soup.find_all('div', class_='item')

    urls = []
    titles = []
    for item in items:
        urls.append(base_url + item.find('a')['href'])
        titles.append(item.find('h3').text.strip())

    img_urls = []
    for first_url in urls:
        browser.visit(first_url)
        time.sleep(1)
        html = browser.html
        soup = bs(html, 'html.parser')
        first_url = base_url+soup.find('img',class_='wide-image')['src']
        img_urls.append(first_url)

    hemisphere_image_urls = []

    for i in range(len(titles)):
        hemisphere_image_urls.append({'title':titles[i],'img_url':img_urls[i]})

    # Assigning scraped data to a page
    
    marspage = {}
    marspage["news_title"] = news_title
    marspage["news_p"] = news_p
    marspage["featured_image_url"] = featured_image_url
    marspage["marsfacts_html"] = df.to_html() 
    marspage["hemisphere_image_urls"] = hemisphere_image_urls

    return marspage
    