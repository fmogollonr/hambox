#!flask/bin/python
from flask import Flask, jsonify, abort
from flask import request
import json
import sys
import os

#sys.path.append(os.path.join(os.path.dirname(
#    os.path.abspath(__file__)), '../engine'))
import logger


app = Flask(__name__)

hambox = {
    'freq': "144.500",
    'mode': u'VOICE',
    'status': u'TX',
}
json.dumps(hambox)


@app.route('/hambox/status', methods=['GET'])
def get_hambox():
    return jsonify({'hambox': hambox})


@app.route('/hambox/freq', methods=['GET'])
def get_freq():
    return jsonify({'freq': hambox['freq']})


@app.route('/hambox/freq', methods=['POST'])
def set_freq():
    if not request.json:
        abort(400)
    hambox['freq'] = request.json['freq']
    return jsonify({'freq': hambox['freq']})


if __name__ == '__main__':
    app.run(debug=True)
