import numpy as np
from datetime import datetime, timedelta
from enum import Enum
import soundfile
from nptdms import TdmsFile
from scipy.signal.windows import hamming, tukey
import scipy.signal
import struct


class windowing_methods(Enum):
    """
    The available windowing methods for the waveform
    """

    hanning = 1
    hamming = 2
    tukey = 3
    rectangular = 4


class generic_time_waveform:
    """
    This is a generic base class that contains the start time, samples and sample rate for a waveform.  Some limited
    operations exist within this class for manipulation of the base data within the class.
    """

    def __init__(self, pressures, sample_rate, start_time):
        """
        Default constructor
        :param pressures: float, array-like - the list of pressure values
        :param sample_rate: float - the number of samples per second
        :param start_time: float or datetime - the time of the first sample
        """

        self._samples = pressures
        self._samples -= np.mean(self._samples)
        self.fs = sample_rate
        self.time0 = start_time

    @property
    def duration(self):
        """
        Determine the duration of the waveform by examining the number of samples and the sample rate
        :return: float - the total number of seconds within the waveform
        """
        return float(len(self._samples)) / self.fs

    @property
    def end_time(self):
        """
        Determine the end time - if the start time was a datetime, then this returns a datetime.  Otherwise a floating
        point value is returned
        :return: float or datetime - the end of the file
        """
        if isinstance(self.time0, datetime):
            return self.time0 + timedelta(seconds=self.duration)
        else:
            return self.time0 + self.duration

    @property
    def samples(self):
        """
        The actual pressure waveform
        :return: float, array-like - the collection of waveform data
        """
        return self._samples

    @samples.setter
    def samples(self, array):
        self._samples = array

    @property
    def sample_rate(self):
        """
        The number of samples per second to define the waveform.
        :return: float - the number of samples per second
        """
        return self.fs

    @sample_rate.setter
    def sample_rate(self, value):
        self.fs = value

    @property
    def start_time(self):
        """
        The time of the first sample
        :return: float or datetime - the time of the first sample
        """

        return self.time0

    @start_time.setter
    def start_time(self, value):
        self.time0 = value

    @property
    def times(self):
        """
        This determines the time past midnight for the start of the audio and returns a series of times for each sample
        :return: float, array-like - the sample times for each element of the samples array
        """

        if isinstance(self.start_time, datetime):
            t0 = (60*(60*self.start_time.hour+self.start_time.minute)+self.start_time.second +
                  self.start_time.microsecond * 1e-6)
        else:
            t0 = self.start_time

        return np.arange(0, len(self.samples)) / self.sample_rate + t0

    def trim(self, s0: int, s1: int):
        """
        This function will remove the samples before s0 and after s1 and adjust the start time
        :param s0: integer - the sample index of the new beginning of the waveform
        :param s1: integer - the sample index of the end of the new waveform
        :return: generic_time_waveform object
        """

        if isinstance(self.start_time, datetime):
            t0 = self.start_time + timedelta(seconds=s0 / self.sample_rate)
        else:
            t0 = self.start_time + s0 / self.sample_rate

        return generic_time_waveform(self.samples[np.arange(s0, s1)].copy(),
                                     self.sample_rate,
                                     t0)

    def apply_window(self, window: windowing_methods=windowing_methods.hanning, windowing_parameter=None):
        """
        This will apply a window with the specific method that is supplied by the window argument and returns a
        generic_time_waveform with the window applied

        :param window:windowing_methods - the enumeration that identifies what type of window to apply to the waveform
        :param windowing_parameter: int or float - an additional parameter that is required for the window
        :returns: generic_time_waveform - the waveform with the window applied
        """

        W = []

        if window == windowing_methods.tukey:
            W = tukey(len(self.samples), windowing_parameter)

        elif window == windowing_methods.rectangular:
            W = tukey(len(self.samples), 0)

        elif window == windowing_methods.hanning:
            W = tukey(len(self.samples), 1)

        elif window == windowing_methods.hamming:
            W = hamming(len(self.samples))

        return generic_time_waveform(self.samples * W, self.fs, self.start_time)

    @staticmethod
    def from_tdms(filename: str, channel_name: str, start_time: datetime):
        """
        This will open a generic_time_waveform from the TDMS data that originated with the Aeroacoustic Research Complex
        based on the filename and the channel_name within file.

        :param filename: str - the full path to the file that we want to process
        :param channel_name: str - the name within the file that we want to extract the data from
        :param start_time: datetime - the start time of the waveform
        :return: generic_time_waveform
        """

        #   Open the TDMS file

        with TdmsFile.open(filename) as tdms:
            #   Get the sample rate from the file

            fs = int(np.floor(tdms.properties['Sample Rate (Hz)']))

            #   Get the voltage range for the specified channel

            sensitivity = float(tdms['Sensitivity'][channel_name][0])
            max_voltage = tdms['Voltage Range'][channel_name][0]

            y = tdms['WaveformData'][channel_name] * max_voltage / 2 ** 31 / sensitivity

            tdms.close()

            return generic_time_waveform(y, fs, start_time)

    def apply_iir_filter(self, b, a):
        """
        This function will be able to apply a filter to the samples within the file and return a new
        generic_time_waveform object

        :param b: double, array-like - the forward coefficients of the filter definition
        :param a: double, array-like - the reverse coefficients of the filter definition
        """

        return generic_time_waveform(scipy.signal.lfilter(b, a, self.samples), self.sample_rate, self.start_time)

    @staticmethod
    def AC_Filter_Design(fs):
        """
        AC_Filter_Design.py

        Created on Mon Oct 18 19:27:36 2021

        @author: Conner Campbell, Ball Aersopace

        Description
        ----------
        Coeff_A, Coeff_C = AC_Filter_Design(fs)

        returns Ba, Aa, and Bc, Ac which are arrays of IRIR filter
        coefficients for A and C-weighting.  fs is the sampling
        rate in Hz.

        This progam is a recreation of adsgn and cdsgn
        by Christophe Couvreur, see	Matlab FEX ID 69.


        Parameters
        ----------
        fs : double
            sampling rate in Hz

        Returns
        -------

        Coeff_A: list
            List of two numpy arrays, feedforward and feedback filter
            coeffecients for A-weighting filter. Form of lits is [Ba,Aa]

        Coeff_c: list
            List of two numpy arrays, feedforward and feedback filter
            coeffecients for C-weighting filter. Form of lits is [Bc,Ac]

        Code Dependencies
        -------
        This program requires the following python packages:
        scipy.signal, numpy

        References
        -------
        IEC/CD 1672: Electroacoustics-Sound Level Meters, Nov. 1996.

        ANSI S1.4: Specifications for Sound Level Meters, 1983.

        ACdsgn.m: Christophe Couvreur, Faculte Polytechnique de Mons (Belgium)
        couvreur@thor.fpms.ac.be
        """

        # Define filter poles for A/C weight IIR filter according to IEC/CD 1672

        f1 = 20.598997
        f2 = 107.65265
        f3 = 737.86223
        f4 = 12194.217
        A1000 = 1.9997
        C1000 = 0.0619
        pi = np.pi

        # Calculate denominator and numerator of filter tranfser functions

        coef1 = (2 * pi * f4) ** 2 * (10 ** (C1000 / 20))
        coef2 = (2 * pi * f4) ** 2 * (10 ** (A1000 / 20))

        Num1 = np.array([coef1, 0.0])
        Den1 = np.array([1, 4 * pi * f4, (2 * pi * f4) ** 2])

        Num2 = np.array([1, 0.0])
        Den2 = np.array([1, 4 * pi * f1, (2 * pi * f1) ** 2])

        Num3 = np.array([coef2 / coef1, 0.0, 0.0])
        Den3 = scipy.signal.convolve(np.array([1, 2 * pi * f2]).T, (np.array([1, 2 * pi * f3])))

        # Use scipy.signal.bilinear function to get numerator and denominator of
        # the transformed digital filter transfer functions.

        B1, A1 = scipy.signal.bilinear(Num1, Den1, fs)
        B2, A2 = scipy.signal.bilinear(Num2, Den2, fs)
        B3, A3 = scipy.signal.bilinear(Num3, Den3, fs)

        Ac = scipy.signal.convolve(A1, A2)
        Aa = scipy.signal.convolve(Ac, A3)

        Bc = scipy.signal.convolve(B1, B2)
        Ba = scipy.signal.convolve(Bc, B3)

        Coeff_A = [Ba, Aa]
        Coeff_C = [Bc, Ac]
        return Coeff_A, Coeff_C

    def apply_a_weight(self):
        """
        This function specifically applies the a-weighting filter to the acoustic data, and returns a new waveform with
        the filter applied.

        :returns: generic_time_waveform - the filtered waveform
        """
        a, c = generic_time_waveform.AC_Filter_Design(self.sample_rate)

        return self.apply_iir_filter(a[:, 0], a[:, 1])

    def apply_c_weight(self):
        """
        This function specifically applies the a-weighting filter to the acoustic data, and returns a new waveform with
        the filter applied.

        :returns: generic_time_waveform - the filtered waveform
        """
        a, c = generic_time_waveform.AC_Filter_Design(self.sample_rate)

        return self.apply_iir_filter(c[:, 0], c[:, 1])

    def apply_lowpass(self, cutoff: float, order: int = 4):
        """
        This function applies a Butterworth filter to the samples within this class.

        :param cutoff: double - the true frequency in Hz
        :param order: double (default: 4) - the order of the filter that will be created and applied

        :returns: generic_time_waveform - the filtered waveform
        """

        #   Determine the nyquist frequency

        nyquist = self.sample_rate / 2.0

        #   Determine the normalized frequency

        normalized_cutoff = cutoff / nyquist

        #   Design the filter

        b, a = scipy.signal.butter(order, normalized_cutoff, btype='low', analog=False)

        #   Filter the data and return the new waveform object

        return self.apply_iir_filter(b, a)

