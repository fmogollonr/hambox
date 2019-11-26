import ffmpy
from src.common.logger import Logger
from src.common.config import Config
from multiprocessing import Process
import psutil


class HamboxEngine:

    def __init__(self):
        self.log = {}
        self.log = Logger("HamboxEngine")
        self.process_pid=0

    @staticmethod
    def alsa_inout(inputHw, outputHw):
        ff = ffmpy.FFmpeg(
            inputs={
                "hw:" + str(inputHw): ["-hide_banner", "-re", "-loglevel", "quiet", "-f", "s16le", "-ar", "44100", "-ac", "1", "-f", "alsa"]},
            outputs={"hw:" + str(outputHw): ["-f", "alsa", "-ac", "2"]}
        )
        process = Process(target=ff.run, args=())
        process.daemon = False
        process.start()
        return process.pid

    def tx(self):
        config = Config()
        audioconfig = config.read_audio_config()
        self.kill_previous_process()
        self.process_pid = self.alsa_inout(audioconfig['mic'], audioconfig['rf_in'])
        return

    def rx(self):
        config = Config()
        audioconfig = config.read_audio_config()
        self.kill_previous_process()
        self.process_pid = self.alsa_inout(audioconfig['rf_out'], audioconfig['spk'])
        return

    def kill_previous_process(self):
        print("process is "+str(self.process_pid))
        if self.process_pid is not 0:
            try:
                parent = psutil.Process(self.process_pid)
                for child in parent.children(recursive=True):
                    child.kill()
            except:
                print("PID ", self.process_pid, " was dead")

