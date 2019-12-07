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

    def __getitem__(self, key):
        if key not in self.settings.keys():
            raise KeyError
        return self.settings[key]

    def __setitem__(self, key, value):
        if key not in self.settings.keys():
            raise KeyError

        self.settings[key] = value
        self.set_dmosetgroup()


    def send_atcommand(self, cmd):
        '''
        Sends commands via serial.
        Expects: serial device, and command string.

        Returns boolean
        '''
        if self.ser and cmd:
            self.ser.write(cmd.encode())

    def set_volume(self, vol):
        '''
        Sets the volume on the dorji chip,

        Expects: serial device, and volume int (1-8)

        Returns boolean
        '''
        if vol:
            if self.send_atcommand(self.ser, 'AT+DMOSETVOLUME=%s\r\n' % (volume)):
                return True
            else:
                return False

    def set_filter(self):
        '''
        Used to turn on/off Pre/de-emphasis, lowpass, and highpass filters

        Expects a serial device and dict with:
        {pre_de_emph},{highpass},{lowpass}

        Returns boolean
        '''
        if filter:
            cmd = 'AT+SETFILTER={pre_de_emph},{highpass},{lowpass}\r\n'.format(**self.settings)

            if self.send_atcommand(cmd):
                return True
            else:
                return False

    def set_dmosetgroup(self):
        '''
        Configure a group of Dorji module options.

        Expects a serial device and a dict with:
        {channel_space},{tx_freq},{rx_freq},{tx_ctcss},{sq},{rx_ctcss}

        Returns a array with [0] - Status, [1] - Message
        '''
        cmd = 'AT+DMOSETGROUP={gwb},{tx},{rx},{tx_ctcss},{sq},{rx_ctcss}\r\n'.format(**self.settings)
        if self.send_atcommand(cmd):
            return True
        else:
            return False
