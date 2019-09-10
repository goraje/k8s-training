import json

from flask import Flask, jsonify, request


app = Flask(__name__)
output_file = '/mnt/data/message.json'


@app.route('/writejson', methods=['POST'])
def write_json():
    message = request.get_json()
    with open(output_file, 'w') as out:
        json.dump(message, out)
    return jsonify(dict(out=f'Wrote message to: {output_file}'))


@app.route('/readjson')
def read_json():
    with open(output_file) as f:
        message = json.load(f)
        return jsonify(message)
