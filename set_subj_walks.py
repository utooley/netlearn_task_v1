#!/usr/bin/env python
# -*- coding: utf-8 -*-

# this file imports custom routes into the experiment server
# Import PsychoPy
import psychopy
import pandas as pd#have this first to avoid a lookup error
from psychopy import gui #may need to change this

encoding = 'utf-8'
# Import other packages
import sys
sys.path.append('.')

import os
import csv
import random
import re
from random import shuffle
import math
import networkx as nx
from scipy import stats

from json import dumps, loads
import numpy as np

#Export experiment parameters from experiment_config file
from experiment_config import *
psychopy.prefs.general['shutdownKey'] = 'q'

random.seed()

# get subjID
subjDlg = gui.Dlg(title="Get Walk and Graph for Image Viewing Task")
subjDlg.addField('Enter Subject ID:')
subjDlg.addField('Enter 0 here unless you are Abby testing adults:')
subjDlg.show()

if gui.OK:
    subj_id=subjDlg.data[0]
    adulttest=float(subjDlg.data[1])
else:
    sys.exit()

####################################
# Pre-experiment functions
####################################
# Randomize order of faces
def shuffle_images():

    print "Shuffling images"
    image_names = ['Monster-1.png','Monster-2.png','Monster-3.png','Monster-4.png',
    'Monster-5.png','Monster-6.png','Monster-7.png','Monster-8.png','Monster-9.png','Monster-10.png']

    """
    Generate a list of images for a given subject
    """
    order = range(len(image_names)) #order starts at 0, goes up to # of images - 1
    shuffle(order)
    # Take image IDs and make a list of file names
    images = [image_names[im] for im in order]
    #images.extend(images_counter1)
    # Add directory name on
    images = ["stimuli/%s" % (im) for im in images]

    """
    Map sounds to images for a given subject
    """
    print "Shuffling sounds"
    sound_names=['Monster-Sounds-1.wav','Monster-Sounds-2.wav','Monster-Sounds-3.wav','Monster-Sounds-4.flac',
    'Monster-Sounds-5.wav','Monster-Sounds-6.wav', 'Monster-Sounds-7.wav', 'Monster-Sounds-9.wav','Monster-Sounds-11.wav', 'Monster-Sounds-12.aiff', 'Monster-Sounds-13.wav','Monster-Sounds-14.wav']
    order = range(len(sound_names)) #order starts at 0, goes up to # of images - 1
    shuffle(order)
    # Take image IDs and make a list of file names
    sounds = [sound_names[sou] for sou in order]
    #images.extend(images_counter1)
    # Add directory name on
    sounds = ["sounds/%s" % (sou) for sou in sounds]
    sounds=sounds[0:len(images)]
    """
    Map movements to images for a given subject
    """
    print "Shuffling movements "
    movement_strings_right=['imgR.ori = 15*(np.sin(6*(globalClock.getTime()-onset)));imgR.pos = [7, -4+np.sin(5*(globalClock.getTime()-onset))]',
    'imgR.pos = [7, -4+np.sin((globalClock.getTime()-onset))/2]',
    'imgR.pos=[7+np.sin((globalClock.getTime()-onset)),-4+np.sin((globalClock.getTime()-onset))*3]',
    'imgR.ori = 10*(np.sin(10*(globalClock.getTime()-onset)))',
    'imgR.ori = 25*(np.sin(4*(globalClock.getTime()-onset)))',
    'imgR.ori = 15*(np.sin(6*(globalClock.getTime()-onset)))',
    'imgR.pos = [7, -4+np.sin(3*(globalClock.getTime()-onset))*2]',
    'imgR.pos = [7, -4+np.sin(5*(globalClock.getTime()-onset))]',
    'imgR.pos = [7, -4+np.sin(3*(globalClock.getTime()-onset))/3]',
    'imgR.pos = [7, -4+np.sin((globalClock.getTime()-onset))*3]',
    'imgR.pos = [7+np.sin((globalClock.getTime()-onset)), -4+np.sin(3*(globalClock.getTime()-onset))*2]',
    'imgR.pos = [7+np.sin(5*(globalClock.getTime()-onset)), -4+np.sin(5*(globalClock.getTime()-onset))]',
    'imgR.pos = [7+np.sin(3*(globalClock.getTime()-onset)), -4+np.sin(3*(globalClock.getTime()-onset))/3]',
    'imgR.pos = [7+np.sin((globalClock.getTime()-onset)), -4+np.sin((globalClock.getTime()-onset))*3]',
    'imgR.pos = [7-np.sin((globalClock.getTime()-onset)), -4]',
    'imgR.pos = [7-np.sin(4*(globalClock.getTime()-onset)), -4]',
    'imgR.pos = [7-np.sin(3*(globalClock.getTime()-onset)), -4]',
    'imgR.pos = [7-np.sin(2*(globalClock.getTime()-onset)),-4]']
    order = range(len(movement_strings_right)) #order starts at 0, goes up to # of images - 1
    shuffle(order)
    # Take image IDs and make a list of file names
    movements_right = [movement_strings_right[sou] for sou in order]
    #Assign only as many movements as there are aliens
    movements_right=movements_right[0:len(images)]

    print "Duplicating movements for left image"
    movements_left=[w.replace('imgR.', 'imgL.') for w in movements_right]
    #replace all position arguments with negatives for the L side
    movements_left=[w.replace('[7,','[-7,').replace('[7-np.', '[-7-np.').replace('[7+np.', '[-7+np.') for w in movements_left]
    return images,sounds,movements_left, movements_right

#Save the randomized image to node mapping
def save_image_mapping(images,sounds, movements_left, movements_right):

    # create numpy array to store exposure data
    image_mapping = np.c_[range(len(images)),images,sounds, movements_left, movements_right]

    # create file name
    file_name="subjData/%s/image_mapping.csv" % subj_id

    # create header to store info about columns
    data_headers = 'image_nums,image_filenames,sounds, movements_left, movements_right'

    np.savetxt(file_name,image_mapping,delimiter=",",fmt="%21s",header=data_headers,comments="")

def add_path_to_walk(W,m,s,movements_left, movements_right):
    print "Adding paths to walk"
    print "Walk length= {}".format(len(W))
    print "Image list length= {}".format(len(m))
    #print "Altered list length= {}".format(len(a))
    walk = W #random walk
    imgs = m #ordered list of images
    sounds=s
    #altered = a #random altered T/F list
    node1=[]
    node2=[]
    path = []
    path2=[]
    sound1=[]
    sound2=[]
    movement1=[]
    movement2=[]
    for i in range(len(walk)-1):
        node=walk[i]
        nextnode=walk[i+1]
        node1.append(node)
        node2.append(nextnode)
        #print "Node for trial #:{} is {}".format(i,node)
        #if altered[i]:
        #    p = imgs[node+10]
        #else:
        p = imgs[node]
        p2=imgs[nextnode]
        s1=sounds[node]
        s2=sounds[nextnode]
        path.append(p)
        path2.append(p2)
        sound1.append(s1)
        sound2.append(s2)
        m1=movements_left[node]
        m2=movements_right[nextnode]
        movement1.append(m1)
        movement2.append(m2)
        #print "Path for trial #:{}, node #:{} is: {}".format(i,node,p)
    return node1,node2, path, path2, sound1, sound2, movement1, movement2


# def add_paths_to_train(t,m):
#     print "Adding paths to walk"
#     print "Walk length= {}".format(len(t))
#     print "Image list length= {}".format(len(m))
#     print "Altered list length= {}".format(len(s))
#     trials = t #trial order
#     imgs = m #ordered list of images
#     #side = s #random side of rotated image
#     pathL = []
#     pathR = []
#     #print len(imgs)
#     for i,node in enumerate(trials):
#         #print "Node for trial #:{} is {}".format(i,node)
#         if side[i]==0:
#             l = imgs[node+10]
#             r = imgs[node]
#         else:
#             r = imgs[node+10]
#             l = imgs[node]
#         pathL.append(l)
#         pathR.append(r)
#         #print "Path for trial #:{}, node #:{} is: {}".format(i,node,p)
#     return pathL, pathR

def random_walk(G, n):
    node = random.choice(G.nodes())
    walk = [node]
    for i in range(n - 1):
        node = random.choice(G[node].keys())
        walk.append(node)
    return walk

def shorten_walk_by_last_element(walk):
    walk.pop()
    return walk

def load_omot_questions():

    conservative=[[0,1,9,9],[3,4,8,8],[7,6,2,2]];
    non_conservative=[[0,4,9,9],[1,3,5,5],[8,5,1,1]];
    catch=[[5,7,8,5],[0,2,4,4]]; ## TOOK OUT CATCH TRIALS

    #df = pd.DataFrame(conservative+non_conservative+catch)
    df = pd.DataFrame(conservative+non_conservative+catch)
    df.columns=['Image1', 'Image2', 'Image3', 'Ans']
    #add trial types
    df['trial_type']=(['conservative'] * 3 + ['non_conservative']* 3 + ['catch']*2)
    new_elements1=df[['Image2','Image1', 'Image3', 'Ans','trial_type']] #create 6 different permutations of the OMOT orders
    new_elements2=df[['Image2','Image3','Image1', 'Ans', 'trial_type']]
    new_elements3=df[['Image3','Image1', 'Image2', 'Ans', 'trial_type']]
    new_elements4=df[['Image3','Image2', 'Image1', 'Ans', 'trial_type']]
    new_elements5=df[['Image1','Image3', 'Image2', 'Ans', 'trial_type']]
    new_elements1.columns=['Image1', 'Image2', 'Image3', 'Ans', 'trial_type'] #rearrange columns to duplicate trial types in other ordere
    new_elements2.columns=['Image1', 'Image2', 'Image3', 'Ans', 'trial_type']
    new_elements3.columns=['Image1', 'Image2', 'Image3', 'Ans', 'trial_type']
    #new_elements4.columns=['Image1', 'Image2', 'Image3', 'Ans', 'trial_type']
    #new_elements5.columns=['Image1', 'Image2', 'Image3', 'Ans', 'trial_type']
    df=df.append([new_elements1,new_elements2], ignore_index=True)#add to original
    #shuffle them
    q_order = range(len(df))
    shuffle(q_order)
    node_seq_df = df.loc[q_order].reset_index(drop=True)
    return(node_seq_df)

#these are adding file paths!
def add_paths_to_omot(df,map):
    print "Adding paths to OMOT"
    print "OMOT length= {}".format(len(df))
    print "Image list length= {}".format(len(map))
    trials = df #image tuples
    imgs = map #ordered list of images
    path1 = []
    path2 = []
    path3 = []
    #print len(imgs)
    for i in range(len(trials)):
        i1=trials['Image1'][i]
        i2=trials['Image2'][i]
        i3=trials['Image3'][i]
        p1=imgs[i1]
        p2=imgs[i2]
        p3=imgs[i3]
        path1.append(p1)
        path2.append(p2)
        path3.append(p3)
        #print "Path for trial #:{}, image #1 is: {}".format(i,p1)
        #print "Path for trial #:{}, image #2 is: {}".format(i,p2)
        #print "Path for trial #:{}, image #3 is: {}".format(i,p3)
    df['path1']=path1
    df['path2']=path2
    df['path3']=path3
    return df

def load_seq_completion_questions():
    #node_sequences = [[0,1,2],[2,3,4],[5,6,7],[4,5,7]];


    # reversed = [[0,1,2],[2,1,0],[2,1,6],[2,6,1],[6,1,2],[6,2,1], \
    #                [2,3,7],[2,7,3],[3,2,7],[3,7,2],[7,2,3],[7,3,2], \
    #                [1,3,5],[1,5,3],[3,1,5],[3,5,1],[5,1,3],[5,3,1], \
    #                [0,6,7],[0,7,6],[6,0,7],[6,7,0],[7,0,6],[7,6,0], \
    #                [1,7,8],[1,8,7],[7,1,8],[7,8,1],[8,1,7],[8,7,1], \
    #                [3,6,8],[3,8,6],[6,3,8],[6,8,3],[8,3,6],[8,6,3]];
    # #This defines which of the 2 images completing the sequence is correct. Choose randomly the
    #images in complete1 and complete2 that are incorrect
    if adulttest ==0:
        x = """{
          "SequenceImage1":[0,2,7,8,2,0,8,7,0,0,8,8,2,2,7,7],
          "SequenceImage2":[2,0,8,7,0,2,7,8,3,3,6,6,1,1,9,9],
          "SequenceImage3":[1,1,9,6,3,3,9,6,4,4,5,5,4,4,5,5],
          "SequenceImage4":[4,4,5,5,4,4,5,5,5,5,4,4,5,5,4,4],
          "CompletionImage1":[3,5,6,4,1,5,6,4,6,2,1,3,6,9,6,8],
          "CompletionImage2":[5,3,4,9,5,1,4,9,1,9,9,7,3,0,3,1],
          "Within_Ans":[3,3,6,9,1,3,6,9,1,2,9,7,3,0,6,8]

        }"""
        df = pd.DataFrame(loads(x))
        df['trial_type']=(['transition'] * 8 + ['impossible_close', 'impossible_far'] *4)
    elif adulttest==1:
        x = """{
          "SequenceImage1":[0,2,7,8,2,0,8,7,0,0,8,8,2,2,7,7,0,0,8,8],
          "SequenceImage2":[2,0,8,7,0,2,7,8,3,3,6,6,1,1,9,9,3,3,6,6],
          "SequenceImage3":[1,1,9,6,3,3,9,6,4,4,5,5,4,4,5,5,4,4,5,5],
          "SequenceImage4":[4,4,5,5,4,4,5,5,5,5,4,4,5,5,4,4,5,5,4,4],
          "CompletionImage1":[3,5,6,4,1,5,6,4,6,2,1,3,6,9,6,8,1,8,0,9],
          "CompletionImage2":[5,3,4,9,5,1,4,9,1,9,9,7,3,0,3,1,8,1,9,0],
          "Within_Ans":[3,3,6,9,1,3,6,9,1,2,9,7,3,0,6,8,1,1,9,9]

        }"""
        df = pd.DataFrame(loads(x))
        df['trial_type']=(['transition'] * 8 + ['impossible_close', 'impossible_far'] *4+['impossible_2edgeseach'] *4)
    q_order = range(len(df))
    shuffle(q_order)
    node_seq_df = df.loc[q_order].reset_index(drop=True)

    return node_seq_df

def load_seq_completion_paths(node_seq_df,map):
    print "Adding paths to sequence completion"
    print "Sequence completion task length= {}".format(len(node_seq_df))
    print "Image list length= {}".format(len(map))
    trials = node_seq_df #image tuples
    imgs = map #ordered list of images
    seq1path = []
    seq2path = []
    seq3path = []
    seq4path = []
    completepath1 = []
    completepath2 = []
    #print len(imgs)
    for i in range(len(trials)):
        i1=trials['SequenceImage1'][i]
        i2=trials['SequenceImage2'][i]
        i3=trials['SequenceImage3'][i]
        i4=trials['SequenceImage4'][i]
        i5=trials['CompletionImage1'][i]
        i6=trials['CompletionImage2'][i]
        p1=imgs[i1]
        p2=imgs[i2]
        p3=imgs[i3]
        p4=imgs[i4]
        p5=imgs[i5]
        p6=imgs[i6]
        seq1path.append(p1)
        seq2path.append(p2)
        seq3path.append(p3)
        seq4path.append(p4)
        completepath1.append(p5)
        completepath2.append(p6)
        #print "Path for trial #:{}, image #1 is: {}".format(i,p1)
        #print "Path for trial #:{}, image #2 is: {}".format(i,p2)
        #print "Path for trial #:{}, image #3 is: {}".format(i,p3)
    node_seq_df['seq1path']=seq1path
    node_seq_df['seq2path']=seq2path
    node_seq_df['seq3path']=seq3path
    node_seq_df['seq4path']=seq4path
    node_seq_df['completepath1']=completepath1
    node_seq_df['completepath2']=completepath2
    return node_seq_df

def load_dyadic_choice_trials():
    friends_within=[[0,2],[4,3],[6,5],[8,7]];
    friends_between=[[4,5]];
    non_friends_within=[[9,6],[7,5],[1,3],[2,4]];
    non_friends_between_dist2=[[4,9],[1,5]];
    non_friends_between_dist4=[[8,3],[0,7]];

    df = pd.DataFrame(friends_within+friends_between+non_friends_within+non_friends_between_dist2+non_friends_between_dist4,
    columns=['element1', 'element2'])
    #add trial types
    df['trial_type']=(['friends_within'] * 4 + ['friends_between']+ ['non_friends_within'] * 4+
    ['non_friends_between_dist2']*2+ ['non_friends_between_dist4']*2)
    new_elements=df[['element2','element1', 'trial_type']] #copy the df
    new_elements.columns=['element1', 'element2','trial_type'] #rearrange columns to duplicate trial types in other ordere
    df=df.append(new_elements, ignore_index=True)#add to original
    #shuffle them
    q_order = range(len(df))
    shuffle(q_order)
    node_seq_df = df.loc[q_order].reset_index(drop=True)
    return(node_seq_df)

def load_dyadic_choice_paths(node_seq_df,map):
    print "Adding paths to dyadic choice"
    print "Dyadic Choice task length= {}".format(len(node_seq_df))
    print "Image list length= {}".format(len(map))
    trials = node_seq_df #image tuples
    imgs = map #ordered list of images
    dyadic1path = []
    dyadic2path = []
    #print len(imgs)
    for i in range(len(trials)):
        i1=trials['element1'][i]
        i2=trials['element2'][i]
        p1=imgs[i1]
        p2=imgs[i2]
        dyadic1path.append(p1)
        dyadic2path.append(p2)
        #print "Path for trial #:{}, image #1 is: {}".format(i,p1)
        #print "Path for trial #:{}, image #2 is: {}".format(i,p2)
        #print "Path for trial #:{}, image #3 is: {}".format(i,p3)
    node_seq_df['dyadic1path']=dyadic1path
    node_seq_df['dyadic2path']=dyadic2path
    return node_seq_df

# Ignore this code for now since we're not manipulating network type
#cond = get_cond(uniqueId)
#cond = 0 #set cond to 0 since we're only interested in using the random walk for this first test
#if cond == 0:  # Random
#    kind = 'random'
#elif cond == 1:  # schapiro
#    kind = 'lattice'
#elif cond == 2:  # Lattice
#    kind = 'schapiro'
#else:
#    raise ValueError('Incorrect condition')

# for now, set 'kind' to schapiro network for all subjs

kind = 'schapiro'

# check for subj directory and create if not present
if not os.path.exists(os.path.join('subjData/%s/' % subj_id)):
    print "creating subject directory"
    directory="subjData/%s/" % subj_id
    os.makedirs(directory)

#check for OMOT directory and create if not present
if not os.path.exists(os.path.join('subjData/%s/OMOT' % subj_id)):
    directory="subjData/%s/OMOT" % subj_id
    os.makedirs(directory)

#check for Seq Cmpl directory and create if not present
if not os.path.exists(os.path.join('subjData/%s/seqcmpl' % subj_id)):
    directory="subjData/%s/seqcmpl" % subj_id
    os.makedirs(directory)

if not os.path.exists(os.path.join('subjData/%s/dyad_choice' % subj_id)):
    directory="subjData/%s/dyad_choice" % subj_id
    os.makedirs(directory)

print "CREATING IMAGE MAPPING"

# get shuffled images
images,sounds,movements_left, movements_right=shuffle_images()

# save CSV file with shuffle image order
save_image_mapping(images,sounds, movements_left, movements_right)

# # 10 non-social unrotated images
# orig1 = images[0:10]
#
# # 10 social unrotated images
# orig2 = images[10:20]
#
# # 10 non-social rotated images
# rotated1 = images[20:30]
#
# # 15 social rotated images
# rotated2 = images[30:40]
#
# images1=orig1+rotated1
# images2=orig2+rotated2

print "CREATING EXPOSURE RANDOM WALKS"

# get network structure
_graph_list = {
    0: [1, 2, 3],
    1: [0, 2, 4],
    2: [1, 3, 0],
    3: [0, 2, 4],
    4: [1, 3, 5],
    5: [4, 6, 9],
    6: [5, 7, 8],
    7: [6, 8, 9],
    8: [6, 7, 9],
    9: [7, 8, 5]}

schapiro = nx.from_dict_of_lists(_graph_list)

#Create random walk
G=schapiro
if (subj_id == 'test' or subj_id == 'Test' or subj_id=='TEST'):
    EXPOSURE_STEPS=8
    walk1=random_walk(G, EXPOSURE_STEPS)

walk1=random_walk(G, EXPOSURE_STEPS)

#############################
## WALK CONDITIONS 2.18.19 ##
#############################

# #Define a function to count the number of times the transition edge is crossed
def seq_count(data, pattern):
    count = 0
    for i in range(len(data)-len(pattern)+1):
        tmp = data[i:(i+len(pattern))]

        if tmp == pattern:
            count +=1

    return count
trans_cross=seq_count(walk1,[4,5])+seq_count(walk1,[5,4])
# #look at the node distribution, is it uniform?
ks_stat=stats.kstest(walk1, stats.uniform(loc=0.0, scale=9.0).cdf)[0]#this is the KS-test statistic, not the p-value
# #commented out sections allow me to look at the plot distributions in real time
# #import matplotlib.pyplot as plt
# #i=0
# #see if all conditions are met
if not (subj_id == 'test' or subj_id == 'Test' or subj_id=='TEST'):
    while ks_stat > KS_CUTOFF or trans_cross < MIN_TRANS_EDGE or trans_cross > MAX_TRANS_EDGE:
        print 'Walk conditions not satisfied'
        #i+=1
        #plt.subplot(6, 6, i)
        #plt.hist(walk1)
        walk1=random_walk(G, EXPOSURE_STEPS)
        trans_cross=seq_count(walk1,[4,5])+seq_count(walk1,[5,4])
        ks_stat=stats.kstest(walk1, stats.uniform(loc=0.0, scale=9.0).cdf)[0]
        continue
    print "We found a uniform walk with KS < {} and # of transitions between {} and {}".format(KS_CUTOFF, MIN_TRANS_EDGE, MAX_TRANS_EDGE)
# #plt.show()
#print "We found a uniform walk with KS < {} and # of transitions between {} and {}".format(KS_CUTOFF, MIN_TRANS_EDGE, MAX_TRANS_EDGE)
# #plt.hist(walk1)
# #HOW TO PLOT THE UNIFORM DISTRIBUTION
# d=stats.uniform(loc=0.0, scale=9.0)
# rv=d.rvs(150)
# pd.Series(rv).hist()

#Add paths to random walk
node1,node2,path1,path2,sound1,sound2,movement1,movement2 = add_path_to_walk(walk1,images,sounds, movements_left, movements_right)
#path2 = add_path_to_walk(walk2,images)

#pop the last node off the walk, to account for not having a last element to pair
walk1=shorten_walk_by_last_element(walk1)

# create file name
file_name1="subjData/%s/exposure_walk1.csv" % subj_id
#file_name2="subjData/subj%s/exposure_walk2.csv" % subj_id

# create numpy array to store exposure data
data1 = np.c_[range(len(walk1)),walk1,node1,node2,path1,path2,sound1,sound2, movement1, movement2]
#data2 = np.c_[range(len(walk1)),walk2,path2]

if not subj_id=='test':
    # create header to store info about columns
    data_headers1 = 'trialNum,walk,path1,path2,sound1,sound2, movement1, movement2,trans_cross,ks_stat'
    data_headers2 = 'trialNum,walk,path1,path2,sound1,sound2, movement1, movement2,trans_cross,ks_stat'

    #np.savetxt(file_name1,data1,delimiter=",",fmt="%2.1d",header=data_headers1,comments="")
    #np.savetxt(file_name2,data2,delimiter=",",fmt="%2.1d",header=data_headers2,comments="")

    with open(file_name1, 'w') as outfile:
        writer = csv.writer(outfile)
        outfile.write('pID,trialNum,walk,node1,node2,path1,path2,sound1,sound2,movement1,movement2,trans_cross,ks_stat\n')
        for row in zip(([subj_id]*len(walk1)),range(len(walk1)),walk1,node1,node2,path1,path2,sound1,sound2,movement1,movement2,([trans_cross]*len(walk1)),([ks_stat]*len(walk1))):
            writer.writerow(row)
else:
    # create header to store info about columns
    data_headers1 = 'trialNum,walk,path1,path2,sound1,sound2, movement1, movement2'
    data_headers2 = 'trialNum,walk,path1,path2,sound1,sound2, movement1, movement2'

    #np.savetxt(file_name1,data1,delimiter=",",fmt="%2.1d",header=data_headers1,comments="")
    #np.savetxt(file_name2,data2,delimiter=",",fmt="%2.1d",header=data_headers2,comments="")

    with open(file_name1, 'w') as outfile:
        writer = csv.writer(outfile)
        outfile.write('pID,trialNum,walk,node1,node2,path1,path2,sound1,sound2,movement1,movement2\n')
        for row in zip(([subj_id]*len(walk1)),range(len(walk1)),walk1,node1,node2,path1,path2,sound1,sound2,movement1,movement2):
            writer.writerow(row)
#
# with open(file_name2, 'w') as outfile:
#     writer = csv.writer(outfile)
#     outfile.write('pID,trialNum,walk,path\n')
#     for row in zip(([subj_id]*len(walk2)),range(len(walk2)),walk2,nextnode2,path2):
#         writer.writerow(row)


####################################
# Post-scan Odd-Man-Out Test (OMOT)
####################################

print "POST-SCAN ODD-MAN-OUT TEST"
print "Randomizing OMOT trials"
#Create randomized list of image triplets for omot
df1=load_omot_questions()
#df2=load_omot_questions()

print "Adding paths to OMOT trials"
#Add paths to omot trials
df1=add_paths_to_omot(df1,images)
#df2=add_paths_to_omot(df2,images2)

print "Saving OMOT as CSV"
# create file name
omotFile1="subjData/{}/OMOT/omot1.csv".format(subj_id)
#omotFile2="OMOT/subjData/subj{}/omot2.csv".format(subj_id)

#Save omot df to csv file
df1.to_csv(omotFile1, sep=',', encoding='utf-8')
#df2.to_csv(omotFile2, sep=',', encoding='utf-8')

####################################
# Post-scan Sequence-Completion Task
####################################

print "POST-SCAN Sequence Completion Task"
print "Randomizing sequence completion trials"
#Create randomized list of image triplets for omot
df1=load_seq_completion_questions()
#df2=load_omot_questions()

print "Adding paths to sequence completion trials"
#Add paths to omot trials
df1=load_seq_completion_paths(df1,images)
#df2=add_paths_to_omot(df2,images2)

print "Saving sequence completion as CSV"
# create file name
seqcmplFile1="subjData/{}/seqcmpl/seqcmpl1.csv".format(subj_id)
#omotFile2="OMOT/subjData/subj{}/omot2.csv".format(subj_id)

#Save omot df to csv file
df1.to_csv(seqcmplFile1, sep=',', encoding='utf-8')
#df2.to_csv(omotFile2, sep=',', encoding='utf-8')


####################################
# Dyadic choice task
####################################

print "POST-SCAN Dyadic choice task"
print "Randomizing dyadic choice trials"
#Create randomized list of image triplets for omot
df1=load_dyadic_choice_trials()
#df2=load_omot_questions()

print "Adding paths to dyadic choice trials"
#Add paths to omot trials
df1=load_dyadic_choice_paths(df1,images)
#df2=add_paths_to_omot(df2,images2)

print "Saving dyadic choice as CSV"
# create file name
dyadchoiceFile1="subjData/{}/dyad_choice/dyad_choice1.csv".format(subj_id)
#omotFile2="OMOT/subjData/subj{}/omot2.csv".format(subj_id)

#Save omot df to csv file
df1.to_csv(dyadchoiceFile1, sep=',', encoding='utf-8')
#df2.to_csv(omotFile2, sep=',', encoding='utf-8')
