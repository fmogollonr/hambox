import json
from .logger import Logger


class Config:
    def __init__(self):
        self.log = {}
        self.log = Logger("HamboxConfig")
        self.config_path = "../common/config.json"

    def read_config(self):
        self.log.send_log("debug", "Reading file")
        with open(self.config_path) as json_file:
            data = json.load(json_file)
            hambox = data['hambox']
            return hambox

    def set_freq(self, freq):
        hambox = self.read_config()
        self.write_config(freq, hambox['mode'], hambox['status'])
        return

    def set_mode(self, mode):
        hambox = self.read_config()
        self.write_config(hambox['freq'], mode, hambox['status'])
        return

    def set_status(self, status):
        hambox = self.read_config()
        self.write_config(hambox['freq'], hambox['mode'], status)
        return

    def write_config(self, freq, mode, status):
        hambox = {'hambox':{'freq': freq, 'mode': mode, 'status': status}}
        with open(self.config_path, 'w') as outfile:
            json.dump(hambox, outfile)

        self.log.send_log("debug", "Writing file")
        return
