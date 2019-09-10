import os
import redis
import time

from flask import Flask, jsonify


app = Flask(__name__)

conn = redis.Redis(host=os.environ.get('REDIS_HOST'), 
                   port=int(os.environ.get('REDIS_PORT')))


def get_page_hits():
    retries = 3
    while True:
        try:
            return conn.incr('page_hits')
        except redis.exceptions.ConnectionError as exc:
            if retries == 0:
                raise exc
            retries -= 1
            time.sleep(1)

@app.route('/')
def hello_world():
    page_hits = get_page_hits()
    message = dict(
        appVersion='4',
        message=f'Page hits: {page_hits}'
    )

    return jsonify(message)
