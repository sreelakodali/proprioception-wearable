# Data Analysis functions

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
import constants as CONST

def extractSubjectAttemptAngles(p, n):
	data = pd.read_csv(CONST.PATH_LAPTOP + 'SUBJECT' + str(n) + '/'+p + '/processed_' + p + '.csv', delimiter = ",").astype(float)
	time = data['time'].tolist()
	angle = data['flex sensor'].tolist()
	nTrial = data["'Trial Number'"].tolist()
	targets = data["'Target Angle'"].tolist()

	idx = [i for i in range(1,len(nTrial)) if nTrial[i]!=nTrial[i-1] ]
	#print(len(time))
	for i in list(range(0,len(targets) - 1)):
		if ((targets[i] == 0) and (targets[i+1] == 180)):
			x = [i]
			break

	idx1 = x + idx 
	idx2 = idx + [len(time)-1]

	nTrial_afterEachChange = [nTrial[i] for i in idx1]
	targets_afterEachChange = [targets[i] for i in idx1]
	angle_afterEachChange = [angle[i] for i in idx2]

	g = open(CONST.PATH_LAPTOP + 'SUBJECT' + str(n) + '/'+p + "/subjectAngleAttempts_" + p + ".csv", 'w+', encoding='UTF8', newline='')
	#g = open(p + "WELP_SubjectAttempts" + fileName, 'w+', encoding='UTF8', newline='')
	w = csv.writer(g)
	for a in angle_afterEachChange:
		w.writerow([a])
	g.close()
	print("Subject angle attempts extracted and saved.")
	return angle_afterEachChange

def generateSubjectAttemptsTargets(n):

	path = CONST.PATH_LAPTOP+"SUBJECT"+str(n)
	allSubDirs = [d for d in os.listdir(path) if os.path.isdir(os.path.join(path, d))]
	experimentDataDirs = [ d for d in allSubDirs if d.find('subject')==-1]
	print(experimentDataDirs)

	subjectAttempts = []
	targets = []
	idx = 0
	# go through all the subdirs without 'subject' and in order of when it was created.
	for d in experimentDataDirs:


		# if it doesn't have subjectAngleAttempts,extract and add to subject angle attempts list. add targets with same length
		fileName = [f for f in os.listdir(path+'/'+d) if (f.find('subjectAngleAttempts')!=-1)]
		#print(len(fileName))
		if(len(fileName) == 0):
			file = [f for f in os.listdir(path+'/'+d) if (f.find('processed')!=-1)]
			file = file[0]
			print(d)
			s = extractSubjectAttemptAngles(d, n)
			#print(len(s))
			subjectAttempts = subjectAttempts + s

			# add targets
				# read target file
			data1 = pd.read_csv(path+'/'+d + '/targetAngles_'+d +'.csv', delimiter = "\n", header=None).astype(float)
			t = [i[0] for i in data1.values.tolist()]
				# copy 0 to len(s) target angles into targets
			targets = targets + t[idx:idx+len(s)]
			idx = idx + len(s)

		else:
			# read in its subjectAngleAttempts and add it to the total
			data = pd.read_csv(path+'/'+d + '/subjectAngleAttempts_'+d +'.csv', delimiter = "\n", header=None).astype(float)
			s = [i[0] for i in data.values.tolist()]
			subjectAttempts = subjectAttempts + s

			data2 = pd.read_csv(path+'/'+d + '/targetAngles_'+d +'.csv', delimiter = "\n", header=None).astype(float)
			t = [i[0] for i in data2.values.tolist()]
			targets = targets + t[idx:idx+len(s)]

			break
			
	print(len(targets))
	print(len(subjectAttempts))

	if (len(subjectAttempts) == 110 and len(targets) == 110):
		print("we have all the data, let's proceed!")
		g = open(CONST.PATH_LAPTOP + 'SUBJECT' + str(n) + "/subjectAngleAttempts_" + 'SUBJECT' + str(n) + ".csv", 'w+', encoding='UTF8', newline='')
		w = csv.writer(g)
		for a in subjectAttempts:
			w.writerow([a])
		g.close()

		g = open(CONST.PATH_LAPTOP + 'SUBJECT' + str(n) + "/targetAngles_" + 'SUBJECT' + str(n) + ".csv", 'w+', encoding='UTF8', newline='')
		w = csv.writer(g)
		for a in targets:
			w.writerow([a])
		g.close()

		print("combined subject data generated")


	else:
		print("missing and/or extra data. data length =" + str(len(subjectAttempts)))
		# if attempt total == 110, have all the data. can proceed. otherwise: data missing error


def combineProcessRaw():


# def plotForceVsTime():


# def computeABSError():


# def computeError():


# def combineRaw():

