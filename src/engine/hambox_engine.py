import ffmpy, subprocess
from src.common.logger import Logger


class HamboxEngine:

    def __init__(self):
        self.log = {}
        self.log = Logger.logger("HamboxEngine")

    @staticmethod
    def alsa_inout(inputHw, outputHw):
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
        self.alsa_inout("1:0", "1:1")
        print("finished")
        return
