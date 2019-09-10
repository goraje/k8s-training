from flask import Flask, jsonify


app = Flask(__name__)


@app.route('/')
def hello_world():
    message = dict(
        appVersion='2',
        message='Hello, World!'
    )

    return jsonify(message)
