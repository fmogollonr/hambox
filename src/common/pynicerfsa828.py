#!/usr/bin/env python

import serial


class Sa828:
    '''
    A class for managing the NiceRF Sa828 chip via serial
    '''

    def __init__(self, **kwargs):
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
            'tx_ctcss': "0000",
            'rx_ctcss': "0000",
            'sq': "1",
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
        self.send_atcommand("AAFAA")
        rcv = self.read_line()
        print("received settings: ")
        print(rcv)
        return rcv

    def read_memory_configuration(self):
        self.send_atcommand("AAFA1")
        rcv = self.read_line()
        print("memory configuration: ")
        print(rcv)
        return rcv

    def set_full_configuration(self, freq, txcts=None, rxctcs=None, squelch=None):
        configuration = [None] *35
        if txcts is None:
            txcts = self.settings['tx_ctcss']
        if rxctcs is None:
            rxctcs = self.settings['rx_ctcss']
        if squelch is None:
            squelch = self.settings['sq']
        for pos in range(0, 15):
            self.set_mem_position(freq, 0, pos, configuration)
            self.set_mem_position(freq, 1, pos, configuration)

        self.set_mem_position(txcts, 2, 32, configuration)
        self.set_mem_position(rxctcs, 2, 33, configuration)
        self.set_mem_position(squelch, 2, 34, configuration)

        print(configuration)
        return


    # type 0 TX
    # type 1 RX
    # type 2 special txcts, rxcts, squelch
    def set_mem_position(self, freq, type, position, configuration):
        offset = 0
        if type is 1:
            offset = 16
        print(configuration)
        print("position")
        configuration[position+offset] = freq

        return configuration

    def set_memory_configuration(self, memory):
        config = str(memory).strip('[]')
        self.send_atcommand("AAFA3 "+config)
        rcv = self.read_line()
        print("set memory configuration: ")
        print(rcv)
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
        return

    def send_atcommand(self, cmd):
        '''
        Sends commands via serial.
        Expects: serial device, and command string.

        Returns boolean
        '''
        if self.ser and cmd:
            self.ser.write(cmd.encode())

