#!/usr/bin/env python2
# -*- coding: utf-8 -*-

####
# SETUP
#####
#Internet says that to run scripts from Terminal on new Macs, modules need to be imported in this order
from pandas import DataFrame, read_csv
from psychopy import core
from psychopy import gui
#from psychopy import data, event, logging, visual
## UNCOMMENT THIS LINE IF NEEDED ON NEWER COMPUTERS

# Import modules
import os
import random
import re
import urllib
import csv
import datetime
import sys

from psychopy import prefs
#prefs.general['audioLib'] = ['pyo']
prefs.general['audioLib'] = ['pygame']
prefs.general['shutdownKey'] = 'q'
from psychopy import sound

#add working directory to path if it's not already there
sys.path.append('.')

#####
# SUBJECT SETUP
#######

# get subjID
subjDlg = gui.Dlg(title="Net Learn Study")
subjDlg.addField('Enter Subject ID:')
subjDlg.addField('Enter Condition #:')
subjDlg.show()

if gui.OK:
    subj_id=subjDlg.data[0]
    cond=float(subjDlg.data[1])
    print('Subject ID is',subj_id)
    print('Condition is',cond)
else:
    sys.exit()


expdir = os.getcwd()
logdir = '{}/subjects/{}'.format(expdir,subj_id)

print logdir

#######
# SCREEN SETUP
#######

#import all config file preferences and python scripts
print('Importing Relevant Scripts')
from config import *
from setupStimuliandWalks import *
print('Done importing pretask stuff')
#from pretask import *

######
# RUN MAIN TASK
#####
print('Defining functions')
def fulltask():

    #set values and parameters for trials
    #print('Set Vals for Trials')
    #get_trials(subj_id)

    #instructions
    print('Instruction Screen for Task')
    show_instructions()
    print('done instructions')
    #Load data for practice Trials
    prac_trials=set_practicedata(subj_id)

    #Load the data for the walks (trials, etc.)
    log_file,logname,trials= set_walkdata(subj_id)

    #Run practice Trials
    do_runpractrials(subj_id,prac_trials,1)

    show_ready_screen()

    #Walk round 1
    do_runtrials(subj_id,trials,logname.replace('.csv','_run1.csv'),1)

    show_completion_screen()


if __name__ == '__main__':
    print('RUNNING TASK')

    if cond==1:
        fulltask()
        #NSTask_NoTrain()
        from seqcmpl.seqcmpl import *
        fullsqcmpltask(subj_id, cond)

        from OMOT.OMOT_master import *
        fullomoTask(subj_id, cond)
    elif cond==2:
        fulltask()

        from OMOT.OMOT_master import *
        fullomoTask(subj_id, cond)

        from seqcmpl.seqcmpl import *
        fullsqcmpltask(subj_id, cond)

#Option #1: Open existing CSV file and append new row
pID='{}'.format(subj_id)
condNum='cond{}'.format(cond)
endTime=str(datetime.datetime.now())
#write participant ID to existing conditions file
with open('subjects/conditions.csv', 'a') as f:
    writer = csv.DictWriter(f, fieldnames=('pID', 'condition', 'date'))
    new_data = {'pID': pID,
                'condition': condNum,
                'date': endTime }
    writer.writerow(new_data)


with open('subjData/conditions.csv', 'a') as f:
    writer = csv.DictWriter(f, fieldnames=('pID', 'condition', 'date'))
    new_data = {'pID': pID,
                'condition': condNum,
                'date': endTime }
    writer.writerow(new_data)
#fields=[pID,condNum,endTime]
#with open('experiment/conditions.csv', 'a') as f:
#    writer = csv.writer(f)
#    writer.writerow(fields)


core.quit()
