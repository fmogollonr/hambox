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


@app.route('/hambox/config', methods=['GET'])
def get_hambox():
    hambox_json = get_config()
    return jsonify({'hambox': hambox_json})


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
