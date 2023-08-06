from unittest import TestCase
from nptdms import TdmsFile, TdmsGroup, TdmsChannel
from pytimbre2.AudioSignal import AudioSignal as timbre_AudioSignal
from pytimbre2.Representations.spectro_temporal.Spectro_Temporal import STFT_Spectro_Temporal_Method
import pandas as pd, os.path
import soundfile
from UnitTestDataLocations import DataLocations


class Test_NIOSH(TestCase):
    def test_process_NIOSH_tdms(self):
        with TdmsFile.open(DataLocations.niosh_tool_example()) as tdms:
            grp = tdms['SP']

            if not isinstance(grp, TdmsGroup):
                raise ValueError("Never happens")

            fs = 50000

            samples = grp['0'].read_data()

            signal = timbre_AudioSignal(samples, fs)
            signal

            values = signal.get_features()