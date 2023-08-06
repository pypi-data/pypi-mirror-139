import os
import numpy as np
import pandas as pd
from ..pytimbre.SoundFile import SoundFile
import glob
from sys import exit
import matplotlib.pyplot as plt
import traceback

#   Set the root of the data

data_root = './examples'

#   List the wave files within this folder

files = glob.glob(os.path.join(data_root, 'stimulus*.wav'))

#   Prepare the configuration for the execution of the Timbre analysis

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
            if (process_config['ERB_descr'][i]['name'] ==
                    process_config['Harmonic_descr'][j]['name']):
                #   Remove the element from the Harmonic descriptors

                del process_config['Harmonic_descr'][j]
                break

for i in range(len(files)):

    #   Process the features out of the SoundFile
    try:
        sf = SoundFile.fromfile(files[i], [1], config=process_config)
        #   Generate the pools for the evaluation of the attributes
        sf.generate()
        #   Evaluate the seleted attributes
        sf.evaluate()
        #   Extract the data and determine the features
        sf.extract()
        parameters = sf.output()
        print("the audio file {} passed!".format(files[i]))
    except IndexError as eee:
        print('Something went wrong')
        traceback.print_exc()
        exit(-1000)
exit(0)