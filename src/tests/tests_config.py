import sys
sys.path.append("..")
from common.config import Config
import unittest
import json


class TestConfig(unittest.TestCase):
    def test_read_hambox_config(self):
        Config.set_path(self,"common/configtest.json")
        self.assertEqual(Config.get_path(self),"common/configtest.json")
    
    def test_get_full_conf(self):
        Config.set_path(self,"../common/configtest.json")
        config_json='{"hambox": {"freq": "145.5000","mode": "SSTV","status": "TX","callsign": "EB2ELU" }, "audioconf": { \
        "rf_in": "hw:audio_b",\
        "rf_out": "alsa_input.MyCard2.analog-mono",\
        "mic": "alsa_input.MyCard1.analog-mono",\
        "spk": "hw:audio_a"\
        },\
        "radio": "nicerf"\
        }'
        config_dict=json.loads(config_json)
        self.assertEqual(config_dict,Config.get_full_conf(self))



if __name__ == "__main__":
    unittest.main()