from bs4 import BeautifulSoup
from splinter import Browser
import pandas as pd
import datetime as dt 

executable_path = {'executable_path': './chromedriver.exe'}
browser = Browser('chrome', **executable_path, headless=False)

def mars_news(browser):
    url = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'
    browser.visit(url)

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    try:
        news_title = soup.find(class_="bottom_gradient").text

        news_p = soup.find(class_="rollover_description_inner").text
    except AttributeError:
        return None, None
    return news_title, news_p


# Visit URL
def featured_image(browser):
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    base_url = 'https://www.jpl.nasa.gov'
    browser.visit(url)

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    try:
        feature_image_url = str(base_url + soup.find(class_="button fancybox")['data-fancybox-href'])
    except AttributeError:
        return None 
    return feature_image_url


def twitter_weather(browser):
    url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(url)

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    try:
        mars_weather = soup.find('p',class_="TweetTextSize TweetTextSize--normal js-tweet-text tweet-text").text
    except AttributeError:
        return None
    return mars_weather


def mars_facts():
    try:
        url='https://space-facts.com/mars/'

        tables = pd.read_html(url)

    except BaseException:
        return None
    df = pd.DataFrame(tables[0])
    df.columns = ['Fact','Value']
    df['Fact']=df['Fact'].str.replace(':','')
    df.set_index('Fact', inplace=True)

    return df.to_html(classes="table table-striped")


def hemisphere(browser):
    url='https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    hemispheres = soup.find_all('h3')

    hemisphere_image_urls = []
    n=0

    for hemi in hemispheres:
        item = soup.find_all('h3')[n].text
    
        browser.click_link_by_partial_text(item)
        item_html=browser.html
        item_soup = BeautifulSoup(item_html, 'html.parser')
    
        item_url=item_soup.find('div',class_="downloads")
        item_url=item_url.find('a')['href']
    
        item = item.replace(' Enhanced','')
    
        dict_item = {"title":item,"img_url":item_url}
        hemisphere_image_urls.append(dict_item)
    
        browser.click_link_by_partial_text('Back')

        n=n+1
    return hemisphere_image_urls


def scrape_all(): # main bot 
    executable_path = {'executable_path': './chromedriver.exe'}
    browser = Browser('chrome', **executable_path)

    news_title, news_p = mars_news(browser)
    img_url = featured_image(browser)
    mars_weather = twitter_weather(browser)
    facts = mars_facts()
    hemisphere_image_urls = hemisphere(browser)
    

    timestamp = dt.datetime.now()

    data = {
        "news_title": news_title,
        "news_paragraph": news_p,
        "featured_image": img_url,
        "weather": mars_weather,
        "facts": facts,
        "hemispheres": hemisphere_image_urls,
        "last_modified": timestamp
    }
    browser.quit()
    return data 


if __name__ == "__main__":
    print(scrape_all())