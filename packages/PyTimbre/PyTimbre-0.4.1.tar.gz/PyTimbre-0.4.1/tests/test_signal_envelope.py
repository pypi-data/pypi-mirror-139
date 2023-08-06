from unittest import TestCase
import numpy as np
from UnitTestDataLocations import DataLocations
from pytimbre2.Representations.Global.signal_envelope import envelope
from tqdm import tqdm


class Test_envelope(TestCase):
    def test_constructor(self):
        data = np.loadtxt(DataLocations.ml_envelope(), delimiter=',')

        env = envelope(DataLocations.test_signal_file())

        self.assertEqual(44100, env.fs)
        self.assertEqual(len(data), len(env.waveform))

        with tqdm(total=len(env.waveform))as t:
            for i in range(len(env.waveform)):
                self.assertAlmostEqual(data[i], env.signal_envelope[i], delta=1e-10)
                t.update()

    def test_features(self):
        env = envelope(DataLocations.test_signal_file())

        self.assertEqual(44100, env.fs)

        self.assertAlmostEqual(-1.04259579968574, env.log_attack, delta=1e-8)
        self.assertAlmostEqual(0.0300226757369615, env.attack, delta=1e-2)
        self.assertAlmostEqual(0.141451247165533, env.decrease, delta=1e-2)
        self.assertAlmostEqual(3.99199546485261, env.release, delta=1e-4)
        self.assertAlmostEqual(10.2201294649487, env.attack_slope, delta=1e-5)
        self.assertAlmostEqual(-0.00177289595957093, env.decrease_slope, delta=1e-5)
        self.assertAlmostEqual(2.02851979623896, env.temporal_centroid, delta=1e-5)
        self.assertAlmostEqual(3.92981859410431, env.effective_duration, delta=1e-5)
        self.assertAlmostEqual(1.12395775200773, env.frequency_modulation, delta=1e-5)
        self.assertAlmostEqual(1.54543330332658e-06, env.amplitude_modulation, delta=1e-5)

    def test_vox_example_b(self):
        env = envelope(DataLocations.vox_example_b())

        self.assertEqual(16000, env.fs)

        try:
            results = env.get_features()
        except RuntimeWarning as error:
            self.assertTrue(False, msg=error)

    def test_vox_example_c(self):
        env = envelope(DataLocations.vox_example_c())

        self.assertEqual(16000, env.fs)

        try:
            results = env.get_features()
        except RuntimeWarning as error:
            self.assertTrue(False, msg=error)

    def test_vox_example_e(self):
        env = envelope(DataLocations.vox_example_e())

        self.assertEqual(16000, env.fs)

        try:
            results = env.get_features()
        except RuntimeWarning as error:
            self.assertTrue(False, msg=error)