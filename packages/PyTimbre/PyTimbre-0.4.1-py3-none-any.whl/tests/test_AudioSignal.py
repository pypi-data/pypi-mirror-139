from unittest import TestCase
import numpy as np
from pytimbre2.AudioSignal import AudioSignal as timbre_AudioSignal
from pytimbre2.Representations.spectro_temporal.Spectro_Temporal import STFT_Spectro_Temporal_Method
import pandas as pd, os.path
import soundfile
from UnitTestDataLocations import DataLocations


class TestAudioSignal(TestCase):
    def test_vox_example(self):
        signal = timbre_AudioSignal(DataLocations.vox_example_a())

        results = signal.get_features()

        self.assertTrue(not np.isnan(results['spectral flatness']))

        signal = timbre_AudioSignal(DataLocations.vox_example_b())

        results = signal.get_features()

