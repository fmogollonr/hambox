import ffmpy
from src.common.logger import Logger
from src.common.config import Config
from multiprocessing import Process
import psutil
import datetime


class HamboxEngine:

    def __init__(self):
        self.log = {}
        self.log = Logger("HamboxEngine")
        self.process_pid = 0
        self.record_pid = 0

    @staticmethod
    def pulseaudio_inout(inputHw, outputHw):
        ff = ffmpy.FFmpeg(
            inputs={
                str(inputHw): ["-hide_banner", "-re", "-loglevel", "quiet", "-f", "s16le", "-ar", "44100", "-ac", "1", "-f", "pulse"]},
            outputs={str(outputHw): ["-f", "pulse", "-ac", "2"]}
        )
        process = Process(target=ff.run, args=())
        process.daemon = False
        process.start()
        return process.pid

# ffmpeg -f s16le -ar 44100 -ac 1 -f alsa -i hw:audio_b -f s16le -ar 44100 -ac 1 -f alsa -i hw:audio_a -filter_complex [0:a][1:a]join=inputs=2:channel_layout=stereo[a] -map [a] output.wav
    @staticmethod
    def pulseaudio_record(first_inputHw, second_inputHw, fileOutput):
        ff = ffmpy.FFmpeg(
            inputs={
                str(first_inputHw): ["-hide_banner", "-re", "-loglevel", "quiet", "-f", "s16le", "-ar", "44100", "-ac", "1", "-f", "pulse"],
                str(second_inputHw): ["-f", "s16le", "-ar", "44100", "-ac", "1", "-f", "pulse"]},
            outputs={str(fileOutput): ["-filter_complex", "[0:a][1:a]join=inputs=2:channel_layout=stereo[a]", "-map", "[a]"]}
        )
        process = Process(target=ff.run, args=())
        process.daemon = False
        process.start()
        return process.pid

    def tx(self):
        config = Config()
        audioconfig = config.read_audio_config()
        self.kill_process(self.process_pid)
        self.process_pid = self.pulseaudio_inout(audioconfig['mic'], audioconfig['rf_in'])
        return

    def rx(self):
        config = Config()
        audioconfig = config.read_audio_config()
        self.kill_process(self.process_pid)
        self.process_pid = self.pulseaudio_inout(audioconfig['rf_out'], audioconfig['spk'])
        return

    def rec(self):
        config = Config()
        audioconfig = config.read_audio_config()
        hamboxconfig = config.read_hambox_config()
        file_name = hamboxconfig['callsign']
        date = datetime.datetime.now()
        print("Date is "+str(date.strftime("%Y%m%d_%H%M%S")))
        self.record_pid = self.pulseaudio_record(audioconfig['rf_out'], audioconfig['mic'], file_name + date.strftime("%Y%m%d_%H%M%S") + ".wav")
        return file_name

    def stop_rec(self):
        self.kill_process(self.record_pid)
        self.record_pid = 0
        return

    @staticmethod
    def kill_process(pid):
        print("process is "+str(pid))
        if pid is not 0:
            try:
                parent = psutil.Process(pid)
                for child in parent.children(recursive=True):
                    child.kill()
            except:
                print("PID ", pid, " was dead")

