import ffmpy, subprocess
from src.common.logger import Logger
from src.common.config import Config


class HamboxEngine:

    def __init__(self):
        self.log = {}
        self.log = Logger("HamboxEngine")

    @staticmethod
    def alsa_inout(inputHw, outputHw):
        ff = ffmpy.FFmpeg(
            inputs={"hw:" + str(inputHw): ["-hide_banner", "-re", "-f", "s16le", "-ar", "44100", "-ac", "1", "-f", "alsa" ]},
            outputs={"hw:" + str(outputHw): ["-f", "alsa", "-ac", "2" ]}
        )
        try:
            stdout, stderr = ff.run(stderr=subprocess.PIPE, stdout=subprocess.PIPE)
        except ffmpy.FFRuntimeError as err:
            print("There was an error")
            raise err

    def tx(self):
        config = Config()
        audioconfig = config.read_audio_config()
        self.alsa_inout(audioconfig['mic'], audioconfig['rf_in'])
        return

    def rx(self):
        config = Config()
        audioconfig = config.read_audio_config()
        self.alsa_inout(audioconfig['rf_out'], audioconfig['spk'])
        return
