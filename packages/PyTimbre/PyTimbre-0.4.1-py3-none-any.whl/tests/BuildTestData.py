# -*- coding: utf-8 -*-
"""
Created on Fri Apr 24 09:23:52 2020

@author: frankmobley

This gives a platform for testing the PyTimbre code and fixing issues found
in the processing of the DCASE Community Challenge files
"""

from ..pytimbre.SoundFile import SoundFile
import time, os, pandas as pd, numpy as np
from os.path import abspath

path = abspath("./examples/uh1 without jackhammer.wav")
if os.path.exists(path):
    sf = SoundFile.fromfile(path)
    sf.generate()
    sf.evaluate()
    print("the audio file {} passed!".format(path))
    exit(0)
else:
    print("the audio file doesn't exist. Please check the path {}".format(path))
    folder = abspath('./Examples')
    if os.path.exists(folder):
        all_files = os.listdir(folder)
        if 'uh1 without jackhammer.wav' not in all_files: # there is not a problem, it doesn't exist
            exit(0)
        # for file in all_files:
        #     print('the file {} exists'.format(file))
    else:
        print("the folder {} does not exist.".format(folder))
        if 'build' in folder:
            exit(0)
exit(1)

