import sys
import numpy as np
import pandas as pd


class spectrum:
    """
    This class represents the conversion of the time waveform to a set of times, frequencies, and sound pressure levels.
    The method(s) for obtaining the representation is found in the Spectro_Temporal.py file.  However, all calculations
    conducted on the acoustic levels are completed here.
    """

    def __init__(self, f, fs=48000, time=None, spl=None):
        """
        This function will load the information into the class for measuring the variety of features that were extracted
        from the TimbreToolbox code.

        :param f: string or float, array-like - either the filename for the loading of the data from a file or the list
        of floating point frequency values
        :param fs: float or int - the number of samples per second for the waveform
        :param time: float or datetime, array-like - the collection of times where the measurement of the sound was
        conducted
        :param spl: float, matrix- or array-like - the values of the sound pressure level as determined from a spectro-
        gram calculation with the shape of (len(times), len(f))
        """

        #   if the first object is a string, then it is expected to be a full-path to the data that is stored in a CSV
        #   formatted file...

        if isinstance(f, str):
            data = pd.read_csv(f)
            self._times = np.asarray(data.iloc[:, 0])
            self._levels = np.asarray(data.iloc[:, 1:])
            self._frequencies = np.zeros((data.shape[1] - 1,))

            for i in range(1, data.shape[1]):
                self._frequencies[i - 1] = float(data.columns.values[i])

        elif not isinstance(f, str) and time is not None and spl is not None:
            self._frequencies = f
            self._times = time
            self._levels = spl
        else:
            raise ValueError("It is either expected that the constructor have a single string parameter, or three " +
                             "array parameters.")

        self._sample_rate = fs

        denom = np.sum(self.levels, axis=1).reshape((-1, 1)).dot(np.ones((1, len(self.frequencies))))
        denom += sys.float_info.epsilon

        self.probability_distro = self.levels / denom
        self.Y = (self.normalized_frequency.reshape(-1, 1) * np.ones((1, len(self.times)))).transpose()
        self.mean_center = None

    @property
    def probability(self):
        return self.probability_distro

    @property
    def frequencies(self):
        return self._frequencies * self.sample_rate

    @property
    def times(self):
        return self._times

    @property
    def levels(self):
        return self._levels

    @property
    def frequency_increment(self):
        df = np.diff(self.frequencies)
        return np.mean(df)

    @property
    def sample_rate(self):
        return self._sample_rate

    @property
    def normalized_frequency(self):
        return self._frequencies

    @property
    def spectral_centroid(self):
        centroid = np.sum(self.Y * self.probability_distro, axis=1)
        self.mean_center = self.Y - (centroid.reshape((-1, 1)).dot(
            np.ones((1, len(self.frequencies)))))
        return centroid

    @property
    def spectral_spread(self):
        if self.mean_center is None:
            self.spectral_centroid
        return np.sqrt(np.sum(np.square(self.mean_center) * self.probability_distro, axis=1))

    @property
    def spectral_skewness(self):
        if self.mean_center is None:
            self.spectral_centroid
        return np.sum(self.mean_center ** 3 * self.probability_distro, axis=1) / (
                (self.spectral_spread+sys.float_info.epsilon) ** 3)

    @property
    def spectral_kurtosis(self):
        if self.mean_center is None:
            self.spectral_centroid
        return np.sum(self.mean_center ** 4 * self.probability_distro, axis=1) / (
                (self.spectral_spread+sys.float_info.epsilon) ** 4)

    @property
    def spectral_slope(self):
        numerator = len(self.normalized_frequency)
        numerator *= (self.normalized_frequency.reshape((-1, 1)).transpose().dot(self.probability_distro.transpose()))
        numerator -= (np.sum(self.normalized_frequency) * np.sum(self.probability_distro, axis=1))
        denominator = (len(self.normalized_frequency) * np.sum(self.normalized_frequency ** 2) -
                       np.sum(self.normalized_frequency) ** 2)

        return numerator.transpose().reshape((-1,)) / denominator

    @property
    def spectral_decrease(self):
        denominator = 1 / np.arange(1, len(self.frequencies))
        numerator = self.levels[:, 1:].copy()
        numerator -= self.levels[:, 0].reshape((-1, 1)).dot(np.ones((1, len(self.frequencies) - 1)))

        decrease = denominator.transpose().dot(numerator.transpose())
        decrease /= np.sum(self.levels[:, 1:] + sys.float_info.epsilon, axis=1)

        return decrease

    @property
    def spectral_roll_off(self):
        #   This will only be correct according to the definition if the power spectrum is used as it assumes that the
        #   amplitude values have already been squared

        threshold = 0.95
        cumulative_sum = np.cumsum(self.levels, axis=1)
        vector_sum = np.sum(self.levels, axis=1) * threshold
        binary_search = 1. * (cumulative_sum > vector_sum.reshape((-1, 1)).dot(np.ones((1, len(self.frequencies)))))
        cumulative_sum = np.cumsum(self.levels, axis=1)
        vector_sum = np.sum(self.levels, axis=1) * threshold
        binary_search = 1. * (
                    cumulative_sum > vector_sum.reshape((-1, 1)).dot(np.ones((1, len(self.normalized_frequency)))))
        cumulative_binary_search_sum = np.cumsum(binary_search, axis=1)
        idx = np.zeros(self.times.shape, dtype='int')
        for i in range(len(self.times)):
            idx = np.zeros(self.times.shape, dtype='int')
        for i in range(len(self.times)):
            indeces = np.where(cumulative_binary_search_sum[i, :] >= 1)[0]

            if len(indeces) > 0:
                idx[i] = indeces[0]
            else:
                idx[i] = len(self.frequencies)-1

        return self.normalized_frequency[idx]
        return normalized_frequency[idx]

    @property
    def spectral_variation(self):
        a = self.levels.copy()
        b = np.row_stack([np.zeros((1, len(self.frequencies))), self.levels[:-1, :]])
        cross_product = np.sum(a * b, axis=1)

        auto_product = np.sum(self.levels ** 2, axis=1)
        auto_product *= np.sum(b**2, axis=1)

        spectral_variation = 1 - (cross_product / (np.sqrt(auto_product) + sys.float_info.epsilon))
        spectral_variation[0] = spectral_variation[1]

        return spectral_variation

    @property
    def spectral_energy(self):
        return np.sum(self.levels, axis=1)

    @property
    def spectral_flatness(self):
        geometric_mean = np.exp(np.sum(np.log(self.levels + sys.float_info.epsilon), axis=1) / len(self.frequencies))
        arithmetic_mean = np.mean(self.levels + sys.float_info.epsilon, axis=1)

        return geometric_mean / arithmetic_mean

    @property
    def spectral_crest(self):
        return np.max(self.levels, axis=1) / np.mean(self.levels + sys.float_info.epsilon, axis=1)

    @property
    def features(self):
        results = dict()

        results['spectral centroid'] = self.spectral_centroid
        results['spectral spread'] = self.spectral_spread
        results['spectral skewness'] = self.spectral_skewness
        results['spectral kurtosis'] = self.spectral_kurtosis
        results['spectral slope'] = self.spectral_slope
        results['spectral decrease'] = self.spectral_decrease
        results['spectral rolloff'] = self.spectral_roll_off
        results['spectral variation'] = self.spectral_variation
        results['spectral energy'] = self.spectral_energy
        results['spectral flatness'] = self.spectral_flatness
        results['spectral crest'] = self.spectral_crest

        return results

    @staticmethod
    def feature_names():
        names = list()

        names.append('spectral centroid')
        names.append('spectral spread')
        names.append('spectral skewness')
        names.append('spectral kurtosis')
        names.append('spectral slope')
        names.append('spectral decrease')
        names.append('spectral rolloff')
        names.append('spectral variation')
        names.append('spectral energy')
        names.append('spectral flatness')
        names.append('spectral crest')

        return names
