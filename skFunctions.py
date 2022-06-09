# Supporting Functions for Sensory Substitution Devce 
# Written by: Sreela Kodali (kodali@stanford.edu) 

import numpy as np
import math
from scipy import signal
import constants as CONST
from operator import itemgetter
import matplotlib
matplotlib.use("TkAgg")
from matplotlib import pyplot as plt
import constants as CONST
import random


## CALIBRATION
# zero force
# max position and force of user
# min position and force for user (detection)

## FUNCTIONS ##
# Offloading computation that isn't needed real-time to computer

# Function 0: Mapping float value x in different range 
def mapFloat(x, in_min, in_max, out_min, out_max):
	return (float) ((x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min)

# Function 1: millisecond --> second
def millisToSeconds(s):
	return s/1000

# Function 2: place holder for angle function
def computeAngle(data):
	a = 180 - float(data)/64.0 #float(data)
	return a
	#if a > 90: return a
	#else: return a - 0.2*(90-a)
	 
	#mapFloat(data, CONST.ANGLE_DATA_MIN, CONST.ANGLE_DATA_MAX, CONST.ANGLE_MIN, CONST.ANGLE_MAX)

# Function 3: Servo command (degrees) --> actuator position (mm)
def commandToPosition(c):
	return mapFloat(c, CONST.ACTUATOR_COMMAND_MIN, CONST.ACTUATOR_COMMAND_MAX, CONST.ACTUATOR_POSITION_MIN, CONST.ACTUATOR_POSITION_MAX)
	#return 0.22*c - 10.7

# Function 4: Feedback signal from actuator (1/1024th of V) to actuator position (mm)
def feedbackToPosition(f):
	return mapFloat(f, CONST.ACTUATOR_FEEDBACK_MIN, CONST.ACTUATOR_FEEDBACK_MAX, CONST.ACTUATOR_POSITION_MAX, CONST.ACTUATOR_POSITION_MIN)

# delta change in feedback signal results in how much change in actuator position in mm
# slope of the previous function
# returns mm
def delta_feedbackToPosition(delta):
	return delta*CONST.ACTUATOR_POSITION_MAX/(CONST.ACTUATOR_FEEDBACK_MAX-CONST.ACTUATOR_FEEDBACK_MIN)

# Function 5: Digital value from force sensor --> force measurement (N)
def computeForce(data):
	return ((data - 255) * (45.0)/511) - CONST.ZERO_FORCE #(data - 256) * (45.0)/511 
	#changed bc uncalibrated

dataFunc = {'time':millisToSeconds, 'flex sensor':computeAngle,'actuator position, command':commandToPosition, \
			'actuator position, measured':feedbackToPosition, 'force':computeForce}
columnNames = list(dataFunc.keys())

def processNewRow(val, loopIncrement):
	r = []
	for key in dataFunc:
		# if (key == 'flex sensor'):
		# 	#print(float(val[columnNames.index(key)]))
		# 	x = dataFunc[key](float(val[columnNames.index(key)]))
		# 	r.append(x)
		if (val[columnNames.index(key)].lstrip("-").rstrip().isnumeric()): # negatives removed otherwise seen as char
			x = dataFunc[key](float(val[columnNames.index(key)]))
			# old code, if serial flush pushes garbage
			# if (loopIncrement < 20 and key == 'time' and x > 2):
			# 	break
			r.append(x)
	return r

def validPacket(val):
	if (len(val) == len(dataFunc)):
		forceData = float(val[(len(dataFunc)-1)].lstrip("-").rstrip())
		if (forceData > 100): 
			return True
	return False

def generateRandomTrials():
	trialAngles = []
	for i in range (0,6):
		t = list(range(40,180,15))
	
		if i < 2:
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
	
		else: random.shuffle(t)
		trialAngles = trialAngles + t
	return trialAngles

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

def findRisingEdge(s, t, minThresh, w):
	avg1 = sum(s[:w])/len(s[:w])
	avg2 = sum(s[-w:])/len(s[-w:])
	# print(avg1)
	# print(avg2)

	ix_start = 0
	ix_end = 0
	avgThresh = 0

	# check if edge present
	if (abs(avg2 - avg1) >= minThresh):
		avgThresh = math.floor(abs(avg2 - avg1))
		#print(avgThresh)

		for i in range(len(s) - w):
			a = s[w+i]
			if (abs(a-avg1) >= avgThresh):
				ix_end = w+i
				break

		if (ix_end > 0):
			for i in range(ix_end-1, ix_end-w, -1):
				b = s[i]
				# print(i)
				# print(abs(s[ix_end] - b))
				if(abs(s[ix_end] - b) >= avgThresh):
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
		maxCorr.append(timeArr[i+np.argmax(c)] - timeArr[i])
		#maxCorr.append(np.argmax(c))

	t_d = np.mean(maxCorr)

	idx_peaksPositionMeasured, _ = signal.find_peaks(np.asarray(positionMeasured), height=(6,25), distance=n_window)
	idx_peaksPositionMeasured = idx_peaksPositionMeasured.tolist()
	t_peaksPositionMeasured = list(itemgetter(*idx_peaksPositionMeasured)(timeArr))

	idx_peaksAngle = []
	for t in t_peaksPositionMeasured:
		t = t - t_d
		idx_peaksAngle.append((np.abs(timeArr-t)).argmin())
	t_peaksAngle = list(itemgetter(*idx_peaksAngle)(timeArr))

	t_peakDelays = list(zip(t_peaksAngle, t_peaksPositionMeasured))

	return t_d, t_peakDelays, idx_peaksAngle, idx_peaksPositionMeasured

def delayPeakToPeak(angle, positionMeasured, timeArr):
	n_window = findNWindow(timeArr)

	max_peaksPositionMeasured = signal.argrelextrema(np.asarray(positionMeasured), np.greater)
	min_peaksPositionMeasured = signal.argrelextrema(np.asarray(positionMeasured), np.less)
	#idx_peaksPositionMeasured, _ = signal.find_peaks(np.asarray(positionMeasured), height=(0,25), distance=n_window)
	idx_peaksPositionMeasured = max_peaksPositionMeasured[0].tolist() + min_peaksPositionMeasured[0].tolist()

	t_peaksPositionMeasured = list(itemgetter(*idx_peaksPositionMeasured)(timeArr))
	#print(t_peaksPositionMeasured)

	max_peaksAngle = signal.argrelextrema(np.asarray(angle), np.greater)
	min_peaksAngle = signal.argrelextrema(np.asarray(angle), np.less)
	#idx_peaksAngle, _ = signal.find_peaks(np.asarray(angle), height=(0,180), distance=n_window)
	idx_peaksAngle = max_peaksAngle[0].tolist() + min_peaksAngle[0].tolist()

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

def plot_timingAll(s, p, fileName, time, command, measured):
	fig, ax1 = plt.subplots()
	plt.suptitle("All Timing Data " + fileName[:-4], name='Arial', weight='bold')
	ax1.set_xlabel("Time (ms)", name='Arial')
	plt.xticks(name='Arial')
	plt.yticks(name='Arial')

	ax1.set_ylabel("Actuator Position (mm)", name='Arial')
	ax1.plot(time, command, 'mediumaquamarine', time, measured, 'g')
	ax1.set_ylim(0,21)

	#l_all = l1#+l2#+l3#+l4
	#labels = [l.get_label() for l in l_all]

	plt.grid(True)
	#ax1.legend(l_all, labels, loc=0)
	if s==1: plt.savefig(p +"fig_"+fileName[:-4])
	plt.show()


def plot_timingWindow(s, p, fileName, time, command, measured, i_startC, i_endC, i_startM, i_endM):
	fig, ax1 = plt.subplots()
	plt.suptitle("Window of Timing Data " + fileName[:-4], name='Arial', weight='bold')
	ax1.set_xlabel("Time (ms)", name='Arial')
	plt.xticks(name='Arial')
	plt.yticks(name='Arial')

	ax1.set_ylabel("Actuator Position (mm)", name='Arial')
	ax1.plot(time, command, 'mediumaquamarine', time, measured, 'g')
	ax1.set_ylim(min(measured)-0.25,max(command)+0.25)

	#l_all = l1#+l2#+l3#+l4
	#labels = [l.get_label() for l in l_all]
	ax1.plot(time, measured,'gD',markevery=[i_startM, i_endM])
	ax1.plot(time, command,'cD',markevery=[i_startC, i_endC])
	
	ax1.axvspan(time[i_startM], time[i_endM], color='lime', alpha=0.5)
	ax1.axvspan(time[i_endC], time[i_endM], color='powderblue', alpha=0.5)

	plt.grid(True)
	#ax1.legend(l_all, labels, loc=0)
	if s==1: plt.savefig(p +"fig_"+fileName[:-4])
	plt.show()

def plot_timingAnalysis(s, p, fileName, t_delay, t_risingEdge, speed, command):
	fig, ax1 = plt.subplots()
	ax2 = ax1.twinx()
	plt.suptitle("Timing Analysis " + fileName[:-4], name='Arial', weight='bold')
	ax1.set_xlabel("Actuator Command", name='Arial')
	plt.xticks(name='Arial')
	plt.yticks(name='Arial')

	ax1.set_ylabel("Time (ms)", name='Arial')
	#ax1.plot(command, t_delay, 'powderblue', command, t_risingEdge, 'c')
	ax1.scatter(command, t_delay, c='powderblue')
	ax1.scatter(command, t_risingEdge, c='c')
	ax1.set_ylim(0,300)

	ax2.set_ylabel("Speed (mm/s)", name='Arial',)
	ax2.scatter(command, speed, c='m')
	#ax2.plot(command, speed, 'm')
	ax2.set_ylim(0,28)

	plt.grid(True)
	#ax1.legend(l_all, labels, loc=0)
	if s==1: plt.savefig(p +"fig_"+fileName[:-4])
	plt.show()



def plot_NoDelay(s, p, fileName, time, angle, force, device1_positionMeasured, device1_positionCommand):
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

	#l4 = ax3.plot(time, device1_positionCommand, color='orange', linewidth=1.75, label='Actuator Position (Command)')

	l_all = l1+l2+l3#+l4
	labels = [l.get_label() for l in l_all]

	plt.grid(True)
	#ax1.legend(l_all, labels, loc=0)
	if s==1: plt.savefig(p +"fig_"+fileName[:-4])
	plt.show()
	

def plot_SingleTactor(s, p, fileName, time, angle, force, device1_positionMeasured, t_d, t_peakDelays, idx_peaksAngle, idx_peaksPositionMeasured):
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
	ax1.plot(time, angle,'bD',markevery=idx_peaksAngle)
	ax3.plot(time, device1_positionMeasured,'gD',markevery=idx_peaksPositionMeasured)
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
	
