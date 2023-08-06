from pathlib import Path


class DataLocations:
    @staticmethod
    def test_signal_file():
        return str(Path(__file__).parents[0]) + "/../Examples/backseat_stripped.wav"

    @staticmethod
    def matlab_spectrum_file():
        return str(Path(__file__).parents[0]) + "/../Examples/matlab_spectrum.csv"

    @staticmethod
    def ml_prob_dist():
        return str(Path(__file__).parents[0]) + "/../Examples/matlab_spectrum_probabilityDistribution.csv"

    @staticmethod
    def ml_spectro_temporal_features():
        return str(Path(__file__).parents[0]) + "/../Examples/ml_spetro-temporal_features.csv"

    @staticmethod
    def ml_variable_of_integration():
        return str(Path(__file__).parents[0]) + "/../Examples/variable of integration.csv"

    @staticmethod
    def ml_mean_center():
        return str(Path(__file__).parents[0]) + "/../Examples/matlab_mean_center.csv"

    @staticmethod
    def ml_envelope():
        return str(Path(__file__).parents[0]) + "/../Examples/ml_envelope.csv"

    @staticmethod
    def ml_tee_autocorrelation():
        return str(Path(__file__).parents[0]) + "/../Examples/ml_autocorrelation_coefficients.csv"

    @staticmethod
    def ml_tee_zcr():
        return str(Path(__file__).parents[0]) + "/../Examples/ml_zero_crossing_rate.csv"

    @staticmethod
    def vox_example_a():
        return str(Path(__file__).parents[0]) + "/../Examples/00001a.wav"

    @staticmethod
    def vox_example_b():
        return str(Path(__file__).parents[0]) + "/../Examples/00001.wav"

    @staticmethod
    def vox_example_c():
        return str(Path(__file__).parents[0]) + "/../Examples/00013.wav"

    @staticmethod
    def vox_example_d():
        return str(Path(__file__).parents[0]) + "/../Examples/00001c.wav"

    @staticmethod
    def vox_example_e():
        return str(Path(__file__).parents[0]) + "/../Examples/00002b.wav"

    @staticmethod
    def niosh_tool_example():
        return str(Path(__file__).parents[0]) + "/../Examples/mdy_05072009_hms_155350_vibs50_snd50.tdms"

