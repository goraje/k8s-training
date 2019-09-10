import os

from flask import Flask, jsonify


app = Flask(__name__)


@app.route('/')
def hello_world():
    message = dict(
        appVersion='3',
        message=os.environ.get('APP_MESSAGE')
    )

    return jsonify(message)
