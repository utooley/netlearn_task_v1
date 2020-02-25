#Config file
### NOT BEING USED AT THE MOMENT ###

from psychopy import visual, core, event, data, gui, logging
# Import modules
import os
import random
import re
import urllib
import csv

expdir = os.getcwd()



################
# Set up window #
################

useFullScreen=False
win = visual.Window([1920,1080], monitor="testMonitor", units="deg", fullscr=False, allowGUI=True)


##############
# Parameters #
##############

frame_rate = 60
trial_duration=12
