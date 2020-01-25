import json
from .logger import Logger


class Config:
    def __init__(self):
        self.log = {}
        self.log = Logger("HamboxConfig")
        self.config_path = "common/config.json"

    def get_full_conf(self):
        with open(self.config_path) as json_file:
            data = json.load(json_file)
            return data

    def read_hambox_config(self):
        self.log.send_log("debug", "read_hambox_config")
        full_conf = self.get_full_conf()
        return full_conf['hambox']

    def read_audio_config(self):
        self.log.send_log("debug", "read_audio_config")
        full_conf = self.get_full_conf()
        return full_conf['audioconf']

    def read_radio_config(self):
        self.log.send_log("debug", "read_radio_config")
        full_conf = self.get_full_conf()
        return full_conf['radio']

    def set_freq(self, freq):
        hambox = self.read_hambox_config()
        self.write_config(freq, hambox['mode'], hambox['status'])
        return

    def set_mode(self, mode):
        hambox = self.read_hambox_config()
        self.write_config(hambox['freq'], mode, hambox['status'])
        return

    def set_status(self, status):
        hambox = self.read_hambox_config()
        self.write_config(hambox['freq'], hambox['mode'], status)
        return

    def write_config(self, freq, mode, status):
        hambox = {'hambox': {'freq': freq, 'mode': mode, 'status': status}}
        audioconfig = self.read_audio_config()
        radio = self.read_radio_config()
        self.write_full_config(hambox, audioconfig, radio)
        return

    def write_audio_config(self, rf_in, rf_out, mic, spk):
        audioconfig = {'audioconf': {'rf_in': rf_in, 'rf_out': rf_out, 'mic': mic, 'spk': spk}}
        hambox = self.read_hambox_config()
        radio = self.read_radio_config()
        self.write_full_config(hambox, audioconfig, radio)
        return

    def write_full_config(self, hambox_config, audio_config, radio_config):
        hambox_full = {
            'hambox': {'freq': hambox_config['hambox']['freq'], 'mode': hambox_config['hambox']['mode'],
                       'status': hambox_config['hambox']['status']},
            'audioconf': {'rf_in': audio_config['rf_in'], 'rf_out': audio_config['rf_out'], 'mic': audio_config['mic'],
                          'spk': audio_config['spk']},
            'radio': radio_config}

        with open(self.config_path, 'w') as outfile:
            json.dump(hambox_full, outfile)
        return
