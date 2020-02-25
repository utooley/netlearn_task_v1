#Config file
#Internet says that to run scripts from Terminal on new Macs, modules need to be imported in this order
from pandas import DataFrame, read_csv
from psychopy import core, gui
from psychopy import data, event, logging, visual
# Import modules
import os
import random
import re
import urllib
import csv

from psychopy import prefs
#prefs.general['audioLib'] = ['pyo']
prefs.general['audioLib'] = ['pygame']
prefs.general['shutdownKey'] = 'q'
from psychopy import sound
print sound.Sound()

expdir = os.getcwd()



################
# Set up window #
################

useFullScreen=True
win = visual.Window([1920,1080], monitor="testMonitor", units="deg", fullscr=True, allowGUI=True)


##############
# Parameters #
##############

frame_rate = 60

fixDur=.5 #seconds
trainDur=5 #seconds
alien_duration=18
alien_duration_short=1.5 #seconds each alien moves for

frames = {
    'fixation': 10*frame_rate,
    'train': 2*frame_rate,
    'trial': int(1.5*frame_rate),
    'disdaq': 5*frame_rate
}
