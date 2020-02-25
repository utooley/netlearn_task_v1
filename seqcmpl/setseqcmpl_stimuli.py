
from pandas import DataFrame, read_csv
from psychopy import core, gui
from psychopy import data, event, logging, visual, prefs
# Import modules
import os
import random
import re
import urllib
import csv

#from configseqcmpl import *
trial_duration=10

################
# Set up window #
################
#useFullScreen=True
win = visual.Window([1920,1080], monitor="testMonitor", units="deg", fullscr=True, allowGUI=True)

################
# Set up Non-Social stimuli #
################

#instruction text
sqcmplInstruct1="""
\n\n\
You will see 4 aliens, and your job is to pick which one comes next.
\n\n\
If you're not sure, just take a guess.
\n\n\
If you do really well, you'll get a sticker! \
"""

#Set up instructions to show
fixation = visual.TextStim(win, text="+", height=2, color="#FFFFFF")
sqcmplInstructScreen1 = visual.TextStim(win, text=sqcmplInstruct1, wrapWidth=35, alignHoriz="center", height=1.0, color="#FFFFFF")

#Set Walk Trial Stimuli
img1 = visual.ImageStim(win,'stimuli/null.png', size=12)
img2 = visual.ImageStim(win,'stimuli/null.png', size=12)
img3 = visual.ImageStim(win,'stimuli/null.png', size=12 )
img4 = visual.ImageStim(win,'stimuli/null.png', size=12 )
img5 = visual.ImageStim(win,'stimuli/null.png', size=13)
img6 = visual.ImageStim(win,'stimuli/null.png', size=13 )

question=visual.TextStim(win, text="?", height=3, color="#FFFFFF", bold=True)
resp_prompt1 = visual.TextStim(win, text="Which alien comes next?", wrapWidth=35, pos=(0,-13),  height=1.4, color="#FFFFFF", bold=True)
#resp_prompt2 = visual.TextStim(win, text="", wrapWidth=35, pos=(0,8),  height=1.0, color="#FFFFFF")

#Set up a mouse
mymouse = event.Mouse(win=win)
