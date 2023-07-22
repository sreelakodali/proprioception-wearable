#analyze pilot results V5
# extracts learning data. for each subject, creates matrix with the dimensions N x M, where N is # of target angles and M is 
# learning stages = 6. 2 in target practice w visual feedback, 4 more with no visual feedback (in order, pseudorandom, randomx2)

import csv
import os
import datetime
import sys, getopt
import shutil
import numpy as np
import pandas as pd
from scipy import signal # import lfilter, lfilter_zi, filtfilt, butter
# from scipy.signal import lfilter, lfilter_zi, filtfilt, butter
from operator import itemgetter
import skFunctions as sk
import skDataAnalysisFunctions as skD
import constants as CONST

# ##Give input file
# opts, args = getopt.getopt(sys.argv[1:],"i:",["ifile="])
# for opt, arg in opts:
# 	if opt in ("-i", "--ifile"):
# 		p = arg
# print(p)


#hapticsConditionsTest = [0, 1, 0, 0, 1]
subjects = [1, 3, 4, 5, 6, 7, 9, 10, 11, 12, 13, 14, 15, 16]
subjects = [1, 3, 4, 5, 6, 7, 9, 10, 11, 12, 13, 14, 15, 16]
hapticsConditionsTest = [1, 1, 1, 0, 1, 0, 0, 1, 0, 0, 1, 1, 0, 0]

# print(len(hapticsConditionsTest))
# print(len(subjects))


targetAngles = list(range(45,195,15))
totalData =  [[[0] * 6] * len(targetAngles)]* len(subjects)

# print(totalData)
# print(totalData[0])

for i in list(range(0, len(subjects))):
	data=  [[0] * 6] * len(targetAngles)
	p = "SUBJECT" + str(subjects[i]) + '/'
	print(p)
	for f in os.listdir(CONST.PATH_LAPTOP + p):
		if f.startswith('subject') and f.endswith('.csv'):
			data0 = pd.read_csv(CONST.PATH_LAPTOP + p + f, delimiter = "\n", header=None).astype(float)
			subjectAttempt = [i[0] for i in data0.values.tolist()]
			#print(subjectAttempt)
		elif f.startswith('targetAngles') and f.endswith('.csv'):
			data1 = pd.read_csv(CONST.PATH_LAPTOP + p + f, delimiter = "\n", header=None).astype(float)
			target = [i[0] for i in data1.values.tolist()]
			#print(target)

	# practice = list(range(30,70)) # haptics, no visual
	# error = [target[j] - subjectAttempt[j] for j in practice]
	# errorABS = [abs(target[j] - subjectAttempt[j]) for j in practice]

	subjectAttempt_prax = subjectAttempt[0:20] + subjectAttempt[30:70]
	target_prax = target[0:20] + target[30:70]
	# print(subjectAttempt_prax)
	# print(target_prax)

	for k in list(range(len(targetAngles))):
		# find the index
		#print("target angle: " + str(k))

		if (subjects[i] == 1):
			idx = [idx1 for idx1 in range(len(target_prax)) if ((target_prax[idx1] == targetAngles[k]) or ((target_prax[idx1] == targetAngles[k]-5)) ) ]
		else:
			idx = [idx1 for idx1 in range(len(target_prax)) if (target_prax[idx1] == targetAngles[k] ) ]
		errorABS = [abs(target_prax[j] - subjectAttempt_prax[j]) for j in idx]
		errorABS = [targetAngles[k]] + errorABS
		#print(targetAngles[k])
		#print(idx)
		
		# print(data[0])
		data[k] = errorABS

		print(errorABS)

	#print(data)

	totalData[i] = data
	# f = open(CONST.PATH_LAPTOP + p + 'learning_SUBJECT' + str(subjects[i]) + '.csv','w+', encoding='UTF8', newline='')
	# writer = csv.writer(f)
	# writer.writerows(data)
	# f.close()

	#print(totalData)

# averaging across total data
totalData = np.array(totalData)
print(totalData.shape)
std = np.std(totalData,axis=(0, 1))
std = std/np.sqrt(140)
print(std.shape)
print(std)
avgTotalData = np.average(totalData,axis=0)
print(avgTotalData.shape)
print(avgTotalData)

# f = open(CONST.PATH_LAPTOP + 'averageLearning_ALL_S1-16_n2_n8.csv','w+', encoding='UTF8', newline='')
# writer = csv.writer(f)
# writer.writerows(avgTotalData)
# f.close()
