from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
import os
import pickle

def mouse_click(element):
    ActionChains(driver).click(element).perform()

tedx_url = "http://tedxtalks.ted.com/browse/talks-by-language/english?search=tag%3A%26quot%3Benglish%26quot%3B&page=1"
chromedriver = "/Users/PandaGongfu/Downloads/chromedriver_2"
os.environ["webdriver.chrome.driver"] = chromedriver
driver = webdriver.Chrome(chromedriver)
driver.get(tedx_url)

page_xpath = "//a[@class='mvp-pagenum- mvp-pagenum-pagelink']"
pages = driver.find_elements_by_xpath(page_xpath)

links = [page.get_attribute('href') for page in pages]

while pages[-2].text != '1,340':
    print(pages[-2].text)
    mouse_click(pages[-2])
    time.sleep(2)
    page_xpath = "//a[@class='mvp-pagenum- mvp-pagenum-pagelink']"
    pages = driver.find_elements_by_xpath(page_xpath)
    links.extend([page.get_attribute('href') for page in pages])

links = list(set(links))

title_list = []
for link in links:
    driver.get(link)
    time.sleep(2.5)
    title_xpath = "//div[@class='mvp_grid_panel_title']//a"
    titles = driver.find_elements_by_xpath(title_xpath)
    title_list.extend([t.get_attribute('title') for t in titles])

pickle.dump(title_list, open('tedx_titles.pickle', 'wb'))











