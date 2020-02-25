
import sys
sys.path.append('.')
from pandas import DataFrame, read_csv
from psychopy import core, gui
from psychopy import data, event, logging, visual, prefs
# Import modules
import os
import random
import re
import urllib
import csv
import datetime
prefs.general['shutdownKey'] = 'q'

##### SET UP #######
######

# # get subjID
# subjDlg = gui.Dlg(title="Dyad Choice")
# subjDlg.addField('Enter Subject ID:')
# subjDlg.addField('Enter Condition:')
# subjDlg.show()
#
# if gui.OK:
#     subj_id=subjDlg.data[0]
#     cond=float(subjDlg.data[1])
# else:
#     sys.exit() #commented out when strung all together

#import custom scripts

##### IMPORT PYTHON SCRIPTS #######
print('Importing relevant scripts')
#from config_dyadic_choice import * #when string together, do not import
from set_dyadic_stimuli import *
print('Done setting parameters and stimuli')


################
# DEFINE TASK #
################

print('Defining task functions')

print('Defining setdata function')

def setdata(subj_id):
    expdir = os.getcwd()
    logdir = '{}/subjData/{}/dyad_choice/'.format(expdir,subj_id)

    print logdir

    #########
    # log file
    # Get logfile name
    ct = 0
    while 'logname' not in locals() or os.path.exists(logname):
        if ct > 0:
            lognum = '_%d' % (ct)
        else:
            lognum = ''
        logname = '{}/{}_log_dyad_choice{}.csv'.format(logdir, subj_id, lognum)
        ct += 1

    ######
    # set up trial handler
    dyad_choice_trialFile = 'subjData/{}/dyad_choice/dyad_choice1.csv'.format(subj_id)
    dyad_choice_trialList = [ item for item in csv.DictReader(open(dyad_choice_trialFile,'rU'))]
    dyad_choice_trials = data.TrialHandler(dyad_choice_trialList,nReps=1,method='sequential')


    #Add data types to trials
    dyad_choice_trials.data.addDataType('resp')
    dyad_choice_trials.data.addDataType('rt')
    dyad_choice_trials.data.addDataType('correct')

    # setup logging #
    log_file = logging.LogFile("subjData/%s/dyad_choice/%s_dyad_choice.log" % (subj_id, subj_id),  level=logging.DATA, filemode="w")

    return (log_file,logname,dyad_choice_trials)

print('Defining instruct_dyad_choice function')

def instruct_dyad_choice(subj_id):
    print('Starting instructions')
    mymouse.setPos((0,0))
    mymouse.getPos()
    press1=False
    press2=False
    press3=False
    press4=False
    #core.wait(3)
    while not press1 and not press2 and not press3 and not press4:
        dyad_choice_InstructScreen1.draw()
        win.flip()
        core.wait(4)
        if mymouse.mouseMoved():
            press1 = True
            core.wait(.2)
    while not press2 and not press3 and not press4:
        mymouse.getPos()
        dyad_choice_InstructScreen2.draw()
        win.flip()
        if mymouse.mouseMoved():
            press2= True
            core.wait(.2)
    while not press3 and not press4:
        mymouse.getPos()
        dyad_choice_InstructScreen3.draw()
        win.flip()
        if mymouse.mouseMoved():
            press3= True
            core.wait(.2)
    while not press4:
        mymouse.getPos()
        dyad_choice_InstructScreen4.draw()
        win.flip()
        if mymouse.mouseMoved():
            press4= True
            core.wait(.2)
print('Defining do_dyad_choice function')

def do_dyad_choice(trials,logname,subj_id):
    print('Starting Task')
    #log_file = logging.LogFile("logs/subj%s_NS.log" % (subj_id),  level=logging.DATA, filemode="w")

    # set clock
    globalClock = core.Clock()
    logging.setDefaultClock(globalClock)

    logging.log(level=logging.DATA, msg="** START dyad_choice**")
    trials.extraInfo={'START':globalClock.getTime()}
    tidx = 0

    for tidx, trial in enumerate(trials):
        print('In trial {} - image #1={}, image #2={}, trial type={}'.format(tidx+1,trial['dyadic1path'],trial['dyadic2path'],trial['trial_type']))

        logging.log(level=logging.DATA, msg='Trial {} - image #1={}, image #2={}, trial type={}'.format(tidx+1,trial['dyadic1path'],trial['dyadic2path'],trial['trial_type']))

        #Set values for trial
        img1.setImage(trial['dyadic1path'])
        img2.setImage(trial['dyadic2path'])
        #scale the images by half on each trial
        img1.size=None
        img2.size=None
        img2.setSize(img2.size/2)
        img1.setSize(img1.size/2)

        onset = globalClock.getTime()
        trials.addData('onset', onset)
        correct=None
        responses=None
        key=None
        rt=None
        Pressed=False
        mymouse.setPos((0,15))
        mymouse.getPos()

        while not Pressed:
            #to get all stimuli to 'sit' on the same plane
            img1.pos=(-7,(-2+(img1.size[1]/2)))
            img2.pos=(7,(-2+(img2.size[1]/2))) ##CHANGE THESE
            yesimg.pos=(-5,-9)
            noimg.pos=(5,-9)
            # img2.pos=(0,-1)
            # img3.pos=(10,-1)
            img1.draw()
            img2.draw()
            yesimg.draw()
            noimg.draw()
            resp_prompt1.draw()
            win.flip()

            #need to change this to be catching pushes on the characters rather than keys
            key=event.getKeys(keyList=('escape'))
            #mouseclick=mymouse.getPressed()
            yesclick=mymouse.isPressedIn(yesimg)
            noclick=mymouse.isPressedIn(noimg)
            #rt=globalClock.getTime()-onset
            mymouse.getPos()
            if yesimg.contains(mymouse) or noimg.contains(mymouse):
                rt=globalClock.getTime()-onset
                if (yesimg.contains(mymouse) and (trial['trial_type']=='friends_within' or trial['trial_type']=='friends_between')):
                    correct=1
                    responses='yes'
                    core.wait(.1)
                    Pressed= True
                    #clear out all the sizes so they can be reset on each trial based on image size
                    img1.size=None
                    img2.size=None
                    event.clearEvents()
                elif (yesimg.contains(mymouse) and (trial['trial_type']=='non_friends_within' or trial['trial_type']=='non_friends_between_dist4' or trial['trial_type']=='non_friends_between_dist2')):
                    correct=0
                    responses='yes'
                    core.wait(.1)
                    Pressed= True
                    img1.size=None
                    img2.size=None
                    event.clearEvents()
                elif (noimg.contains(mymouse) and (trial['trial_type']=='non_friends_within' or trial['trial_type']=='non_friends_between_dist4' or trial['trial_type']=='non_friends_between_dist2')):
                    correct=1
                    responses='no'
                    core.wait(.1)
                    Pressed= True
                    img1.size=None
                    img2.size=None
                    event.clearEvents()
                elif (noimg.contains(mymouse) and (trial['trial_type']=='friends_within' or trial['trial_type']=='friends_between')):
                    correct=0
                    responses='no'
                    core.wait(.1)
                    Pressed= True
                    img1.size=None
                    img2.size=None
                    event.clearEvents()
                else:
                    print 'something went wrong'
            elif 'escape' in key:
                logging.flush() # if you are using logger
                trials.saveAsWideText(fileName=logname, delim=',', appendFile=False)
                win.close()
                core.quit()
                break
            # elif (key[0][0]==trial['Key']):
            #     correct=1
            # else:
            #     correct=0

            # event.clearEvents()

            # record response
        trials.addData('resp',responses)
        trials.addData('rt',rt)
        trials.addData('correct',correct)

    logging.log(level=logging.DATA, msg="*** END dyad_choice****")

    trials.extraInfo['END']=globalClock.getTime()
    trials.saveAsWideText(fileName=logname, delim=',', appendFile=False)


print('Defining full dyad choice function')


def full_dyad_choice(subj_id, cond):

    #set values and parameters for tasks
    print('Set Vals for Task')
    log_file,logname,dyad_choice_trials=setdata(subj_id)

    #Instructions
    instruct_dyad_choice(subj_id)

    #dyad_choice_ Task
    do_dyad_choice(dyad_choice_trials,logname,subj_id)

print('Done setting up functions')

if __name__ == '__main__':
    full_dyad_choice()
    # if cond==1:
    #     fullNSTask()
    #     fullSocTask()
    # elif cond==2:
    #     fullSocTask()
    #     fullNSTask()

    core.quit()
