#!flask/bin/python
from flask import Flask, jsonify, abort
from flask import request
import json
from src.common.logger import Logger
from src.common.config import Config
from src.engine.hambox_engine import HamboxEngine

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
    engine.rx()
    return jsonify({'RX': 'OK'})


if __name__ == '__main__':
    app.run(debug=True)
