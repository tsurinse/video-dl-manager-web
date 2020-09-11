import os
import sys

import redis
from flask import Flask
from flask import render_template
from flask import request


# Flask init
app = Flask(__name__)


# Redis init
redis_url = ''

if 'REDIS_URL' in os.environ:
    redis_url = os.environ['REDIS_URL']

r = redis.Redis.from_url(redis_url)


# Routing
@app.route('/')
def index():
    return render_template('index.html')


@app.route('/submit', methods=['POST'])
def submit():
    if request.form['pass'] != os.environ['VDLM_PASS']:
        return render_template('index.html')

    print(request.form)
    r.set(request.form['url'], request.form['dest'])
    return render_template('index.html')
