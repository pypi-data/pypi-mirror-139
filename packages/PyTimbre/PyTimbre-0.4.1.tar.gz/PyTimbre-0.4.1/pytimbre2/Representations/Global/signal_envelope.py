import numpy as np
from scipy.signal import hilbert, butter, lfilter
import soundfile
import sys


class envelope:
    def __init__(self, f, fs=None, cutoff_frequency=5, channel=0, NFFT=None):
        """
        This is the constructor for the class and will populate the data from either a file that is a wave file, or from
        a waveform that is passed to the class constructor

        :param f: string or float, array-like - either the path to the file or the signal array itself
        :param fs: float or int - the number of samples per second
        :param cutoff_frequency: float - the upper limit to the calculation of the signal envelope
        :param channel: integer - the zero based index of the channel to process
        :param NFFT: integer - frequency resolution for the amplitude modulation of the input signal
        """

        if isinstance(f, str):
            self.waveform, self.fs = soundfile.read(f)
            if len(self.waveform.shape) > 1:
                self.waveform = self.waveform[:, channel]
        else:
            self.waveform = np.copy(f)

            if fs is not None:
                self.fs = fs
            else:
                self.fs = 48000

        self._cutoff_frequency = cutoff_frequency
        self._centroid_threshold = 0.15
        self._effective_duration_threshold = 0.4

        if NFFT is None:
            self._nfft = len(self.waveform)
        else:
            self._nfft = NFFT

        #   Since all the functions within here require the envelope, we will calculate than now.

        self._calculate_envelope()

        self._log_attack = sys.float_info.epsilon
        self._increase = sys.float_info.epsilon
        self._decrease = sys.float_info.epsilon
        self._address = None
        self._temporal_centroid = sys.float_info.epsilon
        self._effective_duration = sys.float_info.epsilon
        self._frequency_modulation = sys.float_info.epsilon
        self._amplitude_modulation = sys.float_info.epsilon

    @property
    def centroid_threshold(self):
        return self._centroid_threshold

    @centroid_threshold.setter
    def centroid_threshold(self, value):
        self._centroid_threshold = value
        self._temporal_centroid = sys.float_info.epsilon

    @property
    def cutoff_frequency(self):
        return self._cutoff_frequency

    @cutoff_frequency.setter
    def cutoff_frequency(self, value):
        self._cutoff_frequency = value
        self._calculate_envelope()

    @property
    def effective_duration_threshold(self):
        return self._effective_duration_threshold

    @effective_duration_threshold.setter
    def effective_duration_threshold(self, value):
        self._effective_duration_threshold = value

    @property
    def temporal_centroid(self):
        if self._temporal_centroid == sys.float_info.epsilon:
            env_max_idx = np.argmax(self.signal_envelope)
            over_threshold_idcs = np.where(self.normal_signal_envelope > self.centroid_threshold)[0]

            over_threshold_start_idx = over_threshold_idcs[0]
            if over_threshold_start_idx == env_max_idx:
                over_threshold_start_idx = over_threshold_start_idx - 1

            over_threshold_end_idx = over_threshold_idcs[-1]

            over_threshold_TEE = self.signal_envelope[over_threshold_start_idx - 1:over_threshold_end_idx - 1]
            over_threshold_support = [*range(len(over_threshold_TEE))]
            over_threshold_mean = np.divide(np.sum(np.multiply(over_threshold_support, over_threshold_TEE)),
                                            np.sum(over_threshold_TEE))

            self._temporal_centroid = ((over_threshold_start_idx + 1 + over_threshold_mean) / self.fs)

        return self._temporal_centroid

    @property
    def effective_duration(self):
        if self._effective_duration == sys.float_info.epsilon:
            env_max_idx = np.argmax(self.signal_envelope)
            over_threshold_idcs = np.where(self.normal_signal_envelope > self.effective_duration_threshold)[0]

            over_threshold_start_idx = over_threshold_idcs[0]
            if over_threshold_start_idx == env_max_idx:
                over_threshold_start_idx = over_threshold_start_idx - 1

            over_threshold_end_idx = over_threshold_idcs[-1]

            self._effective_duration = (over_threshold_end_idx - over_threshold_start_idx + 1) / self.fs

        return self._effective_duration

    @property
    def log_attack(self):
        if self._log_attack == sys.float_info.epsilon:
            self._log_attack, self._increase, self._decrease, self._address = self._calculate_log_attack()

        return self._log_attack

    @property
    def attack_slope(self):
        if self._increase == sys.float_info.epsilon:
            self._log_attack, self._increase, self._decrease, self._address = self._calculate_log_attack()

        return self._increase

    @property
    def decrease_slope(self):
        if self._decrease == sys.float_info.epsilon:
            self._log_attack, self._increase, self._decrease, self._address = self._calculate_log_attack()

        return self._decrease

    @property
    def attack(self):
        if self._address is None:
            self._log_attack, self._increase, self._decrease, self._address = self._calculate_log_attack()

        return self._address[0]

    @property
    def decrease(self):
        if self._address is None:
            self._log_attack, self._increase, self._decrease, self._address = self._calculate_log_attack()

        return self._address[1]

    @property
    def release(self):
        if self._address is None:
            self._log_attack, self._increase, self._decrease, self._address = self._calculate_log_attack()

        return self._address[4]

    @property
    def frequency_modulation(self):
        if self._frequency_modulation == sys.float_info.epsilon:
            self._calculate_modulation()

        return self._frequency_modulation

    @property
    def amplitude_modulation(self):
        if self._amplitude_modulation == sys.float_info.epsilon:
            self._calculate_modulation()

        return self._amplitude_modulation

    def _calculate_modulation(self):
        """
        Calculate the frequency/amplitude modulations of the signal.  This can be accomplished with either a Fourier or
        Hilbert method.
        """

        sample_times = np.arange(len(self.signal_envelope) - 1) / self.fs

        sustain_start_time = self._address[1]
        sustain_end_time = self._address[4]

        is_sustained = False

        pos_v = 0

        if (sustain_end_time - sustain_start_time) > 0.02:
            pos_v = np.where((sustain_start_time <= sample_times) & (sample_times <= sustain_end_time))[0]
            if len(pos_v) > 0:
                is_sustained = True

        if not is_sustained:
            amplitude_modulation = 0
            frequency_modulation = 0
        else:
            envelop_v = self.signal_envelope[pos_v]
            temps_sec_v = sample_times[pos_v]
            M = np.mean(envelop_v)

            #   Taking the envelope

            mon_poly = self._calculate_linear_fit(temps_sec_v, np.log(envelop_v + sys.float_info.epsilon))
            hat_envelope_v = np.exp(np.polyval(mon_poly[::-1], temps_sec_v))
            signal_v = envelop_v - hat_envelope_v

            sa_v = hilbert(signal_v, N=self._nfft)
            sa_amplitude_v = abs(signal_v)
            sa_phase_v = np.unwrap(np.angle(sa_v))
            sa_instantaneous_frequency = (1 / 2 / np.pi) * sa_phase_v / (len(temps_sec_v) / self.fs)

            self._amplitude_modulation = np.median(sa_amplitude_v)
            self._frequency_modulation = np.median(sa_instantaneous_frequency)

    def _calculate_envelope(self):
        analytic_signal = hilbert(self.waveform)
        amplitude_modulation = np.abs(analytic_signal).real
        normalized_freq = self.cutoff_frequency / (self.fs / 2)
        b, a = butter(3, normalized_freq, btype='low')
        self.signal_envelope = abs(lfilter(b, a, amplitude_modulation))
        self.normal_signal_envelope = self.signal_envelope / np.max(self.signal_envelope)

        self._log_attack = sys.float_info.epsilon
        self._increase = sys.float_info.epsilon
        self._decrease = sys.float_info.epsilon
        self._address = None

    def _calculate_log_attack(self):
        """
        This calculates the various global attributes.

        In some cases the calculation of the attack did not return an array, so
        the error is trapped for when a single values is returned rather than
        an array.

        Returns
        -------
        attack_start : TYPE
            DESCRIPTION.
        log_attack_time : TYPE
            DESCRIPTION.
        attack_slope : TYPE
            DESCRIPTION.
        attack_end : TYPE
            DESCRIPTION.
        release : TYPE
            DESCRIPTION.
        release_slope : TYPE
            DESCRIPTION.

        """

        #   Define some specific constants for this calculation

        method = 3
        noise_threshold = 0.15
        decrease_threshold = 0.4

        #   Calculate the position for each threshold

        percent_step = 0.1
        percent_value_value = np.arange(percent_step, 1 + percent_step, percent_step)
        percent_value_position = np.zeros(percent_value_value.shape)

        for p in range(len(percent_value_value)):
            percent_value_position[p] = np.where(self.normal_signal_envelope >= percent_value_value[p])[0][0]

        #   Detection of the start (start_attack_position) and stop (end_attack_position) of the attack

        position_value = np.where(self.normal_signal_envelope > noise_threshold)[0]

        #   Determine the start and stop positions based on selected method

        if method == 1:  # Equivalent to a value of 80%
            start_attack_position = position_value[0]
            end_attack_position = position_value[int(np.floor(0.8 / percent_step))]
        elif method == 2:  # Equivalent to a value of 100%
            start_attack_position = position_value[0]
            end_attack_position = position_value[int(np.floor(1.0 / percent_step))]
        elif method == 3:
            #   Define parameters for the calculation of the search for the start and stop of the attack

            # The terminations for the mean calculation

            m1 = int(round(0.3 / percent_step)) - 1
            m2 = int(round(0.6 / percent_step))

            #   define the multiplicative factor for the effort

            multiplier = 3

            #   Terminations for the start attack correction

            s1att = int(round(0.1 / percent_step)) - 1
            s2att = int(round(0.3 / percent_step))

            #   Terminations for the end attack correction

            e1att = int(round(0.5 / percent_step)) - 1
            e2att = int(round(0.9 / percent_step))

            #   Calculate the effort as the effective difference in adjacent position values

            dpercent_position_value = np.diff(percent_value_position)

            #   Determine the average effort

            M = np.mean(dpercent_position_value[m1:m2])

            #   Start the start attack calculation
            #   we START JUST AFTER THE EFFORT TO BE MADE (temporal gap between percent) is too large

            position2_value = np.where(dpercent_position_value[s1att:s2att] > multiplier * M)[0]

            if len(position2_value) > 0:
                index = int(np.floor(position2_value[-1] + s1att))
            else:
                index = int(np.floor(s1att))

            start_attack_position = percent_value_position[index]

            #   refinement: we are looking for the local minimum

            delta = int(np.round(0.25 * (percent_value_position[index + 1] - percent_value_position[index]))) - 1
            n = int(np.floor(percent_value_position[index]))

            if n - delta >= 0:
                min_position = np.argmin(self.normal_signal_envelope[n - delta:n + delta])
                start_attack_position = min_position + n - delta - 1

            #   Start the end attack calculation
            #   we STOP JUST BEFORE the effort to be made (temporal gap between percent) is too large

            position2_value = np.where(dpercent_position_value[e1att:e2att] > multiplier * M)[0]

            if len(position2_value) > 0:
                index = int(np.floor(position2_value[0] + e1att))
            else:
                index = int(np.floor(e1att))

            end_attack_position = percent_value_position[index]

            #   refinement: we are looking for the local minimum

            delta = int(np.round(0.25 * (percent_value_position[index] - percent_value_position[index - 1])))
            n = int(np.floor(percent_value_position[index]))

            if n - delta >= 0:
                min_position = np.argmax(self.normal_signal_envelope[n - delta:n + delta + 1])
                end_attack_position = min_position + n - delta

        #   Calculate the Log-attack time

        if start_attack_position == end_attack_position:
            start_attack_position -= 1

        rise_time_n = end_attack_position - start_attack_position
        log_attack_time = np.log10(rise_time_n / self.fs)

        #   Calculate the temporal growth - New 13 Jan 2003
        #   weighted average (Gaussian centered on percent=50%) slopes between satt_posn and eattpos_n

        start_attack_position = int(np.round(start_attack_position))
        end_attack_position = int(np.round(end_attack_position))

        start_attack_value = self.normal_signal_envelope[start_attack_position]
        end_attack_value = self.normal_signal_envelope[end_attack_position]

        threshold_value = np.arange(start_attack_value, end_attack_value, 0.1)
        threshold_position_seconds = np.zeros(np.size(threshold_value))

        level_distributions = self.normal_signal_envelope[start_attack_position:end_attack_position].copy()
        for i in range(len(threshold_value)):
            position = np.where(level_distributions >= threshold_value[i])[0]
            if len(position) > 0:
                threshold_position_seconds[i] = position[0] / self.fs
            else:
                threshold_position_seconds[i] = end_attack_position / self.fs

        slopes = np.divide(np.diff(threshold_value), np.diff(threshold_position_seconds))

        #   Calculate the increase

        thresholds = (threshold_value[:-1] + threshold_value[1:]) / 2
        weights = np.exp(-(thresholds - 0.5) ** 2 / (0.5 ** 2))
        increase = np.sum(np.dot(slopes, weights)) / np.sum(weights)

        #   Calculate the time decay

        envelope_max_index = np.where(self.normal_signal_envelope == np.max(self.normal_signal_envelope))[0]
        envelope_max_index = int(np.round(0.5 * (envelope_max_index + end_attack_position)))

        stop_position = np.where(self.normal_signal_envelope > decrease_threshold)[0][-1]

        if envelope_max_index == stop_position:
            if stop_position < len(self.normal_signal_envelope):
                stop_position += 1
            elif envelope_max_index > 1:
                envelope_max_index -= 1

        #   Calculate the decrease

        X = np.arange(envelope_max_index, stop_position) / self.fs
        X_index = np.arange(envelope_max_index, stop_position)
        Y = np.log(self.normal_signal_envelope[X_index] + sys.float_info.epsilon)
        decrease = self._calculate_linear_fit(X, Y)[1]

        #   Create the list of addresses that we are interested in storing for later consumption

        addresses = np.array([start_attack_position, envelope_max_index, 0, 0, stop_position], dtype='float') / self.fs

        return log_attack_time, increase, decrease, addresses

    def get_feature(self, name):
        return self.get_features()[name]

    @staticmethod
    def _calculate_linear_fit(x, y):
        """
        This function calculates the linear least-squares regression and returns the slope parameter for the curve
        fit.
        """

        xx = np.zeros((2, 2))
        xx[0, 0] = len(x)
        xx[0, 1] = np.sum(x)
        xx[1, 0] = np.sum(x)
        xx[1, 1] = np.sum(x ** 2)

        yy = np.array([np.sum(y), np.sum(x.dot(y))])

        a = np.linalg.pinv(xx).dot(yy)

        return a

    @staticmethod
    def _calculate_linear_fit_value(a, x):
        aa = a[::-1]

        return np.polyval(aa, x)

    def get_features(self):
        features = dict()

        features['attack'] = self.attack
        features['decrease'] = self.decrease
        features['release'] = self.release
        features['log_attack'] = self.log_attack
        features['attack slope'] = self.attack_slope
        features['decrease slope'] = self.decrease_slope
        features['temporal centroid'] = self.temporal_centroid
        features['effective duration'] = self.effective_duration
        features['amplitude modulation'] = self.amplitude_modulation
        features['frequency modulation'] = self.frequency_modulation

        return features

    @property
    def feature_names(self):
        names = list()

        names.append('attack')
        names.append('decrease')
        names.append('release')
        names.append('log_attack')
        names.append('attack slope')
        names.append('decrease slope')
        names.append('temporal centroid')
        names.append('effective duration')
        names.append('amplitude modulation')
        names.append('frequency modulation')

        return names
