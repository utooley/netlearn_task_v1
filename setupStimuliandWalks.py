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
import numpy as np

from psychopy import prefs
#prefs.general['audioLib'] = ['pyo']
prefs.general['audioLib'] = ['pygame']
prefs.general['shutdownKey'] = 'q'
from psychopy import sound

from config import *
#print prefs

################
# Set up instruction stimuli #
################

#prior to task
pretask_instruc_1="""Now we're going to play the alien game.
\n\n
You'll see two alien friends. You can tap either alien to see the next set of friends.
\n\n
Try to tap on the aliens as fast as you can.
\n\n
Now, let's practice!
"""

#Set up instructions to show
fixation = visual.TextStim(win, text="+", height=2, color="#FFFFFF")
pretask_instrucScreen_1= visual.TextStim(win, text=pretask_instruc_1, wrapWidth=30, alignHoriz="center", height=1.0, color="#FFFFFF")
#set up a mouse
mymouse = event.Mouse(win=win)
mymouse.setPos((0,0))

#transition to task
transition_instruc_1="""Great! Now, let's play for real.
\n\n
Remember, your job as a scientist is to watch the aliens and try to figure out who's friends with who!\
\n\n
Ready? Let's go!
"""

transition_screen_1= visual.TextStim(win, text=transition_instruc_1, wrapWidth=30, alignHoriz="center", height=1.0, color="#FFFFFF")

# Final SCREEN

completion_instruc_1="""Great job!
\n\n
Now you're back on Planet Earth...
\n\n
Remember how when you saw two aliens together, that meant they were friends?
\n\n\
Now we're going to ask you about the aliens you just saw.
"""
completion_screen_1= visual.TextStim(win, text=completion_instruc_1, wrapWidth=30, alignHoriz="center", height=1.0, color="#FFFFFF")

################
# Import trial lists #
################

# def get_trials(subj_id):
#     # import trial list and info and set up trial handler
#     trialFile = 'subjects/subj{}/walks1.csv'.format(subj_id)
#     trial_list = [ item for item in csv.DictReader(open(trialFile,'rU'))]
#     trials = data.TrialHandler(trial_list,nReps=1,method='sequential')
#     return trials

#####
#   SHOW INSTRUCTIONS
#####

#define a function to show instructions
def show_instructions():
    print('started instructionss')
    mymouse.setPos((0,0))
    mymouse.getPos()
    press1=False
    press2=False
    press3=False
    press4=False
    #core.wait(3)
    print('started instruct 2')
    # while not press1 and not press2 and not press3 and not press4:
    pretask_instrucScreen_1.draw()
    win.flip()
    core.wait(3)
    event.waitKeys()
    # if mymouse.mouseMoved():
    #     press1 = True
    #     core.wait(.2)

#####
#   READY SCREEN INSTRUCTIONS
#####

#define a function to show instructions
def show_ready_screen():
    mymouse.setPos((0,0))
    mymouse.getPos()
    press1=False
    press2=False
# while not press1 and press2:
    transition_screen_1.draw()
    win.flip()
    event.waitKeys()
    # if mymouse.mouseMoved():
    #     press1 = True
    #     core.wait(.2)

############
# Set up trial stimuli #
##############
#background image
background_image = visual.ImageStim(win, 'stimuli/Monster-Bkg-1-BW.jpg')

#Set up a mouse?
mymouse = event.Mouse(win=win)

#Import audio wav files
#soundL = sound.Sound('sounds/low_200.wav')
#soundR = sound.Sound('sounds/high_200.wav')

#Set Trial Stimuli
img = visual.ImageStim(win,'stimuli/null.png')
imgL = visual.ImageStim(win,'stimuli/null.png',pos=(-7,-4), size=10)
imgR = visual.ImageStim(win,'stimuli/null.png',pos=(7,-4), size=10)

#Completion sound
donesound=sound.Sound('sounds/high_200.wav')
#####
#Make a function to get the practice trial data #
####
def set_practicedata(subj_id):
    #########
    # log file
    # Get logfile name

    #Split trials into here runs if desired
    #trials=get_trials(subj_id)
    # import trial list and info and set up trial handler
    trialFile = 'subjData/{}/exposure_walk1.csv'.format(subj_id)
    trial_list = [ item for item in csv.DictReader(open(trialFile,'rU'))]
    prac_trial_list=trial_list[0:4]
    prac_trials = data.TrialHandler(prac_trial_list,nReps=1,method='sequential')
    #return trials

    ### DON'T NEED THIS ANYMORE
    # import animation conditions and info and set up list
    #animateFile = 'stimuli/animation_conds.csv'
    #animate_list = [ item for item in csv.DictReader(open(animateFile,'rU'))]

    #Add data types to trials
    #trials.data.addDataType('resp')
    prac_trials.data.addDataType('onset')
    prac_trials.data.addDataType('rt')

    # setup logging #
    #log_file = logging.LogFile("logs/subj%s.log" % (subj_id),  level=logging.DATA, filemode="w")
    return (prac_trials)

#####
#Make a function to get the walk data #
####
def set_walkdata(subj_id):
    #########
    # log file
    # Get logfile name

    expdir = os.getcwd()
    logdir = '{}/logs/{}'.format(expdir,subj_id)

    print logdir

    #if one participant is run more than once, make sure their log is saved separately
    ct = 0
    while 'logname' not in locals() or os.path.exists(logname):
        if ct > 0:
            lognum = '_%d' % (ct)
        else:
            lognum = ''
        logname = '{}/{}_log{}.csv'.format(logdir, subj_id, lognum)
        ct += 1

    if not os.path.exists(os.path.join('logs/%s/' % subj_id)):
        print "creating subject data directory"
        directory="logs/%s/" % subj_id
        os.makedirs(directory)

    #Split trials into here runs if desired
    #trials=get_trials(subj_id)
    # import trial list and info and set up trial handler
    trialFile = 'subjData/{}/exposure_walk1.csv'.format(subj_id)
    trial_list = [ item for item in csv.DictReader(open(trialFile,'rU'))]
    trial_list=trial_list[5:len(trial_list)]
    trials = data.TrialHandler(trial_list,nReps=1,method='sequential')
    #return trials

    # import animation conditions and info and set up list
    #animateFile = 'stimuli/animation_conds.csv'
    #animate_list = [ item for item in csv.DictReader(open(animateFile,'rU'))]

    #Add data types to trials
    #trials.data.addDataType('resp')
    trials.data.addDataType('onset')
    trials.data.addDataType('rt')

    # setup logging #
    log_file = logging.LogFile("logs/%s/subj%s.log" % (subj_id, subj_id),  level=logging.DATA, filemode="w")
    return (log_file,logname,trials)

#####
#Make a function to run the practice trials #
####

def do_runpractrials(subj_id,prac_trials,runID):
    #log_file = logging.LogFile("logs/subj%s.log" % (subj_id),  level=logging.DATA, filemode="w")
    #change logging level to DATA if don't want so much info

    ########################
     # SHOW READY SCREEN #
    ########################
    mymouse.getPos()
    atimer=core.CountdownTimer(1.5)
    while atimer.getTime() > 0:
        fixation.draw()
        win.flip()

    # wait for trigger from scanner
    #specify a key here
    #event.waitKeys()

    # set clock
    globalClock = core.Clock()
    logging.setDefaultClock(globalClock)

    logging.log(level=logging.DATA, msg="** START TASK **")
    prac_trials.extraInfo={'START':globalClock.getTime()}
    prac_trials.extraInfo={'participant':subj_id}

#    # disdaq fixation
#    logging.log(level=logging.DATA, msg="FIXATION")
#    for frame in range(frames['disdaq']):
#        fixation.draw()
#        win.flip()
    #size_list=[-= 0.1, -= 2, += 0.5, += 0.1]
    tidx = 0

    for tidx, trial in enumerate(prac_trials):
        print('In trial {} - node1 = {} node2 = {}'. format(tidx+1, trial['node1'], trial['node2']))
        print(trial['path1'],trial['path2'])

        logging.log(level=logging.DATA, msg="Trial %i - Stimuli1 %s - Stimuli2 %s" % (tidx+1, trial['path1'], trial['path2']))

        #Set values for trial
        imgL.setImage(trial['path1'])
        imgR.setImage(trial['path2'])
        #pick at random from animate_list
        animateone=trial['movement1']
        animatetwo=trial['movement2']
        #print(animateone,animatetwo)
        #add sounds here
        soundL=sound.Sound(trial['sound1'], secs=0.1)
        soundR=sound.Sound(trial['sound2'], secs=0.1)
        #soundR=sound.Sound(trial['sound2'])
        #imgR.size(0.1, '+')
        onset = globalClock.getTime()
        prac_trials.addData('onset', onset)
        #event.Mouse.clickReset(mouseclick)
        #correct=None
        #responses=None
        mymouse.setPos((0,0))
        mymouse.getPos()
        key=None
        rt=None
        Pressed=False

        #while not mouseclick.getPressed():
        #while globalClock.getTime() < (tidx+1)*trialDur:
        #timeimg1 = core.CountdownTimer(alien_duration_short)#how long the entire trial lasts for
        while not Pressed:
            #img_rect.draw()
            #set moving animation characteristics here after resetting normal!
            imgL.ori=(0)
            imgR.ori=(0)
            imgL.opacity=(1)
            imgR.opacity=(1)
            imgL.size=(10)
            imgR.size=(10)
            # imgL.pos=(-7,-4)
            # imgR.pos = (7,-4)
            #exec('imgR.'+ animateone['animation'])
            #exec('imgL.' + animatetwo['animation'])
            #print(animateone)
            #print(animatetwo)

            #show the result of the above
            background_image.draw()
            imgL.draw()
            imgR.draw()

            win.flip()
            soundL.play()
            timeimg1 = core.CountdownTimer(alien_duration_short)
            #mymouse.getPos()
            #while (timeimg1.getTime() > 2 and np.all(mymouse.getPos()) == 0):
            while (timeimg1.getTime() > 0 and not (imgL.contains(mymouse) or imgR.contains(mymouse))):
            #while localClock.getTime() < fixDur:
            #for frame in range(10*frame_rate):
                exec(animateone)#first have the left image zoom off
                background_image.draw()
                imgL.draw()
                imgR.draw()
                win.flip()
            #mymouse.getPos()
            soundR.play(loops=0)
            timeimg2=core.CountdownTimer(alien_duration_short)
            while (timeimg2.getTime() > 0 and not (imgL.contains(mymouse) or imgR.contains(mymouse))):
            #while (timeimg1.getTime() > 0 and timeimg1.getTime() < 2 and np.all(mymouse.getPos()) == 0):
            #while localClock.getTime() < fixDur:
            #for frame in range(10*frame_rate):
                exec(animatetwo)#first have the left image zoom off
                background_image.draw()
                imgL.draw()
                imgR.draw()
                win.flip()
            if len(event.getKeys(['escape'])):
                logging.flush()
                win.close()
                core.quit()
                break
            if imgL.contains(mymouse) or imgR.contains(mymouse):
            #if np.any(mymouse.getPos()) != 0 or timeimg1.getTime() < 0:
                donesound.play()
                rt=globalClock.getTime()-onset
                soundL.stop()
                soundR.stop()
                timer1 = core.CountdownTimer(.6)#how fast L image moves off screen.
                while timer1.getTime() > 0:
                #while localClock.getTime() < fixDur:
                #for frame in range(10*frame_rate):
                    imgL.pos-=(.25,0)#first have the left image zoom off
                    background_image.draw()
                    imgL.draw()
                    imgR.draw()
                    win.flip()
                #imgL.size += 10
                donesound.stop()
                timer2 = core.CountdownTimer(.9)
                while timer2.getTime() > 0:
                    imgR.pos-=(.25,0)#then move the right image over
                    background_image.draw()
                    imgR.draw()
                    win.flip()
                core.wait(.25)
                Pressed= True
                event.clearEvents()
                soundL.stop()
                soundR.stop()
                imgL.pos=(-7,-4)
                imgR.pos = (7,-4)

            #event.clearEvents()
        # If no response, play low sound
        #if responses==None:
            #low.play()
            #responses='NA'
            #rt='NA'
            #correct=0
        # record response
        #trials.addData('resp',responses)
        prac_trials.addData('rt',rt)

    # final fixation
    timer = core.CountdownTimer(fixDur)
    while timer.getTime() > 0:
    #while localClock.getTime() < fixDur:
    #for frame in range(10*frame_rate):
        fixation.draw()
        win.flip()

#    # break
#    if runID<5:
#        NS_breakScreen.draw()
#        win.flip()
#        event.waitKeys(keyList=('1'))

    logging.log(level=logging.DATA, msg="*** END ****")

    prac_trials.extraInfo['END']=globalClock.getTime()
#####
#Make a function to run the trials #
####

def do_runtrials(subj_id,trials,logname,runID):
    log_file = logging.LogFile("logs/%s/subj%s.log" % (subj_id, subj_id),  level=logging.DATA, filemode="w")
    #change logging level to DATA if don't want so much info

    ########################
     # SHOW READY SCREEN #
    ########################
    atimer=core.CountdownTimer(1.5)
    while atimer.getTime() > 0:
        fixation.draw()
        win.flip()
    # wait for trigger from scanner

    # set clock
    globalClock = core.Clock()
    logging.setDefaultClock(globalClock)

    logging.log(level=logging.DATA, msg="** START TASK **")
    trials.extraInfo={'START':globalClock.getTime()}
    trials.extraInfo={'participant':subj_id}

#    # disdaq fixation
#    logging.log(level=logging.DATA, msg="FIXATION")
#    for frame in range(frames['disdaq']):
#        fixation.draw()
#        win.flip()
    #size_list=[-= 0.1, -= 2, += 0.5, += 0.1]
    tidx = 0

    for tidx, trial in enumerate(trials):
        print('In trial {} - node1 = {} node2 = {}'. format(tidx+1, trial['node1'], trial['node2']))
        print(trial['path1'],trial['path2'])

        logging.log(level=logging.DATA, msg="Trial %i - Stimuli1 %s - Stimuli2 %s" % (tidx+1, trial['path1'], trial['path2']))

        #Set values for trial
        imgL.setImage(trial['path1'])
        imgR.setImage(trial['path2'])
        #pick at random from animate_list
        animateone=trial['movement1']
        animatetwo=trial['movement2']
        #print(animateone,animatetwo)
        #add sounds here
        soundL=sound.Sound(trial['sound1'], secs=0.1)
        soundR=sound.Sound(trial['sound2'], secs=0.1)
        #soundR=sound.Sound(trial['sound2'])
        #imgR.size(0.1, '+')
        onset = globalClock.getTime()
        trials.addData('onset', onset)
        #event.Mouse.clickReset(mouseclick)
        #correct=None
        #responses=None
        mymouse.setPos((0,0))
        mymouse.getPos()
        key=None
        rt=None
        Pressed=False

        #while not mouseclick.getPressed():
        #while globalClock.getTime() < (tidx+1)*trialDur:
        #timeimg1 = core.CountdownTimer(alien_duration)
        while not Pressed:
            #img_rect.draw()
            #set moving animation characteristics here after resetting normal!
            imgL.ori=(0)
            imgR.ori=(0)
            imgL.opacity=(1)
            imgR.opacity=(1)
            imgL.size=(10)
            imgR.size=(10)
            imgL.pos=(-7,-4)
            imgR.pos = (7,-4)
            #print(animateone)
            #print(animatetwo)

            #show the result of the above
            background_image.draw()
            imgL.draw()
            imgR.draw()

            win.flip()
            timeimg1 = core.CountdownTimer(alien_duration_short)#how fast L image moves off screen.
            soundL.play()
            while (timeimg1.getTime() > 0 and not (imgL.contains(mymouse) or imgR.contains(mymouse))):
            #while (timeimg1.getTime() > 0 and not (imgL.contains(mymouse) or imgR.contains(mymouse))):
            #while localClock.getTime() < fixDur:
            #for frame in range(10*frame_rate):
                exec(animateone)#first have the left image zoom off
                background_image.draw()
                imgL.draw()
                imgR.draw()
                win.flip()
            timeimg2 = core.CountdownTimer(alien_duration_short)#how fast L image moves off screen.
            soundR.play()
            while (timeimg2.getTime() > 0 and not (imgL.contains(mymouse) or imgR.contains(mymouse))):
            #while localClock.getTime() < fixDur:
            #for frame in range(10*frame_rate):
                exec(animatetwo)#first have the left image zoom off
                background_image.draw()
                imgL.draw()
                imgR.draw()
                win.flip()
            if len(event.getKeys(['escape'])):
                logging.flush()
                trials.saveAsWideText(fileName=logname, delim='\t', appendFile=False)
                win.close()
                core.quit()
                break
            if imgL.contains(mymouse) or imgR.contains(mymouse):
            #if np.any(mymouse.getPos()) != 0 or timeimg1.getTime() < 0:
                donesound.play()
                rt=globalClock.getTime()-onset
                soundL.stop()
                soundR.stop()
                timer1 = core.CountdownTimer(.6)#how fast L image moves off screen.
                while timer1.getTime() > 0:
                #while localClock.getTime() < fixDur:
                #for frame in range(10*frame_rate):
                    imgL.pos-=(.25,0)#first have the left image zoom off
                    background_image.draw()
                    imgL.draw()
                    imgR.draw()
                    win.flip()
                donesound.stop()
                timer2 = core.CountdownTimer(.9)
                while timer2.getTime() > 0:
                    imgR.pos-=(.25,0)#then move the right image over
                    background_image.draw()
                    imgR.draw()
                    win.flip()
                core.wait(.25)
                Pressed= True
                event.clearEvents()
                soundL.stop()
                soundR.stop()
            #event.clearEvents()
        # record response
        #trials.addData('resp',responses)
        #imgL.pos-=(1,0)
        trials.addData('rt',rt)


#    # break
#    if runID<5:
#        NS_breakScreen.draw()
#        win.flip()
#        event.waitKeys(keyList=('1'))

    logging.log(level=logging.DATA, msg="*** END ****")

    trials.extraInfo['END']=globalClock.getTime()
    trials.saveAsWideText(fileName=logname, delim='\t', appendFile=False)

#####
#   COMPLETION SCREEN
#####

#define a function to show instructions
def show_completion_screen():
    mymouse.setPos((0,0))
    mymouse.getPos()
    press1=False
    press2=False
    # while not press1 and not press2:
    completion_screen_1.draw()
    win.flip()
    event.waitKeys()
    # core.wait(2)
    # if mymouse.mouseMoved():
    #     press1 = True
    #     core.wait(.2)
    print('done')
    win.close()

####
# If this script is run by itself, not loaded as a module, do the below:
####

if __name__ == '__main__':
    subj_id = 1

    #just show the instructions
    #show_instructions()

    #and then run through trials
    log_file,logname,trials = set_walkdata(subj_id)
    practrials=set_practicedata(subj_id)

    #round 1
    do_runpractrials(subj_id, practrials)
    do_runtrials(subj_id,trials,logname.replace('.csv','_run1.csv'),1)
