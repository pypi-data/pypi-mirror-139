import numpy as np
from numpy.linalg import LinAlgError
from enum import Enum
import scipy.signal
import scipy.fft
from ..StaticMethods import StaticMethods
from .spectrum import spectrum
from scipy.signal import spectrogram


class STFT_Spectro_Temporal_Method(Enum):
    """
    The two methods for calculating the spectrogram within the short-time Fourier Transform methods.
    """
    magnitude = 1
    power = 2
    complex = 3
    magnitude_no_scaling = 4


class ERB_Spectro_Temporal_Method(Enum):
    """
    The available methods for interpreting and calculating the spectrogram using the equivalent rectangular band
    representation.
    """

    fft = 1
    gamma_tone = 2


class Spectro_Temporal:
    """
    This is a generic class that contains the methods for interpreting the spectrogram data into a series of features.
    """

    def __init__(self, signal, fs, nfft=None):
        """
        Default constructor

        :param signal: float, array-like - this is the samples defining the actual waveform
        :param fs: float or int - the number of samples per second within the waveform
        :param nfft: integer - the number of bins to divide the frequency range into
        """
        self._value = signal
        self.fs = fs

        self.window_size_seconds = 0.0232
        self.hop_size_seconds = 0.0058
        self.window_size = self.window_size_seconds * self.sample_rate
        self.hop_size = self.hop_size_seconds * self.sample_rate

        if nfft is None:
            self.fft_size = Spectro_Temporal.next_pow2(self.window_size)
        else:
            self.fft_size = nfft

        self.bin_size = self.sample_rate / self.fft_size
        self.sample_rate_x = self.sample_rate / self.hop_size
        self.sample_rate_y = self.fft_size / self.sample_rate_x
        self.window = np.hamming(self.windowsize)
        self.window_overlap = self.windowsize - self.hopsize

        #   Define the spectrogram objects

        self.levels = None
        self.frequencies = None
        self.times = None

    @staticmethod
    def next_pow2(x: int):
        """
        Determine the next power of two that will encapsulate this value

        :param x: integer - the number that we are approximating as a power of 2
        """
        n = np.log2(x)
        return 2 ** (np.floor(n) + 1)

    def calculate_spectrogram(self):
        """
        This function calculates the spectrogram for the signal that is passed as a function to the constructor - this
        function is overloaded for any derived class.
        """
        pass

    def get_features(self):
        """
        This function determines the features for the signal using the internal spectrogram and the method that is
        provided during the initialization of the class.

        Returns
        -------
        results : dict
            A collection of features that are calculated on the spectrogram.
        """

        results = dict()

        #   Calculate the spectrogram

        self.calculate_spectrogram()

        spec = spectrum(self.frequencies / self.sample_rate, self.sample_rate, self.times, self.levels)

        return spec.features

    @property
    def feature_names(self):
        return spectrum.feature_names()

    def get_feature(self, name):
        """
        Obtain a single feature from the analysis

        :param name: str - the name of the feature to extract
        """

        self.calculate_spectrogram()

        spec = spectrum(self.frequencies / self.sample_rate, self.sample_rate, self.times, self.levels)

        return spec.features[name]

    @property
    def windowsize_seconds(self):
        return self.window_size_seconds

    @windowsize_seconds.setter
    def windowsize_seconds(self, value: float):
        self.window_size_seconds = value
        self.window_size = self.window_size_seconds * self.sample_rate
        self.window = np.hamming(self.window_size)
        self.window_overlap = self.window_size - self.hop_size

    @property
    def signal(self):
        return self._value

    @property
    def sample_rate(self):
        return self.fs

    @property
    def windowing_function(self):
        return self.window

    @windowing_function.setter
    def windowing_function(self, value):
        self.window = value

    @property
    def hopsize_seconds(self):
        return self.hop_size_seconds

    @hopsize_seconds.setter
    def hopsize_seconds(self, value: float):
        self.hop_size_seconds = value
        self.hop_size = int(np.floor(self.hop_size_seconds * self.sample_rate))
        self.sample_rate_x = self.sample_rate / self.hop_size
        self.window_overlap = self.window_size - self.hop_size

    @property
    def windowsize(self):
        return int(np.floor(self.window_size))

    @windowsize.setter
    def windowsize(self, value: int):
        self.window_size = value
        self.window_size_seconds = self.window_size / self.sample_rate
        self.window = np.hamming(self.window_size)
        self.window_overlap = self.window_size - self.hop_size

    @property
    def hopsize(self):
        return int(np.floor(self.hop_size))

    @hopsize.setter
    def hopsize(self, value: int):
        self.hop_size = value
        self.hop_size_seconds = self.hop_size / self.sample_rate
        self.sample_rate_x = self.sample_rate / self.hop_size
        self.window_overlap = self.window_size - self.hop_size

    @property
    def frequency_count(self):
        return self.fft_size

    @frequency_count.setter
    def frequency_count(self, value: int):
        if value < self.window_size:
            raise OverflowError("The window size must be greater than the number of frequencies")

        self.fft_size = value
        self.sample_rate_y = self.fft_size / self.sample_rate_x
        self.bin_size = self.sample_rate / self.fft_size


class spectrogram_representation(Spectro_Temporal):
    """
    Rather than implement our own version of the conversion to frequency space, we will use the built-in spectrogram
    function within Python.
    """

    def __init__(self, signal, fs, nfft=None):
        """
        The generic constructor that is built from the signal and the sample rate.

        Parameters
        ----------
        signal : double array-like
            the time varying signal that we desire to analyze
        fs : double or integer
            the number of samples per second
        nfft : double or integer
            the number of frequencies to process
        """

        super().__init__(signal, fs, nfft)
        self._method = STFT_Spectro_Temporal_Method.magnitude

    @property
    def analysis_method(self):
        return self._method

    @analysis_method.setter
    def analysis_method(self, value: STFT_Spectro_Temporal_Method):
        self._method = value

    def calculate_spectrogram(self):
        """
        This function calculates the spectrogram using the SciPy function
        """

        if self.analysis_method == STFT_Spectro_Temporal_Method.magnitude:
            self.frequencies, self.times, self.levels = spectrogram(
                self.signal,
                fs=self.fs,
                return_onesided=True,
                scaling='spectrum',
                mode='magnitude',
                nfft=self.fft_size
            )
        elif self.analysis_method == STFT_Spectro_Temporal_Method.complex:
            self.frequencies, self.times, self.levels = spectrogram(
                self.signal,
                fs=self.fs,
                return_onesided=True,
                scaling='spectrum',
                mode='complex',
                nfft=self.fft_size
            )
        elif self.analysis_method == STFT_Spectro_Temporal_Method.power:
            self.frequencies, self.times, self.levels = spectrogram(
                self.signal,
                fs=self.fs,
                return_onesided=True,
                scaling='density',
                mode='magnitude',
                nfft=self.fft_size
            )

        self.levels = abs(np.transpose(self.levels))


class Short_Time_Fourier_Transform(Spectro_Temporal):
    """
    This class is a collection of specific implementation from MATLAB to build a spectrogram based on an implementation
    of the Short-Time Fourier Transform (STFT).
    """

    def __init__(self, signal, fs, nfft=None):
        """
        The generic constructor that is built from the signal and the sample rate.

        Parameters
        ----------
        signal : double array-like
            the time varying signal that we desire to analyze
        fs : double or integer
            the number of samples per second
        nfft : double or integer
            the number of frequencies to process
        """

        super().__init__(signal, fs, nfft)
        self._method = STFT_Spectro_Temporal_Method.magnitude

    @property
    def analysis_method(self):
        return self._method

    @analysis_method.setter
    def analysis_method(self, value: STFT_Spectro_Temporal_Method):
        self._method = value

    def calculate_spectrogram(self):
        overlap = int(np.floor(super().windowsize - super().hopsize)) + 1

        #   If the window is centered at t, this is the starting index at which to loop up the signal which you want
        #   to multiply bu the window.  It is a negative number because (almost) half of the window will be before
        #   time t and half after.  In fact, if the length of the window N is an even number, it is set up so this
        #   number equals -1 * (N / 2 -1).  If the length of the window is od, this number equals -1 * (N - 1) / 2

        left_hand_window_size = int(np.ceil(-(super().windowsize - 1) / 2))

        #   This is the last index at which to look up signal values and is equal to (N - 1) / 2 if the length N of
        #   the window is odd and N / 2 if the length of the window is even.  This means that in the even case, the
        #   window has an unequal number of past and future values, i.e., time t is not the center of the window,
        #   but slightly to the left of the center of the window (before it).

        right_hand_window_size = int(np.ceil((super().windowsize - 1) / 2))

        #   prepad the signal

        signal = np.zeros((len(super().signal) - left_hand_window_size,))
        signal[abs(left_hand_window_size):] = super().signal

        signal = scipy.signal.hilbert(signal)

        last_index = np.floor((len(super().signal) -
                               (right_hand_window_size + 1)) / super().hopsize) * super().hopsize + 1

        #   Define some support vectors

        index = np.arange(0, last_index, super().hopsize, dtype=int) - left_hand_window_size
        size_x = len(index)
        size_y = super().frequency_count / 2
        time = np.arange(0, size_x) / (super().sample_rate / super().hopsize)
        normalized_frequency = np.arange(0, size_y) / size_y / 2

        #   Create the windowed signal

        distribution_pts = np.zeros((super().frequency_count, size_x), dtype='complex')
        for i in range(size_x):
            rng = np.arange(0, super().windowsize + 1, dtype=int) + (index[i] + left_hand_window_size)
            frame = signal[rng]
            if len(super().windowing_function) != len(frame):
                windowing_function = np.hamming(len(frame))
            else:
                windowing_function = super().windowing_function
            frame *= windowing_function
            distribution_pts[:int(super().windowsize + 1), i] = frame

        #   Calculate the FFT

        # scipy.fftpack = pyfftw.interfaces.scipy_fftpack
        # pyfftw.interfaces.cache.enable()

        distribution_pts = scipy.fft.fft(distribution_pts, n=self.frequency_count, axis=0)

        #   Apply the specific scaling for the analysis

        if self._method == STFT_Spectro_Temporal_Method.magnitude:
            distribution_pts = abs(distribution_pts)
            distribution_pts /= np.sum(abs(super().windowing_function))
        elif self._method == STFT_Spectro_Temporal_Method.power:
            distribution_pts = abs(distribution_pts) ** 2
            distribution_pts /= (np.sum(super().windowing_function) ** 2)
        elif self._method == STFT_Spectro_Temporal_Method.complex:
            distribution_pts /= np.sum(super().windowing_function)
        elif self._method == STFT_Spectro_Temporal_Method.magnitude_no_scaling:
            distribution_pts = abs(distribution_pts)

        #   Only keep the first half of the spectrum

        self.levels = distribution_pts[:int(round(super().frequency_count / 2)), :]
        self.frequencies = normalized_frequency
        self.times = time


class Equivalent_Rectangular_Band(Spectro_Temporal):
    """
    This class implements a variation of the Spectro_Temporal class and determines the spectrogram at the frequencies
    and bandwidths defined by the equivalent rectangular band representation.
    """

    def __init__(self, signal, fs, nfft=None):
        """
        Default constructor

        :param signal: float, array-like - this is the samples defining the actual waveform
        :param fs: float or int - the number of samples per second within the waveform
        :param nfft: integer - the number of bins to divide the frequency range into
        """
        super().__init__(signal, fs, nfft)
        self.signal = Equivalent_Rectangular_Band.outmidear(signal, fs)
        self.method = ERB_Spectro_Temporal_Method.fft

    @property
    def analysis_method(self):
        return self._method

    @analysis_method.setter
    def analysis_method(self, value: ERB_Spectro_Temporal_Method):
        self._method = value
    
    @staticmethod
    def CFERB(cf):
        """
        Critical band equivalent rectangular bandwidth

        :param cf: the center frequency to calculate the equivalent rectangular band
        :return: the critical banddwidth at the requested center frequency
        """
        return np.multiply(24.7, np.add(1, np.multiply(4.37, np.divide(cf, 1000))))
    
    def calculate_spectrogram(self, bwfactor = 1, signal_padding = []):
        """
        This function calculates the spectrogram using the equivalent rectangular band methods

        :param bwfactor: int - the multiplicative factor for the ERB bandwidth
        :param signal_padding: array-like - additional elements to pad the calculation
        """

        # return super().calculate_spectrogram()
        lo = 30
        hi = 16000
        cferb = Equivalent_Rectangular_Band.CFERB(self.fs / 2)
        cferb = self.fs / 2 - cferb / 2
        hi = min(hi, cferb)
        nchans = round(2 * (Equivalent_Rectangular_Band.ERBfromhz(hi) - Equivalent_Rectangular_Band.ERBfromhz(lo)))
        cfarray = Equivalent_Rectangular_Band.ERBspace(lo, hi, nchans)
        shape = np.shape(self.signal)
        if len(shape) == 1:
            m = 1
            n = shape[0]
        else:
            m = shape[0]
            n = shape[1]
        if m > 1:
            signal = np.transpose(self.signal)
            if n > 1:
                raise Exception("Signal should be 1D")
            n = m

        #   Build the spectrogram based on the analysis method

        if self.method == ERB_Spectro_Temporal_Method.gamma_tone:
            shape = np.shape(cfarray)
            if len(shape) == 1:
                nchans = 1
                m = shape[0]
            else:
                nchans, m = shape[0], shape[1]
            if m > 1:
                cfarray = np.transpose(cfarray)
                if nchans > 1:
                    raise Exception("channel array should be 1D")
                nchans = m
            shape = np.shape(signal_padding)
            if len(shape) == 1:
                m_pad = 1
                n_pad = shape[0]
            else:
                m_pad, n_pad = shape[0], shape[1]
            if m_pad > 1:
                signalPadding = np.transpose(signal_padding)
                if n_pad > 1:
                    raise Exception("signal padding should be 1D")
                n_pad = m_pad
            l_pad = len(signalPadding)
            first = np.concatenate((signalPadding, signal))
            b = Equivalent_Rectangular_Band.gtfbank(first, self.fs, cfarray, bwfactor)
            b = Equivalent_Rectangular_Band.fbankpwrsmooth(b, self.fs, cfarray)
            b = StaticMethods.col_smooth(b, self.hop_size, pass_count=1, clip=True)
            b = np.maximum(b, 0)
            b = b[:, l_pad:]
            m, n = np.shape(b)
            start_samples = [*range(0, n, self.hop_size)]
            self.levels = b[:, start_samples]
            self.frequencies = cfarray
            self.times = np.divide(start_samples, self.fs)
        elif self.method == ERB_Spectro_Temporal_Method.fft:
            bw0 = 24.7
            b0 = bw0 / 0.982
            ERD = 0.495 / b0
            wsize = self.next_pow2(int(ERD * self.fs * 2))
            window = Equivalent_Rectangular_Band.get_window(wsize, wsize / (ERD * self.fs))
            _1 = np.power(window, 2)
            offset = np.ceil(Equivalent_Rectangular_Band.centroid(_1)[0]) - 1
            other = np.zeros(offset)
            signal = np.concatenate((other, signal))
            last_index = np.floor((n - (wsize - offset)) / self.hop_size) * self.hop_size
            start_samples = [x for x in range(0, last_index + 1, self.hop_size)]
            b = np.divide(Equivalent_Rectangular_Band.CFERB(cfarray), 0.982)
            bb = np.sqrt(np.subtract(np.power(b, 2), np.power(b0, 2)))
            mat = np.multiply([x + 1 for x in range(int(wsize / 2))], self.fs / wsize)
            fSupport = np.tile(mat[:, np.newaxis], (1, nchans))
            cf = np.tile(cfarray, (wsize // 2, 1))
            bb = np.tile(bb, (wsize // 2, 1))
            a1 = np.subtract(fSupport, cf)
            a2 = np.multiply(len(start_samples), a1)
            a3 = np.add(a2, bb)
            a4 = np.power(a3, 4)
            a5 = np.divide(1, a4)
            a6 = np.abs(a5)
            wfunct = np.power(a6, 2)
            adjustweight = np.divide(Equivalent_Rectangular_Band.CFERB(cfarray), sum(wfunct))
            wfunct = np.multiply(wfunct, np.tile(adjustweight, (wsize // 2, 1)))
            wfunct = np.divide(wfunct, np.max(np.max(wfunct)))
            fr = np.zeros((len(start_samples), wsize))
            for index in range(len(start_samples)):
                signal_start = start_samples[index]
                signal_end = start_samples[index] + (wsize)
                cur_signal = signal[signal_start:signal_end]
                that = np.multiply(cur_signal, window)
                fr[:][index] = that
            fft = scipy.fft.fft(fr)
            abs1 = np.abs(fft)
            pwrspect = np.power(abs1, 2)
            trans_power = np.transpose(pwrspect)  # lol
            pwrspect = trans_power[:wsize // 2]
            trans = np.transpose(wfunct)
            self.levels = np.matmul(trans, pwrspect)
            self.frequencies = cfarray
            self.times = np.divide(start_samples, self.fs)

    @staticmethod
    def outmidear(x, fs):
        """
        Calculated the outer middle ear function

        :param x:
        :param fs: The sample rate
        :return:
        """
        maf, f = Equivalent_Rectangular_Band.isomaf([])
        val = Equivalent_Rectangular_Band.isomaf([1000])
        g = [(val[0] - xy) for xy in maf]
        g = [10 ** (xy / 20) for xy in g]
        f.insert(0, 0)
        f.append(20000)
        g.insert(0, np.finfo(float).eps)
        g.append(g[-1])
        if (fs / 2) > 20000:
            f.append((fs / 2))
            g.append(g[-1])
        fc = 680
        q = 0.65
        pwr = 2
        a = Equivalent_Rectangular_Band.sof(fc / fs, q)
        b = [sum(a) - 1, -a[1], -a[2]]
        for index_k in range(pwr):
            x = scipy.signal.lfilter(b, a, x) #TODO This is copied correctly, but is it correct? It looks like it's repeatedly filtering the same thing.
        ff, gg = scipy.signal.freqz(b=b, a=a)
        gg = np.power(np.abs(gg), pwr)
        ff = np.multiply(ff, (fs / (2 * np.pi)))
        function = scipy.interpolate.interp1d(x=f, y=g, kind='linear')
        g = function(ff)
        gain = np.divide(g, (np.add(gg, np.finfo(float).eps)))
        for index_ff in range(len(ff)):
            if ff[index_ff] < f[1]:
                gain[index_ff] = 1
        N = 50
        b, a =  StaticMethods.fir2(N, np.linspace(0, 1, len(gain)), gain)
        y = scipy.signal.lfilter(b, 1, x)
        return y

    @staticmethod
    def isomaf(f: list):
        """
        The International Standard representation of the minimum audible field
        :param f: the frequency to evaluate the Minimum Audible Field at
        :return: the interpolated threshold value
        """
        x = [100, 150, 200, 300, 400, 500, 700, 1000, 1500, 2000, 2500, 3000, 3500, 4000, 4500, 5000, 6000, 7000,
             8000, 9000, 10000]
        y = [33, 24, 18.5, 12, 8, 6, 4.7, 4.2, 3, 1, -1.2, -2.9, -3.9, -3.9, -3, -1, 4.6, 10.9, 15.3, 17, 16.4]
        if len(f) == 0:
            return y, x
        else:
            if len(f) == 1:
                if f[0] < x[0]:
                    return [y[0]], f
                elif f[0] > x[-1]:
                    return [y[-1]], f
            function = scipy.interpolate.interp1d(x=x, y=y, kind='cubic')
            ynew = function(f)
            return ynew, f

    @staticmethod
    def sof(f, q):
        import collections
        rho = np.exp(-np.pi * np.divide(f, q))
        length = 1
        if isinstance(rho, collections.abc.Iterable):
            length = len(rho)
        theta = 2 * np.pi * np.multiply(f, np.sqrt(1 - np.divide(1, 4 * np.power(q, 2))))
        _1 = np.ones(length)
        _2 = np.cos(theta)
        _3 = np.multiply(rho, _2)
        _4 = np.multiply(-2, _3)
        a = np.append(_1, _4)
        a = np.append(a, np.power(rho, 2))
        return a

    @staticmethod
    def ERBfromhz(f, formula='glasberg90'):
        """
        Return the value of the equivalent rectangular band based on a frequency.
        :param f: the frequency to calculate the ERB from
        :param formula: the formula to use in the conversion: 'glasberg90' or 'moore83', default = 'glasberg90'
        :return:
        """
        if formula == 'glasberg90':
            e = 9.26 * np.log(0.00437 * f + 1)
        elif formula == 'moore83':
            erb_k1 = 11.17
            erb_k2 = 0.312
            erb_k3 = 14.675
            erb_k4 = 43
            f = f / 1000
            e = erb_k1 * np.log((f + erb_k2) / (f + erb_k3)) + erb_k4
        else:
            raise Exception("unexpected formula")
        return e

    @staticmethod
    def ERBspace(lo, hi, N=100):
        a = 9.26449 * 24.7
        a1 = [x for x in range(int(round(N)))]
        a2 = hi + a
        a3 = lo + a
        a4 = -np.log(a2) + np.log(a3)
        a5 = N - 1
        b = np.multiply(a1, a4)
        c = np.divide(b, a5)
        a6 = np.divide(b, a5)
        cf = np.add(-a, np.multiply(np.exp(a6), a2))
        y = list(reversed(cf))
        return y

    @staticmethod
    def gtfbank(a, sr, cfarray=None, bwfactor=1):
        # print('gtf start')
        if cfarray is None:
            cfarray = []
        if len(cfarray) == 0:
            lo = 30
            hi = 16000
            cferb = Equivalent_Rectangular_Band.CFERB(sr / 2)
            cferb = sr / 2 - cferb / 2
            hi = min(hi, cferb)
            nchans = round(2 * Equivalent_Rectangular_Band.ERBfromhz(hi) - Equivalent_Rectangular_Band.ERBfromhz(lo))
            cfarray = Equivalent_Rectangular_Band.ERBspace(lo, hi, nchans)
        shape = np.shape(cfarray)
        if len(shape) == 1:
            nchans = 1
            m = shape[0]
        else:
            nchans, m = shape[0], [1]
        if m > 1:
            cfarray = np.transpose(cfarray)
            if nchans > 1:
                raise Exception("channel array should be 1D")
            nchans = m
        shape = np.shape(a)
        if len(shape) == 1:
            m = 1
            n = shape[0]
        else:
            m, n = shape[0], shape[1]
        if m > 1:
            a = np.transpose(a)
            if n > 1:
                raise Exception("signal should be 1D")
            n = m
        fcoefs = Equivalent_Rectangular_Band.MakeERBCoeffs(sr, cfarray, bwfactor)
        a0 = fcoefs[:, 0]
        a11 = fcoefs[:, 1]
        a12 = fcoefs[:, 2]
        a13 = fcoefs[:, 3]
        a14 = fcoefs[:, 4]
        a2 = fcoefs[:, 5]
        b0 = fcoefs[:, 6]
        b1 = fcoefs[:, 7]
        b2 = fcoefs[:, 8]
        gain = fcoefs[:, 9]
        b = np.zeros((nchans, len(a)))
        # print('chans: {}'.format(nchans))
        for chan in range(nchans):
            x = a0[chan] / gain[chan]
            y = a11[chan] / gain[chan]
            z = a2[chan] / gain[chan]
            y1 = scipy.signal.lfilter([x, y, z], [b0[chan], b1[chan], b2[chan]], a)
            y2 = scipy.signal.lfilter([a0[chan], a12[chan], a2[chan]], [b0[chan], b1[chan], b2[chan]], y1)
            y3 = scipy.signal.lfilter([a0[chan], a13[chan], a2[chan]], [b0[chan], b1[chan], b2[chan]], y2)
            y4 = scipy.signal.lfilter([a0[chan], a14[chan], a2[chan]], [b0[chan], b1[chan], b2[chan]], y3)
            b[chan, :] = y4
        return b

    @staticmethod
    def MakeERBCoeffs(fs, cfarray=None, Bfactor=1):
        import cmath
        if cfarray is None:
            cfarray = Equivalent_Rectangular_Band.ERBspace(100, fs / 4, 25)
        T = 1 / fs
        ear_q = 9.26449
        minBW = 24.7
        order = 1
        if len(cfarray) == 1:
            cfarray = np.transpose(cfarray)
        cf = cfarray
        _1 = np.divide(cf, ear_q)
        _2 = np.power(_1, order)
        _3 = minBW ** order
        _4 = _2 + _3
        _5 = np.power(_4, (1 / order))
        B = np.multiply(_5, 1.019 * 2 * np.pi * Bfactor)
        _exp0 = np.exp(np.multiply(B, T))

        A0 = T
        A2 = 0
        B0 = 1
        # _1 = np.multiply(cf, 2*math.pi*T)
        # _2 = np.cos(_1)
        # _3 = np.multiply(-2, _2)

        a = np.multiply(cf, 2 * np.pi * T)
        b = np.cos(a)
        c = np.exp(np.multiply(B, T))
        d = np.divide(b, c)
        e = np.multiply(d, 2 * T)
        f = np.sin(a)
        g = np.divide(f, c)
        h = np.multiply(T, g)
        i = 2 ** 1.5
        j = np.sqrt(np.add(3, i))
        k = np.sqrt(np.subtract(3, i))
        l = np.multiply(np.multiply(2, j), h)
        m = np.multiply(np.multiply(2, k), h)
        A11 = np.divide(np.negative(np.add(e, l)), 2)
        A12 = np.divide(np.negative(np.subtract(e, l)), 2)
        A13 = np.divide(np.negative(np.add(e, m)), 2)
        A14 = np.divide(np.negative(np.subtract(e, m)), 2)
        B1 = np.multiply(-2, d)
        B2 = np.exp(np.multiply(-2 * T, B))

        i = cmath.sqrt(-1)
        a = np.multiply(cf, np.pi * T * i)
        b = np.multiply(4, a)
        c = np.exp(b)
        d = np.multiply(2, c)
        e = np.multiply(d, T)
        f = np.multiply(2, a)
        g = np.multiply(B, T)
        h = np.add(np.negative(g), f)
        ii = np.exp(h)
        j = np.multiply(ii, T)
        k = np.multiply(cf, 2 * np.pi * T)
        l = np.cos(k)
        m = np.sin(k)
        n = 2 ** (3 / 2)
        o = 3 - n
        p = 3 + n
        q = np.sqrt(o)
        r = np.sqrt(p)
        s = np.multiply(q, m)
        t = np.multiply(r, m)
        u = np.subtract(l, s)
        v = np.add(l, s)
        w = np.subtract(l, t)
        x = np.add(l, t)
        y = np.multiply(j, u)
        z = np.multiply(j, v)
        a2 = np.multiply(j, w)
        b2 = np.multiply(j, x)
        c2 = np.multiply(2, y)
        d2 = np.multiply(2, z)
        e2 = np.multiply(2, a2)
        f2 = np.multiply(2, b2)
        g2 = np.add(np.negative(e), c2)
        h2 = np.add(np.negative(e), d2)
        i2 = np.add(np.negative(e), e2)
        j2 = np.add(np.negative(e), f2)
        k2 = np.multiply(2, g)
        l2 = np.exp(k2)
        m2 = np.exp(g)
        n2 = np.divide(2, l2)
        aa = c.real
        bb = (c.imag * 1j)
        cc = np.add(l, aa)
        dd = np.add(cc, bb)
        o2 = np.add(l, c)
        p2 = np.divide(o2, m2)
        q2 = np.multiply(2, p2)
        a0 = np.negative(n2)
        b0 = np.subtract(a0, d)

        first = b0[0]
        second = q2[0]
        after = first + second

        r2 = np.add(b0, q2)
        s2 = np.power(r2, 4)
        t2 = np.multiply(np.multiply(np.multiply(g2, h2), i2), j2)
        u2 = np.divide(t2, s2)
        gain = np.abs(u2)

        allfilts = np.ones(len(cf))
        fcoefs = np.transpose([np.multiply(A0, allfilts), A11, A12, A13, A14, np.multiply(A2, allfilts),
                               np.multiply(B0, allfilts), B1, B2, gain])
        return fcoefs

    @staticmethod
    def fbankpwrsmooth(a, sr, cfarray):
        shape = np.shape(cfarray)
        if len(shape) == 1:
            nchans = 1
            m = shape[0]
        else:
            nchans, m = shape[0], shape[1]
        if m > 1:
            cfarray = np.transpose(cfarray)
            if nchans > 1:
                raise Exception("channel array should be 1D")
            nchans = m
        shift = np.round(np.divide(sr, np.multiply(4, cfarray))).astype(int)
        a = a ** 2
        b = np.zeros(shape=np.shape(a))
        for j in range(nchans):
            first = a[j, shift[j]:]
            second = np.zeros(shift[j])
            full = np.concatenate((first, second))
            a0 = a[j, :]
            b0 = np.add(a0, full)
            b[j, :] = np.divide(b0, 2)
        return b

    @staticmethod
    def get_window(n, b=2, order=4):
        t = [x / n for x in range(n)]
        y = np.multiply(np.multiply(b ** order, np.power(t, (order - 1))), np.exp(np.multiply(t, -2 * b * np.math.pi)))
        y = list(reversed(y))
        y = np.divide(y, max(y))
        return y

    @staticmethod
    def centroid(x):
        shape = np.shape(x)
        if len(shape) == 1:
            m = shape[0]
            n = 1
        else:
            m = shape[0]
            n = shape[1]
        idx = np.tile([*range(1, m + 1)], n)
        c = sum(np.multiply(x, idx))
        w = sum(x)
        c = np.divide(np.add(c, np.finfo(float).eps), np.add(w, np.finfo(float).eps))
        _1 = np.tile(c, (m, 1))
        _2 = np.subtract(idx, _1)
        _3 = np.power(_2, 2)
        _4 = np.multiply(x, _3)
        s = sum(_4)
        # s = sum(np.multiply(x, np.power(np.subtract(idx, np.tile(c, (m, 1))), 2)))
        s = np.divide(np.add(s, np.finfo(float).eps), np.add(w, np.finfo(float).eps))
        s = np.power(s, 0.5)
        return c, s


class Harmonic(Spectro_Temporal):
    def __init__(self, signal, fs, nfft=None):
        super().__init__(signal, fs, nfft)
        self.stft = Short_Time_Fourier_Transform(signal, fs)
        self.times = self.stft.times
        self.signal = signal
        self.n_harms = 20
        self.threshold = 0.3
        self.partialFreqs = None
        self.partialAmps = None
    
    def calculate_spectrogram(self):
        # return super().calculate_spectrogram()
        freqCorrs = np.linspace(-5, 5, 101)
        nFreqCorrs = len(freqCorrs)
        inharmCoeffs = np.linspace(0, 0.001, 21)
        nInharmCoeffs = 21
        tSupport = np.subtract(self.times, self.times[0])
        tSize = len(tSupport)
        distr = self.stft.distribution
        pitchLims = np.array([50, 500])
        estPitches, estTimes, estStrengths = Harmonic.swipep(self.signal, self.fs,
            pitchLims, (self.stft.hop_size / self.sound.InputRepresentations['AudioSignal'].sampleRate),
                                                             1 / 48, 0.1, 0.2, -np.inf)

        try:
            curmax = np.nanmax(estStrengths)
        except ValueError:
            curmax = np.max(estStrengths)
        nans = np.isnan(estPitches)
        anyy = any(nans)
        if anyy:
            estPitches[np.isnan(estPitches)] = np.median(estPitches[not np.isnan(estPitches)])
        fundamentalFreqs = None
        if curmax > self.threshold:
            estTimePitchPairs = np.zeros((len(estTimes), 2))
            estTimePitchPairs[:, 0] = estTimes
            estTimePitchPairs[:, 1] = estPitches
            fundamentalFreqs = Harmonic.Fevalbp(estTimePitchPairs, tSupport)
            fundamentalFreqs = np.transpose(fundamentalFreqs)
        else:
            import logging
            logging.warning('Sound deemed not harmonic. Setting f0 estimate to 0.')
            self.distribution = np.zeros((2 * self.n_harms, tSize))
            self.partialFreqs = np.zeros((self.n_harms, tSize))
            self.partialAmps = np.zeros((self.n_harms, tSize))
            self.frequencies = np.zeros((1, tSize))
            return
        a = np.empty((len(fundamentalFreqs), nFreqCorrs))
        for column in range(np.shape(a)[1]):
            a[:, column] = fundamentalFreqs
        b = np.empty((tSize, len(freqCorrs)))
        for row in range(np.shape(b)[0]):
            b[row, :] = freqCorrs
        corrFreqsTF = np.add(a, b)

        a = np.empty((self.n_harms, nInharmCoeffs))
        for column in range(np.shape(a)[1]):
            a[:, column] = [*range(1, self.n_harms + 1)]
        b = np.power([*range(1, self.n_harms + 1)], 2)
        b1 = b[:, None]
        b2 = inharmCoeffs[None, :]
        c = np.matmul(b1, b2)
        d = np.add(1, c)
        inharmFactorsHI = np.multiply(a, np.sqrt(d))
        shape1 = np.reshape(corrFreqsTF, (tSize * nFreqCorrs, 1), order='F')
        shape2 = np.reshape(inharmFactorsHI, (1, self.n_harms * nInharmCoeffs), order='F')
        shape3 = np.reshape(np.multiply(shape1, shape2), (tSize, nFreqCorrs, self.n_harms, nInharmCoeffs),
                            order='F')
        shape4 = np.divide(1, self.stft.bin_size)
        shape5 = np.multiply(shape4, shape3)
        shape6 = np.round(shape5)
        fSupIdcsTFHI = np.add(1, shape6)
        fSupIdcsTFHI[fSupIdcsTFHI > self.stft.f_size] = self.stft.f_size

        a = np.array([*range(0, tSize)])
        a2 = a[:, None, None, None]
        b = np.tile(a2, (1, nFreqCorrs, self.n_harms, nInharmCoeffs))
        c = np.multiply(self.stft.f_size, b)
        d = np.add(fSupIdcsTFHI, c)
        e = d.astype(int)
        distrIdcsTFHI = np.subtract(e, 1)
        shape = np.shape(distrIdcsTFHI)

        _0 = distr.flatten('F')
        _1 = distrIdcsTFHI.flatten('F')
        _2 = np.take(_0, _1)

        a = np.reshape(_2, shape, order='F')
        totalErgTFI = np.sum(a, axis=2)

        scoreTI = np.max(totalErgTFI, 1)
        inharmCoeffIdcsT = np.argmax(scoreTI, 1)
        maxScoreTI = np.array([scoreTI[i, inharmCoeffIdcsT[i]] for i in range(len(inharmCoeffIdcsT))])
        a = np.subtract(maxScoreTI, scoreTI[:, 0])
        b = np.divide(a, scoreTI[:, 0])
        c = b <= 0.01
        inharmCoeffIdcsT[c] = 0
        tile1 = np.add([*range(1, tSize + 1)], np.multiply(tSize * nFreqCorrs, inharmCoeffIdcsT))
        repmat1 = np.tile(tile1, (nFreqCorrs, 1)).transpose()
        tile2 = [tSize * (x) for x in range(nFreqCorrs)]
        repmat2 = np.tile(tile2, (tSize, 1))
        colIdcs = np.reshape(np.add(repmat1, repmat2), (tSize * nFreqCorrs, 1), order='F')
        totalErgTFI_flat = totalErgTFI.flatten('F')
        totalErgTF = np.take(totalErgTFI_flat, np.subtract(colIdcs, 1))
        totalErgTF = np.reshape(totalErgTF, (tSize, nFreqCorrs), order='F')

        reshape1 = np.reshape(
            np.add([*range(1, tSize + 1)], np.multiply(tSize * nFreqCorrs * self.n_harms, inharmCoeffIdcsT)),
            (tSize, 1, 1), order='F')
        repmat1 = np.tile(reshape1, (1, nFreqCorrs, self.n_harms))
        reshape2 = np.reshape([*range(1, nFreqCorrs + 1)], (1, nFreqCorrs, 1), order='F')
        repmat2 = np.tile(reshape2, (tSize, 1, self.n_harms))
        reshape3 = np.reshape([*range(1, self.n_harms + 1)], (1, 1, self.n_harms), order='F')
        repmat3 = np.tile(reshape3, (tSize, nFreqCorrs, 1))

        a = np.subtract(repmat3, 1)
        b = np.multiply(nFreqCorrs, a)
        c = np.subtract(np.add(repmat2, b), 1)  # ???? Switch
        d = np.multiply(tSize, c)
        e = np.add(repmat1, d)
        colIdcs = np.reshape(e, (tSize * nFreqCorrs * self.n_harms, 1), order='F')
        fSupIdcsTFHI_flat = fSupIdcsTFHI.flatten('F')
        fSupIdcsHTF = np.take(fSupIdcsTFHI_flat, np.subtract(colIdcs, 1))
        fSupIdcsHTF = np.reshape(fSupIdcsHTF, (tSize, nFreqCorrs, self.n_harms), order='F')
        fSupIdcsHTF = np.transpose(fSupIdcsHTF, [2, 0, 1])
        freqCorrIdcsT = np.argmax(totalErgTF, 1)

        repmat1 = np.tile([*range(1, self.n_harms + 1)], (tSize, 1)).transpose()
        a = freqCorrIdcsT
        b = np.multiply(tSize, a)
        c = np.subtract(np.add([*range(1, tSize + 1)], b), 1)
        d = np.multiply(self.n_harms, c)
        repmat2 = np.tile(d, (self.n_harms, 1))
        colIdcs = np.reshape(np.add(repmat1, repmat2), (self.n_harms * tSize, 1), order='F')
        #   An index error is possible at this location, so we will attempt to trap the data
        try:
            fSupIdcsHTF_flat = fSupIdcsHTF.flatten('F')
            fSup = np.take(fSupIdcsHTF_flat, np.subtract(colIdcs, 1)).astype(int)
            partialFreqs = np.take(self.stft.f_support, np.subtract(fSup, 1))
            partialFreqs = np.reshape(partialFreqs, (self.n_harms, tSize), order='F')
        except IndexError as ie:
            import logging
            logging.error("Index error!")

        repmat1 = np.tile([*range(0, tSize)], (self.n_harms, 1))
        reshape1 = np.reshape(repmat1, (self.n_harms * tSize, 1), order='F')
        aa = fSup
        bb = np.multiply(self.stft.f_size, reshape1)
        cc = np.add(aa, bb)
        distr_flat = distr.flatten('F')
        partialAmps = np.take(distr_flat, np.subtract(cc, 1))
        partialAmps = np.reshape(partialAmps, (self.n_harms, tSize), order='F')
        aaa = np.concatenate((partialFreqs, partialAmps))
        self.frequencies = aaa[0, :]
        self.partialFreqs = aaa[:self.n_harms, :]
        self.partialAmps = aaa[self.n_harms:(2 * self.n_harms), :]
        self.levels = aaa

    def swipep(self, signal, sampRate, pitchLims=None, timeStep=0.001, log2PitchStep=(1 / 48), ERBStep=0.1,
               normOverlap=0.5, strenThresh=-np.inf):
        """
        Added code to trap and handle errors in the linear algebra

        20200510 - FSM - Added try...except for determination of the pitches 
            with the polyval.
            
        Parameters
        ----------
        signal : TYPE
            DESCRIPTION.
        sampRate : TYPE
            DESCRIPTION.
        pitchLims : TYPE, optional
            DESCRIPTION. The default is None.
        timeStep : TYPE, optional
            DESCRIPTION. The default is 0.001.
        log2PitchStep : TYPE, optional
            DESCRIPTION. The default is (1 / 48).
        ERBStep : TYPE, optional
            DESCRIPTION. The default is 0.1.
        normOverlap : TYPE, optional
            DESCRIPTION. The default is 0.5.
        strenThresh : TYPE, optional
            DESCRIPTION. The default is -math.inf.

        Raises
        ------
        Exception
            DESCRIPTION.

        Returns
        -------
        pitches : TYPE
            DESCRIPTION.
        times : TYPE
            DESCRIPTION.
        strengths : TYPE
            DESCRIPTION.

        """
        if pitchLims is None:
            pitchLims = [30, 5000]
        if normOverlap < 0 or normOverlap > 1:
            raise Exception("Window overlap must be between 0 and 1.")
        times = np.arange(0, (len(signal) / sampRate), timeStep)
        log2PitchCands = np.arange(np.log2(pitchLims[0]), np.log2(pitchLims[1]), log2PitchStep)
        pitchCands = np.power(2, log2PitchCands)
        globStrenMtrx = np.zeros((len(pitchCands), len(times)))
        logWinSizeLims = np.round(np.log2(np.divide(8 * sampRate, pitchLims))).astype(int)
        winSizes = np.power(2, range(logWinSizeLims[0], logWinSizeLims[1] - 1, -1))
        winSizeOptPitches = np.divide(8 * sampRate, winSizes)
        log2DistWin1OptPitchAndPitchCands = np.add(np.subtract(log2PitchCands, np.log2(winSizeOptPitches[0])), 1)
        herbs1 = Harmonic.hz2erbs(min(pitchCands) / 4)
        herbs2 = Harmonic.hz2erbs(sampRate / 2)
        ERBs = Harmonic.erbs2hz(np.arange(herbs1, herbs2, ERBStep))
        for winSizeIdx in range(len(winSizes)):
            hop_size = int(max(1, round((1 - normOverlap) * winSizes[winSizeIdx])))
            paddedSignal = np.concatenate(
                (np.zeros(winSizes[winSizeIdx] // 2), signal, np.zeros(hop_size + winSizes[winSizeIdx] // 2)))
            win = StaticMethods.get_window('hann', winSizes[winSizeIdx])
            overlap = max(0, winSizes[winSizeIdx] - hop_size)
            fSupport, tSupport, Zxx = StaticMethods.stft(paddedSignal, window=win, nfft=len(win),
                                                                       noverlap=overlap, fs=sampRate)
            if len(winSizes) == 1:
                optPitchCandsIdcs = [x for x in range(len(pitchCands))]
                imperfectFitIdcs = []
            elif winSizeIdx == (len(winSizes) - 1):
                optPitchCandsIdcs = [ind for ind, x in enumerate(log2DistWin1OptPitchAndPitchCands) if
                                     (x - (winSizeIdx + 1)) > -1]
                imperfectFitIdcs = [index for (index, x) in
                                    enumerate(log2DistWin1OptPitchAndPitchCands[optPitchCandsIdcs]) if
                                    (x - (winSizeIdx + 1)) < 0]
            elif (winSizeIdx + 1) == 1:
                optPitchCandsIdcs = [ind for ind, x in enumerate(log2DistWin1OptPitchAndPitchCands) if
                                     (x - (winSizeIdx + 1)) < 1]
                imperfectFitIdcs = [index for (index, x) in
                                    enumerate(log2DistWin1OptPitchAndPitchCands[optPitchCandsIdcs]) if
                                    (x - (winSizeIdx + 1)) > 0]
            else:
                optPitchCandsIdcs = [ind for ind, x in enumerate(log2DistWin1OptPitchAndPitchCands) if
                                     abs(x - (winSizeIdx + 1)) < 1]
                imperfectFitIdcs = [x for x in range(len(optPitchCandsIdcs))]
            over = (pitchCands[optPitchCandsIdcs[0]] / 4)
            index_start = [ind for (ind, x) in enumerate(ERBs) if (x > over)][0]
            ERBs = ERBs[index_start:]
            distr_abs = np.abs(Zxx)
            shape = np.shape(distr_abs)
            ERBInterp = np.zeros((len(ERBs), shape[1]))
            for index in range(shape[1]):
                spline = scipy.interpolate.UnivariateSpline(fSupport, distr_abs[:, index], s=0)
                ERBInterp[:, index] = spline(ERBs)
            ERBsDistrValues = np.sqrt(np.maximum(0, ERBInterp))
            locStrenMtrx = Harmonic.pitchStrengthAllCandidates(ERBs, ERBsDistrValues, pitchCands[optPitchCandsIdcs])
            if len(locStrenMtrx[1]) > 1:
                # print warnings?
                func = scipy.interpolate.interp1d(tSupport, np.transpose(locStrenMtrx), kind='linear', axis=0,
                                                  bounds_error=False, fill_value=np.nan)
                locStrenMtrx = np.transpose(func(times))
            else:
                locStrenMtrx = np.empty((len(locStrenMtrx), len(times)))
                locStrenMtrx[:] = np.nan
            currWinRelStren = np.ones(np.shape(optPitchCandsIdcs))
            log2DistCurrWinOptPitchAndOptPitchCands = np.subtract(
                [x2 for (ind2, x2) in enumerate(log2DistWin1OptPitchAndPitchCands) if
                 ind2 in [x1 for (ind1, x1) in enumerate(optPitchCandsIdcs) if ind1 in imperfectFitIdcs]],
                (winSizeIdx + 1))
            for index in range(len(imperfectFitIdcs)):
                currWinRelStren[imperfectFitIdcs[index]] = 1 - abs(log2DistCurrWinOptPitchAndOptPitchCands[index])
            shape = np.shape(locStrenMtrx)
            a = np.zeros((np.shape(currWinRelStren)[0], shape[1]))
            for column in range(np.shape(a)[1]):
                a[:, column] = currWinRelStren
            # a = np.tile(currWinRelStren, (44, 1127))
            b = np.multiply(a, locStrenMtrx)
            for index in range(len(optPitchCandsIdcs)):
                globStrenMtrx[optPitchCandsIdcs[index]] = np.add(globStrenMtrx[optPitchCandsIdcs[index]], b[index])

        pitches = np.empty(len(globStrenMtrx[1]))
        pitches[:] = np.nan
        strengths = np.empty(len(globStrenMtrx[1]))
        strengths[:] = np.nan
        for timeIdx in range(len(globStrenMtrx[1])):
            col = globStrenMtrx[:, timeIdx]
            try:
                maxStrenPitchIdx = np.nanargmax(col)
            except ValueError:
                maxStrenPitchIdx = np.argmax(col)
            strengths[timeIdx] = globStrenMtrx[maxStrenPitchIdx, timeIdx]
            if strengths[timeIdx] < strenThresh:
                continue
            if maxStrenPitchIdx == 0 or maxStrenPitchIdx == (len(pitchCands) - 1):
                pitches[timeIdx] = pitchCands[maxStrenPitchIdx]
            else:
                maxStrenPitchLocIdcs = [*range(maxStrenPitchIdx - 1, maxStrenPitchIdx + 1 + 1)]
                tc = np.divide(1, pitchCands[maxStrenPitchLocIdcs])
                ntc = np.multiply(np.subtract(np.divide(tc, tc[1]), 1), 2 * np.pi)
                b = globStrenMtrx[maxStrenPitchLocIdcs, timeIdx]
                try:
                    c = np.polyfit(ntc, b, 2)
                    ftc = np.divide(1, np.power(2, np.arange(np.log2(
                        pitchCands[maxStrenPitchLocIdcs[0]]), np.log2(
                        pitchCands[maxStrenPitchLocIdcs[2]]), 1 / 12 / 100)))
                    nftc = np.multiply(np.subtract(np.divide(ftc, tc[1]), 1),
                                       2 * np.pi)
                    fit = np.polyval(c, nftc)
                    maxPolyFitIdcs = np.argmax(fit)
                    strengths[timeIdx] = fit[maxPolyFitIdcs]
                    a = maxStrenPitchLocIdcs[0]
                    b = pitchCands[a]
                    c = np.log2(b)
                    d = (maxPolyFitIdcs) / 12 / 100
                    pitch = np.power(2, np.add(c, d))
                    pitches[timeIdx] = pitch
                except LinAlgError:
                    pitches[timeIdx] = -9999
        return pitches, times, strengths

    @staticmethod
    def hz2erbs(Hzs):
        return np.multiply(6.44, np.subtract(np.log2(np.add(229, Hzs)), 7.84))

    @staticmethod
    def erbs2hz(ERBs):
        return np.subtract(np.power(2, np.add(np.divide(ERBs, 6.44), 7.84)), 229)

    @staticmethod
    def pitchStrengthOneCandidate(ERBs, normERBsDistrValues, pitchCand):
        n = StaticMethods.fix(ERBs[-1] / pitchCand - 0.75)
        if n == 0:
            return np.nan
        k = np.zeros(len(ERBs))
        q = np.divide(ERBs, pitchCand)
        primes = StaticMethods.get_primes(n)
        primes.insert(0, 1)

        cos = np.cos(np.multiply(q, 2 * np.pi))
        for i in primes:
            a = np.abs(np.subtract(q, i))
            k = [cos[index] if a[index] < 0.25 else val + cos[index] / 2 if 0.25 < a[index] < 0.75 else val for
                 index, val in enumerate(k)]

        k = np.multiply(k, np.sqrt(np.divide(1, ERBs)))
        k = np.divide(k, np.linalg.norm([x for x in k if x > 0]))
        result = np.matmul(k, normERBsDistrValues)
        return result

    @staticmethod
    def pitchStrengthAllCandidates(ERBs, ERBsDistrValues, pitchCands):
        locStrenMtrx = np.zeros((len(pitchCands), len(ERBsDistrValues[1])))
        k = np.ones(len(pitchCands) + 1).astype(np.int32)
        for j in range(0, len(k) - 1):
            a = k[j] - 1
            b = ERBs[k[j] - 1:]
            c = pitchCands[j] / 4
            d = [ind + 1 for ind, x in enumerate(b) if x > (c)]
            e = a + d[0]
            k[j + 1] = e
        k = k[1:]
        _1 = np.multiply(ERBsDistrValues, ERBsDistrValues)
        _2 = np.flip(_1)
        _3 = np.cumsum(_2, axis=0)
        _4 = np.flip(_3)
        N = np.sqrt(_4)
        for j in range(len(pitchCands)):
            n = N[k[j] - 1]
            n[n == 0] = np.inf
            NL = np.divide(ERBsDistrValues[k[j] - 1:], np.tile(n, (len(ERBsDistrValues) - k[j] + 1, 1)))
            locStrenMtrx[j] = Harmonic.pitchStrengthOneCandidate(ERBs[int(k[j] - 1):], NL, pitchCands[j])
        return locStrenMtrx

    @staticmethod
    def Fevalbp(bp, x_v):
        if np.isnan(np.max(bp)):
            raise Exception("bp is NaN.")
        if np.isnan(np.max(x_v)):
            raise Exception("x_v is NaN.")
        y_v = np.zeros(len(x_v))
        pos1 = [ind for (ind, x) in enumerate(x_v) if x < bp[0, 0]]
        if len(pos1) > 0:
            y_v[pos1] = bp[0, 1]
        pos2 = [ind for (ind, x) in enumerate(x_v) if x > bp[-1, 0]]
        if len(pos2) > 0:
            y_v[pos2] = bp[-1, 1]
        pos = [ind for (ind, x) in enumerate(x_v) if x >= bp[0, 0] and x <= bp[-1, 0]]
        if len(pos) > 1:
            func = scipy.interpolate.interp1d(bp[:, 0], bp[:, 1])
            y_v[pos] = func(x_v[pos])
        else:
            y_v = np.zeros(len(x_v))
            for n in range(len(x_v)):
                x = x_v[n]
                minPos = np.argmin(np.abs(np.subtract(bp[:, 0], x)))
                minVal = bp[minPos, 1]
                L = np.size(bp, 1)
                if (minVal == x) or (L == 1) or ((minVal < x) and (minPos == L)) or ((minVal > x) and (minPos == 1)):
                    y_v[n] = bp[minPos, 1]
                elif minVal < x:
                    y_v[n] = (bp[minPos + 1, 1] - bp[minPos, 1]) / (bp[minPos + 1, 0] - bp[minPos, 0]) * (
                                x - bp[minPos, 0]) + bp[minPos, 1]
                elif minVal > x:
                    y_v[n] = (bp[minPos, 1] - bp[minPos - 1, 1]) / (bp[minPos, 0] - bp[minPos - 1, 0]) * (
                                x - bp[minPos - 1, 0]) + bp[minPos - 1, 1]
                else:
                    raise Exception("Not a case?")
        return y_v
