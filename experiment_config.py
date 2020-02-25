#!/usr/bin/env python
# -*- coding: utf-8 -*-

PRETEST_LOOPS = 1
PRACTICE_LOOPS = 1

EXPOSURE_STEPS = 150#change this to change number of trials

#UNIFORMITY OF THE DISTRIBUTION OF NODES SEEN
KS_CUTOFF= 0.135#how close does it have to be to a uniform distribution?
MIN_TRANS_EDGE=7 #what is the range for number of times cross the transition edge?
MAX_TRANS_EDGE=13

### OFFLINE TEST
OFFLINE_ACCURACY_BONUS = 1.0
OFFLINE_BONUS_THRESHOLD = 0.6

RATE_PER_MINUTE = 0.10  # dollars per minute
EXPOSURE_BONUS = 1.0
OFFLINE_BONUS = 1.0
TEST_BONUS = 0.0

MAX_BONUS = 10.0
