# Supporting Functions for Sensory Substitution Devce 
# Written by: Sreela Kodali (kodali@stanford.edu) 

import numpy as np
import math
import os
import shutil
import datetime
from scipy import signal
import constants as CONST
from operator import itemgetter
import matplotlib   #FIX: fix for newer python environment
matplotlib.use("TkAgg")
from matplotlib import pyplot as plt
from scipy.signal import lfilter, lfilter_zi, filtfilt, butter
import random
import sys
import random

# # if calibrated user study, get constants from new file
# print("Use values from recent user calibration?")
# calibratedUserValues = input()

# if (int(calibratedUserValues)):
# 	sys.path.append('/Users/Sreela/Documents/School/Stanford/Year3_2/PIEZO2/Data/Pilot2/2022-09-19_11-03_subjectrachel')
# 	import constantsCalibrated as CONST

## CALIBRATION
# zero force
# max position and force of user
# min position and force for user (detection)

## FUNCTIONS ##
# Offloading computation that isn't needed real-time to computer
def getCreationTime(path):
    return os.stat(path).st_birthtime

# Mapping float value x in different range 
def mapFloat(x, in_min, in_max, out_min, out_max):
	return (float) ((x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min)

#  millisecond --> second
def millisToSeconds(s):
	return s/1000

def doNothing(data):
	return data

# Computing angle from flex sensor data
def computeAngle(data):
	a = 180 - data
	return a
	#a = 180 - float(data)/64.0 #float(data)
	#return a
	#if a > 90: return a
	#else: return a - 0.2*(90-a)
	 
	#return mapFloat(data, CONST.ANGLE_DATA_MIN, CONST.ANGLE_DATA_MAX, CONST.ANGLE_MIN, CONST.ANGLE_MAX) # NEEDS CALIBRATED VAL

# Servo command (degrees) --> actuator position (mm)
def commandToPosition(c):
	# FIX: double check this
	return mapFloat(c, CONST.ACTUATOR_COMMAND_MIN, CONST.ACTUATOR_COMMAND_MAX, CONST.ACTUATOR_POSITION_MIN, CONST.ACTUATOR_POSITION_MAX)
	#return 0.22*c - 10.7
	# I guess could be a precomputed look up table lol

def commandToPosition_Actuator2(c):
	return mapFloat(180-c, 139, 46, 0, 20)
	#return 0.22*c - 10.7

# Feedback signal from actuator (1/1024th of V) to actuator position (mm)
def feedbackToPosition(f):
	return mapFloat(f, CONST.ACTUATOR_FEEDBACK_MIN, CONST.ACTUATOR_FEEDBACK_MAX, CONST.ACTUATOR_POSITION_MAX, CONST.ACTUATOR_POSITION_MIN) # NEEDS CALIBRATED VAL

# delta change in feedback signal results in how much change in actuator position in mm
# slope of the previous function
# returns mm
def delta_feedbackToPosition(delta):
	return delta*CONST.ACTUATOR_POSITION_MAX/(CONST.ACTUATOR_FEEDBACK_MAX-CONST.ACTUATOR_FEEDBACK_MIN) # NEEDS CALIBRATED VAL

# Function 5: Digital value from force sensor --> force measurement (N)
def computeForce(data):
	return round(((data - CONST.ZERO_FORCE) * (45.0)/512), 2) #(data - 256) * (45.0)/511 # NEEDS CALIBRATED VAL
	#changed bc uncalibrated

# dataFunc = {'time':millisToSeconds, 'flex sensor':computeAngle,'actuator position, command':commandToPosition, \
# 			'actuator position, measured':feedbackToPosition, 'force':computeForce}
# columnNames = list(dataFunc.keys())

def processNewRow(dataFunc, val):
	columnNames = list(dataFunc.keys())
	r = []
	for key in dataFunc:
		x = dataFunc[key](float((val[columnNames.index(key)]).rstrip()))
		# old code, if serial flush pushes garbage
		# if (loopIncrement < 20 and key == 'time' and x > 2):
		# 	break
		r.append(x)
	return r

def sendAngle_PCToWearable(a, m):
	a = int(a)
	if (a > 180):
		a = 180
	elif (a < 40):
		a = 40

	if (a < 100):
		m.write(str(0).encode())
	m.write(str(a).encode())

	return a

def validPacket(val):
	if (len(val) == len(dataFunc)):
		forceData = float(val[(len(dataFunc)-1)].lstrip("-").rstrip())
		if (forceData > 100): 
			return True
	return False

def generateAngles(txt, N, M, A):
	t1 = list(range(180,40,-15))
	trialAngles = []
	for i in range(0, N):
		trialAngles = trialAngles + t1

	if txt in ['TARGET', 'PRACTICE', 'TEST']:
		for i in range(0,M):
			t = list(range(180,40,-15))#list(range(40,180,15))
			r = [t.pop(random.randrange(len(t)))]
			r.append(t.pop(random.randrange(len(t))))
			half1 = t[:4]
			half2 = t[4:]

			x = random.randrange(2)
			if (x == 0): half1.reverse()
			else: half2.reverse()
			x = random.randrange(2)
			if (x == 0): t = half1 + half2 + r
			else: t = half2 + half1 + r

			trialAngles = trialAngles + t

	if txt in ['PRACTICE', 'TEST']:
		for i in range(0,A):
			t2 = list(range(180,40,-15))#list(range(40,180,15))
			random.shuffle(t2)
			trialAngles = trialAngles + t2

	return trialAngles

	


def generateRandomTrials(N, M, A):
	trialAngles = []
	t1 = list(range(180,40,-15))

	# with visual w/o haptics, in order
	trialAngles = trialAngles + t1

	#with visual w/o haptics, randomized
	t2 = list(range(180,40,-15))
	random.shuffle(t2)
	trialAngles = trialAngles + t2

	# visual window for a second with haptics, in order
	for i in range(0, N):
		trialAngles = trialAngles + t1

	# visual window for a second with haptics, some order + random
	for i in range(0,M):
		t = list(range(40,180,15))
		r = [t.pop(random.randrange(len(t)))]
		r.append(t.pop(random.randrange(len(t))))
		half1 = t[:4]
		half2 = t[4:]

		x = random.randrange(2)
		if (x == 0): half1.reverse()
		else: half2.reverse()
		x = random.randrange(2)
		if (x == 0): t = half1 + half2 + r
		else: t = half2 + half1 + r

		trialAngles = trialAngles + t

	for i in range(0,A):
		random.shuffle(t)
		trialAngles = trialAngles + t

	# test
	for i in range(0,4):
		random.shuffle(t)
		trialAngles = trialAngles + t

	return trialAngles
	

def generateKeyboardInc():
	if (random.randrange(2)):
		inc = 3
	else:
		inc = 1
	return inc


def findNWindow(timeArr):
	i = 1
	while ((timeArr[i] - timeArr[0]) < 1):
		i+=1
	return i

#def data rate

def evaluatePilotPerformance(time, trial, targetAngle):

	prevTrial = -1
	t_start = []
	rowCount = 0

	for i in trial:
		t = time[int(i)]

		# if it's not the first row, update prevTrial
		if ((rowCount != 0)):
			prevTrial = trial[rowCount-1]

		# if it's the first trial, min t is the first
		if ((i != prevTrial) and (rowCount == 0)):
			t_min = t # set the min time
			t_max = 0

		# if its a new trial and not first trial
		if ((i != prevTrial) and (rowCount != 0)):
			#t_diff.append(t_max - t_min)
			t_start.append(t_min)

			t_min = time[rowCount] # set the min time
			t_max = 0



		# #elif: (t < t_min): t_min = t

		if (t > t_max): t_max = t
		rowCount = rowCount + 1

	#t_diff.append(t_max - t_min)
	t_start.append(t_min)
	t_start.append(1210.299)

	print(len(t_start))


	t_diff = []

	for i in range(0, len(t_start)-1):
		if (i != 0):
			t_diff.append(t_start[i]-t_start[i-1])

	t_avg = [sum(t_diff[0:10])/len(t_diff[0:10]), sum(t_diff[11:20])/len(t_diff[11:20]), sum(t_diff[21:30])/len(t_diff[21:30]), sum(t_diff[31:40])/len(t_diff[31:40]), sum(t_diff[41:50])/len(t_diff[41:50]), sum(t_diff[51:])/len(t_diff[51:])]
	print(t_avg)
	return t_diff

def findRisingEdge(s, t, minThresh, w, measureDelay_force):
	avg1 = sum(s[:w])/len(s[:w])
	avg2 = sum(s[-w:])/len(s[-w:])
	# print("avg1 = " + str(avg1))
	# print("avg2 = " + str(avg2))

	ix_start = 0
	ix_end = 0
	avgThresh = 0
	# plateauLength = 0
	# minPlateauLength = w/2

	# check if edge present
	if (abs(avg2 - avg1) >= minThresh): #0):
		avgThresh = math.floor(abs(avg2 - avg1))
		#print("avgThresh=" + str(avgThresh))

		if (measureDelay_force == True):
			for i in range(len(s) - w - 1, w, -1):
				a = s[i]
				diff = (avg2 - a)
				if (diff >= avgThresh):
					ix_end = i+1
					break

			if (ix_end > 0):
				for i in range(ix_end-1, ix_end-w, -1): # don't want to be limited to w window for length of rising
				# for i in range(ix_end-1, 0, -1):
					b = s[i]
					# print(i)
					# print(abs(s[ix_end] - b))
					#print(abs(b-avg1))
					if((abs(s[ix_end] - b) >= avgThresh)):
						ix_start = i

						if (ix_start > 0):
							if (s[ix_start-1] > b):
								break

		else:
			for i in range(len(s) - w):
				a = s[w+i]
				diff = abs(a-avg1)
				if (diff >= avgThresh): 
					ix_end = w+i#
					break

			if (ix_end > 0):
				#for i in range(ix_end-1, ix_end-w, -1): # don't want to be limited to w window for length of rising
				for i in range(ix_end-1, 0, -1):
					b = s[i]
					# print(i)
					# print(abs(s[ix_end] - b))
					#print(abs(b-avg1))
					if((abs(s[ix_end] - b) >= avgThresh)):
						ix_start = i
						break

	# print(ix_start)
	# print(ix_end)
	return ix_start, ix_end, avgThresh



def actuatorSpeed(deltaFeedbackSignal, t_risingEdge):
	# returns mm/s
	# rising edge is in milliseconds, hence why 1000 const included
	# delta_feedbackToPosition returns mm
	return delta_feedbackToPosition(deltaFeedbackSignal)*1000/t_risingEdge


def plot_pilotResults(t_diff):
	fig, ax1 = plt.subplots()
	l1 = ax1.plot(range(0,len(t_diff)), t_diff, 'b', linewidth=1.75, label='time per trial')
	plt.suptitle("Time Per Trial: Pilot Results", name='Arial', weight='bold')
	ax1.set_ylabel("Time", name='Arial')
	ax1.set_xlabel("Trial Count", name='Arial')
	plt.show()

def delayCrossCorrelation(angle, positionMeasured, timeArr):
	n_window = findNWindow(timeArr)
	ind = np.random.choice(len(timeArr)-n_window, CONST.N_CORR)
	maxCorr = []
	for i in ind:
		a = angle[i:i+n_window]
		p = positionMeasured[i:i+n_window]
    
		n = len(a)
		c = signal.correlate(a, p, mode='same') / np.sqrt(signal.correlate(a, a, mode='same')[int(n/2)] * signal.correlate(p, p, mode='same')[int(n/2)])
		maxCorr.append(timeArr[i+np.argmin(c)] - timeArr[i])
		#maxCorr.append(np.argmax(c))

	t_d = np.mean(maxCorr)

	idx_peaksPositionMeasured, _ = signal.find_peaks(np.asarray(positionMeasured), height=(0,25), distance=n_window)
	idx_peaksPositionMeasured = idx_peaksPositionMeasured.tolist()
	t_peaksPositionMeasured = list(itemgetter(*idx_peaksPositionMeasured)(timeArr))

	idx_peaksAngle = []
	for t in t_peaksPositionMeasured:
		t = t - t_d
		idx_peaksAngle.append((np.abs(timeArr-t)).argmin())
	t_peaksAngle = list(itemgetter(*idx_peaksAngle)(timeArr))

	t_peakDelays = list(zip(t_peaksAngle, t_peaksPositionMeasured))

	return t_d, t_peakDelays, idx_peaksAngle, idx_peaksPositionMeasured

def butter_lowpass(cutoff, fs, order=5):
    nyq = 0.5 * fs
    normal_cutoff = cutoff / nyq
    b, a = butter(order, normal_cutoff, btype='low', analog=False)
    return b, a

def butter_lowpass_filter(data, cutoff, fs, order=5):
    b, a = butter_lowpass(cutoff, fs, order=order)
    y = lfilter(b, a, data)
    return y

def delayPeakToPeak(angle, positionMeasured, timeArr):
	n_window = findNWindow(timeArr)

	# max_peaksPositionMeasured = signal.argrelextrema(np.asarray(positionMeasured), np.greater)
	# min_peaksPositionMeasured = signal.argrelextrema(np.asarray(positionMeasured), np.less)
	idx_peaksPositionMeasured, _ = signal.find_peaks(np.asarray(positionMeasured), height=(0,25), distance=n_window)
	# idx_peaksPositionMeasured = max_peaksPositionMeasured[0].tolist() + min_peaksPositionMeasured[0].tolist()

	t_peaksPositionMeasured = list(itemgetter(*idx_peaksPositionMeasured)(timeArr))
	#print(t_peaksPositionMeasured)

	# max_peaksAngle = signal.argrelextrema(np.asarray(angle), np.greater)
	# min_peaksAngle = signal.argrelextrema(np.asarray(angle), np.less)
	idx_peaksAngle, _ = signal.find_peaks(np.asarray(angle), height=(-40,250), distance=n_window)
	# idx_peaksAngle = max_peaksAngle[0].tolist() + min_peaksAngle[0].tolist()

	t_peaksAngle = list(itemgetter(*idx_peaksAngle)(timeArr))
	#print(t_peaksAngle)
	t_d = 0
	n_pairs = 0
	j = 0
	minLength = min(len(t_peaksAngle), len(t_peaksPositionMeasured))

	# fix this

	#t_peakDelays = []
	for i in range(0, minLength):
		for j in range(0, minLength):
		# find matching pair of points. <1.0 >0.0
		# while((diff < 0.0) or (diff > 1.0)):
		# 	j = j + 1
		# 	diff = t_peaksPositionMeasured[i] - t_peaksAngle[j]

			diff = t_peaksPositionMeasured[i] - t_peaksAngle[j]
			if ((diff > 0.0) and (diff < 1.0)):
				t_d += diff
				n_pairs += 1
				#t_peakDelays.append((t_peaksAngle[j], t_peaksPositionMeasured[i]))
	
	t_d = t_d / n_pairs
	t_peakDelays = list(zip(t_peaksAngle, t_peaksPositionMeasured))

	return t_d, t_peakDelays, idx_peaksAngle, idx_peaksPositionMeasured

#def plot_timingAll(s, p, fileName, time, command, measured, i_startC, i_endM, i):
def plot_timingActuatorAll(s, p, fileName, time, command, position, force, actuatorType):
	fig, ax1 = plt.subplots()
	ax2 = ax1.twinx()

	plt.suptitle("All Timing Data " + fileName[:-4], name='Arial', weight='bold')
	ax1.set_xlabel("Time (ms)", name='Arial')
	plt.xticks(name='Arial')
	plt.yticks(name='Arial')

	ax1.set_ylabel("Actuator Position (mm)", name='Arial')
	if (actuatorType == 1):
		ax1.plot(time, command, 'mediumaquamarine', time, position, 'g')
	#ax1.set_ylim(0,21)
	elif (actuatorType == 2):
		ax1.plot(time, command, 'mediumaquamarine')
	

	ax2.set_ylabel("Force (N)", name='Arial')
	ax2.plot(time, force, 'r')
	#ax2.set_ylim(0,18)

	#ax1.axvspan(time[i*200 + i_startC], time[i*200 + i_endM], color='powderblue', alpha=0.5)

	#l_all = l1#+l2#+l3#+l4
	#labels = [l.get_label() for l in l_all]

	plt.grid(True)
	#ax1.legend(l_all, labels, loc=0)
	if s==1: plt.savefig(p +"fig_"+fileName[:-4])
	plt.show()


def plot_timingActuatorWindow(s, p, fileName, time, command, measured, i_startC, i_endC, i_startM, i_endM, measureDelay_force):
	#plt.ion()

	fig, ax1 = plt.subplots()
	ax2 = ax1.twinx()
	plt.suptitle("Window of Timing Data " + fileName[:-4], name='Arial', weight='bold')
	ax1.set_xlabel("Time (ms)", name='Arial')
	plt.xticks(name='Arial')
	plt.yticks(name='Arial')

	ax1.set_ylabel("Actuator Position (mm)", name='Arial')
	ax1.plot(time, command, 'mediumaquamarine')
	ax1.set_ylim(min(command)-0.25, max(command)+0.25)
	ax1.plot(time, command,'cD',markevery=[i_startC, i_endC])

	if (not(measureDelay_force)):
		ax1.plot(time, command, 'mediumaquamarine', time, measured, 'g') # switch
		ax1.set_ylim(min(measured)-0.25,max(command)+0.25) # switch
		ax1.plot(time, measured,'gD',markevery=[i_startM, i_endM]) # switch axis and colo
		ax1.axvspan(time[i_startM], time[i_endM], color='lime', alpha=0.5) # switch axis

	else:
		ax2.set_ylabel("Force (N)", name='Arial') # switch
		ax2.plot(time,measured,'r')
		ax2.set_ylim(min(measured)-0.25, max(measured)+0.25)
		ax2.plot(time, measured,'rD',markevery=[i_startM, i_endM]) # switch axis and colo
		ax2.axvspan(time[i_startM], time[i_endM], color='lime', alpha=0.5) # switch axis

	#l_all = l1#+l2#+l3#+l4
	#labels = [l.get_label() for l in l_all]
	
	ax1.axvspan(time[i_endC], time[i_endM], color='powderblue', alpha=0.5)

	plt.grid(True)
	#ax1.legend(l_all, labels, loc=0)
	if s==1: plt.savefig(p +"fig_"+fileName[:-4])
	plt.show()

def plot_timingActuatorAnalysis(s, p, fileName, t_delay, t_risingEdge, speed, command, xaxis_time):
	fig, ax1 = plt.subplots()
	#ax2 = ax1.twinx()
	plt.suptitle("Timing Analysis " + fileName[:-4], name='Arial', weight='bold')
	if (xaxis_time): ax1.set_xlabel("Time", name='Arial') # switch
	else: ax1.set_xlabel("Actuator Extension (mm)", name='Arial') # switch
	plt.xticks(name='Arial')
	plt.yticks(name='Arial')

	ax1.set_ylabel("Time (ms)", name='Arial')
	#ax1.plot(command, t_delay, 'powderblue', command, t_risingEdge, 'c')
	ax1.scatter(command, t_delay, c='powderblue')
	#ax1.scatter(command, t_risingEdge, c='c')
	ax1.set_ylim(0,1200)

	# ax2.set_ylabel("Speed (mm/s)", name='Arial',) 
	# ax2.scatter(command, speed, c='m')
	# #ax2.plot(command, speed, 'm')
	# ax2.set_ylim(0,28)

	plt.grid(True)
	#ax1.legend(l_all, labels, loc=0)
	if s==1: plt.savefig(p +"fig_"+fileName[:-4])
	plt.show()


def plot_Force(s, p, fileName, time, force):
	fig, ax1 = plt.subplots()
	plt.suptitle("Real-time Data " + fileName, name='Arial', weight='bold')
	ax1.set_xlabel("Time (s)", name='Arial')
	plt.xticks(name='Arial')
	plt.yticks(name='Arial')

	ax1.set_ylabel("Force (N)", name='Arial',)
	#ax1.scatter(time, force)
	l1 = ax1.plot(time, force, 'r', linewidth=1.75, label='Force')
	ax1.yaxis.label.set_color('r')
	ax1.tick_params(axis='y', color='r')
	#ax1.set_ylim(-2,10)
	#ax1.set_ylim(0,2)

	plt.grid(True)
	#ax1.legend(l_all, labels, loc=0)
	if s==1: plt.savefig(p +"fig_"+fileName)
	plt.show()

def plot_ForceVsDist(s, p, fileName, time, force):
	fig, ax1 = plt.subplots()
	plt.suptitle("Real-time Data " + fileName, name='Arial', weight='bold')
	ax1.set_xlabel("Distance (mm)", name='Arial')
	plt.xticks(name='Arial')
	plt.yticks(name='Arial')

	ax1.set_ylabel("Force (N)", name='Arial',)
	#ax1.scatter(time, force)
	#l1 = ax1.plot(time, force, 'r', linewidth=1.75, label='Force')
	ax1.scatter(time, force, edgecolors='g')
	ax1.yaxis.label.set_color('r')
	ax1.tick_params(axis='y', color='r')
	ax1.set_ylim(-2,10)
	#ax1.set_ylim(0,2)

	plt.grid(True)
	#ax1.legend(l_all, labels, loc=0)
	if s==1: plt.savefig(p +"fig_"+fileName)
	plt.show()

def plot_ForceDistance(s, p, fileName, time, force):
	fig, ax1 = plt.subplots()
	plt.suptitle("Real-time Data " + fileName, name='Arial', weight='bold')
	ax1.set_xlabel("Actuator Command (pwm)", name='Arial')
	plt.xticks(name='Arial')
	plt.yticks(name='Arial')

	ax1.set_ylabel("Force (N)", name='Arial',)
	ax1.scatter(time, force)
	#l1 = ax1.plot(time, force, 'r', linewidth=1.75, label='Force')
	#ax1.yaxis.label.set_color('r')
	#ax1.tick_params(axis='y', color='r')
	ax1.set_ylim(0,max(force)+1)

	plt.grid(True)
	#ax1.legend(l_all, labels, loc=0)
	if s==1: plt.savefig(p +"fig_"+fileName)
	plt.show()

def plot_Angle(s, p, fileName, time, angle):
	fig, ax1 = plt.subplots()
	plt.suptitle("Real-time Data " + fileName, name='Arial', weight='bold')
	ax1.set_xlabel("Time (s)", name='Arial')
	plt.xticks(name='Arial')
	plt.yticks(name='Arial')

	ax1.set_ylabel("Angle (degrees)", name='Arial',)
	l1 = ax1.plot(time, angle, 'b', linewidth=1.75, label='Force')
	ax1.yaxis.label.set_color('b')
	ax1.tick_params(axis='y', color='b')
	ax1.set_ylim(-50,200)

	plt.grid(True)
	#ax1.legend(l_all, labels, loc=0)
	if s==1: plt.savefig(p +"fig_"+fileName)
	plt.show()

def plot_Angles(s, p, fileName, time, angle1, angle2):
	fig, ax1 = plt.subplots(2,2, sharex=True, sharey=True)

	plt.suptitle("Real-time Data " + fileName, name='Arial', weight='bold')
	ax1.set_xlabel("Time (s)", name='Arial')
	plt.xticks(name='Arial')
	plt.yticks(name='Arial')

	ax1.set_ylabel("Angle (degrees)", name='Arial',)
	l1 = ax1.plot(time, angle1, 'b', linewidth=1.75, label='target')
	l1 = ax1.plot(time, angle2, 'o', linewidth=1.75, label='subject attempt')
	#ax1.yaxis.label.set_color('b')
	# ax1.tick_params(axis='y', color='b')
	ax1.set_ylim(40,200)

	plt.grid(True)
	#ax1.legend(l_all, labels, loc=0)
	if s==1: plt.savefig(p +"fig_"+fileName)
	plt.show()


def plot_Noise(s, p, fileName, time, fftSensor):
	fig, ax1 = plt.subplots()
	plt.suptitle("Real-time Data " + fileName, name='Arial', weight='bold')
	ax1.set_xlabel("Time Delay in Loop (ms)", name='Arial')
	plt.xticks(name='Arial')
	plt.yticks(name='Arial')

	ax1.set_ylabel("Max Noise Power", name='Arial',)
	#l1 = ax1.plot(time, fftSensor)
	l1 = ax1.scatter(time, fftSensor)
	#ax1.yaxis.label.set_color('r')
	ax1.tick_params(axis='y')
	#ax1.set_xlim(0,200)
	#ax1.set_ylim(0,25)

	plt.grid(True)
	#ax1.legend(l_all, labels, loc=0)
	if s==1: plt.savefig(p +"fig_"+fileName)
	plt.show()


def plot_System(s, p, fileName, time, angle, force, device1_positionMeasured, device1_positionCommand):
	fig, ax1 = plt.subplots()
	fig.subplots_adjust(right=0.75)

	ax2 = ax1.twinx()
	ax3 = ax1.twinx()
	# ax4 = ax1.twinx()
	plt.suptitle("Real-time Data " + fileName[:-4], name='Arial', weight='bold')
	ax1.set_xlabel("Time (s)", name='Arial')
	plt.xticks(name='Arial')
	plt.yticks(name='Arial')

	# temporary!!
	ax1.set_ylabel("Angle (degrees)", name='Arial')
	l1 = ax1.plot(time, angle, 'b', linewidth=1.75, label='Angle')
	ax1.yaxis.label.set_color('b')
	ax1.tick_params(axis='y', color='b')
	#ax1.set_ylim(30,180)
	ax3.spines['left'].set_color('b')

	ax2.set_ylabel("Force (N)", name='Arial',)
	l2 = ax2.plot(time, force, 'r', linewidth=1.75, label='Force')
	ax2.yaxis.label.set_color('r')
	ax2.spines['right'].set_color('r')
	ax2.tick_params(axis='y', color='r')
	ax2.set_ylim(0,15)

	ax3.spines['right'].set_position(('axes',1.2))
	ax3.set_ylabel("Actuator Position (mm)", name='Arial')
	l3 = ax3.plot(time, device1_positionMeasured, 'g', linewidth=1.75, label='Actuator Position (Measured)')
	ax3.yaxis.label.set_color('g')
	ax3.spines['right'].set_color('g')
	ax3.tick_params(axis='y', color='g')
	ax3.set_ylim(0,20)

	l4 = ax3.plot(time, device1_positionCommand, color='orange', linewidth=1.75, label='Actuator Position (Command)')

	#l_all = l1+l2+l3#+l4
	#labels = [l.get_label() for l in l_all]

	plt.grid(True)
	#ax1.legend(l_all, labels, loc=0)
	if s==1: plt.savefig(p +"fig_"+fileName[:-4])
	plt.show()
	

def plot_SystemWithDelay(s, p, fileName, time, angle, force, device1_positionMeasured, t_d, t_peakDelays, idx_peaksAngle, idx_peaksPositionMeasured):
	fig, ax1 = plt.subplots()
	fig.subplots_adjust(right=0.75)

	ax2 = ax1.twinx()
	ax3 = ax1.twinx()
	# ax4 = ax1.twinx()
	plt.suptitle("Real-time Data " + fileName[:-4], name='Arial', weight='bold')
	ax1.set_xlabel("Time (s)", name='Arial')
	plt.xticks(name='Arial')
	plt.yticks(name='Arial')

	ax1.set_ylabel("Angle (degrees)", name='Arial')
	l1 = ax1.plot(time, angle, 'b', linewidth=1.75, label='Angle')
	ax1.yaxis.label.set_color('b')
	ax1.tick_params(axis='y', color='b')
	#ax1.set_ylim(30,180)
	ax3.spines['left'].set_color('b')

	ax2.set_ylabel("Force (N)", name='Arial',)
	l2 = ax2.plot(time, force, 'r', linewidth=1.75, label='Force')
	ax2.yaxis.label.set_color('r')
	ax2.spines['right'].set_color('r')
	ax2.tick_params(axis='y', color='r')
	ax2.set_ylim(0,15)

	ax3.spines['right'].set_position(('axes',1.2))
	ax3.set_ylabel("Actuator Position (mm)", name='Arial')
	l3 = ax3.plot(time, device1_positionMeasured, 'g', linewidth=1.75, label='Actuator Position (Measured)')
	ax3.yaxis.label.set_color('g')
	ax3.spines['right'].set_color('g')
	ax3.tick_params(axis='y', color='g')
	ax3.set_ylim(0,20)

	# #l4 = ax2.plot(time, device1_positionCommand, color='orange', linewidth=1.75, label='Actuator Position (Command)')
	for d in t_peakDelays:
		ax1.axvspan(d[0], d[1], color='teal', alpha=0.5)
	ax1.plot(time, angle,'bD',markevery=idx_peaksAngle.tolist())
	ax3.plot(time, device1_positionMeasured,'gD',markevery=idx_peaksPositionMeasured.tolist())
	plt.title("Time Delay = %.2f ms" % (t_d*1000), name='Arial')

	l_all = l1+l2+l3#+l4
	labels = [l.get_label() for l in l_all]

	plt.grid(True)
	ax1.legend(l_all, labels, loc=0)
	if s==1: plt.savefig(p +"fig_"+fileName[:-4])
	plt.show()
	

def plot_TwoTactor(s, p, fileName, time, angle, force, device1_positionMeasured, t_d, t_peakDelays, idx_peaksAngle, idx_peaksPositionMeasured):
	fig, axs = plt.subplots(3)
	plt.suptitle("Real-time Data " + fileName[4:-4], name='Arial', weight='bold')
	axs[2].set_xlabel("Time (s)", name='Arial')
	plt.xticks(name='Arial')
	plt.yticks(name='Arial')
	axs2 = axs[1].twinx()
	axs3 = axs[2].twinx()

	axs[0].set_ylabel("Angle (degrees)", name='Arial')
	l1 = axs[0].plot(time, angle, 'b', linewidth=1.75, label='Angle')
	axs[0].yaxis.label.set_color('b')
	axs[0].tick_params(axis='y', color='b')
	axs[0].set_ylim(0,200)
	axs[0].spines['left'].set_color('b')

	axs[1].set_ylabel("Force (N)", name='Arial')
	l2 = axs[1].plot(time, force, 'r', linewidth=1.75, label='Force')
	axs[1].yaxis.label.set_color('r')
	axs[1].tick_params(axis='y', color='r')
	axs[1].set_ylim(0,15)
	axs2.spines['left'].set_color('r')

	axs2.set_ylabel("Actuator Position (mm)", name='Arial')
	l3 = axs2.plot(time, device1_positionMeasured, 'g', linewidth=1.75, label='Actuator Position (Measured)')
	axs2.yaxis.label.set_color('g')
	axs2.tick_params(axis='y', color='g')
	axs2.set_ylim(0,20)
	axs2.spines['right'].set_color('g')

	axs[2].set_ylabel("Force (N)", name='Arial')
	# l2 = axs[1].plot(time, force, 'r', linewidth=1.75, label='Force')
	axs[2].yaxis.label.set_color('r')
	axs[2].tick_params(axis='y', color='r')
	axs[2].set_ylim(0,15)
	axs3.spines['left'].set_color('r')

	axs3.set_ylabel("Actuator Position (mm)", name='Arial')
	#l3 = axs2.plot(time, device1_positionMeasured, 'g', linewidth=1.75, label='Actuator Position (Measured)')
	axs3.yaxis.label.set_color('g')
	axs3.tick_params(axis='y', color='g')
	axs3.set_ylim(0,20)
	axs3.spines['right'].set_color('g')
	if s==1: plt.savefig(p +"fig_"+fileName[4:-4])
	plt.show()
	
