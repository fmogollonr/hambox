#!/usr/bin/env python

#import pyserial
from fakeserial import Serial
class Dorji:
    '''
    A class for managing the Dorji818 chip via serial
    '''

    def __init__( self, **kwargs ):
        '''
        Set defaults

        Establish a serial connection to device at baud rate, uses pyserial

          Serial options:
            * baud - Baud rate string        | Default: "9600"
            * device - a device string       | Default: "/dev/ttyS0"

          Frequency options:
            * tx - transmit frequency string | Default: "134.0000"
            * rx - receive frequency string  | Default: "134.0000"
            * sq - squelch integer 1-8       | Default: 1
            * vol - volume integer 1-8       | Default: 1
            * gwb - Channel Space 1-25000    | Default: 0

          Filter options:
           * pre_de_emph -  ??               | Default: 1
           * highpass - highpass filter      | Default: 1
           * lowpass - lowpass filter        | Default: 1

          Continuous Tone-Coded Squelch System
            * tx_ctcss - transmit - string   | Default: "0000"
            * rx_ctcss - receive - string    | Default"0000"

        Also runs a handshake validation that the Dorji module is working.
        '''

        self.settings = {
            'tx' : "134.0000",
            'rx' : "134.0000",
            'tx_ctcss' : "0000",
            'rx_ctcss' : "0000",
            'gwb' : "0",
            'sq' : "1",
            'device' : "/dev/ttyS0",
            'baud' : "9600",
            'vol' : "1",
            'pre_de_emph' : "1",
            'highpass' : "1",
            'lowpass' : "1",
        }

        self.settings.update(kwargs)

        self.ser = Serial(self.settings['device'],
                            self.settings['baud'], timeout=2)

        if not self.ser.isOpen():
            exit("error")

        if not self.send_atcommand('AT+DMOCONNECT\r\n'): exit("Handshake Error.")
        if not self.set_dmosetgroup(): print("DMO Settings Error")
        if not self.set_filter(): print("Filter Settings Error")


    def __getitem__(self, key):
        if key not in self.settings.keys():
            raise KeyError
        return self.settings[key]


    def __setitem__(self, key, value):
        if key not in self.settings.keys():
            raise KeyError

        self.settings[key] = value
        self.set_dmosetgroup()


    def scan_freq(self,freq):
        '''
        Scans wanted frequency for signal
        Expects: Frequency (xxx.yyyy)
        Returns: boolean
        '''
        if self.ser and freq:
            cmd="S+%s" %(freq)
            self.ser.write(cmd)
            r = self.ser.readline().split("=")[1].rstrip('\r\n')
            if r == "1": return False
            elif r == "0": return True
            else: return False


    def send_atcommand(self,cmd):
        '''
        Sends commands via serial.
        Expects: serial device, and command string.

        Returns boolean
        '''
        if self.ser and cmd:
            self.ser.write(cmd)
            r = self.ser.readline().split(":")[1].rstrip('\r\n')

            if r == "1": return False
            elif r == "0": return True
            else: return False


    def set_volume(self,vol):
        '''
        Sets the volume on the dorji chip,

        Expects: serial device, and volume int (1-8)

        Returns boolean
        '''
        if vol:
            if self.send_atcommand(self.ser,'AT+DMOSETVOLUME=%s\r\n' %(volume)):
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
