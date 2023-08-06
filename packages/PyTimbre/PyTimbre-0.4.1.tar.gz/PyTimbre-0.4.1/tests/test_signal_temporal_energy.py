from unittest import TestCase

import numpy as np

from pytimbre2.Representations.Global.signal_temporal_energy import tee
from UnitTestDataLocations import DataLocations


class Test_tee(TestCase):
    def test_get_features(self):
        inst_energy = tee(DataLocations.test_signal_file())

        ac_coefficients = inst_energy.auto_correlation_coefficients

        ac = np.transpose(np.loadtxt(DataLocations.ml_tee_autocorrelation(), delimiter=','))

        self.assertEqual(ac_coefficients.shape[0], ac.shape[0])

        for i in range(ac.shape[0]):
            for j in range(ac.shape[1]):
                self.assertAlmostEqual(ac[i, j], ac_coefficients[i, j], delta=1e-4)

        zcr = np.loadtxt(DataLocations.ml_tee_zcr(), delimiter=',')

        self.assertEqual(len(zcr), len(inst_energy.zero_crossing_rates))

        for i in range(len(zcr)):
            self.assertAlmostEqual(zcr[i], inst_energy.zero_crossing_rates[i], delta=1e-8)

    def test_vox_example_b(self):
        inst_energy = tee(DataLocations.vox_example_b())

        results = inst_energy.get_features()

