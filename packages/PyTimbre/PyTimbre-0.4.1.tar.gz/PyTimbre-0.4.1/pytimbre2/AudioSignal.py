from enum import Enum
import numpy as np
from .Representations.Global.GlobalTimeFeatures import GlobalTimeFeatures
from .Representations.spectro_temporal.Spectro_Temporal import ERB_Spectro_Temporal_Method, STFT_Spectro_Temporal_Method
from .Representations.spectro_temporal.Spectro_Temporal import Short_Time_Fourier_Transform, Equivalent_Rectangular_Band
from .Representations.spectro_temporal.Spectro_Temporal import Spectro_Temporal, spectrogram_representation
import soundfile
from .waveform.files.wave_file import wave_file


class AvailableStatistics(Enum):
    mean = 1
    median = 2
    std = 3
    max = 5
    min = 6
    none = 7


class AudioSignal:
    """
    This class wraps the processing of the audio features so that we can provide a file, or a signal and perform the
    Timbre feature extraction to obtain the various Global Time and Spectro-temporal features from the audio data.
    """

    def __init__(self, signal, fs=None, channel_index=0):
        """
        Constructor - this will create the information within the class from either the audio file or passing a signal
        through the argument list.

        Parameters
        ----------

        signal : double array-like or string
            If string, then the constructor interprets signal as the full path to a file that we want to read, otherwise
            it is interpreted as the single channel of audio data to process.
        fs : double or integer
            the number of samples per second
        """

        if (not (signal is None) and isinstance(signal, str)) and fs is None:
            wfm = wave_file(signal)

            if channel_index < wfm.samples.shape[1]:
                self.signal = wfm.samples[:, channel_index]
            else:
                raise ValueError("You have requested a channel index that does not exist within the audio file")

            self.fs = wfm.sample_rate
        elif isinstance(signal, wave_file):
            if channel_index < signal.samples.shape[1]:
                self.signal = signal.samples[:, channel_index]
            else:
                raise ValueError("You have requested a channel index that does not exist within the audio file")

            self.fs = signal.sample_rate
        else:
            self.signal = signal
            self.fs = fs

        #   Now create the instances of the various analyzers that we might process the data later

        self.TimeProcessor = GlobalTimeFeatures(self.signal, self.fs, 2048)
        self.spectro_temporal_processor = spectrogram_representation(self.signal, self.fs, 4096)

        #   initialize the results objects

        self.global_results = None
        self.spectral_results = None

    @property
    def sample_rate(self):
        return self.fs

    @property
    def Signal(self):
        return self.signal

    @property
    def processor(self):
        return self.spectro_temporal_processor

    @processor.setter
    def processor(self, value: Spectro_Temporal):
        self.spectro_temporal_processor = value

    @property
    def get_spectrogram(self):
        self.spectro_temporal_processor.calculate_spectrogram()

        return self.spectro_temporal_processor.frequencies, \
               self.spectro_temporal_processor.times, \
               self.spectro_temporal_processor.distribution

    @property
    def get_feature_names(self):
        names = self.TimeProcessor.feature_names

        for name in self.spectro_temporal_processor.feature_names:
            names.append(name)

        return names

    @property
    def temporal_hop_size(self):
        return self.TimeProcessor.hop_size_seconds

    @temporal_hop_size.setter
    def temporal_hop_size(self, value):
        self.TimeProcessor.hop_size_seconds = value

    def get_feature(self, feature_name):
        """
        This function searches through the list of names and ensures that we know how to calculate the requested value,
        and then returns the entire set of data calculated from this feature.

        :param feature_name: str - the name of the feature that must be contained within the list
        """

        if not isinstance(feature_name, str) and not(feature_name in self.get_feature_names):
            return None

        #   Now we need to determine which element this feature exists within

        if feature_name in self.spectro_temporal_processor.feature_names:
            return self.spectro_temporal_processor.get_feature(feature_name)
        else:
            return self.TimeProcessor.get_feature(feature_name)

    def get_features(self, statistic=AvailableStatistics.mean):
        """
        This function provides the user the ability to get the features from the temporal/global class and the selected
        spectro-temporal class.
        """

        self.global_results = self.TimeProcessor.get_features()
        self.spectral_results = self.spectro_temporal_processor.get_features()

        results = dict()

        if statistic == AvailableStatistics.mean:
            for key in self.global_results.keys():
                if np.size(self.global_results[key]) == 1:
                    results[key] = self.global_results[key]
                elif not isinstance(self.global_results[key], float) > 1:
                    values = np.mean(self.global_results[key], axis=0)
                    if np.size(values) > 1:
                        for i in range(len(values)):
                            results['{}_{:02.0f}'.format(key, i)] = values[i]
                    else:
                        results[key] = values
                else:
                    results[key] = self.global_results[key]

            for key in self.spectral_results.keys():
                if np.size(self.spectral_results[key]) == 1:
                    results[key] = self.spectral_results[key]
                elif not isinstance(self.spectral_results[key], float) > 1:
                    values = np.mean(self.spectral_results[key], axis=0)
                    if np.size(values) > 1:
                        for i in range(len(values)):
                            results['{}_{:02.0f}'.format(key, i)] = values[i]
                    else:
                        results[key] = values
                else:
                    results[key] = self.spectral_results[key]
        elif statistic == AvailableStatistics.median:
            for key in self.global_results.keys():
                if np.size(self.global_results[key]) == 1:
                    results[key] = self.global_results[key]
                elif not isinstance(self.global_results[key], float) > 1:
                    values = np.median(self.global_results[key], axis=0)
                    if np.size(values) > 1:
                        for i in range(len(values)):
                            results['{}_{:02.0f}'.format(key, i)] = values[i]
                    else:
                        results[key] = values
                else:
                    results[key] = self.global_results[key]

            for key in self.spectral_results.keys():
                if np.size(self.spectral_results[key]) == 1:
                    results[key] = self.spectral_results[key]
                elif not isinstance(self.spectral_results[key], float) > 1:
                    values = np.median(self.spectral_results[key], axis=0)
                    if np.size(values) > 1:
                        for i in range(len(values)):
                            results['{}_{:02.0f}'.format(key, i)] = values[i]
                    else:
                        results[key] = values
                else:
                    results[key] = self.spectral_results[key]
        elif statistic == AvailableStatistics.std:
            for key in self.global_results.keys():
                if np.size(self.global_results[key]) == 1:
                    results[key] = self.global_results[key]
                elif not isinstance(self.global_results[key], float) > 1:
                    values = np.std(self.global_results[key], axis=0)
                    if np.size(values) > 1:
                        for i in range(len(values)):
                            results['{}_{:02.0f}'.format(key, i)] = values[i]
                    else:
                        results[key] = values
                else:
                    results[key] = self.global_results[key]

            for key in self.spectral_results.keys():
                if np.size(self.spectral_results[key]) == 1:
                    results[key] = self.spectral_results[key]
                elif not isinstance(self.spectral_results[key], float) > 1:
                    values = np.std(self.spectral_results[key], axis=0)
                    if np.size(values) > 1:
                        for i in range(len(values)):
                            results['{}_{:02.0f}'.format(key, i)] = values[i]
                    else:
                        results[key] = values
                else:
                    results[key] = self.spectral_results[key]
        elif statistic == AvailableStatistics.min:
            for key in self.global_results.keys():
                if np.size(self.global_results[key]) == 1:
                    results[key] = self.global_results[key]
                elif not isinstance(self.global_results[key], float) > 1:
                    values = np.min(self.global_results[key], axis=0)
                    if np.size(values) > 1:
                        for i in range(len(values)):
                            results['{}_{:02.0f}'.format(key, i)] = values[i]
                    else:
                        results[key] = values
                else:
                    results[key] = self.global_results[key]

            for key in self.spectral_results.keys():
                if np.size(self.spectral_results[key]) == 1:
                    results[key] = self.spectral_results[key]
                elif not isinstance(self.spectral_results[key], float) > 1:
                    values = np.min(self.spectral_results[key], axis=0)
                    if np.size(values) > 1:
                        for i in range(len(values)):
                            results['{}_{:02.0f}'.format(key, i)] = values[i]
                    else:
                        results[key] = values
                else:
                    results[key] = self.spectral_results[key]
        elif statistic == AvailableStatistics.max:
            for key in self.global_results.keys():
                if np.size(self.global_results[key]) == 1:
                    results[key] = self.global_results[key]
                elif not isinstance(self.global_results[key], float) > 1:
                    values = np.max(self.global_results[key], axis=0)
                    if np.size(values) > 1:
                        for i in range(len(values)):
                            results['{}_{:02.0f}'.format(key, i)] = values[i]
                    else:
                        results[key] = values
                else:
                    results[key] = self.global_results[key]

            for key in self.spectral_results.keys():
                if np.size(self.spectral_results[key]) == 1:
                    results[key] = self.spectral_results[key]
                elif not isinstance(self.spectral_results[key], float) > 1:
                    values = np.max(self.spectral_results[key], axis=0)
                    if np.size(values) > 1:
                        for i in range(len(values)):
                            results['{}_{:02.0f}'.format(key, i)] = values[i]
                    else:
                        results[key] = values
                else:
                    results[key] = self.spectral_results[key]

        elif statistic == AvailableStatistics.none:
            for key in self.global_results.keys():
                results[key] = self.global_results[key]

            for key in self.spectral_results.keys():
                results[key] = self.spectral_results[key]

        return results

    @staticmethod
    def from_file(self, filename):
        y, fs = soundfile.read(filename)

        return AudioSignal(y, fs)
