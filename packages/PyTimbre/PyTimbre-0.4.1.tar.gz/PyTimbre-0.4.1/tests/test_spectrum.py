from unittest import TestCase
import soundfile
import numpy as np
from tqdm import tqdm
from UnitTestDataLocations import DataLocations
from pytimbre2.Representations.spectro_temporal.spectrum import spectrum
from pytimbre2.Representations.spectro_temporal.Spectro_Temporal import spectrogram_representation


class Test_spectrum(TestCase):
    def test_constructor(self):
        spec = spectrum(DataLocations.matlab_spectrum_file())

        self.assertEqual(2048, len(spec.frequencies))
        self.assertEqual(686, len(spec.times))

        ml_prob_distro = np.loadtxt(DataLocations.ml_prob_dist(), delimiter=',')

        with tqdm(total=len(spec.times), desc="Probability Distribution") as t:
            for i in range(len(spec.times)):
                for j in range(len(spec.frequencies)):
                    self.assertAlmostEqual(ml_prob_distro[i, j], spec.probability_distro[i, j], delta=1e-10,
                                           msg="Error at [i, j] = [{}, {}]".format(i, j))

                t.update()

        integration_variable = np.loadtxt(DataLocations.ml_variable_of_integration(), delimiter=',')

        with tqdm(total=len(spec.times), desc="Variable of integration") as t:
            for i in range(len(spec.times)):
                for j in range(len(spec.frequencies)):
                    self.assertAlmostEqual(integration_variable[j, i], spec.Y[i, j], delta=1e-10,
                                           msg="Error at [i, j] = [{}, {}]".format(i, j))

                t.update()

    def test_spectral_centroid(self):
        spec = spectrum(DataLocations.matlab_spectrum_file())

        self.assertEqual(2048, len(spec.frequencies))
        self.assertEqual(686, len(spec.times))

        spectro_temporal_features = np.loadtxt(DataLocations.ml_spectro_temporal_features(), delimiter=',')

        with tqdm(total=len(spec.times), desc='Spectral Centroid') as t:
            value = spec.spectral_centroid
            for i in range(len(value)):
                self.assertAlmostEqual(spectro_temporal_features[i, 0], value[i], delta=1e-8)

                t.update()

    def test_spectral_spread(self):
        spec = spectrum(DataLocations.matlab_spectrum_file())

        self.assertEqual(2048, len(spec.frequencies))
        self.assertEqual(686, len(spec.times))

        spectro_temporal_features = np.loadtxt(DataLocations.ml_spectro_temporal_features(), delimiter=',')

        with tqdm(total=len(spec.times), desc='Spectral Spread') as t:
            value = spec.spectral_spread
            for i in range(len(spec.times)):
                self.assertAlmostEqual(spectro_temporal_features[i, 1], value[i], delta=1e-10)

                t.update()

    def test_spectral_skew(self):
        spec = spectrum(DataLocations.matlab_spectrum_file())

        self.assertEqual(2048, len(spec.frequencies))
        self.assertEqual(686, len(spec.times))

        spectro_temporal_features = np.loadtxt(DataLocations.ml_spectro_temporal_features(), delimiter=',')

        with tqdm(total=len(spec.times), desc='Spectral Skewness') as t:
            value = spec.spectral_skewness
            for i in range(len(spec.times)):
                self.assertAlmostEqual(spectro_temporal_features[i, 2], value[i], delta=1e-10)

                t.update()

    def test_spectral_kurtosis(self):
        spec = spectrum(DataLocations.matlab_spectrum_file())

        self.assertEqual(2048, len(spec.frequencies))
        self.assertEqual(686, len(spec.times))

        spectro_temporal_features = np.loadtxt(DataLocations.ml_spectro_temporal_features(), delimiter=',')

        with tqdm(total=len(spec.times), desc='Spectral Skewness') as t:
            value = spec.spectral_kurtosis
            for i in range(len(spec.times)):
                self.assertAlmostEqual(spectro_temporal_features[i, 3], value[i], delta=1e-9)

                t.update()

    def test_spectral_slope(self):
        spec = spectrum(DataLocations.matlab_spectrum_file())

        self.assertEqual(2048, len(spec.frequencies))
        self.assertEqual(686, len(spec.times))

        spectro_temporal_features = np.loadtxt(DataLocations.ml_spectro_temporal_features(), delimiter=',')

        with tqdm(total=len(spec.times), desc='Spectral Skewness') as t:
            value = spec.spectral_slope
            for i in range(len(spec.times)):
                self.assertAlmostEqual(spectro_temporal_features[i, 4], value[i], delta=1e-9)

                t.update()

    def test_spectral_decrease(self):
        spec = spectrum(DataLocations.matlab_spectrum_file())

        self.assertEqual(2048, len(spec.frequencies))
        self.assertEqual(686, len(spec.times))

        spectro_temporal_features = np.loadtxt(DataLocations.ml_spectro_temporal_features(), delimiter=',')

        with tqdm(total=len(spec.times), desc='Spectral Decrease') as t:
            value = spec.spectral_decrease
            for i in range(len(spec.times)):
                self.assertAlmostEqual(spectro_temporal_features[i, 5], value[i], delta=1e-3)

                t.update()

    def test_spectral_roll_off(self):
        spec = spectrum(DataLocations.matlab_spectrum_file())

        self.assertEqual(2048, len(spec.frequencies))
        self.assertEqual(686, len(spec.times))

        spectro_temporal_features = np.loadtxt(DataLocations.ml_spectro_temporal_features(), delimiter=',')

        with tqdm(total=len(spec.times), desc='Spectral Roll_off') as t:
            value = spec.spectral_roll_off
            for i in range(len(spec.times)):
                self.assertAlmostEqual(spectro_temporal_features[i, 6], value[i], delta=5e-3)

                t.update()

    def test_spectral_variance(self):
        spec = spectrum(DataLocations.matlab_spectrum_file())

        self.assertEqual(2048, len(spec.frequencies))
        self.assertEqual(686, len(spec.times))

        spectro_temporal_features = np.loadtxt(DataLocations.ml_spectro_temporal_features(), delimiter=',')

        with tqdm(total=len(spec.times), desc='Spectral variation') as t:
            value = spec.spectral_variation
            for i in range(len(spec.times)):
                self.assertAlmostEqual(spectro_temporal_features[i, 7], value[i], delta=5e-3)

                t.update()

    def test_spectral_energy(self):
        spec = spectrum(DataLocations.matlab_spectrum_file())

        self.assertEqual(2048, len(spec.frequencies))
        self.assertEqual(686, len(spec.times))

        spectro_temporal_features = np.loadtxt(DataLocations.ml_spectro_temporal_features(), delimiter=',')

        with tqdm(total=len(spec.times), desc='Spectral variation') as t:
            value = spec.spectral_energy
            for i in range(len(spec.times)):
                self.assertAlmostEqual(spectro_temporal_features[i, 8], value[i], delta=5e-3)

                t.update()

    def test_spectral_flatness(self):
        spec = spectrum(DataLocations.matlab_spectrum_file())

        self.assertEqual(2048, len(spec.frequencies))
        self.assertEqual(686, len(spec.times))

        spectro_temporal_features = np.loadtxt(DataLocations.ml_spectro_temporal_features(), delimiter=',')

        with tqdm(total=len(spec.times), desc='Spectral flatness') as t:
            value = spec.spectral_flatness
            for i in range(len(spec.times)):
                self.assertAlmostEqual(spectro_temporal_features[i, 9], value[i], delta=5e-3)

                t.update()

    def test_spectral_crest(self):
        spec = spectrum(DataLocations.matlab_spectrum_file())

        self.assertEqual(2048, len(spec.frequencies))
        self.assertEqual(686, len(spec.times))

        spectro_temporal_features = np.loadtxt(DataLocations.ml_spectro_temporal_features(), delimiter=',')

        with tqdm(total=len(spec.times), desc='Spectral variation') as t:
            value = spec.spectral_crest
            for i in range(len(spec.times)):
                self.assertAlmostEqual(spectro_temporal_features[i, 10], value[i], delta=5e-3)

                t.update()

    def test_features(self):
        spec = spectrum(DataLocations.matlab_spectrum_file())

        self.assertEqual(2048, len(spec.frequencies))
        self.assertEqual(686, len(spec.times))

        spectro_temporal_features = np.loadtxt(DataLocations.ml_spectro_temporal_features(), delimiter=',')

        results = spec.features

        n = 0

        for key in results.keys():
            self.assertAlmostEqual(np.mean(spectro_temporal_features[:, n]), np.mean(results[key]), delta=5e-3)
            n += 1

    def test_vox_example_d(self):
        y, fs = soundfile.read(DataLocations.vox_example_d())
        spectro = spectrogram_representation(y, fs, nfft=4096)
        spectro.calculate_spectrogram()

        spec = spectrum(spectro.frequencies / spectro.sample_rate, spectro.sample_rate, spectro.times, spectro.levels)

        try:
            results = spec.features
        except Exception as ee:
            self.assertTrue(False, msg=ee)

        for key in results.keys():
            self.assertFalse(np.any(np.isnan(results[key])))
            self.assertFalse(np.any(np.isinf(results[key])))
