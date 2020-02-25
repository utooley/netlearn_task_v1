
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
# subjDlg = gui.Dlg(title="OMO Task")
# subjDlg.addField('Enter Subject ID:')
# subjDlg.addField('Enter Condition:')
# subjDlg.show()
#
# if gui.OK:
#     subj_id=subjDlg.data[0]
#     cond=float(subjDlg.data[1])
# else:
#     sys.exit() #commented out for linking all together

#import custom scripts
##### IMPORT PYTHON SCRIPTS #######
print('Importing relevant scripts')
#from configOMOT import *
from setOMOT_stimuli import *
print('Done setting parameters and stimuli')
#import Soc_OMOT as soc1
#print('Done importing Soc_OMOT')
#import NS_OMOT as ns1
#print('Done importing NS_OMOT')


################
# DEFINE TASK #
################

print('Defining task functions')

print('Defining setdata function')

def setdata(subj_id):
    expdir = os.getcwd()
    logdir = '{}/subjData/{}/OMOT'.format(expdir,subj_id)

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
        logname = '{}/{}_log_omot{}.csv'.format(logdir, subj_id, lognum)
        ct += 1

    ######
    # set up trial handler
    omot_trialFile = 'subjData/{}/OMOT/omot1.csv'.format(subj_id)
    omot_trialList = [ item for item in csv.DictReader(open(omot_trialFile,'rU'))]
    omot_trials = data.TrialHandler(omot_trialList,nReps=1,method='sequential')


    #Add data types to trials
    omot_trials.data.addDataType('resp')
    omot_trials.data.addDataType('rt')
    omot_trials.data.addDataType('correct')

    # setup logging #
    log_file = logging.LogFile("subjData/%s/OMOT/%s_OMOT.log" % (subj_id, subj_id),  level=logging.DATA, filemode="w")

    return (log_file,logname,omot_trials)

print('Defining instruct_omot function')

def instruct_omot(subj_id):
    print('Starting instructions')
    mymouse.setPos((0,0))
    mymouse.getPos()
    # press1=False
    # press2=False
    # press3=False
    # #core.wait(3)
    # while not press1 and not press2 and not press3:
    omotInstructScreen1.draw()
    win.flip()
    event.waitKeys()
    # core.wait(4)
    # if mymouse.mouseMoved():
    #     press1 = True
    #     core.wait(.2)
# while not press2 and not press3:
    mymouse.getPos()
    omotInstructScreen2.draw()
    win.flip()
    event.waitKeys()
    # if mymouse.mouseMoved():
    #     press2= True
    #     core.wait(.2)

print('Defining do_omot function')

def do_omot(trials,logname,subj_id):
    print('Starting Task')
    #log_file = logging.LogFile("logs/subj%s_NS.log" % (subj_id),  level=logging.DATA, filemode="w")

    # set clock
    globalClock = core.Clock()
    logging.setDefaultClock(globalClock)

    logging.log(level=logging.DATA, msg="** START OMOT**")
    trials.extraInfo={'START':globalClock.getTime()}
    trials.extraInfo={'participant':subj_id}
    tidx = 0

    for tidx, trial in enumerate(trials):
        print('In trial {} - image #1={}, image #2={}, image #3={}'.format(tidx+1,trial['path1'],trial['path2'],trial['path3']))

        logging.log(level=logging.DATA, msg='Trial {} - image #1={}, image #2={}, image #3={}'.format(tidx+1,trial['path1'],trial['path2'],trial['path3']))

        #Set values for trial
        img1.setImage(trial['path1'])
        img2.setImage(trial['path2'])
        img3.setImage(trial['path3'])
        # print(img1.size[1])
        # print(img1.size[0])
        #scale the images by half on each trial
        img3.setSize(img3.size/2)
        img2.setSize(img2.size/2)
        img1.setSize(img1.size/2)

        core.wait(1.2) #to prevent kids from tapping so quickly that they skip.
        onset = globalClock.getTime()
        trials.addData('onset', onset)
        mymouse.setPos((0,15))
        mymouse.getPos()
        correct=None
        responses=None
        key=None
        rt=None
        Pressed=False

        while not Pressed:
            #to get all stimuli to 'sit' on the same plane
            img1.pos=(-10,(-8+(img1.size[1]/2)))
            img2.pos=(0,(-8+(img2.size[1]/2)))
            img3.pos=(10,(-8+(img3.size[1]/2)))
            # img2.pos=(0,-1)
            # img3.pos=(10,-1)
            img1.draw()
            img2.draw()
            img3.draw()
            resp_prompt1.draw()
            win.flip()

            #need to change this to be catching pushes on the characters rather than keys
            key=event.getKeys(keyList=('escape'))
            #mouseclick=mymouse.getPressed()
            # mouseclick1=mymouse.isPressedIn(img1)
            # mouseclick2=mymouse.isPressedIn(img2)
            # mouseclick3=mymouse.isPressedIn(img3)
            mymouse.getPos()
            if img1.contains(mymouse) or img2.contains(mymouse) or img3.contains(mymouse):
                rt=globalClock.getTime()-onset
                #if (mouseclick1==True and trial['Key']=='1'):
                if (img1.contains(mymouse) and (trial['Image1']==trial['Ans'])):
                    print('1')
                    correct=1
                    responses=trial['Image1']
                    core.wait(.05)
                    Pressed= True
                    win.flip()
                    #clear out all the sizes so they can be reset on each trial based on image size
                    img1.size=None
                    img2.size=None
                    img3.size=None
                    event.clearEvents()
                elif (img2.contains(mymouse)==True and (trial['Image2']==trial['Ans'])):
                    print('2')
                    correct=1
                    responses=trial['Image2']
                    core.wait(.05)
                    win.flip()
                    Pressed= True
                    img1.size=None
                    img2.size=None
                    img3.size=None
                    event.clearEvents()
                elif (img3.contains(mymouse) and (trial['Image3']==trial['Ans'])):
                    print('3')
                    correct=1
                    responses=trial['Image3']
                    core.wait(.05)
                    win.flip()
                    Pressed= True
                    img1.size=None
                    img2.size=None
                    img3.size=None
                    event.clearEvents()
                else:
                    if (img1.contains(mymouse)):
                        print('4')
                        responses=trial['Image1']
                        correct=0
                        core.wait(.05)
                        win.flip()
                        Pressed= True
                        img1.size=None
                        img2.size=None
                        img3.size=None
                        event.clearEvents()
                    elif (img2.contains(mymouse)):
                        print('5')
                        responses=trial['Image2']
                        correct=0
                        core.wait(.05)
                        win.flip()
                        Pressed= True
                        img1.size=None
                        img2.size=None
                        img3.size=None
                        event.clearEvents()
                    elif (img3.contains(mymouse)):
                        print('6')
                        responses=trial['Image3']
                        correct=0
                        core.wait(.05)
                        win.flip()
                        Pressed= True
                        img1.size=None
                        img2.size=None
                        img3.size=None
                        event.clearEvents()
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

    logging.log(level=logging.DATA, msg="*** END OMOT ****")

    trials.extraInfo['END']=globalClock.getTime()
    trials.saveAsWideText(fileName=logname, delim=',', appendFile=False)
    win.close()

def fullomoTask(subj_id, cond):

    #set values and parameters for tasks
    print('Set Vals for Task')
    log_file,logname,omot_trials=setdata(subj_id)

    #Instructions
    instruct_omot(subj_id)

    #OMOT Task
    do_omot(omot_trials,logname,subj_id)

print('Done setting up functions')

if __name__ == '__main__':
    fullomoTask()
    # if cond==1:
    #     fullNSTask()
    #     fullSocTask()
    # elif cond==2:
    #     fullSocTask()
    #     fullNSTask()

    core.quit()
