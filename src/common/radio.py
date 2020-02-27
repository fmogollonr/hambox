import json
from common.pynicerfsa828 import Sa828
from common.pydorji import Dorji
from common.config import Config
from .logger import Logger


class Radio:
    def __init__(self):
        self.radio_device = Config().read_radio_config()
        self.log = Logger("RadioEngine")

    def get_info_sa828(self):
        self.log.send_log("debug", "get_info_sa828")
        radio_engine = Sa828()
        info = radio_engine.get_info()
        return info

    def get_radio_memory(self):
        self.log.send_log("debug", "get_radio_memory")
        if 'nicerf' in self.radio_device:
            radio_engine = Sa828()
            memory = radio_engine.read_memory_configuration()
            return memory

    def get_info(self):
        self.log.send_log("debug", "get_info")
        if 'nicerf' in self.radio_device:
            info = self.get_info_sa828()
            return info
        if 'dorji' in self.radio_device:
            radio_engine = Dorji()
            info = radio_engine.say_hello()
            return info            

    def get_freq(self):
        return

    def set_freq(self, freq):
        self.log.send_log("debug", "set_freq")
        if 'nicerf' in self.radio_device:
            radio_engine = Sa828()
            radio_engine.set_full_configuration(freq)
        if 'dorji' in self.radio_device:
            radio_engine = Dorji()
            radio_engine['tx']=str(freq)
            radio_engine['rx']=str(freq)
            response = radio_engine.set_dmosetgroup()
            print(response)
        return

    def set_tx(self):
        if 'nicerf' in self.radio_device:
            radio_engine = Sa828()
            print("TXTXTXTX")
            radio_engine.set_tx()
        if 'dorji' in self.radio_device:
            radio_engine = Dorji()
            print("TXTXTXTX")
            radio_engine.set_tx()
        return

    def set_rx(self):
        if 'nicerf' in self.radio_device:
            radio_engine = Sa828()
            print("RXRXRXRXRX")
            radio_engine.set_rx()
        return

    def set_squelch(self):
        return
