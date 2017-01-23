import os
# We'll render HTML templates and access data sent by POST
# using the request object from flask. Redirect and url_for
# will be used to redirect the user once the upload is done
# and send_from_directory will help us to send/show on the
# browser the file that the user just uploaded
from flask import Flask, render_template, request, jsonify, send_from_directory
import numpy as np
from annoy import AnnoyIndex
import random
import pickle
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time 
import shutil
import glob

def wordcloud(index):
    all_texts = pickle.load(open('models/all_lemma.pickle', 'rb'))

    chromedriver = "/Users/PandaGongfu/Downloads/chromedriver_2"
    os.environ["webdriver.chrome.driver"] = chromedriver
    driver = webdriver.Chrome(chromedriver)
    driver.get('https://www.jasondavies.com/wordcloud/')

    textbox_xpath = "//textarea[@id='text']"
    textbox = driver.find_elements_by_xpath(textbox_xpath)[0]
    textbox.clear()
    textbox.send_keys(' '.join(all_texts[index]))

    time.sleep(5)
    go_xpath = "//button[@id='go']"
    go_button = driver.find_elements_by_xpath(go_xpath)[0]
    go_button.click()

    time.sleep(2)
    svg_xpath = "//button[@id='download-svg']"
    svg_button = driver.find_elements_by_xpath(svg_xpath)[0]
    svg_button.click()

    time.sleep(2)
    download_svg = '/Users/PandaGongfu/Downloads/wordcloud.svg'
    temp_svg = 'wordcloud.svg'
    shutil.copyfile(download_svg, temp_svg)
    os.remove(download_svg)

    os.system('qlmanage -t -s 500 -o . wordcloud.svg')
    png_file = 'wordcloud.svg.png'

    existing_files = glob.glob('static/*.png')
    dst_file = 'images/word_cloud_' + '{:03d}'.format(int(existing_files[-1][-7:-4])+1) + '.png'

    shutil.copyfile(png_file, dst_file)
    os.remove(png_file)
    os.remove(temp_svg)

    return dst_file

# Initialize the Flask application
app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/<filename>')
def send_image(filename):
    return send_from_directory("images", filename)

@app.route("/recommend/", methods=["POST"])
def recommend():
    """
    When A POST request with json data is made to this uri,
    Read the example from the json, predict probability and
    send it with a response
    """
    # Get decision score for our example that came with the request
    data = request.json

    prob_nmf = pickle.load(open('models/prob_nmf.pickle', 'rb'))
    all_titles = pickle.load(open('models/all_titles.pkl', 'rb'))

    f = 30
    t = AnnoyIndex(f)  # Length of item vector that will be indexed
    for i, row in enumerate(prob_nmf):
        v = row
        t.add_item(i, v)

    t.build(10) # 10 trees

    title = data["example"].strip('\"')
    clean_titles = [t[5:] for t in all_titles]

    title_id = clean_titles.index(title)

    dst_file = wordcloud(title_id)
    idx = t.get_nns_by_item(title_id, 1000)

    tedx_list = []
    for i in idx:
        if all_titles[i][:5] == 'TEDX_':
            tedx_list.append(all_titles[i][5:])
            if len(tedx_list) > 2:
                break

    blog_list = ["", ""]
    count = 0
    for i in idx:
        if all_titles[i][:5] == 'IDEA_':
            blog_list[count] = all_titles[i][5:]
            count += 1
            if count > 1:
                break               

    # Put the result in a nice dict so we can send it as json
    results = {"recommend_tedx": tedx_list,
               "recommend_blog": blog_list,
               "img": dst_file.split('/')[1]}
             
    return jsonify(results)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8808, debug=True)
