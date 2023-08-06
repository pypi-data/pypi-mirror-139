from enum import Enum
from typing import TYPE_CHECKING
import scipy
import numpy as np
import scipy.fft

from pytimbre2.Representations.Global.signal_envelope import envelope
from pytimbre2.Representations.Global.signal_temporal_energy import tee


class GlobalTimeFeatures:
    """
    This input representation calculates attributes on the time series rather than the spectrogram
    """

    def __init__(self, signal, fs, auto_temp_hop_size=True, nfft=None):
        """
        Default constructor for AudioSignal input representation

        :param signal: the signal that is to be processed rather than obtaining the data from an audio file
        :param fs: The sample rate
        :param auto_temp_hop_size: boolean - a flag to determine whether to automatically set the size of the temporal
            step in the analysis, or to automatically set it based on the number of elements within the signal
        :param nfft: integer - the size of the Fourier transform estimation used in the Hilbert transform that estimates
            the envelope of the signal
        """

        #   Set the default values for the various parameters that are required for the sub features we will calculate
        #   later

        self.sampleRate = fs
        self.value = signal
        self.length = len(signal) * (1 / fs)  # length in seconds
        self.t_support = np.arange(0, self.length, (1 / fs))

        #   Adjust the temporal hop size to a fraction of the length of the signal rather than a constant value

        self.envelope = envelope(signal, fs, NFFT=nfft)
        self.instantaneous_temporal_features = tee(signal, fs)

        if auto_temp_hop_size:
            self.hop_size_seconds = self.length / 1000

    """
    These are properties for the processing of the data
    """

    @property
    def effective_duration_threshold(self):
        return self.envelope.effective_duration_threshold

    @effective_duration_threshold.setter
    def effective_duration_threshold(self, value):
        self.envelope.effective_duration_threshold = value

    @property
    def centroid_threshold(self):
        return self.envelope.centroid_threshold

    @centroid_threshold.setter
    def centroid_threshold(self, value):
        self.envelope.centroid_threshold = value

    @property
    def cutoff_frequency(self):
        return self.envelope.cutoff_frequency

    @cutoff_frequency.setter
    def cutoff_frequency(self, value):
        self.envelope.cutoff_frequency = value

    @property
    def window_size_seconds(self):
        return self.instantaneous_temporal_features.window_size_seconds

    @window_size_seconds.setter
    def window_size_seconds(self, value):
        self.instantaneous_temporal_features.window_size_seconds = value

    @property
    def hop_size_seconds(self):
        return self.instantaneous_temporal_features.hop_size_seconds

    @hop_size_seconds.setter
    def hop_size_seconds(self, value):
        self.instantaneous_temporal_features.hop_size_seconds = value

    @property
    def window_size_samples(self):
        return int(np.round(self.window_size_seconds * self.sampleRate))

    @property
    def hop_size_samples(self):
        return int(round(self.hop_size_seconds * self.sampleRate))

    @property
    def coefficient_count(self):
        """
        The number of coefficients to generate for the available data
        """

        return self.instantaneous_temporal_features.coefficient_count

    @coefficient_count.setter
    def coefficient_count(self, value):
        """
        Set the number of coefficients for the analysis
        """

        self.instantaneous_temporal_features.coefficient_count= value

    def duration(self):
        """
        The length of the signal in seconds
        """
        return (self.length - 1) / self.sampleRate

    def get_features(self):
        """
        This function calculates the various features within the global time analysis and stores the results in the
        class object.  At the end, a dictionary of the values is available and returned to the calling function.

        Returns
        -------
        features : dict()
            The dictionary containing the various values calculated within this method.
        """

        #   Create the dictionary that will hold the data for return to the user

        features = dict()

        envelope_features = self.envelope.get_features()
        for key in envelope_features.keys():
            features[key] = envelope_features[key]

        tee_features = self.instantaneous_temporal_features.get_features()
        for key in tee_features.keys():
            features[key] = tee_features[key]

        return features

    def get_feature(self, name):
        if not isinstance(name, str) and (name in self.envelope.feature_names or
                                          name in self.instantaneous_temporal_features.feature_names):
            return None

        if name in self.envelope.feature_names:
            return self.envelope.get_feature(name)
        else:
            return self.instantaneous_temporal_features.get_feature(name)

    @property
    def feature_names(self):
        names = self.envelope.feature_names

        for name in self.instantaneous_temporal_features.feature_names:
            names.append(name)

        return names
