
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
# subjDlg = gui.Dlg(title="SeqCmpl Task")
# subjDlg.addField('Enter Subject ID:')
# subjDlg.addField('Enter Condition:')
# subjDlg.show()

# if gui.OK:
#     subj_id=subjDlg.data[0]
#     cond=float(subjDlg.data[1])
# else:
#     sys.exit() #commented out for linking all scripts together

#import custom scripts
##### IMPORT PYTHON SCRIPTS #######
print('Importing relevant scripts')
#from configseqcmpl import *
from setseqcmpl_stimuli import *
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
    logdir = '{}/subjData/{}/seqcmpl'.format(expdir,subj_id)

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
        logname = '{}/{}_log_seqcmpl{}.csv'.format(logdir, subj_id, lognum)
        ct += 1

    ######
    # set up trial handler
    sqcmpl_trialFile = 'subjData/{}/seqcmpl/seqcmpl1.csv'.format(subj_id)
    sqcmpl_trialList = [ item for item in csv.DictReader(open(sqcmpl_trialFile,'rU'))]
    sqcmpl_trials = data.TrialHandler(sqcmpl_trialList,nReps=1,method='sequential')


    #Add data types to trials
    sqcmpl_trials.data.addDataType('resp')
    sqcmpl_trials.data.addDataType('rt')
    sqcmpl_trials.data.addDataType('correct')

    # setup logging #
    log_file = logging.LogFile("subjData/%s/seqcmpl/%s_seqcmpl.log" % (subj_id, subj_id),  level=logging.DATA, filemode="w")

    return (log_file,logname,sqcmpl_trials)

print('Defining instruct_sqcmpl function')

def instruct_sqcmpl(subj_id):
    print('Starting instructions')
    mymouse.setPos((0,0))
    mymouse.getPos()
    # press1=False
    # press2=False
    # press3=False
    # while not press1 and not press2 and not press3:
    sqcmplInstructScreen1.draw()
    win.flip()
    event.waitKeys()
    # core.wait(4)
    # if mymouse.mouseMoved():
    #     press1 = True
    #     core.wait(.2)

print('Defining do_sqcmpl function')

def do_sqcmpl(trials,logname,subj_id):
    print('Starting Task')
    #log_file = logging.LogFile("logs/subj%s_NS.log" % (subj_id),  level=logging.DATA, filemode="w")

    # set clock
    globalClock = core.Clock()
    logging.setDefaultClock(globalClock)

    logging.log(level=logging.DATA, msg="** START sqcmpl**")
    trials.extraInfo={'START':globalClock.getTime()}
    trials.extraInfo={'participant':subj_id}
    tidx = 0

    for tidx, trial in enumerate(trials):
        print('In trial {} - image #1={}, image #2={}, image #3={} completeimage #1={} completeimage #2={}'.format(tidx+1,trial['seq1path'],trial['seq2path'],trial['seq3path'],trial['completepath1'],trial['completepath2']))

        logging.log(level=logging.DATA, msg='Trial {} - image #1={}, image #2={}, image #3={} completeimage #1={} completeimage #2={}'.format(tidx+1,trial['seq1path'],trial['seq2path'],trial['seq3path'],trial['completepath1'],trial['completepath2']))

        #Set values for trial
        img1.setImage(trial['seq1path'])
        img2.setImage(trial['seq2path'])
        img3.setImage(trial['seq3path'])
        img4.setImage(trial['seq4path'])
        img5.setImage(trial['completepath1'])
        img6.setImage(trial['completepath2'])
        # print(img1.size[1])
        # print(img1.size[0])
        #scale the images by half on each trial
        # img3.setSize(img3.size/2)
        # img2.setSize(img2.size/2)
        # img1.setSize(img1.size/2)

        correct=None
        responses=None
        key=None
        rt=None
        Pressed=False
        img1.pos=(-7,-2)
        img2.pos=(7,-2)
        img3.pos=(7,-2)
        img4.pos=(7,-2)
        question.pos=(7,-2)
        img1.size=12
        img2.size=12
        img3.size=12
        img4.size=12

        img1.draw()
        img2.draw()
        win.flip()
        core.wait(.5)
        timer1=core.CountdownTimer(trial_duration)
        while timer1.getTime() > 9.4:
            #win.flip()
            #core.wait(.25)#first have the left image zoom off
            img1.pos-=(.33,0)
            img1.draw()
            img2.draw()
            #core.wait(0.5)
            win.flip()
        while timer1.getTime() > 8.8 and timer1.getTime() < 9.4:
            img2.pos-=(.33,0)
            img2.draw()
            win.flip()
            img3.pos=(7,-2)
        while timer1.getTime() > 8.7 and timer1.getTime() < 8.8:
            #img2.pos=(-7,-4)
            img2.draw()
            img3.draw()
            win.flip()
            #first have the left image zoom off
        while timer1.getTime() > 8.2 and timer1.getTime() < 8.7:
            img2.pos-=(.33,0)
            img2.draw()
            img3.draw()
            #core.wait(0.5)
            win.flip()
            #core.wait(1)
        while timer1.getTime() > 7.6 and timer1.getTime() < 8.2:
            #win.flip()
            #core.wait(.25)#first have the left image zoom off
            img3.pos-=(.33,0)
            img3.draw()
            #img4.draw()
            #core.wait(0.5)
            win.flip()
        while timer1.getTime() > 7.5 and timer1.getTime() < 7.6:
            #win.flip()
            #core.wait(.25)#first have the left image zoom off
            img3.draw()
            img4.draw()
            #core.wait(0.5)
            win.flip()
        while timer1.getTime() > 7.0 and timer1.getTime() < 7.5:
            img3.pos-=(.33,0)
            #core.wait(.25)#first have the left image zoom off
            img3.draw()
            img4.draw()
            #core.wait(0.5)
            win.flip()
        while timer1.getTime() > 6.4 and timer1.getTime() < 7:
            img4.pos-=(.33,0)
            #core.wait(.5)#first have the left image zoom off
            #img3.draw()
            img4.draw()
            #core.wait(0.5)
            win.flip()
        while timer1.getTime() > 5 and timer1.getTime() < 6.4:
            img4.draw()
            question.draw()
            #core.wait(0.5)
            win.flip()
        # while timer1.getTime() > 4 and timer1.getTime() < 6:
        # img2.draw()
        # win.flip()
        # core.wait(0.5)
        # timer2=core.CountdownTimer(trial_duration)
        # while timer2.getTime() > 0:
        #     img2.draw()
        #     img2.pos-=(.25,0)
        #     win.flip()
        #
        # img3.draw()
        # win.flip()
        # core.wait(0.5)
        # timer3=core.CountdownTimer(trial_duration)
        # while timer3.getTime() > 0:
        #     img3.draw()
        #     img3.pos-=(.25,0)
        #     win.flip()
        #
        # img4.draw()
        # win.flip()
        # core.wait(0.5)
        # timer4=core.CountdownTimer(trial_duration)
        # while timer4.getTime() > 0:
        #     img4.draw()
        #     img4.pos-=(.25,0)
        #     win.flip()
        #
        # timer5=core.CountdownTimer(trial_duration)
        # while timer5.getTime() > 0:
        #     question.draw()
        #     win.flip()

        onset = globalClock.getTime()
        trials.addData('onset', onset)
        mymouse.setPos((0,15))
        mymouse.getPos()
        while not Pressed:
            #to get all stimuli to 'sit' on the same plane
            img1.size=8
            img2.size=8
            img3.size=8
            img4.size=8
            img1.pos=(-20,(4+(img1.size[1]/2)))
            img2.pos=(-10,(4+(img2.size[1]/2)))
            img3.pos=(0,(4+(img3.size[1]/2)))
            img4.pos=(10,(4+(img4.size[1]/2))) # FIX THIS POSITIONING
            question.pos=(20,7)

            img5.pos=(-7, -3)
            img6.pos= (7,-3)
            # img2.pos=(0,-1)
            # img3.pos=(10,-1)
            img1.draw()
            img2.draw()
            img3.draw()
            img4.draw()
            question.draw()
            img5.draw()
            img6.draw()
            resp_prompt1.draw()
            win.flip()

            key=event.getKeys(keyList=('escape'))
            #mouseclick=mymouse.getPressed()
            mouseclick1=mymouse.isPressedIn(img5)
            mouseclick2=mymouse.isPressedIn(img6)
            # mouseclick3=mymouse.isPressedIn(img3)
            #print(mouseclick2)
            #rt=globalClock.getTime()-onset
            mymouse.getPos()
            if img5.contains(mymouse) or img6.contains(mymouse):
                rt=globalClock.getTime()-onset
                if (img5.contains(mymouse) and trial['Within_Ans']==trial['CompletionImage1']):
                    correct=1
                    responses=trial['CompletionImage1']
                    core.wait(.1)
                    Pressed= True
                    #clear out all the sizes so they can be reset on each trial based on image size
                    event.clearEvents()
                elif (img6.contains(mymouse) and trial['Within_Ans']==trial['CompletionImage2']):
                    correct=1
                    responses=trial['CompletionImage2']
                    Pressed=True
                    core.wait(.1)
                    event.clearEvents()
                else:
                    if(img5.contains(mymouse)):
                        responses=trial['CompletionImage1']
                        correct=0
                        core.wait(.1)
                        Pressed= True
                        event.clearEvents()
                    elif(img6.contains(mymouse)):
                        responses=trial['CompletionImage2']
                        correct=0
                        core.wait(.1)
                        Pressed= True
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

    logging.log(level=logging.DATA, msg="*** END sqcmpl ****")

    trials.extraInfo['END']=globalClock.getTime()
    trials.saveAsWideText(fileName=logname, delim=',', appendFile=False)
    win.close()


print('Defining combined fullTask function')


def fullsqcmpltask(subj_id, cond): #changed for linking together

    #set values and parameters for tasks
    print('Set Vals for Task')
    log_file,logname,sqcmpl_trials=setdata(subj_id)

    #Instructions
    instruct_sqcmpl(subj_id)

    #sqcmpl Task
    do_sqcmpl(sqcmpl_trials,logname,subj_id)

print('Done setting up functions')

if __name__ == '__main__':
    fullsqcmpltask()
    # if cond==1:
    #     fullNSTask()
    #     fullSocTask()
    # elif cond==2:
    #     fullSocTask()
    #     fullNSTask()
    core.quit()
