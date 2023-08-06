import os.path
import sys
import numpy as np
from dateutil import parser
from datetime import datetime
from io import FileIO

from ..waveform import generic_time_waveform
from .chunk_information import Chunk_Scanner, Format_Chunk, Data_Chunk, Peak_Chunk, List_Chunk, XML_Chunk
import struct
import scipy.signal


class wave_file(generic_time_waveform):
    """
    This class mimics information within the NAudio interface and will read a wave file, however it will only process
    the canonical chunks: RIFF, WAVE, fmt, and data.

    http://www-mmsp.ece.mcgill.ca/Documents/AudioFormats/WAVE/WAVE.html
    """

    @staticmethod
    def audio_info(path:str):
        """
        Sometimes it is important to obtain information about the audio within the wave file without actually reading
        the audio data.  This will scan the chunks and extract the information about the audio from that info.

        :param path: str - the path to the audio file
        :returns:sample_rate - int, channel_count - int, bytes per sample - int, normalized - boolean,
        start_time - datetime,
        """

        scanner = Chunk_Scanner(path)

        with open(path, 'rb') as file:

            #   The format chunk is required by all wav files
            format_chunk = Format_Chunk(file, scanner.format_chunk.chunk_offset, scanner.format_chunk.chunk_size,
                                        scanner.format_chunk.chunk_name)

            #   If there is a peak chunk, read it

            if scanner.peak_chunk is not None:
                peak_chunk = Peak_Chunk(file, scanner.peak_chunk.chunk_offset, scanner.peak_chunk.chunk_size,
                                        scanner.peak_chunk.chunk_name, format_chunk.channel_count)
            else:
                peak_chunk = None

            #   If there is a list chunk, read it

            if scanner.list_chunk is not None:
                list_chunk = List_Chunk(file, scanner.list_chunk.chunk_size, scanner.list_chunk.chunk_offset,
                                        scanner.list_chunk.chunk_name)
                time0 = list_chunk.time0
                if list_chunk.cropping_information is not None:
                    if list_chunk.cropping_information == "normalized":
                        normalized = True
                    else:
                        normlized = False
                else:
                    normalized = False
            else:
                list_chunk = None
                time0 = 0
                normalized = False

        return format_chunk.sample_rate, format_chunk.channel_count, format_chunk.bits_per_sample / 8, normalized, \
               time0

    def __init__(self, path=None, s0: int = None, s1: int = None, fs: int = None, samples=None, time=None):
        """
        This constructor reads the chunks from the wave file and then processes those that are canonical.

        :param path: str - the full path to the file that we want to read
        :param s0: int - the starting sample for the reading of the audio file
        :param s1: int - the ending sample for the reading of the audio file
        :param fs: int - the number of samples per second.  This facilitates calling the based class with the required
            data
        :param samples: ndarray - the actual samples to define the waveform
        :param time: float or datetime - the time of the first sample
        """

        if path is None:
            if(fs is None) and (samples is None) and (time is None):
                self.samples = None
                self.start_time = None
                self.sample_rate = None
                self.list_chunk = None
                self.format_chunk = Format_Chunk()
                self.peak_chunk = None
                self.normalized = False
            elif (fs is not None) and (samples is not None):
                if time is None:
                    t0 = 0
                else:
                    t0 = time

                super().__init__(samples, sample_rate=fs, start_time=t0)

                #   Now build the format chunk from this information

                self.format_chunk = Format_Chunk()
                self.peak_chunk = None
                self.list_chunk = None

            return

        if not isinstance(path, str):
            raise ValueError("You must provide the path to the file")

        if not os.path.exists(path):
            raise ValueError("The supplied path does not lead to a valid file")

        self.filename = path

        #   Parse the chunks

        self.scanner = Chunk_Scanner(self.filename)

        #   Now open the file and read the information from the format and peak chunks for the class

        with open(self.filename, 'rb') as file:

            #   The format chunk is required by all wav files
            self.format_chunk = Format_Chunk(file,
                                             self.scanner.format_chunk.chunk_offset,
                                             self.scanner.format_chunk.chunk_size,
                                             self.scanner.format_chunk.chunk_name)
            self.sample_rate = self.format_chunk.sample_rate

            #   If there is a peak chunk, read it

            if self.scanner.peak_chunk is not None:
                self.peak_chunk = Peak_Chunk(file,
                                             self.scanner.peak_chunk.chunk_offset,
                                             self.scanner.peak_chunk.chunk_size,
                                             self.scanner.peak_chunk.chunk_name,
                                             self.format_chunk.channel_count)
            else:
                self.peak_chunk = None

            #   If there is a list chunk, read it

            if self.scanner.list_chunk is not None:
                self.list_chunk = List_Chunk(file,
                                             self.scanner.list_chunk.chunk_size,
                                             self.scanner.list_chunk.chunk_offset,
                                             self.scanner.list_chunk.chunk_name)
                time0 = self.list_chunk.time0
                if self.list_chunk.cropping_information is not None:
                    if self.list_chunk.cropping_information == "normalized":
                        self.normalized = True
                    else:
                        self.normalized = False
                else:
                    self.normalized = False
            else:
                self.list_chunk = None
                time0 = 0
                self.normalized = False

            if self.scanner.xml_chunk is not None:
                self.xml_chunk = XML_Chunk(file,
                                           self.scanner.xml_chunk.chunk_size,
                                           self.scanner.xml_chunk.chunk_offset,
                                           self.scanner.xml_chunk.chunk_name)

                time0 = self.xml_chunk.start_time
            else:
                self.xml_chunk = None

            #   Read the data chunk, which is also required by all Wav files

            self.data_chunk = Data_Chunk(file,
                                         self.scanner.data_chunk.chunk_offset,
                                         self.scanner.data_chunk.chunk_size,
                                         self.scanner.data_chunk.chunk_name,
                                         self.format_chunk,
                                         self.peak_chunk,
                                         s0,
                                         s1,
                                         self.normalized)

            #   If the peak chunk was not read from the file, we need to create one from the data that was read from
            #   the wav file.

            if self.peak_chunk is None:
                self.peak_chunk = Peak_Chunk()
                self.peak_chunk.peak_amplitude = np.max(self.data_chunk.waveform, axis=0)
                self.peak_chunk.peak_sample = np.argmax(self.data_chunk.waveform, axis=0)

        #   Create the data and build the information for the generic_time_waveform

        super().__init__(self.data_chunk.waveform, self.format_chunk.sample_rate, time0)

    @property
    def full_path(self):
        """
        The fully realized path to the file that was read
        """

        return self.filename

    @property
    def bytes_per_sample(self):
        """
        the number of bytes per sample, which is the bits per sample read from the format chunk divided by 8
        """

        return self.format_chunk.bits_per_sample / 8

    @property
    def peak_value(self):
        return self.peak_chunk.peak_value

    @property
    def channel_count(self):
        return self.format_chunk.num_channels

    @property
    def audio_format(self):
        return self.format_chunk.audio_format

    @property
    def bits_per_sample(self):
        return self.format_chunk.bits_per_sample

    @property
    def block_align(self):
        return self.format_chunk.block_align

    @property
    def meta_data(self):
        if self.list_chunk is None:
            self.list_chunk = List_Chunk()
        return self.list_chunk.meta_data

    @property
    def header(self):
        if self.list_chunk is None:
            self.list_chunk = List_Chunk()
        return self.list_chunk.header

    @property
    def archival_location(self):
        if self.list_chunk is not None:
            return self.list_chunk.archival_location
        else:
            return None

    @archival_location.setter
    def archival_location(self, value):
        if self.list_chunk is None:
            self.list_chunk = List_Chunk()

        self.list_chunk.meta_data["archival_location"] = value

    @property
    def artist(self):
        if self.list_chunk is not None:
            return self.list_chunk.artist
        else:
            return None

    @artist.setter
    def artist(self, value):
        if self.list_chunk is None:
            self.list_chunk = List_Chunk()
        self.list_chunk.meta_data["artist"] = value

    @property
    def commissioned_organization(self):
        if self.list_chunk is not None:
            return self.list_chunk.commissioned_organization
        else:
            return None

    @commissioned_organization.setter
    def commissioned_organization(self, value):
        if self.list_chunk is None:
            self.list_chunk = List_Chunk()
        self.list_chunk.meta_data["commissioned_organization"] = value

    @property
    def general_comments(self):
        if self.list_chunk is not None:
            return self.list_chunk.general_comments
        else:
            return None

    @general_comments.setter
    def general_comments(self, value):
        if self.list_chunk is None:
            self.list_chunk = List_Chunk()
        self.list_chunk.meta_data["general_comments"] = value

    @property
    def copyright(self):
        if self.list_chunk is not None:
            return self.list_chunk.copyright
        else:
            return None

    @copyright.setter
    def copyright(self, value):
        if self.list_chunk is None:
            self.list_chunk = List_Chunk()
        self.list_chunk.meta_data["copyright"] = value

    @property
    def creation_date(self):
        if self.list_chunk is not None:
            return self.list_chunk.creation_date
        else:
            return None

    @creation_date.setter
    def creation_date(self, value):
        if self.list_chunk is None:
            self.list_chunk = List_Chunk()
        self.list_chunk.meta_data["creation_date"] = value

        if isinstance(value, str):
            raise ValueError("Expected the creation date to be a datetime")
        elif isinstance(value, datetime):
            self.list_chunk.time0 = value

    @property
    def cropping_information(self):
        if self.list_chunk is not None:
            return self.list_chunk.cropping_information
        else:
            return None

    @cropping_information.setter
    def cropping_information(self, value):
        if self.list_chunk is None:
            self.list_chunk = List_Chunk()
        self.list_chunk.meta_data["cropping_information"] = value

    @property
    def originating_object_dimensions(self):
        if self.list_chunk is not None:
            return self.list_chunk.originating_object_dimensions
        else:
            return None

    @originating_object_dimensions.setter
    def originating_object_dimensions(self, value):
        if self.list_chunk is None:
            self.list_chunk = List_Chunk()
        self.list_chunk.meta_data["originating_object_dimensions"] = value

    @property
    def dots_per_inch(self):
        if self.list_chunk is not None:
            return self.list_chunk.dots_per_inch
        else:
            return None

    @dots_per_inch.setter
    def dots_per_inch(self, value):
        if self.list_chunk is None:
            self.list_chunk = List_Chunk()
        self.list_chunk.meta_data["dots_per_inch"] = value

    @property
    def engineer_name(self):
        if self.list_chunk is not None:
            return self.list_chunk.engineer_name
        else:
            return None

    @engineer_name.setter
    def engineer_name(self, value):
        if self.list_chunk is None:
            self.list_chunk = List_Chunk()
        self.list_chunk.meta_data["engineer_name"] = value

    @property
    def subject_genre(self):
        if self.list_chunk is not None:
            return self.list_chunk.subject_genre
        else:
            return None

    @subject_genre.setter
    def subject_genre(self, value):
        if self.list_chunk is None:
            self.list_chunk = List_Chunk()
        self.list_chunk.meta_data["subject_genre"] = value

    @property
    def key_words(self):
        if self.list_chunk is not None:
            return self.list_chunk.key_words
        else:
            return None

    @key_words.setter
    def key_words(self, value):
        if self.list_chunk is None:
            self.list_chunk = List_Chunk()
        self.list_chunk.meta_data["key_words"] = value

    @property
    def lightness_settings(self):
        if self.list_chunk is not None:
            return self.list_chunk.lightness_settings
        else:
            return None

    @lightness_settings.setter
    def lightness_settings(self, value):
        if self.list_chunk is None:
            self.list_chunk = List_Chunk()
        self.list_chunk.meta_data["lightness_settings"] = value

    @property
    def originating_object_medium(self):
        if self.list_chunk is not None:
            return self.list_chunk.originating_object_medium
        else:
            return None

    @originating_object_medium.setter
    def originating_object_medium(self, value):
        if self.list_chunk is None:
            self.list_chunk = List_Chunk()
        self.list_chunk.meta_data["originating_object_medium"] = value

    @property
    def title(self):
        if self.list_chunk is not None:
            return self.list_chunk.title
        else:
            return None

    @title.setter
    def title(self, value):
        if self.list_chunk is None:
            self.list_chunk = List_Chunk()
        self.list_chunk.meta_data["title"] = value

    @property
    def color_palette_count(self):
        if self.list_chunk is not None:
            return self.list_chunk.color_palette_count
        else:
            return None

    @color_palette_count.setter
    def color_palette_count(self, value):
        if self.list_chunk is None:
            self.list_chunk = List_Chunk()
        self.list_chunk.meta_data["color_palette_count"] = value

    @property
    def subject_name(self):
        if self.list_chunk is not None:
            return self.list_chunk.subject_name
        else:
            return None

    @subject_name.setter
    def subject_name(self, value):
        if self.list_chunk is None:
            self.list_chunk = List_Chunk()
        self.list_chunk.meta_data["subject_name"] = value

    @property
    def description(self):
        if self.list_chunk is not None:
            return self.list_chunk.description
        else:
            return None

    @description.setter
    def description(self, value):
        if self.list_chunk is None:
            self.list_chunk = List_Chunk()
        self.list_chunk.meta_data["description"] = value

    @property
    def creation_software(self):
        if self.list_chunk is not None:
            return self.list_chunk.creation_software
        else:
            return None

    @creation_software.setter
    def creation_software(self, value):
        if self.list_chunk is None:
            self.list_chunk = List_Chunk()
        self.list_chunk.meta_data["creation_software"] = value

    @property
    def data_source(self):
        if self.list_chunk is not None:
            return self.list_chunk.data_source
        else:
            return None

    @data_source.setter
    def data_source(self, value):
        if self.list_chunk is None:
            self.list_chunk = List_Chunk()
        self.list_chunk.meta_data["data_source"] = value

    @property
    def original_form(self):
        if self.list_chunk is not None:
            return self.list_chunk.original_form
        else:
            return None

    @original_form.setter
    def original_form(self, value):
        if self.list_chunk is None:
            self.list_chunk = List_Chunk()
        self.list_chunk.meta_data["original_form"] = value

    @property
    def digitizing_engineer(self):
        if self.list_chunk is not None:
            return self.list_chunk.digitizing_engineer
        else:
            return None

    @digitizing_engineer.setter
    def digitizing_engineer(self, value):
        if self.list_chunk is None:
            self.list_chunk = List_Chunk()
        self.list_chunk.meta_data["digitizing_engineer"] = value

    @property
    def track_number(self):
        if self.list_chunk is not None:
            return self.list_chunk.track_number
        else:
            return None

    @track_number.setter
    def track_number(self, value):
        if self.list_chunk is None:
            self.list_chunk = List_Chunk()
            self.list_chunk.meta_data['track_no'] = value
        else:
            self.list_chunk.meta_data['track_no'] = value

    def save(self, path):
        """
        This function will save the data to a canonical wav formatted file with appropriate scaling to recover the
        actual Pascal values.

        :param path: str - the output path for the scaled canonical wav format
        """

        #   Ensure that the output path is fully formed before attempting to open the output file

        if not os.path.exists(os.path.dirname(path)):
            os.makedirs(os.path.dirname(path))

        #   Now we open the file

        with open(path, 'wb') as file:
            #   Write the canonical WAVE header with a zero file size that we will return later to modify

            file.write("RIFF".encode('utf-8'))
            file.write(struct.pack("<i", 0))
            file.write("WAVE".encode('utf-8'))

            #   Write the format chunk

            Format_Chunk.write_chunk(file, self.sample_rate, 32, self.format_chunk.channel_count)

            #   To scale the audio data correctly we either need to have a standard limit, or define the maximum in some
            #   other way.  The PEAK chunk provides a new way to represent the audio information, so let's write that
            #   now.

            if self.peak_chunk is None:
                self.peak_chunk = Peak_Chunk()
                self.peak_chunk.peak_amplitude = np.max(self.samples)
                self.peak_chunk.peak_sample = np.argmax(self.samples)

            self.peak_chunk.write_chunk(file)

            #   Write the data chunk header

            file.write("data".encode('utf-8'))
            file.write(struct.pack("<i", 4 * len(self.samples) * self.channel_count))

            #   Now we will loop through the data elements and write the information, scaled to 1.0f full scale based
            #   on the data within the PEAK chunk

            peak_value = np.max(self.samples)

            if self.normalized:
                if self.format_chunk.channel_count > 1:
                    for i in range(self.samples.shape[1]):
                        self.samples[:, i] /= np.max(self.samples[:, i])
                else:
                    self.samples[:] /= np.max(self.samples[:])

            samples_to_write = np.reshape(self.samples, (np.product(self.samples.shape),))
            # bytes_to_write = struct.pack("<{}f".format(len(samples_to_write)), samples_to_write)
            # file.write(bytes_to_write)

            for i in range(len(samples_to_write)):
                file.write(struct.pack("<f", samples_to_write[i]))

            #   Write the LIST chunk

            if self.list_chunk is not None:
                self.list_chunk.write_chunk(file)

            #   Get the current number of bytes within the file

            file_size = file.tell()

            #   Search for the file size - 8 within the header and update the information

            file.seek(4, 0)
            file.write(struct.pack("<i", file_size-8))

    def resample_16kHz_16bit(self, channel_index: int = 0):
        """
        In preparation for the transcription of the waveform with the Vosk wrapping of the Kaldi models we need to
        transform this signal to a 16 Khz, 16-bit signal.  This function performs the resmapling and scaling and returns
        the byte-array that is directly provided to the Vosk interface.

        :param channel_index: int - the index of the channel that will be read into the interface
        """

        #   Determine the resampling levels

        ratio = int(np.floor((16000 * self.samples.shape[0] / self.sample_rate)))

        samples = scipy.signal.resample(self.samples[:, channel_index], ratio)

        #   Now convert the data from current floating point representation to the short representation

        samples *= (2 ** 16) - 1
        int_samples = np.zeros(samples.shape, dtype='int')

        for i in range(len(int_samples)):
            int_samples[i] = int(np.round(samples[i]))

        short_data = int_samples.astype(np.int16)

        #   Now convert this short data to a binary array

        byte_data = bytearray()
        for i in range(len(short_data)):
            byte_data += struct.pack('h', short_data[i])

        return byte_data
