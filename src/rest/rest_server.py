#!flask/bin/python
from flask import Flask, jsonify, abort
from flask import request
import json
from src.common.logger import Logger
from src.common.config import Config

app = Flask(__name__)


def get_config():
    config = Config()
    hambox_json = config.read_config()
    return hambox_json


def set_config(freq, mode, status):
    config = Config()
    hambox_json = config.write_config(freq, mode, status)
    return hambox_json


@app.route('/hambox/config', methods=['GET'])
def get_hambox():
    hambox_json = get_config()
    return jsonify({'hambox': hambox_json})


@app.route('/hambox/config', methods=['POST'])
def set_hambox():
    if not request.json:
        abort(400)
    if request.json['freq'] and request.json['mode'] and request.json['status']:
        set_config(request.json['freq'], request.json['mode'], request.json['status'])
    return jsonify({'hambox': "OK"})


@app.route('/hambox/freq', methods=['GET'])
def get_freq():
    hambox_json = get_config()
    return jsonify({'freq': hambox_json['freq']})


@app.route('/hambox/freq', methods=['POST'])
def set_freq():
    if not request.json:
        abort(400)
    hambox_json = get_config()
    hambox_json['freq'] = request.json['freq']
    return jsonify({'freq': hambox_json['freq']})


if __name__ == '__main__':
    app.run(debug=True)
