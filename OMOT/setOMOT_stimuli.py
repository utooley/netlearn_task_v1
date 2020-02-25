

from pandas import DataFrame, read_csv
from psychopy import core, gui
from psychopy import data, event, logging, visual, prefs
# Import modules
import os
import random
import re
import urllib
import csv

#from configOMOT import *

################
# Set up window #
################

#useFullScreen=True
#win = visual.Window([800,600], monitor="testMonitor", units="deg", fullscr=False, allowGUI=False)

################
# Set up Non-Social stimuli #
################
win = visual.Window([1920,1080], monitor="testMonitor", units="deg", fullscr=True, allowGUI=True)

omotInstruct1="""
We'll show you 3 aliens. Two of them are friends. One of them is NOT friends with the other two.
\n\n\
Your job is to tell me which alien is NOT friends with the other two."""

omotInstruct2="""
If you're not sure, just make a guess.
\n\n\
If you get all of them right, you'll get a sticker!
"""

#Set up instructions to show
fixation = visual.TextStim(win, text="+", height=2, color="#FFFFFF")
omotInstructScreen1 = visual.TextStim(win, text=omotInstruct1, wrapWidth=35, alignHoriz="center", height=1.0, color="#FFFFFF")
omotInstructScreen2 = visual.TextStim(win, text=omotInstruct2, wrapWidth=35, alignHoriz="center", height=1.0, color="#FFFFFF")

#Set Walk Trial Stimuli
img1 = visual.ImageStim(win,'stimuli/null.png', pos=(-10,10))
img2 = visual.ImageStim(win,'stimuli/null.png', pos=(0,-4)) #maybe need to make these where the clicks are?
img3 = visual.ImageStim(win,'stimuli/null.png', pos=(10,-4))

resp_prompt1 = visual.TextStim(win, text="Which alien WASN'T friends with the other two?", wrapWidth=35, pos=(0,-9.5),  height=1.4, color="#FFFFFF", bold=True)
#resp_prompt2 = visual.TextStim(win, text="", wrapWidth=35, pos=(0,8),  height=1.0, color="#FFFFFF")

#Set up a mouse
mymouse = event.Mouse(win=win)
