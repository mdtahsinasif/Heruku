# -*- coding: utf-8 -*-
"""
Created on Thu Mar 19 20:28:02 2020

@author: tahsin.asif
"""

# -*- coding: utf-8 -*-
import pickle

"""
Created on Mon Jan 20 17:30:50 2020
@author: tahsin.asif
"""

from flask import Flask, jsonify, request, render_template
from sklearn.externals import joblib
import pandas as pd
import os
import json
# Importing dependencies
from urllib.parse import urlparse
from tld import get_tld

# Postman input ---{"data":"https://zyxytr.com/acompanhamento/"}
# post  ---- params - http://localhost:8086/predict

json_obj = ''
obj = ''

app = Flask(__name__,template_folder='template')

@app.route('/')
def home():
    return render_template('index.html')


@app.route('/predict', methods=['POST','GET'])
def predict():
    json_ =request.args.get('url')
    print('json:', json_)
    # print('json_g---->',json_g)
    # json_obj = json.dumps(json_)
    # print('json_obj', json_obj)
    number_reviews_json = len(json_)  # Calculating the number of reviews  json_obj.encode("utf-8"))
    print('Length of _json', number_reviews_json)
    ############################
    # testing = {'Url':https://zyxytr.com/acompanhamento}
    url_test = pd.DataFrame([json_])
    # url_test = pd.DataFrame('https://zyxytr.com/acompanhamento')
  #  print('url_test item data---->', url_test['data'])
    # Hostname Length
    # url_test['hostname_length'] = json_.apply(lambda i: len(urlparse(i).netloc))
    url_test['hostname_length'] = len(urlparse(json_).netloc)
    print('------------>', url_test['hostname_length'])

    # fd length
    def fd_length(url):
        urlpath = urlparse(url).path
        try:
            return len(urlpath.split('/')[1])
        except:
            return 0

    # url_test['fd_length'] = url_test.apply(lambda i: fd_length(i))
    url_test['fd_length'] = fd_length(json_)
    print('====================>>>', url_test['fd_length'])

    # tld length
    # Length of Top Level Domain
    # url_test['tld'] = url_test.apply(lambda i: get_tld(i,fail_silently=True))
    url_test['tld'] = get_tld(json_, fail_silently=True)

    def tld_length(tld):
        try:
            return len(tld)
        except:
            return -1

    print('====================>>>', url_test['tld'])

    # url_test['tld_length'] = url_test['tld'].apply(lambda i: tld_length(i))
    url_test['tld_length'] = tld_length(url_test['tld'])
    print('tld Length------------------>', url_test['tld_length'])

    url_test['count-'] = json_.count('-')
    print('Count---------------->', url_test['count-'])
    # url_test['count-'] = url_test.apply(lambda i: i.count('-'))
    url_test['count@'] = json_.count('@')
    print('Count-@---------------->', url_test['count@'])
    # url_test['count@'] = url_test.apply(lambda i: i.count('@'))
    url_test['count?'] = json_.count('?')
    print('Count?---------------->', url_test['count?'])
    # url_test['count?'] = url_test.apply(lambda i: i.count('?'))
    url_test['count%'] = json_.count('%')
    print('Count%---------------->', url_test['count%'])
    # url_test['count%'] = url_test.apply(lambda i: i.count('%'))
    url_test['count.'] = json_.count('.')
    print('Count..---------------->', url_test['count.'])
    # url_test['count.'] = url_test.apply(lambda i: i.count('.'))
    url_test['count='] = json_.count('=')
    print('Count=---------------->', url_test['count='])
    # url_test['count='] = url_test.apply(lambda i: i.count('='))
    url_test['count-http'] = json_.count('http')
    print('Count-http---------------->', url_test['count-http'])
    # url_test['count-http'] = url_test.apply(lambda i : i.count('http'))
    url_test['count-https'] = json_.count('https')
    print('Count-https---------------->', url_test['count-https'])
    # url_test['count-https'] = url_test.apply(lambda i : i.count('https'))
    url_test['count-www'] = json_.count('www')
    print('Count-www---------------->', url_test['count-www'])

    # url_test['count-www'] = url_test.apply(lambda i: i.count('www'))

    def digit_count(url):
        digits = 0
        for i in url:
            if i.isnumeric():
                digits = digits + 1
            return digits

    # url_test['count-digits']= url_test.apply(lambda i: digit_count(i))
    url_test['count-digits'] = digit_count(json_)

    # url_test['count-letters'] = url_test.apply(lambda i: letter_count(i))

    def letter_count(url):
        letters = 0
        for i in url:
            if i.isalpha():
                letters = letters + 1
            return letters

    url_test['count-letters'] = letter_count(json_)

    def no_of_dir(url):
        urldir = urlparse(url).path
        return urldir.count('/')

        # url_test['count_dir'] = url_test.apply(lambda i: no_of_dir(i))

    url_test['count_dir'] = no_of_dir(json_)

    import re
    # Use of IP or not in domain
    def having_ip_address(url):
        match = re.search(
            '(([01]?\\d\\d?|2[0-4]\\d|25[0-5])\\.([01]?\\d\\d?|2[0-4]\\d|25[0-5])\\.([01]?\\d\\d?|2[0-4]\\d|25[0-5])\\.'
            '([01]?\\d\\d?|2[0-4]\\d|25[0-5])\\/)|'  # IPv4
            '((0x[0-9a-fA-F]{1,2})\\.(0x[0-9a-fA-F]{1,2})\\.(0x[0-9a-fA-F]{1,2})\\.(0x[0-9a-fA-F]{1,2})\\/)'  # IPv4 in hexadecimal
            '(?:[a-fA-F0-9]{1,4}:){7}[a-fA-F0-9]{1,4}', url)  # Ipv6
        if match:
            # print match.group()
            return -1
        else:
            # print 'No matching pattern found'
            return 1

    # url_test['use_of_ip'] = url_test.apply(lambda i: having_ip_address(i))
    url_test['use_of_ip'] = having_ip_address(json_)
    print(url_test['use_of_ip'])

    # Predictor Variables
    x = url_test[['hostname_length',
                  'fd_length', 'tld_length', 'count-', 'count@', 'count?',
                  'count%', 'count=', 'count-http', 'count-https', 'count-www', 'count-digits',
                  'count-letters', 'count_dir', 'use_of_ip']]
    ############################

    print('query_df_array::----->', x)
    prediction = log_estimator.predict(x)
    print('Predicted Value;--->', prediction)
    output = pd.Series(prediction)
    return render_template('index.html', prediction_text='Url Type is {}'.format(prediction))
 #   return jsonify(pd.Series(prediction).to_json(orient='values'))


cleanHeadlines_request = []

MODEL_FILE = 'log_model-v1.pkl'
if __name__ == '__main__':
   # os.chdir(MODEL_DIR)
    global log_estimator = joblib.load(MODEL_FILE)
    app.run(debug=True)
