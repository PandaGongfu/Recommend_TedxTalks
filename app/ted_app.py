import os
# We'll render HTML templates and access data sent by POST
# using the request object from flask. Redirect and url_for
# will be used to redirect the user once the upload is done
# and send_from_directory will help us to send/show on the
# browser the file that the user just uploaded
from flask import Flask, render_template, request, jsonify
import numpy as np
from annoy import AnnoyIndex
import random
import pickle

# Initialize the Flask application
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

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
               "recommend_blog": blog_list}
             
    return jsonify(results)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8808, debug=True)
