import csv
import os
import datetime
import sys, getopt
import shutil
import numpy as np
import pandas as pd
from operator import itemgetter
import skFunctions as sk
import skDataAnalysisFunctions as skD
import constants as CONST


# subjectNumber = 4
# path = CONST.PATH_LAPTOP+"/SUBJECT"+str(subjectNumber)
# allSubDirs = [CONST.PATH_LAPTOP+d for d in os.listdir(path) if os.path.isdir(os.path.join(path, d))]
# experimentDataDirs = [ d for d in allSubDirs if d.find('subject')==-1]

# for d in experimentDataDirs:

# # go through all the subdirs without 'subject' and in order of when it was created.
# # if it doesn't have subjectAngleAttempts,extract and add to attempt total. and add to subject angle attempts list. add targets with same length
# # if it does have, add length of its attempts file to attempt total
# # if attempt total == 110, have all the data. can proceed. otherwise: data missing error

# print(experimentDataDirs)
# print(skD.extractSubjectAttemptAngles('2023-02-02_15-52', 4))

skD.generateSubjectAttemptsTargets(4)