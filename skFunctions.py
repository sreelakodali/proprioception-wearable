# Supporting Functions for Sensory Substitution Devce 
# Written by: Sreela Kodali (kodali@stanford.edu) 

import numpy as np
from scipy import signal
import constants as CONST
from operator import itemgetter
import matplotlib.pyplot as plt


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
	return float(data)/64.0 #data

# Function 3: Servo command (degrees) --> actuator position (mm)
def commandToPosition(c):
	return 0.22*c - 10.7

# Function 4: Feedback signal from actuator (1/1024th of V) to actuator position (mm)
def feedbackToPosition(f):
	return mapFloat(f, CONST.ACTUATOR_FEEDBACK_MIN, CONST.ACTUATOR_FEEDBACK_MAX, CONST.ACTUATOR_POSITION_MAX, CONST.ACTUATOR_POSITION_MIN)

# Function 5: Digital value from force sensor --> force measurement (N)
def computeForce(data):
	return (data - 256) * (45.0)/511

dataFunc = {'time':millisToSeconds, 'flex sensor':computeAngle,'actuator position, command':commandToPosition, \
			'actuator position, measured':feedbackToPosition, 'force':computeForce}
columnNames = list(dataFunc.keys())

def processNewRow(val, loopIncrement):
	r = []
	for key in dataFunc:
		if (val[columnNames.index(key)].lstrip("-").rstrip().isnumeric()): # why did I remove negatives
			#print("%s numeric - yep" % str(key))
			x = dataFunc[key](float(val[columnNames.index(key)]))
			# if (loopIncrement < 20 and key == 'time' and x > 2):
			# 	break
			r.append(x)
	return r

def findNWindow(timeArr):
	i = 1
	while ((timeArr[i] - timeArr[0]) < 1):
		i+=1
	return i

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

	idx_peaksPositionMeasured, _ = signal.find_peaks(np.asarray(positionMeasured), height=(6,20), distance=n_window)
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
	idx_peaksPositionMeasured, _ = signal.find_peaks(np.asarray(positionMeasured), height=(6,20), distance=n_window)
	idx_peaksPositionMeasured = idx_peaksPositionMeasured.tolist()
	t_peaksPositionMeasured = list(itemgetter(*idx_peaksPositionMeasured)(timeArr))

	idx_peaksAngle, _ = signal.find_peaks(np.asarray(angle), height=(30,180), distance=n_window)
	idx_peaksAngle = idx_peaksAngle.tolist()
	t_peaksAngle = list(itemgetter(*idx_peaksAngle)(timeArr))

	t_d = 0
	n_pairs = 0
	for i in range(0,min(len(t_peaksAngle), len(t_peaksPositionMeasured))):
		diff = t_peaksPositionMeasured[i] - t_peaksAngle[i]
		if (diff < 1.0):
			t_d += diff
			n_pairs += 1
	t_d = t_d / n_pairs
	t_peakDelays = list(zip(t_peaksAngle, t_peaksPositionMeasured))

	return t_d, t_peakDelays, idx_peaksAngle, idx_peaksPositionMeasured

def plot_OneTactor(s, p, fileName, time, angle, force, device1_positionMeasured, t_d):
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
	# for d in t_peakDelays:
	# 	ax1.axvspan(d[0], d[1], color='teal', alpha=0.5)
	# ax1.plot(time, angle,'bD',markevery=idx_peaksAngle)
	# ax3.plot(time, device1_positionMeasured,'gD',markevery=idx_peaksPositionMeasured)
	plt.title("Time Delay = %.2f ms" % (t_d*1000), name='Arial')

	l_all = l1+l2+l3#+l4
	labels = [l.get_label() for l in l_all]

	plt.grid(True)
	ax1.legend(l_all, labels, loc=0)
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
	
