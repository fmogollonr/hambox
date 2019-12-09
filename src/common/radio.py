import json
from src.common.pynicerfsa828 import Sa828
#from src.common.pydorji import Dorji
from src.common.config import Config


class Radio:
    def __init__(self):
        self.radio_device = Config().read_radio_config()

    def get_info_sa828(self):
        print("get_info_sa828")
        radio_engine = Sa828()
        info = radio_engine.get_info()
        return info

    def get_radio_memory(self):
        if 'nicerf' in self.radio_device:
            radio_engine = Sa828()
            memory = radio_engine.read_memory_configuration()
            return memory

    def get_info(self):
        if 'nicerf' in self.radio_device:
            info = self.get_info_sa828()
            return info

    def get_freq(self):
        return

    def set_freq(self, freq):
        if 'nicerf' in self.radio_device:
            radio_engine = Sa828()
            radio_engine.set_full_configuration(freq)
        return

    def set_tx(self):
        return

    def set_rx(self):
        return

    def set_squelch(self):
        return
