import numpy as np
import soundfile
import statsmodels.api as smfr
from statsmodels.tsa.stattools import acf


class tee:
    def __init__(self, signal, fs=None, channel=0):
        """
        The default constructor - builds the information within the class using either the filename or the signal
        directly.
        """

        if isinstance(signal, str):
            self.signal, self.fs = soundfile.read(signal)
        else:
            self.signal = signal
            if fs is None:
                self.fs = 48000
            else:
                self.fs = fs

        if len(self.signal.shape) > 1:
            self.signal = self.signal[:, channel]

        self._coefficient_count = 12
        self._hop_size_seconds = 0.0029
        self._window_size_seconds = 0.0232
        self._cutoff_frequency = 5
        self.auto_coefficients = None
        self.zero_crossing_rate = None

    @property
    def window_size_seconds(self):
        return self._window_size_seconds

    @window_size_seconds.setter
    def window_size_seconds(self, value):
        self._window_size_seconds = value
        self._determine_instantaneous_temporal_features()

    @property
    def hop_size_seconds(self):
        return self._hop_size_seconds

    @hop_size_seconds.setter
    def hop_size_seconds(self, value):
        self._hop_size_seconds = value
        self._determine_instantaneous_temporal_features()

    @property
    def window_size_samples(self):
        return int(np.round(self.window_size_seconds * self.fs))

    @property
    def hop_size_samples(self):
        return int(round(self.hop_size_seconds * self.fs))

    @property
    def times(self):
        return self._times

    @property
    def coefficient_count(self):
        """
        The number of coefficients to generate for the available data
        """

        return self._coefficient_count

    @coefficient_count.setter
    def coefficient_count(self, value):
        """
        Set the number of coefficients for the analysis
        """

        self._coefficient_count = value
        self._determine_instantaneous_temporal_features()

    @property
    def auto_correlation_coefficients(self):
        if self.auto_coefficients is None:
            self._determine_instantaneous_temporal_features()

        return self.auto_coefficients

    @property
    def zero_crossing_rates(self):
        if self.zero_crossing_rate is None:
            self._determine_instantaneous_temporal_features()

        return self.zero_crossing_rate

    @staticmethod
    def detect_local_extrema(input_v, lag_n):
        """
        This will detect the local maxima of the vector on the interval [n-lag_n:n+lag_n]

        Parameters
        ----------
        input_v : double array-like
            This is the input vector that we are examining to determine the local maxima
        lag_n : double, integer
            This is the number of samples that we are examining within the input_v to determine the local maximum

        Returns
        -------
        pos_max_v : double, array-like
            The locations of the local maxima
        """

        do_affiche = 0
        lag2_n = 4
        seuil = 0

        L_n = len(input_v)

        pos_cand_v = np.where(np.diff(np.sign(np.diff(input_v))) < 0)[0]
        pos_cand_v += 1

        pos_max_v = np.zeros((len(pos_cand_v),))

        for i in range(len(pos_cand_v)):
            pos = pos_cand_v[i]

            if (pos > lag_n) & (pos <= L_n - lag_n):
                tmp = input_v[pos - lag_n:pos + lag2_n]
                position = np.argmax(tmp)

                position = position + pos - lag_n - 1

                if (pos - lag2_n > 0) & (pos + lag2_n < L_n + 1):
                    tmp2 = input_v[pos - lag2_n:pos + lag2_n]

                    if (position == pos) & (input_v[position] > seuil * np.mean(tmp2)):
                        pos_max_v[i] = pos

        return pos_max_v

    @staticmethod
    def next_pow2(x: int):
        n = np.log2(x)
        return 2 ** (np.floor(n) + 1)

    def _determine_instantaneous_temporal_features(self):
        """
        This function will calculate the instantaneous features within the temporal analysis.  This includes the
        auto-correlation and the zero crossing rate.
        """
        count = 0
        dAS_f_SupX_v_count = 0
        self._times = np.zeros((int(np.floor((len(self.signal)-self.window_size_samples)/self.hop_size_samples)+1),))

        self.auto_coefficients = np.zeros((len(self._times), self.coefficient_count))
        self.zero_crossing_rate = np.zeros((len(self._times),))

        #   Loop through the frames

        for n in range(0, len(self._times)):
            #   Get the frame

            frame_length = self.window_size_samples
            start = n * self.hop_size_samples
            frame_index = np.arange(start, frame_length+start)
            f_Frm_v = self.signal[frame_index] * np.hamming(self.window_size_samples)
            self._times[n] = start / self.fs

            count += 1

            #   Calculate the auto correlation coefficients

            self.auto_coefficients[n, :] = smfr.tsa.acf(f_Frm_v, nlags=self.coefficient_count, fft=False)[1:]

            #   Now the zero crossing rate

            i_Sign_v = np.sign(f_Frm_v - np.mean(f_Frm_v))
            i_Zcr_v = np.where(np.diff(i_Sign_v))[0]
            i_Num_Zcr = len(i_Zcr_v)
            self.zero_crossing_rate[n] = i_Num_Zcr / (len(f_Frm_v) / self.fs)

    def get_features(self):
        features = dict()

        features['auto_correlation'] = self.auto_correlation_coefficients
        features['zero crossing rate'] = self.zero_crossing_rates

        return features

    def get_feature(self, name):
        return self.get_features()[name]

    @property
    def feature_names(self):
        names = list()

        names.append("auto_correlation")
        names.append("zero crossing rate")

        return names
