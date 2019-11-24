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

    def write_config(self):
        self.log.send_log("debug", "Writing file")
        return
