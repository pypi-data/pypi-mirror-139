# -*- coding: utf-8 -*-
"""
Created on Mon Jul  6 15:10:56 2020

@author: frankmobley

This is a test file that will run the analysis on the longer (5 min) files used int eh Hoglund experiment.
"""
import numpy as np, pandas as pd, os
from ..pytimbre.SoundFile import SoundFile
from os.path import abspath

#   Get a list of the wav files from the orginal data collection

ambient_files = abspath("./Examples/ambient5.wav")

#   Create the PyTimbre objects that will be used for analysis of the wave file

process_config = SoundFile.default_config()

#   Remove the elements that are not required for this analysis

process_config.pop('STFT')
process_config.pop('STFT_descr')

#   Change the method of the ERB analysis to the gammatone filters
if process_config['ERB']:
    process_config['ERB']['method'] = 'fft'

    #   Now remove the duplicative features from the harmonic analysis

    for i in range(len(process_config['ERB_descr'])):
        for j in range(len(process_config['Harmonic_descr'])):
            if (process_config['ERB_descr'][i]['name'] ==
                    process_config['Harmonic_descr'][j]['name']):
                #   Remove the element from the Harmonic descriptors

                del process_config['Harmonic_descr'][j]
                break

# Do the work to proccess the files
# Create the SoundFile object to define the Timbre attributes

if os.path.exists(ambient_files):
    print('Create SoundFile Object')
    sf = SoundFile.fromfile(ambient_files, config=process_config)
    print('Generate the Spectrograms')
    sf.generate()
    print('Evaluate the attributes')
    sf.evaluate()
    print('Get the statistical values')
    sf.extract()
    print('Save the data to a file')
    sf.to_csv(ambient_files + '.csv')
    print("the audio file {} passed!".format(ambient_files))
    exit(0)
else:
    print("the audio file doesn't exist. Please check the path {}".format(ambient_files))
    folder = abspath('./Examples')
    if os.path.exists(folder):
        all_files = os.listdir(folder)
        if 'ambient5.wav' not in all_files: # there is not a problem, it doesn't exist
            exit(0)
        # for file in all_files:
        #     print('the file {} exists'.format(file))
    else:
        print("the folder {} does not exist.".format(folder))
        if 'build' in folder:
            exit(0)
exit(1)
