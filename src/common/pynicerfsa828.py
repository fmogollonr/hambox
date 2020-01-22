#!/usr/bin/env python

import serial
from .logger import Logger
import RPi.GPIO as GPIO

class Sa828:
    '''
    A class for managing the NiceRF Sa828 chip via serial
    '''

    def __init__(self, **kwargs):
        self.log = Logger("nicerf")
        self.log.send_log("debug", "__init__")
        self.gpio_ptt = 7
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.gpio_ptt, GPIO.OUT)
        '''
        Set defaults

        Establish a serial connection to device at baud rate, uses pyserial

          Serial options:
            * baud - Baud rate string        | Default: "9600"
            * device - a device string       | Default: "/dev/ttyS0"
       '''

        self.settings = {
            'tx': "144.0000",
            'rx': "144.0000",
            'tx_ctcss': "000",
            'rx_ctcss': "000",
            'sq': "0",
            'device': "/dev/ttyS0",
            'baud': "9600",
        }

        self.settings.update(kwargs)

        self.ser = serial.Serial(self.settings['device'],
                                 self.settings['baud'], timeout=2)

        if not self.ser.isOpen():
            exit("error")

    def read_line(self):
        rv = ""
        while True:
            ch = self.ser.read()
            rv += ch.decode()
            if ch.decode() == '\r' or ch == '':
                return rv

    def get_info(self):
        self.log.send_log("debug", "get_info")
        self.send_atcommand("AAFAA")
        rcv = self.read_line()
        self.log.send_log("debug", "received settings: ")
        self.log.send_log("debug", rcv)
        return rcv

    def read_memory_configuration(self):
        self.log.send_log("debug", "read_memory_configuration")
        self.send_atcommand("AAFA1")
        rcv = self.read_line()
        self.log.send_log("debug", rcv)
        return rcv

    def set_full_configuration(self, freq, txcts=None, rxctcs=None, squelch=None):
        self.log.send_log("debug", "set_full_configuration")
        freq_decimal = float(freq)
        filled_freq_decimal = '{:.4f}'.format(freq_decimal)
        self.log.send_log("debug", "decimal: "+str(filled_freq_decimal))
        configuration = [None] * 35
        if txcts is None:
            txcts = self.settings['tx_ctcss']
        if rxctcs is None:
            rxctcs = self.settings['rx_ctcss']
        if squelch is None:
            squelch = self.settings['sq']
        for pos in range(0, 16):
            self.set_mem_position(filled_freq_decimal, 0, pos, configuration)
            self.set_mem_position(filled_freq_decimal, 1, pos, configuration)

        self.set_mem_position(txcts, 2, 32, configuration)
        self.set_mem_position(rxctcs, 2, 33, configuration)
        self.set_mem_position(squelch, 2, 34, configuration)
        self.log.send_log("debug", configuration)
        self.set_memory_configuration(configuration)
        return

    # type 0 TX
    # type 1 RX
    # type 2 special txcts, rxcts, squelch
    def set_mem_position(self, freq, type, position, configuration):
        #self.log.send_log("debug", "set_mem_position")
        offset = 0
        if type is 1:
            offset = 16
        #self.log.send_log("debug", "configuration: "+str(configuration))
        #self.log.send_log("debug", "position: "+str(position + offset))
        configuration[position + offset] = freq
        return configuration

    def set_memory_configuration(self, memory):
        self.log.send_log("debug", "set_memory_configuration")
        config = str(memory).strip('[]').replace("'", "").replace(" ", "")
        self.log.send_log("debug", "AAFA3" + str(config))
        #config="450.1250,450.1250,451.1250,451.1250,452.1250,452.1250,453.1250,453.1250,454.1250,454.1250,455.1250,455.1250,456.1250,456.1250,457.1250,457.1250,458.1250,458.1250,459.1250,459.1250,455.0250,455.0250,455.1250,455.1250,455.2250,455.2250,455.3250,455.3250,455.4250,455.4250,455.5250,455.5250,011,125,8"
        self.send_atcommand("AAFA3" + str(config))
        rcv = self.read_line()
        self.log.send_log("debug", "set memory configuration: "+str(rcv))
        return rcv

    def __getitem__(self, key):
        if key not in self.settings.keys():
            raise KeyError
        return self.settings[key]

    def __setitem__(self, key, value):
        if key not in self.settings.keys():
            raise KeyError

        self.settings[key] = value
        self.set_dmosetgroup()

    def set_rx(self):
        GPIO.output(self.gpio_ptt, 1)
        return

    def send_atcommand(self, cmd):
        self.log.send_log("debug", "send_atcommand")
        '''
        Sends commands via serial.
        Expects: serial device, and command string.

        Returns boolean
        '''
        if self.ser and cmd:
            self.ser.write(cmd.encode())
