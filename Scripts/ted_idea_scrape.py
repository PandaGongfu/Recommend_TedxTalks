import time
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
import os
from collections import defaultdict
import pickle


def mouse_click(element):
    ActionChains(driver).click(element).perform()

def scroll_down():
    # define initial page height for 'while' loop
    last_height = driver.execute_script("return document.body.scrollHeight")
    count = 0
    while True:
        count += 1
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        try:
            load_xpath = "//span[@class='load-more-text']"
            loads = driver.find_elements_by_xpath(load_xpath)
            mouse_click(loads[0])

        except:
            print('no See More button found...')

        time.sleep(5)
        new_height = driver.execute_script("return document.body.scrollHeight")

        print(count, new_height)

        if new_height == last_height:
            break
        else:
            last_height = new_height


target_url_str = "http://ideas.ted.com/"

chromedriver = "/Users/PandaGongfu/Downloads/chromedriver_2"
os.environ["webdriver.chrome.driver"] = chromedriver
driver = webdriver.Chrome(chromedriver)
driver.get(target_url_str)

scroll_down()

blog_xpath = "//a[@rel='bookmark']"
blogs = driver.find_elements_by_xpath(blog_xpath)

blog_links = [blog.get_attribute('href') for blog in blogs]
pickle.dump(list(set(blog_links)), open('tedidea_links.pickle', 'wb'))


# Scrape for text
links = pickle.load(open('tedidea_links.pickle', 'rb'))

from pymongo import MongoClient
client = MongoClient()
ted = client.my_db.ted


docs_list = []
error_load = []

count = 0
for link in links:
    print(count)
    count+=1
    time.sleep(1)
    time1 = time.time()
    document = defaultdict(str)
    driver.get(link)
    time.sleep(2)

    try:
        title_xpath = "//h1[@class='single-post-title']"
        titles = driver.find_elements_by_xpath(title_xpath)
        document['title'] = titles[0].text

        date_xpath = "//span[@class='date']"
        dates = driver.find_elements_by_xpath(date_xpath)
        document['date'] = dates[0].text

        text_xpath = "//p"
        texts = driver.find_elements_by_xpath(text_xpath)
        document['text'] = ' '.join([t.text for t in texts])
        docs_list.append(document)
    except:
        print('Error! %d' % count)
        error_load.append(link)

pickle.dump(docs_list, open('idea_text.pickle', 'wb'))


