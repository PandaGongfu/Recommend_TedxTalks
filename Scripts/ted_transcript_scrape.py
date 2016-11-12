import time
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
import os
from collections import defaultdict
from pymongo import MongoClient
import pickle

def mouse_click(driver, element):
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


target_url_str = "https://www.youtube.com/user/TEDtalksDirector/videos?sort=dd&view=0&flow=grid"

chromedriver = "/Users/PandaGongfu/Downloads/chromedriver_2"
os.environ["webdriver.chrome.driver"] = chromedriver
driver = webdriver.Chrome(chromedriver)
driver.get(target_url_str)

# scroll down to the bottom of the page
scroll_down()

video_xpath = "//a[@class='yt-uix-sessionlink yt-uix-tile-link  spf-link  yt-ui-ellipsis yt-ui-ellipsis-2']"
videos = driver.find_elements_by_xpath(video_xpath)

links = []
for video in videos:
    links.append(video.get_attribute('href'))

pickle.dump(links, open('data/links.pickle', 'wb'))
# Load scripts into Mongodb
client = MongoClient()
ted = client.my_db.ted


#########TED Scrape###########


client = MongoClient()

ted = client.my_db.ted

video_xpath = "//a[@class='yt-uix-sessionlink yt-uix-tile-link  spf-link  yt-ui-ellipsis yt-ui-ellipsis-2']"
videos = driver.find_elements_by_xpath(video_xpath)

links = []
docs_list = []
error_lan = []
error_load = []

for video in videos:
    links.append(video.get_attribute('href'))

links = pickle.load(open('tedx_error_links.pickle', 'rb'))

count = 0
for link in links:
    document = defaultdict(str)
    driver.get(link)
    time.sleep(2)

    try:
        # Viewership
        view_xpath = "//div[@class='watch-view-count']"
        views = driver.find_elements_by_xpath(view_xpath)
        document['viewership'] = views[0].text.split(' views')[0]

        # title
        title_xpath = "//span[@class='watch-title']"
        document['title'] = driver.find_elements_by_xpath(title_xpath)[0].text

        # Run Time
        runtime_xpath = "//span[@class='ytp-time-duration']"
        document['runtime'] = driver.find_elements_by_xpath(runtime_xpath)[0].text

        # Upload Date
        upload_day_xpath = "//strong[@class='watch-time-text']"
        document['upload_day'] = driver.find_elements_by_xpath(upload_day_xpath)[0].text.split('on ')[1]

        # UpVote, DownVote
        upvote_xpath = "//button[@title='I like this']//span[@class='yt-uix-button-content']"
        document['upvote'] = driver.find_elements_by_xpath(upvote_xpath)[0].text

        downvote_xpath = "//button[@title='I dislike this']//span[@class='yt-uix-button-content']"
        document['downvote'] = driver.find_elements_by_xpath(downvote_xpath)[0].text

        time.sleep(0.5)
        # Locate Transcript
        button_xpath = "//button[@id='action-panel-overflow-button']"
        buttons = driver.find_elements_by_xpath(button_xpath)
        mouse_click(buttons[0])
        time.sleep(1)

        transcript_xpath = "//button[@data-trigger-for='action-panel-transcript']"
        transcripts = driver.find_elements_by_xpath(transcript_xpath)
        mouse_click(transcripts[0])
        time.sleep(2)

        # Get Transcript
        doc = ''

        lang_xpath = "//button[@class='yt-uix-button yt-uix-button-default hidden']//span[@class='yt-uix-button-content transcript-lang']"
        language = driver.find_elements_by_xpath(lang_xpath)[0].text

        if language.split()[0] =='English':
            text_xpath = "//div[@class='caption-line-text']"
            texts = driver.find_elements_by_xpath(text_xpath)

            lines = []
            [lines.append(text.text) for text in texts];
            doc = ' '.join(lines)
        else:
            print('language is in %s' % language)
            error_lan.append(count)

        document['transcript'] = doc

        count += 1
        print(count)
        if len(doc):
            ted.insert_one(document)
            docs_list.append(document)
    except:
        print('Error! %d' % count)
        error_load.append(count)












