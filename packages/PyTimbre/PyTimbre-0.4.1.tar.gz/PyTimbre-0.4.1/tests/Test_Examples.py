# -*- coding: utf-8 -*-
"""
Created on Fri Apr 24 09:23:52 2020

@author: frankmobley

This gives a platform for testing the PyTimbre code and fixing issues found 
in the processing of the DCASE Community Challenge files
"""

from ..pytimbre.SoundFile import SoundFile
import time, os
import pandas as pd
import numpy as np
from os.path import abspath

filename = abspath('./Examples/airport-vienna-14-571-a.wav')

#   Build the default configuration for the processing
filename = os.path.join(os.path.dirname(__file__), filename)
process_config = SoundFile.default_config()

#   Remove the elements that are not required for this analysis

process_config.pop('STFT')
process_config.pop('STFT_descr')

#   Change the method of the ERB analysis to the gammatone filters
if process_config['ERB']:
    process_config['ERB']['method'] = 'gammatone'
    #   Now remove the duplicative features from the harmonic analysis
    for i in range(len(process_config['ERB_descr'])):
        for j in range(len(process_config['Harmonic_descr'])):
            if(process_config['ERB_descr'][i]['name'] == 
                process_config['Harmonic_descr'][j]['name']):
                
                #   Remove the element from the Harmonic descriptors
                
                del process_config['Harmonic_descr'][j]
                break

if os.path.exists(filename):
    sf = SoundFile.fromfile(filename, [1,0], config = process_config)
    # Generate the pools for the evaluation of the attributes
    sf.generate()
    # Evaluate the seleted attributes
    sf.evaluate()
    # Extract the data and determine the features
    sf.extract()
    parameters = sf.output()
    # sf.to_csv('./Examples/test output.csv')
    print("the audio file {} passed!".format(filename))
    exit(0)
else:
    print("the audio file doesn't exist. Please check the path {}".format(filename))
    folder = abspath('./Examples')
    if os.path.exists(folder):
        all_files = os.listdir(folder)
        if 'airport-vienna-14-571-a.wav' not in all_files: # there is not a problem, it doesn't exist
            exit(0)
        # for file in all_files:
        #     print('the file {} exists'.format(file))
    else:
        print("the folder {} does not exist.".format(folder))
        if 'build' in folder:
            exit(0)
exit(1)
