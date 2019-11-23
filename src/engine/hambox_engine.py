import os
import sys
import threading
from threading import Thread
import time
import ffmpy, subprocess
#sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'pycode'))
import logger


class hamboxEngine:

    def __init__(self):
        self.log = {}
        self.log = logger.logger("cast2bandFFmpegsystem")

    def alsaInout(self, inputHw, outputHw):
        ff = ffmpy.FFmpeg(
            inputs={input: ["-hide_banner", "-re", "hw:" + str(inputHw)]},
            outputs={output: ["-f", "alsa", "hw:" + str(outputHw)]}
        )
        try:
            stdout, stderr = ff.run(stderr=subprocess.PIPE, stdout=subprocess.PIPE)
            # print ("Launching stdout: ",stdout)
        except ffmpy.FFRuntimeError as err:
            print("There was an error")
            # print ("Error "+str(err.exit_code))
            raise err

    def tx(self):
        self.alsaInout("1:0", "1:1")
        print("finished")
        return
