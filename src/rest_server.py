#!flask/bin/python
from flask import Flask, jsonify, abort, render_template, send_from_directory, redirect
from flask import request
import json
from importlib.machinery import SourceFileLoader
import sys
import os

from engine.hambox_engine import HamboxEngine
from common.logger import Logger
from common.config import Config
from common.radio import Radio

app = Flask(__name__)

engine = HamboxEngine()


def get_config():
    config = Config()
    hambox_json = config.read_hambox_config()
    return hambox_json


def set_config(freq, mode, status):
    config = Config()
    hambox_json = config.write_config(freq, mode, status)
    return hambox_json


@app.route('/hambox/radio/memory', methods=['GET'])
def get_radio_memory():
    radio_engine = radio.Radio()
    memory = radio_engine.get_radio_memory()
    return jsonify({'radio_memory': memory})


@app.route('/hambox/radio/info', methods=['GET'])
def get_radio_info():
    radio_engine = Radio()
    info = radio_engine.get_info()
    return jsonify({'radio_info': info})


@app.route('/hambox/config', methods=['GET'])
def get_hambox():
    hambox_json = get_config()
    return jsonify({'hambox': hambox_json})


@app.route('/hambox/config', methods=['POST'])
def set_hambox():
    if not request.json:
        abort(400)
    if request.json['freq'] and request.json['mode'] and request.json['status']:
        config = Config()
        config.set_config(request.json['freq'], request.json['mode'], request.json['status'])
    return jsonify({'hambox': "OK"})


@app.route('/hambox/freq', methods=['GET'])
def get_freq():
    hambox_json = get_config()
    return jsonify({'freq': hambox_json['freq']})


@app.route('/hambox/freq', methods=['POST'])
def set_freq():
    try:
        request.json['freq']
        config = Config()
        config.set_freq(request.json['freq'])
        radio_engine = Radio()
        radio_engine.set_freq(request.json['freq'])
        return get_hambox()
    except:
        return jsonify({'hambox': 'no_freq_sent'})


@app.route('/hambox/status', methods=['GET'])
def get_status():
    hambox_json = get_config()
    return jsonify({'status': hambox_json['status']})


@app.route('/hambox/status', methods=['POST'])
def set_status():
    try:
        request.json['status']
        config = Config()
        config.set_status(request.json['status'])
        return get_hambox()
    except:
        return jsonify({'hambox': 'no_status_sent'})


@app.route('/hambox/mode', methods=['GET'])
def get_mode():
    hambox_json = get_config()
    return jsonify({'mode': hambox_json['mode']})


@app.route('/hambox/mode', methods=['POST'])
def set_mode():
    try:
        request.json['mode']
        config = Config()
        config.set_mode(request.json['mode'])
        return get_hambox()
    except:
        return jsonify({'hambox': 'no_mode_sent'})


@app.route('/hambox/audioconfig', methods=['GET'])
def get_audioconfig():
    config = Config()
    audioconfig = config.read_audio_config()
    return jsonify({'audioconfig': audioconfig})


@app.route('/hambox/audioconfig', methods=['GET'])
def set_audioconfig():
    config = Config()
    audioconfig = config.read_audio_config()
    return jsonify({'audioconfig': audioconfig})


@app.route('/hambox/TX', methods=['POST'])
def set_tx():
    engine.tx()
    return jsonify({'TX': 'OK'})


@app.route('/hambox/REC', methods=['POST'])
def rec():
    file_name = engine.rec()
    return jsonify({'hambox': file_name})


@app.route('/hambox/REC', methods=['DELETE'])
def stop_rec():
    engine.stop_rec()
    return jsonify({'hambox': 'STOP_REC'})


@app.route('/hambox/RX', methods=['POST'])
def set_rx():
    try:
        request.json['test']
        engine.rx_test()
        return jsonify({'RXTEST': 'OK'})
    except:
        engine.rx()
        return jsonify({'RX': 'OK'})


@app.route('/hambox/css/<path:path>')
def send_css(path):
    return send_from_directory('rest/templates/css', path)


@app.route('/hambox/js/<path:path>')
def send_js(path):
    return send_from_directory('rest/templates/js', path)


@app.route('/', methods=['GET'])
def rehome():
    return redirect("hambox", code=302)


@app.route('/hambox/', methods=['GET'])
def home():
    return render_template("hambox.html")


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
