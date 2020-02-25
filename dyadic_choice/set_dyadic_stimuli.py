
from psychopy import visual, core, event, data, gui, logging
# Import modules
import os
import random
import re
import urllib
import csv

#from config_dyadic_choice import * #when assessments together, do not import

################
# Set up window #
################

#useFullScreen=True
win = visual.Window([1920,1080], monitor="testMonitor", units="deg", fullscr=False, allowGUI=True)

################
# Set up Non-Social stimuli #
################

#instruction text
dyadic_choice_Instruct1="""
Great job! We want to ask you one more thing!
\n\n\
Remember how when you saw two aliens together, that meant they were friends?
\n\n\
So when you saw two aliens together, that meant they were friends.
\n\n\
"""
dyadic_choice_Instruct2="""
Some of the aliens were friends, and some of the aliens weren't friends.
\n\n\
Now, we're going to ask you whether two aliens were friends or not.
\n\n\
Tap the screen to continue. \
"""
dyadic_choice_Instruct3="""
If you think they're friends, press the green 'Yes' button!
\n\n\
If you don't think they're friends, press the red 'No' button!
\n\n\
Tap the screen to continue. \
"""
dyadic_choice_Instruct4="""
This should only take a few minutes.
\n\n\
If you're not sure, just go with your gut feeling.
\n\n\
Tap the screen to continue. \
"""
# sqcmplInstruct3="""
# When each set of aliens is on the screen, click on the one that is NOT friends with the other two.\
# \n\n\
# This should only take a few minutes. \
# If you're not sure, just go with your gut feeling. \
# \n\n\
# Press any key to to continue.\
# """

#Set up instructions to show
fixation = visual.TextStim(win, text="+", height=2, color="#FFFFFF")
dyad_choice_InstructScreen1 = visual.TextStim(win, text=dyadic_choice_Instruct1, wrapWidth=35, alignHoriz="center", height=1.0, color="#FFFFFF")
dyad_choice_InstructScreen2 = visual.TextStim(win, text=dyadic_choice_Instruct2, wrapWidth=35, alignHoriz="center", height=1.0, color="#FFFFFF")
dyad_choice_InstructScreen3 = visual.TextStim(win, text=dyadic_choice_Instruct3, wrapWidth=35, alignHoriz="center", height=1.0, color="#FFFFFF")
dyad_choice_InstructScreen4 = visual.TextStim(win, text=dyadic_choice_Instruct4, wrapWidth=35, alignHoriz="center", height=1.0, color="#FFFFFF")

#Set Walk Trial Stimuli
img1 = visual.ImageStim(win,'stimuli/null.png', size=12)
img2 = visual.ImageStim(win,'stimuli/null.png', size=12)
yesimg = visual.ImageStim(win,'stimuli/yesbutton.png', size=6)
noimg = visual.ImageStim(win,'stimuli/nobutton.png', size=6)

resp_prompt1 = visual.TextStim(win, text="Are these two aliens friends?", wrapWidth=35, pos=(0,-4),  height=1.4, color="#FFFFFF", bold=True)
#resp_prompt2 = visual.TextStim(win, text="", wrapWidth=35, pos=(0,8),  height=1.0, color="#FFFFFF")

#Set up a mouse
mymouse = event.Mouse(win=win)
