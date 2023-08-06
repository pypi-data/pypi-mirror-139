from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from InputRepresentation import InputRepresentation
    from pytimbre2.Representations.Global.GlobalTimeFeatures import AudioSignal
    from pytimbre2.Representations.spectro_temporal.ERB import ERB
    from pytimbre2.Representations.spectro_temporal.Harmonic import Harmonic
    from pytimbre2.Representations.spectro_temporal.STFT import STFT
    from pytimbre2.Representations.Global.TEE import TEE
import math, numpy as np, scipy.signal, scipy.fft, collections
import logging
from scipy.signal import windows


class StaticMethods:
    eps = np.finfo(float).eps

    @staticmethod
    def next_pow2(x: int):
        if x == 0:
            return 1
        else:
            val = 2
            while val < x:
                val = val * 2
            return val

    @staticmethod
    def col_smooth(x, smooth: int, pass_count: int = 1, clip=False):
        """
        col_smooth smooths each column of matrix X by convolution with a square window followed by division by the window
        size.  Multiple passes allow smoothing with a triangular window or window shapes that approach a gaussian.
        Convolution is implemented as a running sum for speed.

        :param x: input matrix
        :param smooth: samples - size of square smoothing window
        :param pass_count: number of smoothing passes (default = 1)
        :param clip: if true, clip Y to same size as X

        :return y: output matrix
        """
        long = np.long
        shape = np.shape(x)
        if len(shape) == 1:
            m = 1
            n = shape[0]
        else:
            m = shape[1]
            n = shape[0]
        if clip:
            yout = np.zeros((m, n))
        else:
            yout = np.zeros((int(m + pass_count * (smooth - 1)), n))
        mm = m + smooth + pass_count * (smooth - 1)
        xx = x.flatten()
        a = np.zeros(mm * n)
        b = np.zeros(mm * n)
        c = yout.flatten('F')
        mm_range = np.multiply(mm, np.arange(n))
        m_range = np.multiply(m, np.arange(n))
        full_jmk = np.array([x + m_range for x in range(m)]).flatten().astype(long)
        full_smooth_add_jmmk = np.array([x + smooth + mm_range for x in range(m)]).flatten().astype(long)
        a[full_smooth_add_jmmk] = xx[full_jmk]
        for h in range(pass_count):
            for k in range(n):
                low = np.add(np.arange(smooth, mm), mm * k)
                high = np.subtract(low, smooth)
                diff = np.subtract(a[low], a[high])
                cumsum = np.cumsum(diff)
                b[low] = np.divide(cumsum, smooth)
            tmp = a
            a = b
            b = tmp
        if clip:
            c[full_jmk] = a[np.add(full_smooth_add_jmmk, (pass_count * (smooth - 1) / 2)).astype(np.long)]
            yout = np.reshape(c, (n, m))
        else:
            j_total = m + pass_count * (smooth - 1)
            _1 = np.array([x + smooth + mm_range for x in range(j_total)]).flatten().astype(long)
            j_range = mm_range = np.multiply(j_total, np.arange(n))
            _2 = np.array([x + j_range for x in range(j_total)]).flatten().astype(long)
            c[_2] = a[_1]
            yout = np.reshape(c, (n, int(m + pass_count * (smooth - 1))))
        return yout

    @staticmethod
    def fix(val):
        if val >= 0:
            return int(math.floor(val))
        else:
            return int(math.ceil(val))

    @staticmethod
    def get_primes(n):
        # https://stackoverflow.com/questions/2068372/fastest-way-to-list-all-primes-below-n-in-python/3035188#3035188
        """ Returns  a list of primes < n """
        sieve = [True] * n
        for i in range(3, int(n ** 0.5) + 1, 2):
            if sieve[i]:
                sieve[i * i::2 * i] = [False] * ((n - i * i - 1) // (2 * i) + 1)
        return [2] + [i for i in range(3, n, 2) if sieve[i]]

    @staticmethod
    def fir2(nn, ff, aa):
        nn = nn + 1
        if nn < 1024:
            npt = 512
        else:
            npt = StaticMethods.next_pow2(nn)
        wind = windows.hamming(nn)
        lap = np.fix(npt / 25)
        mf, nf = StaticMethods.shape(ff)
        ma, na = StaticMethods.shape(aa)
        if ma != mf or na != nf:
            raise Exception("mismatched dimensions")
        nbrk = max((mf, nf))
        if mf < nf:
            ff = np.transpose(ff)
            aa = np.transpose(aa)
        first = abs(ff[0]) > np.finfo(float).eps
        second = abs(ff[nbrk - 1] - 1) > np.finfo(float).eps
        if first or second:
            raise Exception("Invalid range")
        ff[0] = 0
        ff[nbrk - 1] = 1
        H = np.zeros(npt + 1)
        nint = nbrk - 1
        df = np.diff(np.transpose(ff))
        if any(df < 0):
            raise Exception("Invalid Freq Vector")
        npt = npt + 1
        nb = 1
        H[0] = aa[0]
        for i in range(nint):
            if df[i] == 0:
                nb = int(np.ceil(nb - lap / 2))
                ne = nb + lap
            else:
                ne = np.fix(ff[i + 1] * npt)
            if nb < 0 or ne > npt:
                raise Exception("Signal error")
            j = [*range(int(nb), int(ne + 1))]
            j = [int(val) - 1 for val in j]
            if nb == ne:
                inc = 0
            else:
                inc = np.divide(np.subtract(j, nb), (ne - nb))
            H[j] = np.add(np.multiply(inc, aa[i + 1]), np.multiply(np.subtract(1, inc), aa[i]))
            nb = ne + 1
        dt = np.multiply(0.5, np.subtract(nn, 1))
        rad = np.divide(np.multiply(np.multiply(np.multiply(np.multiply(-1, dt), np.sqrt(-1 + 0j)), np.pi),
                                    [*range(npt)]), (npt - 1))
        H = np.multiply(H, np.exp(rad))
        sel = [x - 1 for x in range(npt - 1, 1, -1)]
        H_sel = H[sel]
        H_aft = np.conj(H_sel)
        H = np.concatenate((H, H_aft))
        ifft = np.fft.ifft(H)
        ht = np.real(ifft)
        b = ht[:nn]
        b = np.multiply(b, np.transpose(wind[:]))
        a = 1
        return b, a

    @staticmethod
    def shape(x):
        shape = np.shape(x)
        if len(shape) == 1:
            m = shape[0]
            n = 1
        else:
            m = shape[0]
            n = shape[1]
        return m, n

    @staticmethod
    def get_window(name: str, n: int):
        if name == 'blackman':
            output = [0.42 - 0.5 * math.cos((2 * math.pi * x) / (n - 1)) + 0.08 * math.cos((4 * math.pi * x) / (n - 1))
                      for x in range(n)]
            output = [0 if np.abs(x) < np.finfo(float).eps else x for x in output]
            return output
        elif name == 'hann':
            # Fun fact: The SciPy Hann window starts at 0, while the Matlab one starts at the first non-zero value
            # Another fun fact: the formula IN THE MATHWORKS DOCUMENTATION is wrong!
            # The formula below was taken from https://ccrma.stanford.edu/~jos/sasp/Matlab_Hann_Window.html

            output = [0.5 * (1 - math.cos(2 * math.pi * (x / (n + 1)))) for x in range(1, (n + 1))]
            return output
        elif name == 'hamming':
            output = [0.54 - 0.46 * math.cos(2 * math.pi * (x / (n - 1))) for x in range(0, (n + 0))]
            return output
        else:
            raise Exception("window {} not implemented")

    @staticmethod
    def stft(x, window, noverlap, nfft, fs):
        # Fun fact: SciPy and Matlab compute FFT in different ways: https://stackoverflow.com/questions/38998522/
        # differences-between-scipy-and-matlab-spectogram

        if not isinstance(x, collections.abc.Iterable):
            raise Exception("x is not Iterable.")
        if not isinstance(window, collections.abc.Iterable):
            raise Exception("window is not Iterable.")
        noverlap = int(noverlap)
        nfft = int(nfft)
        nx = np.size(x)
        nwin = np.size(window)
        ncol = int(np.fix((nx - noverlap) / (nwin - noverlap)))
        xin = np.zeros((nwin, ncol), dtype=type(x[0]))
        coloffsets = [xy * (nwin - noverlap) for xy in range(0, ncol)]
        for index in range(len(coloffsets)):
            beg = coloffsets[index]
            end = beg + nwin
            add = x[beg:end]
            xin[:, index] = add * window
        tt = np.divide(np.add(coloffsets, (nwin / 2)), fs)

        if nwin > nfft:
            raise Exception("Not implemented. See Matlab computeDFT")
        else:
            xw = xin
        xx = scipy.fft.fft(xw, n=nfft, axis=0)
        ff = np.linspace(0, int(fs), nfft, endpoint=False)
        if np.iscomplexobj(x):
            return ff, tt, xx
        else:
            return ff[:(nfft // 2) + 1], tt, xx[:(nfft // 2) + 1, :]



    @staticmethod
    def global_spectral_center(rep: InputRepresentation):
        from pytimbre2.Representations.spectro_temporal.Harmonic import Harmonic
        from pytimbre2.Representations.spectro_temporal.STFT import STFT
        from pytimbre2.Representations.spectro_temporal.ERB import ERB
        if isinstance(rep, Harmonic):
            tile1 = np.tile(np.add(np.sum(rep.partialAmps, axis=0), StaticMethods.eps), (rep.config['n_harms'], 1))
            partial_prob = np.divide(rep.partialAmps, tile1)
            spectral_centroid = np.sum(np.multiply(rep.partialFreqs, partial_prob), axis=0)
            tile2 = np.tile(spectral_centroid, (rep.config['n_harms'], 1))
            zero_mean_partial_freqs = np.subtract(rep.partialFreqs, tile2)
            spectral_spread = np.sqrt(np.sum(np.multiply(np.power(zero_mean_partial_freqs, 2), partial_prob), axis=0))
            spectral_skew = np.divide(np.sum(np.multiply(np.power(zero_mean_partial_freqs, 3), partial_prob), axis=0),
                                      np.add(np.power(spectral_spread, 3), StaticMethods.eps))
            spectral_kurtosis = np.divide(np.sum(np.multiply(np.power(zero_mean_partial_freqs, 4), partial_prob),
                                                 axis=0), np.add(np.power(spectral_spread, 4), StaticMethods.eps))
        elif isinstance(rep, STFT) or isinstance(rep, ERB):
            tile1 = np.tile(np.add(np.sum(rep._value, axis=0), StaticMethods.eps), (rep.f_size, 1))
            distr_prob = np.divide(rep._value, tile1)
            f_support_distr = np.transpose([rep.f_support for x in range(rep.t_size)])
            spectral_centroid = np.sum(np.multiply(f_support_distr, distr_prob), axis=0)
            tile2 = np.tile(spectral_centroid, (rep.f_size, 1))
            zero_mean_f_support_distr = np.subtract(f_support_distr, tile2)
            spectral_spread = np.power(np.sum(np.multiply(np.power(zero_mean_f_support_distr, 2), distr_prob), axis=0),
                                       0.5)
            spectral_skew = np.divide(np.sum(np.multiply(np.power(zero_mean_f_support_distr, 3), distr_prob), axis=0),
                                      np.add(np.power(spectral_spread, 3), StaticMethods.eps))
            spectral_kurtosis = np.divide(np.sum(np.multiply(np.power(zero_mean_f_support_distr, 4), distr_prob),
                                                 axis=0), np.add(np.power(spectral_spread, 4), StaticMethods.eps))
        else:
            raise Exception("How did we get here?")
        if 'spectral_centroid' in rep.descriptors.keys():
            rep.descriptors['spectral_centroid']['value'] = spectral_centroid
        if 'spectral_spread' in rep.descriptors.keys():
            rep.descriptors['spectral_spread']['value'] = spectral_spread
        if 'spectral_skew' in rep.descriptors.keys():
            rep.descriptors['spectral_skew']['value'] = spectral_skew
        if 'spectral_kurtosis' in rep.descriptors.keys():
            rep.descriptors['spectral_kurtosis']['value'] = spectral_kurtosis
        return spectral_centroid, spectral_spread, spectral_skew, spectral_kurtosis

    @staticmethod
    def spectral_centroid(rep: InputRepresentation):
        if 'spectral_centroid' not in rep.descriptors.keys():
            return StaticMethods.global_spectral_center(rep)[0]
        else:
            if rep.descriptors['spectral_centroid']['value'] is None:
                return StaticMethods.global_spectral_center(rep)[0]
            else:
                return rep.descriptors['spectral_centroid']['value']

    @staticmethod
    def spectral_spread(rep: InputRepresentation):
        if 'spectral_spread' not in rep.descriptors.keys():
            return StaticMethods.global_spectral_center(rep)[1]
        else:
            if rep.descriptors['spectral_spread']['value'] is None:
                return StaticMethods.global_spectral_center(rep)[1]
            else:
                return rep.descriptors['spectral_spread']['value']

    @staticmethod
    def spectral_skew(rep: InputRepresentation):
        if 'spectral_skew' not in rep.descriptors.keys():
            return StaticMethods.global_spectral_center(rep)[2]
        else:
            if rep.descriptors['spectral_skew']['value'] is None:
                return StaticMethods.global_spectral_center(rep)[2]
            else:
                return rep.descriptors['spectral_skew']['value']

    @staticmethod
    def spectral_kurtosis(rep: InputRepresentation):
        if 'spectral_kurtosis' not in rep.descriptors.keys():
            return StaticMethods.global_spectral_center(rep)[3]
        else:
            if rep.descriptors['spectral_kurtosis']['value'] is None:
                return StaticMethods.global_spectral_center(rep)[3]
            else:
                return rep.descriptors['spectral_kurtosis']['value']

    @staticmethod
    def spectral_crest(rep: InputRepresentation):
        from pytimbre2.Representations.spectro_temporal.Harmonic import Harmonic
        from pytimbre2.Representations.spectro_temporal.STFT import STFT
        from pytimbre2.Representations.spectro_temporal.ERB import ERB
        if isinstance(rep, Harmonic):
            arithmetic_mean = np.divide(np.sum(rep.partialAmps, axis=0), rep.config['n_harms'])
            value = np.divide(np.max(rep.partialAmps, axis=0), np.add(arithmetic_mean, StaticMethods.eps))
        elif isinstance(rep, STFT) or isinstance(rep, ERB):
            arithmetic_mean = np.divide(np.sum(rep._value, axis=0), rep.f_size)
            value = np.divide(np.max(rep._value, axis=0), np.add(arithmetic_mean, StaticMethods.eps))
        else:
            raise Exception("How is this being called...")
        return value

    @staticmethod
    def spectral_decrease(rep: InputRepresentation):
        from pytimbre2.Representations.spectro_temporal.Harmonic import Harmonic
        from pytimbre2.Representations.spectro_temporal.STFT import STFT
        from pytimbre2.Representations.spectro_temporal.ERB import ERB
        if isinstance(rep, Harmonic):
            if rep.config['n_harms'] < 5:
                value = np.zeros(rep.stft.t_size)
            else:
                a = rep.partialAmps[1:rep.config['n_harms'], :]
                b = np.tile(rep.partialAmps[0, :], (rep.config['n_harms'] - 1, 1))
                c = np.subtract(a, b)
                d = np.transpose([[*range(1, rep.config['n_harms'])] for x in range(rep.stft.t_size)])
                numerator = np.sum(np.divide(c, d), axis=0)
                denominator = np.sum(rep.partialAmps[1:rep.config['n_harms'], :], axis=0)
                value = np.divide(numerator, np.add(denominator, StaticMethods.eps))
        elif isinstance(rep, STFT) or isinstance(rep, ERB):
            a = rep._value[1:rep.f_size, :]
            b = np.tile(rep._value[0, :], (rep.f_size - 1, 1))
            numerator = np.subtract(a, b)
            denominator = np.divide(1, [*range(1, rep.f_size)])
            c = np.matmul(denominator, numerator)
            d = np.sum(np.add(rep._value[1:rep.f_size, :], StaticMethods.eps), axis=0)
            value = np.divide(c, d)
        else:
            raise Exception("How did we get here?")
        return value

    @staticmethod
    def spectral_flatness(rep: InputRepresentation):
        from pytimbre2.Representations.spectro_temporal.Harmonic import Harmonic
        from pytimbre2.Representations.spectro_temporal.STFT import STFT
        from pytimbre2.Representations.spectro_temporal.ERB import ERB
        if isinstance(rep, Harmonic):
            geometric_mean = np.exp(np.multiply(1 / rep.config['n_harms'], np.sum(np.log(np.add(rep.partialAmps,
                                                                                                StaticMethods.eps)),
                                                                                  axis=0)))
            arithmetic_mean = np.divide(np.sum(rep.partialAmps, axis=0), rep.config['n_harms'])
        elif isinstance(rep, STFT) or isinstance(rep, ERB):
            a = np.log(np.add(rep._value, StaticMethods.eps))
            b = np.sum(a, axis=0)
            geometric_mean = np.exp(np.multiply(1 / rep.f_size, b))
            arithmetic_mean = np.divide(np.sum(rep._value, axis=0), rep.f_size)
        else:
            raise Exception("How did we get here?")
        value = np.divide(geometric_mean, np.add(arithmetic_mean, StaticMethods.eps))
        return value

    @staticmethod
    def spectral_rolloff(rep: InputRepresentation):
        from pytimbre2.Representations.spectro_temporal.Harmonic import Harmonic
        from pytimbre2.Representations.spectro_temporal.STFT import STFT
        from pytimbre2.Representations.spectro_temporal.ERB import ERB
        config = rep.descriptors['spectral_rolloff']['info']
        if 'threshold' not in config:
            config['threshold'] = 0.95
        if isinstance(rep, Harmonic):
            cumsum = np.cumsum(rep.partialAmps, 0)
            tile1 = np.tile(np.add(np.sum(rep.partialAmps, 0), StaticMethods.eps), (rep.config['n_harms'], 1))
            normalized_cumsum = np.divide(cumsum, tile1)
            value = []
            for index in range(rep.stft.t_size):
                over = normalized_cumsum[:, index] >= config['threshold']
                cum_over_threshold_idcs = np.nonzero(over)[0]
                if len(cum_over_threshold_idcs) > 0:
                    idx = cum_over_threshold_idcs[0]
                    add = rep.partialFreqs[idx, index]
                else:
                    add = rep.partialFreqs[0, index]
                value.append(add)
            value = np.transpose(value)
        elif isinstance(rep, STFT) or isinstance(rep, ERB):
            cumsum = np.cumsum(rep._value, axis=0)
            summ = np.multiply(config['threshold'], np.sum(rep._value, 0))
            tile1 = np.tile(summ, (rep.f_size, 1))
            cum_over_sum_bins = cumsum >= tile1
            equal = np.cumsum(cum_over_sum_bins, axis=0) == 1
            shape = np.shape(equal)
            rows = np.array([np.nonzero(equal[:, x])[0] for x in range(shape[1])])
            rows = rows.flatten()
            value = np.array(rep.f_support)[np.array(rows).astype(int)]
            value = np.transpose(value)
        else:
            raise Exception("How did we get here?")
        return value

    @staticmethod
    def spectral_slope(rep: InputRepresentation):
        from pytimbre2.Representations.spectro_temporal.Harmonic import Harmonic
        from pytimbre2.Representations.spectro_temporal.STFT import STFT
        from pytimbre2.Representations.spectro_temporal.ERB import ERB
        if isinstance(rep, Harmonic):
            tile1 = np.tile(np.add(np.sum(rep.partialAmps, 0), StaticMethods.eps), (rep.config['n_harms'], 1))
            partial_prob = np.divide(rep.partialAmps, tile1)
            numerator = np.subtract(np.multiply(rep.config['n_harms'], np.sum(np.multiply(rep.partialFreqs,
                                                                                          partial_prob), 0)), np.sum(
                rep.partialFreqs, 0))
            denominator = np.subtract(np.multiply(rep.config['n_harms'], np.sum(np.power(rep.partialFreqs, 2), 0)),
                                      np.power(np.sum(rep.partialFreqs, 0), 2))
        elif isinstance(rep, STFT) or isinstance(rep, ERB):
            tile1 = np.tile(np.add(np.sum(rep._value, 0), StaticMethods.eps), (rep.f_size, 1))
            distr_prob = np.divide(rep._value, tile1)
            a = np.matmul(np.transpose(rep.f_support), distr_prob)
            b = np.sum(rep.f_support, axis=0)
            c = np.sum(distr_prob, axis=0)
            numerator = np.subtract(np.multiply(rep.f_size, a), b * c)
            d = np.sum(np.power(rep.f_support, 2), axis=0)
            e = np.power(np.sum(rep.f_support), 2)
            denominator = np.subtract(np.multiply(rep.f_size, d), e)
        else:
            raise Exception("How did we get here?")
        value = np.divide(numerator, denominator, out=np.zeros_like(numerator), where=denominator != 0)
        return value

    @staticmethod
    def spectral_variance(rep: InputRepresentation):
        from pytimbre2.Representations.spectro_temporal.Harmonic import Harmonic
        from pytimbre2.Representations.spectro_temporal.STFT import STFT
        from pytimbre2.Representations.spectro_temporal.ERB import ERB
        if isinstance(rep, Harmonic):
            previous_frame = rep.partialAmps[:, :-1]
            current_frame = rep.partialAmps[:, 1:]
            i_sz = np.max((len(current_frame), len(previous_frame)))
            # Set stuff equal to 0
            if len(current_frame) != len(previous_frame):
                raise Exception("What the heck does this mean? check in Matlab...")
            cross_product = np.sum(np.multiply(previous_frame, current_frame), 0)
            a = np.sum(np.power(previous_frame, 2), 0)
            b = np.sum(np.power(current_frame, 2), 0)
            auto_product = np.sqrt(np.multiply(a, b))
            value = np.subtract(1, np.divide(cross_product, np.add(auto_product, StaticMethods.eps)))
        elif isinstance(rep, STFT) or isinstance(rep, ERB):
            a = rep._value[:, :-1]
            a2 = np.zeros((rep.f_size, 1))
            b = np.column_stack((a2, a))
            cross_product = np.sum(np.multiply(rep._value, b), 0)
            c = np.sum(np.power(rep._value, 2), 0)
            auto_product = np.multiply(c, np.sum(np.power(b, 2), 0))
            value = np.subtract(1, np.divide(cross_product, np.add(np.sqrt(auto_product), StaticMethods.eps)))
            value = value[1:]
        else:
            raise Exception("How did we get here?")
        return value

    @staticmethod
    def global_harmonic_energy(rep: Harmonic):
        frame_energy = np.sum(rep.stft._value, axis=0)
        harm_energy = np.sum(np.power(rep.partialAmps, 2), axis=0)
        noise_energy = np.subtract(frame_energy, harm_energy)
        noisiness = np.divide(noise_energy, np.add(frame_energy, StaticMethods.eps))
        if 'frame_energy' in rep.descriptors.keys():
            rep.descriptors['frame_energy']['value'] = frame_energy
        if 'harmonic_energy' in rep.descriptors.keys():
            rep.descriptors['harmonic_energy']['value'] = harm_energy
        if 'noise_energy' in rep.descriptors.keys():
            rep.descriptors['noise_energy']['value'] = noise_energy
        if 'noisiness' in rep.descriptors.keys():
            rep.descriptors['noisiness']['value'] = noisiness
        return frame_energy, harm_energy, noise_energy, noisiness

    @staticmethod
    def frame_energy(rep: InputRepresentation):
        from pytimbre2.Representations.spectro_temporal.Harmonic import Harmonic
        if not isinstance(rep, Harmonic):
            value = np.sum(rep._value, axis=0)
            return value
        else:
            if 'frame_energy' not in rep.descriptors.keys():
                return StaticMethods.global_harmonic_energy(rep)[0]
            else:
                if rep.descriptors['frame_energy']['value'] is None:
                    return StaticMethods.global_harmonic_energy(rep)[0]
                else:
                    return rep.descriptors['frame_energy']['value']

    @staticmethod
    def harmonic_energy(rep: Harmonic):
        if 'harmonic_energy' not in rep.descriptors.keys():
            return StaticMethods.global_harmonic_energy(rep)[1]
        else:
            if rep.descriptors['harmonic_energy']['value'] is None:
                return StaticMethods.global_harmonic_energy(rep)[1]
            else:
                return rep.descriptors['harmonic_energy']['value']

    @staticmethod
    def noise_energy(rep: Harmonic):
        if 'noise_energy' not in rep.descriptors.keys():
            return StaticMethods.global_harmonic_energy(rep)[2]
        else:
            if rep.descriptors['noise_energy']['value'] is None:
                return StaticMethods.global_harmonic_energy(rep)[2]
            else:
                return rep.descriptors['noise_energy']['value']

    @staticmethod
    def noisiness(rep: Harmonic):
        if 'noisiness' not in rep.descriptors.keys():
            return StaticMethods.global_harmonic_energy(rep)[3]
        else:
            if rep.descriptors['noisiness']['value'] is None:
                return StaticMethods.global_harmonic_energy(rep)[3]
            else:
                return rep.descriptors['noisiness']['value']

    @staticmethod
    def f0(rep: Harmonic):
        value = rep.fundamentalFreqs
        return value

    @staticmethod
    def harmonic_deviation(rep: Harmonic):
        spec_env = rep.partialAmps.copy()
        a = rep.partialAmps[:-2, :]
        b = rep.partialAmps[1:-1, :]
        c = rep.partialAmps[2:, :]
        d = np.divide(np.add(np.add(a, b), c), 3)
        spec_env[1:-1, :] = d
        e = rep.partialAmps[-2, :]
        f = rep.partialAmps[-1, :]
        g = np.divide(np.add(e, f), 2)
        spec_env[-1, :] = g
        value = np.divide(np.sum(np.abs(np.subtract(rep.partialAmps, spec_env)), 0), rep.config['n_harms'])
        return value

    @staticmethod
    def inharmonicity(rep: Harmonic):
        a0 = np.transpose(np.array([*range(1, rep.config['n_harms'] + 1)])[np.newaxis])
        harmonics = np.outer(a0, rep.fundamentalFreqs)
        a = np.abs(np.subtract(rep.partialFreqs, harmonics))
        b = np.power(rep.partialAmps, 2)
        c = np.sum(b, 0)
        d = np.multiply(c, rep.fundamentalFreqs)
        e = np.multiply(a, b)
        f = np.divide(np.sum(e, 0), np.add(d, StaticMethods.eps))
        value = np.multiply(2, f)
        return value

    @staticmethod
    def odd_even_ratio(rep: Harmonic):
        shape = np.shape(rep.partialAmps)
        a = rep.partialAmps[[*range(0, shape[0], 2)], :]
        b = np.sum(np.power(a, 2), 0)
        c = rep.partialAmps[[*range(1, shape[0], 2)], :]
        d = np.sum(np.power(c, 2), 0)
        value = np.divide(b, np.add(d, StaticMethods.eps))
        return value

    @staticmethod
    def tristimulus(rep: Harmonic):
        value = np.zeros((3, len(rep.t_support)))
        a = np.add(np.sum(rep.partialAmps, 0), StaticMethods.eps)
        value[0, :] = np.divide(rep.partialAmps[0, :], a)
        value[1, :] = np.divide(np.sum(rep.partialAmps[[1, 2, 3], :], 0), a)
        value[2, :] = np.divide(np.sum(rep.partialAmps[4:, :], 0), a)
        return value


