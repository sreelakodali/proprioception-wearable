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


# subjectNumber = 1
# data = skD.sortProcessLearningTime(skD.extractLearningTimes(subjectNumber))
# print(data)
# print(data.shape)

subjects = [1, 3, 4, 5, 6, 7, 9, 10, 11, 12, 13, 14, 15, 16]
#subjects = [3, 4, 5, 6, 7, 9, 10, 11, 12, 13, 14, 15, 16]
totalData =  [[[0] * 5] * 10]* len(subjects)

for i in list(range(0, len(subjects))):
	totalData[i] = skD.sortProcessLearningTime(skD.extractLearningTimes(subjects[i]))
# 	#skD.generateForce(i+1)
# 	#skD.passiveHapticSection(i+1)

totalData = np.array(totalData)
print(totalData.shape)
std = np.std(totalData,axis=(0, 1))
std = std/np.sqrt(140)
print(std.shape)
print(std)
avgTotalData = np.average(totalData,axis=0)
print(avgTotalData.shape)
print(avgTotalData)

# f = open(CONST.PATH_LAPTOP + 'averageLearningTime_ALL_S1-16_n2_n8_reshaped.csv','w+', encoding='UTF8', newline='')
# writer = csv.writer(f)
# writer.writerows(avgTotalData)
# f.close()

# skD.generateSubjectAttemptsTargets(subjectNumber)
# skD.combineProcess(subjectNumber)
# skD.combineRaw(subjectNumber)