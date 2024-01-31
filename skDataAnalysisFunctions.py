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
import matplotlib
matplotlib.use("TkAgg")
from matplotlib import pyplot as plt
import constants as CONST



def extractLearningTimes(n):
	path = CONST.PATH_LAPTOP+"SUBJECT"+str(n)
	file = [f for f in os.listdir(path+'/') if (f.find('processed')!=-1)]
	file = file[0]

	print("SUBJECT" + str(n))
	# print(file)
	data = pd.read_csv(CONST.PATH_LAPTOP + 'SUBJECT' + str(n) + '/'+ file, delimiter = ",").astype(float)
	time = data['time'].tolist()
	force = data['force'].tolist()
	angle = data['flex sensor'].tolist()
	nTrial = data["'Trial Number'"].tolist()
	targets = data["'Target Angle'"].tolist()

	idx = [i for i in range(1,len(nTrial)) if nTrial[i]!=nTrial[i-1] ]

	if (idx == []):
		return []
	# print(idx)
	# print(len(time))
	for i in list(range(0,len(targets) - 1)):
		if ((targets[i] == 0) and (targets[i+1] == 180)):
			x = [i+1]
			#print(x)
			break

	if not(x is None):
		idx1 = x + idx 
		#nTrial_afterEachChange = [nTrial[i] for i in idx1]
		targets_afterEachChange = [targets[i] for i in idx1]
		#angleDiff = [0] + [targets_afterEachChange[i] - targets_afterEachChange[i-1] for i in list(range(1,len(targets_afterEachChange)))]
		# print(angleDiff)
		# print(len(angleDiff))

	idx2 = idx1 + [len(time)-1]
	#print(idx2)
	time_afterEachChange = [time[i] for i in idx2]

	# find time length between clicks
	t_diff = [time_afterEachChange[j] - time_afterEachChange[j-1] for j in list(range(1,len(time_afterEachChange)))]

	learningTime = list(zip(targets_afterEachChange, t_diff))

	# g = open(CONST.PATH_LAPTOP + 'SUBJECT' + str(n) + "/learningTime_timeBetweenClicks_" + 'SUBJECT' + str(n) + ".csv", 'w+', encoding='UTF8', newline='')
	# w = csv.writer(g)
	# for a in learningTime:
	# 	w.writerow([a[0], a[1]])
	# g.close()
	print("Time values extracted and saved.")
	# print(time_afterEachChange)
	# print(targets_afterEachChange)
	# print(len(targets_afterEachChange))

	# print(t_diff)
	# print(len(t_diff))

	#print(learningTime[30:70])
	print(len(learningTime))
	return learningTime

def sortProcessLearningTime(d):

	d = d[30:70] # take relevant practice area
	angleDiff = [0] + [abs(d[i][0] - d[i-1][0]) for i in list(range(1, len(d)))]
	#print(angleDiff)

	#unzip d
	d = [[i for i, j in d],
		[j for i, j in d]]
	#print(d)

	speed = [angleDiff[i]/d[1][i] for i in list(range(0, len(angleDiff)))]

	for i in list(range(0,len(d[0]))):
		if d[0][i] in list(range(175,25,-15)):
			d[0][i] = d[0][i] + 5

	#d = list(zip(d[0], speed)) # saving speed data
	d = list(zip(d[0], d[1])) # saving time difference data
	#print(d)
	d = sorted(d, key = lambda x: x[0])

	d = np.array(d)
	targets = np.unique(d[:,0])
	d2 = np.zeros((10,5))
	d2[:,0] = targets
	
	# reshape
	c = 1
	for k in list(range(0, len(d))):
		for u in list(range(0,len(targets))):
			if (d[k,0] == targets[u]):
				d2[u,c] = d[k,1]
				c = c + 1
				if (c == 5):
					c = 1
	print(d2)
	# print(len(d))
	return d2

def extractForce(n):
	path = CONST.PATH_LAPTOP+"SUBJECT"+str(n)
	file = [f for f in os.listdir(path+'/') if (f.find('processed')!=-1)]
	file = file[0]

	# print(file)
	data = pd.read_csv(CONST.PATH_LAPTOP + 'SUBJECT' + str(n) + '/'+ file, delimiter = ",").astype(float)
	time = data['time'].tolist()
	force = data['force'].tolist()
	angle = data['flex sensor'].tolist()
	nTrial = data["'Trial Number'"].tolist()
	targets = data["'Target Angle'"].tolist()

	idx = [i for i in range(1,len(nTrial)) if nTrial[i]!=nTrial[i-1] ]

	if (idx == []):
		return []
	# print(idx)
	# print(len(time))
	for i in list(range(0,len(targets) - 1)):
		if ((targets[i] == 0) and (targets[i+1] == 180)):
			x = [i]
			break

	# if not(x is None):
	# 	idx1 = x + idx 
	# 	nTrial_afterEachChange = [nTrial[i] for i in idx1]
	# 	targets_afterEachChange = [targets[i] for i in idx1]
	idx2 = idx + [len(time)-1]
	print(idx2)
	force_afterEachChange = [force[i] for i in idx2]

	# g = open(CONST.PATH_LAPTOP + 'SUBJECT' + str(n) + "/forceAtClick_" + 'SUBJECT' + str(n) + ".csv", 'w+', encoding='UTF8', newline='')
	# #g = open(p + "WELP_SubjectAttempts" + fileName, 'w+', encoding='UTF8', newline='')
	# w = csv.writer(g)
	# for a in force_afterEachChange:
	# 	w.writerow([a])
	# g.close()
	print("Force values extracted and saved.")
	#print(force_afterEachChange)
	print(len(force_afterEachChange))
	return force_afterEachChange

def extractSubjectAttemptAngles(p, n):
	data = pd.read_csv(CONST.PATH_LAPTOP + 'SUBJECT' + str(n) + '/'+p + '/processed_' + p + '.csv', delimiter = ",").astype(float)
	time = data['time'].tolist()
	angle = data['flex sensor'].tolist()
	nTrial = data["'Trial Number'"].tolist()
	targets = data["'Target Angle'"].tolist()

	idx = [i for i in range(1,len(nTrial)) if nTrial[i]!=nTrial[i-1] ]

	if (idx == []):
		return []
	#print(idx)
	#print(len(time))
	# for i in list(range(0,len(targets) - 1)):
	# 	if ((targets[i] == 0) and (targets[i+1] == 180)):
	# 		x = [i]
	# 		break

	# if not(x is None):
	# 	idx1 = x + idx 
	# 	nTrial_afterEachChange = [nTrial[i] for i in idx1]
	# 	targets_afterEachChange = [targets[i] for i in idx1]
	idx2 = idx + [len(time)-1]
	angle_afterEachChange = [angle[i] for i in idx2]

	g = open(CONST.PATH_LAPTOP + 'SUBJECT' + str(n) + '/'+p + "/subjectAngleAttempts_" + p + ".csv", 'w+', encoding='UTF8', newline='')
	#g = open(p + "WELP_SubjectAttempts" + fileName, 'w+', encoding='UTF8', newline='')
	w = csv.writer(g)
	for a in angle_afterEachChange:
		w.writerow([a])
	g.close()
	print("Subject angle attempts extracted and saved.")
	print(angle_afterEachChange)
	print(len(angle_afterEachChange))
	return angle_afterEachChange

def passiveHapticSection(n):
	path = CONST.PATH_LAPTOP+"SUBJECT"+str(n)
	file = [f for f in os.listdir(path+'/') if (f.find('processed')!=-1)]
	file = file[0]

	# print(file)
	data = pd.read_csv(CONST.PATH_LAPTOP + 'SUBJECT' + str(n) + '/'+ file, delimiter = ",").astype(float)
	time = data['time'].tolist()
	force = data['force'].tolist()
	angle = data['flex sensor'].tolist()
	nTrial = data["'Trial Number'"].tolist()
	targets = data["'Target Angle'"].tolist()
	dist = data["actuator position, measured"].tolist()

	idx = [i for i in range(1,len(nTrial)) if nTrial[i]!=nTrial[i-1] ]

	if (idx == []):
		return []
	# print(idx)
	# print(len(time))
	# for i in list(range(0,len(targets) - 1)):
	# 	if ((targets[i] == 0) and (targets[i+1] == 180)):
	# 		x = [i]
	# 		break

	# if not(x is None):
	# 	idx1 = x + idx 
	# 	nTrial_afterEachChange = [nTrial[i] for i in idx1]
	# 	targets_afterEachChange = [targets[i] for i in idx1]
	idx2 = idx + [len(time)-1]
	k = []
	for z in list(range(0,len(dist))):
		if ((dist[z]) > 0 and force[z]/dist[z] >= 0 and force[z]/dist[z] < 2):
			k.append(force[z]/dist[z])
		else:
			k.append(0)
	#print(time[idx2[20]])
	sk.plot_Force(0, str(n), str(n), time[idx2[20]:idx2[29]], force[idx2[20]:idx2[29]])
	sk.plot_ForceVsDist(0, str(n), str(n), dist[idx2[20]:idx2[29]], force[idx2[20]:idx2[29]])
	#sk.plot_Force(0, str(n), str(n), time[idx2[20]:idx2[29]], force[idx2[20]:idx2[29]])
	#return(idx2[10])
	#force_afterEachChange = [force[i] for i in idx2]

	# g = open(CONST.PATH_LAPTOP + 'SUBJECT' + str(n) + "/forceAtClick_" + 'SUBJECT' + str(n) + ".csv", 'w+', encoding='UTF8', newline='')
	# #g = open(p + "WELP_SubjectAttempts" + fileName, 'w+', encoding='UTF8', newline='')
	# w = csv.writer(g)
	# for a in force_afterEachChange:
	# 	w.writerow([a])
	# g.close()
	# print("Force values extracted and saved.")
	# #print(force_afterEachChange)
	# print(len(force_afterEachChange))
	# return force_afterEachChange

def generateSubjectAttemptsTargets(n):

	path = CONST.PATH_LAPTOP+"SUBJECT"+str(n)
	allSubDirs = [d for d in os.listdir(path) if os.path.isdir(os.path.join(path, d))]
	experimentDataDirs = [ d for d in allSubDirs if d.find('subject')==-1]
	experimentDataDirs = sorted(experimentDataDirs, key=lambda x:sk.getCreationTime(path+'/'+x))
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

def generateForce(n):

	path = CONST.PATH_LAPTOP+"SUBJECT"+str(n)
	file = [f for f in os.listdir(path+'/') if (f.find('processed')!=-1)]
	
	# allSubDirs = [d for d in os.listdir(path) if os.path.isdir(os.path.join(path, d))]
	# experimentDataDirs = [ d for d in allSubDirs if d.find('subject')==-1]
	# experimentDataDirs = sorted(experimentDataDirs, key=lambda x:sk.getCreationTime(path+'/'+x))
	# print(experimentDataDirs)

	force = []
	#idx = 0
	# # go through all the subdirs without 'subject' and in order of when it was created.
	# for d in experimentDataDirs:

		# file = [f for f in os.listdir(path+'/'+d) if (f.find('processed')!=-1)]
	file = file[0]
	#print(d)
		#print(len(s))
	force = extractForce(n)

	# 	# add targets
	# 	# read target file
	# data1 = pd.read_csv(path+'/'+d + '/targetAngles_'+d +'.csv', delimiter = "\n", header=None).astype(float)
	# t = [i[0] for i in data1.values.tolist()]
	# 	# copy 0 to len(s) target angles into targets
	# targets = targets + t[idx:idx+len(s)]
	# idx = idx + len(s)

	force = force[70:]
	print(len(force))

	if (len(force) == 40):
		print("we have all the data, let's proceed!")
		g = open(CONST.PATH_LAPTOP + 'SUBJECT' + str(n) + "/force_" + 'SUBJECT' + str(n) + ".csv", 'w+', encoding='UTF8', newline='')
		w = csv.writer(g)
		for a in force:
			w.writerow([a])
		g.close()

		# g = open(CONST.PATH_LAPTOP + 'SUBJECT' + str(n) + "/targetAngles_" + 'SUBJECT' + str(n) + ".csv", 'w+', encoding='UTF8', newline='')
		# w = csv.writer(g)
		# for a in targets:
		# 	w.writerow([a])
		# g.close()

		print("force data generated woohoo for SUBJECT " + str(n))


	else:
		print("missing and/or extra data. data length =" + str(len(force)))
		# if attempt total == 110, have all the data. can proceed. otherwise: data missing error



def combineProcess(n):

	# find experimentDataDirs. get the processingFile. 
	path = CONST.PATH_LAPTOP+"SUBJECT"+str(n)
	allSubDirs = [d for d in os.listdir(path) if os.path.isdir(os.path.join(path, d))]
	experimentDataDirs = [ d for d in allSubDirs if d.find('subject')==-1]
	experimentDataDirs = sorted(experimentDataDirs, key=lambda x:sk.getCreationTime(path+'/'+x))

	print(experimentDataDirs)

	# copy first processingFile and make that the main
	endTime = 0
	newTime = []
	combinedFile = CONST.PATH_LAPTOP + 'SUBJECT' + str(n) + "/processed_" + 'SUBJECT' + str(n) + ".csv"
	h = open(combinedFile, 'w+', encoding='UTF8', newline='')
	writer = csv.writer(h)
	dataFunc = {'oldTime':sk.millisToSeconds, 'flex sensor':sk.doNothing,'actuator position, command':sk.commandToPosition, \
			'actuator position, measured':sk.feedbackToPosition, 'force':sk.computeForce}

	columnNames = list(dataFunc.keys())
	columnNames.append("'Trial Number'") 
	columnNames.append("'Target Angle'")
	columnNames.append("'Bookmark'")
	writer.writerow(columnNames)
	h.close()

	for d in experimentDataDirs:


		# if it doesn't have subjectAngleAttempts,extract and add to subject angle attempts list. add targets with same length
		file = [f for f in os.listdir(path+'/'+d) if (f.find('processed')!=-1)]
		file = file[0]

		# copy this file into main file by
		# append the other processingFiles
		f = open(combinedFile, 'a', encoding='UTF8', newline='')
		print(path+'/'+ d + '/' + file)
		g = open(path+'/'+ d + '/' + file, 'r', encoding='UTF8', newline='')
		
		counter = 0
		for line in g:
			if not (counter == 0):
				f.write(line)
			counter = counter + 1
		f.close()
		g.close()
		data = pd.read_csv(path+'/'+ d + '/' + file, delimiter = ",").astype(float)
		time = data['time'].tolist()
		revisedTime = [i + endTime for i in time] #endTime + t
		newTime = newTime + revisedTime # create new time vector by 
		endTime = endTime + time[-1]

	# add new time column
	data1 = pd.read_csv(combinedFile, delimiter = ",").astype(float)
	data1['time'] = newTime
	data1.to_csv(combinedFile)
	print("done")
	

def combineRaw(n):
	# find experimentDataDirs. get the processingFile. 
	path = CONST.PATH_LAPTOP+"SUBJECT"+str(n)
	allSubDirs = [d for d in os.listdir(path) if os.path.isdir(os.path.join(path, d))]
	experimentDataDirs = [ d for d in allSubDirs if d.find('subject')==-1]
	experimentDataDirs = sorted(experimentDataDirs, key=lambda x:sk.getCreationTime(path+'/'+x))
	print(experimentDataDirs)

	# copy first processingFile and make that the main
	endTime = 0
	newTime = []
	combinedFile = CONST.PATH_LAPTOP + 'SUBJECT' + str(n) + "/raw_" + 'SUBJECT' + str(n) + ".csv"
	h = open(combinedFile, 'w+', encoding='UTF8', newline='')
	writer = csv.writer(h)
	dataFunc = {'oldTime':sk.millisToSeconds, 'flex sensor':sk.doNothing,'actuator position, command':sk.commandToPosition, \
			'actuator position, measured':sk.feedbackToPosition, 'force':sk.computeForce}

	columnNames = list(dataFunc.keys())
	columnNames.append("'Trial Number'") 
	columnNames.append("'Target Angle'")
	columnNames.append("'Bookmark'")
	writer.writerow(columnNames)
	h.close()

	for d in experimentDataDirs:
		# if it doesn't have subjectAngleAttempts,extract and add to subject angle attempts list. add targets with same length
		file = [f for f in os.listdir(path+'/'+d) if (f.find('raw')!=-1)]
		file = file[0]

		# copy this file into main file by
		# append the other processingFiles
		f = open(combinedFile, 'a', encoding='UTF8', newline='')
		print(path+'/'+ d + '/' + file)
		g = open(path+'/'+ d + '/' + file, 'r', encoding='UTF8', newline='')
		
		#counter = 0
		for line in g:
		#	if not (counter == 0):
			f.write(line)
		#	counter = counter + 1
		f.close()
		g.close()
		data = pd.read_csv(path+'/'+ d + '/' + file, delimiter = ",", header=None).astype(float)
		time = data[0].tolist()
		revisedTime = [i + endTime for i in time] #endTime + t
		newTime = newTime + revisedTime # create new time vector by 
		endTime = endTime + time[-1]

	# add new time column
	print(len(newTime))
	data1 = pd.read_csv(combinedFile, delimiter = ",").astype(float)
	data1['time'] = newTime
	data1.to_csv(combinedFile)
	print("done")


def plotStudySection(p, time,targets,angle,force,nTrial):
	
	idx = [i for i in range(1,len(nTrial)) if nTrial[i]!=nTrial[i-1]]
	idx = idx[70:]

	#print(idx)

	#print(list(range(0, len(idx)-1, 10)))

	for i in list(range(0, len(idx)-1, 10)):
		#print("hi")
		if (i+11) > len(idx):
			sk.plot_Angles(0, p, p, time[idx[i]:idx[-1]], targets[idx[i]:idx[-1]], angle[idx[i]:idx[-1]])
		else:
			sk.plot_Angles(0, p, p, time[idx[i]:idx[i+10]], targets[idx[i]:idx[i+10]], angle[idx[i]:idx[i+10]])

def plotStudyTest(s, p, time,targets,angle,force,nTrial):
	
	idx = [i for i in range(1,len(nTrial)) if nTrial[i]!=nTrial[i-1]]
	idx = idx[70:]

	for i in list(range(0, len(angle))):
		if (angle[i] > 180):
			print(i)
			angle[i] = 180
		elif (angle[i] < 40):
			print(i)
			angle[i] = 40

	fig, ax1 = plt.subplots(2,2, sharex=False, sharey=True)
	
	plt.suptitle("Real-time Data " + p, name='Arial', weight='bold')
	#ax1.set_xlabel("Time (s)", name='Arial')
	plt.xticks(name='Arial')
	plt.yticks(list(range(180, 30, -15)), name='Arial')
	#ax1.set_ylabel("Angle (degrees)", name='Arial',)

	

	ax1[0,0].plot(time[idx[0]:idx[10]], targets[idx[0]:idx[10]], '#648fff', time[idx[0]:idx[10]], angle[idx[0]:idx[10]], '#ffb000', linewidth=1.75, label='case1')
	ax1[0,0].grid(True)
	#ax1[0,0].set_ylim(40,200)


	ax1[0,1].plot(time[idx[10]:idx[20]], targets[idx[10]:idx[20]], '#648fff', time[idx[10]:idx[20]], angle[idx[10]:idx[20]], '#ffb000', linewidth=1.75, label='case2')
	ax1[0,1].grid(True)

	ax1[1,0].plot(time[idx[20]:idx[30]], targets[idx[20]:idx[30]], '#648fff', time[idx[20]:idx[30]], angle[idx[20]:idx[30]], '#ffb000', linewidth=1.75, label='case3')
	ax1[1,0].grid(True)

	ax1[1,1].plot(time[idx[30]:], targets[idx[30]:], '#648fff', time[idx[30]:], angle[idx[30]:], '#ffb000', linewidth=1.5, label='case4')
	ax1[1,1].grid(True)
	#ax1.yaxis.label.set_color('b')
	# ax1.tick_params(axis='y', color='b')
	#ax1.set_ylim(40,200)

	ax1[0,0].grid(True)
	#ax1.legend(l_all, labels, loc=0)
	if s==1: plt.savefig(p +"fig_"+fileName)
	plt.show()

# def plotForceVsTime():


# def computeABSError():


# def computeError():




