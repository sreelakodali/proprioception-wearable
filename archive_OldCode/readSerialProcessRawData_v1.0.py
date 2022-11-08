# Reading, Saving, & Plotting Serial Data from Sensory Substitution Devce 
# Written by: Sreela Kodali (kodali@stanford.edu) 

import serial
import datetime
import csv
import os
import numpy as np
import pandas as pd
from scipy import signal, stats# import lfilter, lfilter_zi, filtfilt, butter
# from numpy.random import randn
# from scipy.signal import lfilter, lfilter_zi, filtfilt, butter
import matplotlib.pyplot as plt
from operator import itemgetter

## CONSTANTS
RUNTIME_LENGTH = 30 # seconds
PORT_NAME = "/dev/cu.usbmodem1101"

N_CORR = 1000
N_WINDOW = 85

ACTUATOR_FEEDBACK_MIN = 9
ACTUATOR_FEEDBACK_MAX = 606
ACTUATOR_POSITION_MIN = 0.0
ACTUATOR_POSITION_MAX = 20.0


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
	return data #float(bin(data))
	#format(255, '008b')
# Function 3: Servo command (degrees) --> actuator position (mm)
def commandToPosition(c):
	return 0.22*c - 10.7

# Function 4: Feedback signal from actuator (1/1024th of V) to actuator position (mm)
def feedbackToPosition(f):
	return mapFloat(f, ACTUATOR_FEEDBACK_MIN, ACTUATOR_FEEDBACK_MAX, ACTUATOR_POSITION_MAX, ACTUATOR_POSITION_MIN)

# Function 5: Digital value from force sensor --> force measurement (N)
def computeForce(data):
	return (data - 256) * (45.0)/511

def processNewRow(val, loopIncrement):
	r = []
	for key in dataFunc:
		if (val[columnNames.index(key)].lstrip("-").rstrip().isnumeric()):
			x = dataFunc[key](float(val[columnNames.index(key)]))
			if (loopIncrement < 20 and key == 'time' and x > 2): #fixme
				break
			r.append(x)
	return r

def delay(angle, positionMeasured, timeArr):

	ind = np.random.choice(len(timeArr)-N_WINDOW, N_CORR)
	maxCorr = []
	for i in ind:
		a = angle[i:i+85]
		p = positionMeasured[i:i+85]
    
		n = len(a)
		c = signal.correlate(a, p, mode='same') / np.sqrt(signal.correlate(a, a, mode='same')[int(n/2)] * signal.correlate(p, p, mode='same')[int(n/2)])
		maxCorr.append(timeArr[i+np.argmax(c)] - timeArr[i])
		#maxCorr.append(np.argmax(c))
	return np.mean(maxCorr)

# Microcontroller Specs
# mcu = serial.Serial(port=PORT_NAME, baudrate=57600, timeout=.1)

dataFunc = {'time':millisToSeconds, 'flex sensor':computeAngle,'actuator position, command':commandToPosition, 'actuator position, measured':feedbackToPosition, 'force':computeForce}
columnNames = list(dataFunc.keys())

# # Data Collection Specs
path = '/Users/Sreela/Documents/School/Stanford/Year3_2/PIEZO2'
# if not (os.path.exists(path)):
# 	os.makedirs(path)
# 	print("New directory created")
# fileName = str(datetime.datetime.now())[0:16] # default name is date and time
# f = open(path + fileName + '.csv', 'w+', encoding='UTF8', newline='')
# writer = csv.writer(f)
# writer.writerow(list(dataFunc.keys()))

# # Read in serial data and save in csv

# i = 0
# endTime = datetime.datetime.now() + datetime.timedelta(seconds=RUNTIME_LENGTH)
# while (datetime.datetime.now() < endTime):
# 	value = mcu.readline()
# 	value = str(value, "utf-8").split()

# 	# if valid data packet, convert to right units and write in csv
# 	if (len(value) == len(dataFunc)):
# 		newRow = processNewRow(value, i)
# 		print(newRow)
# 		writer.writerow(newRow)
# 	i = i + 1
# 	# writer.writerow(str(value, "utf-8").split(mcuDataDelimiter))
# f.close()


# Read in and plot data
data = pd.read_csv(path+'2022-04-01 17_55'+'.csv', delimiter = ",").astype(float)#(path + fileName + '.csv')
time = data['time'].tolist()
angle = data['flex sensor'].tolist() # angle
device1_positionCommand = data['actuator position, command'].tolist()
device1_positionMeasured = data['actuator position, measured'].tolist()
force  = data['force'].tolist()

# position1_Command = list(map(commandToPosition, position1_Command[20:-1]))
# position1_Measured = list(map(mapResistiveFlex, position1_Measured[20:-1]))
# force = list(map(computeForce, force[20:-1]))

# plot
fig, ax1 = plt.subplots()
fig.subplots_adjust(right=0.75)

ax2 = ax1.twinx()
ax3 = ax1.twinx()
# ax4 = ax1.twinx()
plt.suptitle("Real-time Data " + '2022-04-01 17_55', name='Arial', weight='bold')
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

#l4 = ax2.plot(time, device1_positionCommand, color='orange', linewidth=1.75, label='Actuator Position (Command)')


# local max
# localMax = signal.argrelextrema(np.asarray(device1_positionMeasured), np.greater)
# for i in localMax:
# 	for j in i:
# 		plt.axvline(x=time[j], color='orange')

t_d = delay(angle, device1_positionMeasured, time)
print("Time delay between signals: " + str(t_d) + " s")

idx_peaksPositionMeasured, _ = signal.find_peaks(np.asarray(device1_positionMeasured), height=(7,20), distance=150)
idx_peaksPositionMeasured = idx_peaksPositionMeasured.tolist()

t_peaksPositionMeasured = list(itemgetter(*idx_peaksPositionMeasured)(time))
idx_peaksAngle = []
for t in t_peaksPositionMeasured:
	t = t - t_d
	idx_peaksAngle.append((np.abs(time-t)).argmin())
t_peaksAngle = list(itemgetter(*idx_peaksAngle)(time))

t_peakDelays = list(zip(t_peaksAngle, t_peaksPositionMeasured))

for d in t_peakDelays:
	ax1.axvspan(d[0], d[1], color='teal', alpha=0.5)
ax1.plot(time, angle,'bD',markevery=idx_peaksAngle)
ax3.plot(time, device1_positionMeasured,'gD',markevery=idx_peaksPositionMeasured)
plt.title("Time Delay = %.2f ms" % (t_d*1000), name='Arial')
# ax4.spines['right'].set_position(('axes',1.4))
# ax4.set_ylabel("cross correlation", name='Arial')
# corr = delay(angle, device1_positionMeasured, time)
# print(signal.argrelextrema(corr, np.greater))
# #print(time[signal.argrelextrema(corr, np.greater)])
# l4 = ax4.plot(time, corr, color='orange', label='cross correlation')
# ax4.yaxis.label.set_color('orange')
# ax4.spines['right'].set_color('orange')
# ax4.tick_params(axis='y', color='orange')
# ax4.set_ylim(0,1)

l_all = l1+l2+l3#+l4
labels = [l.get_label() for l in l_all]

plt.grid(True)
ax1.legend(l_all, labels, loc=0)
# plt.savefig(path+"fig_"+fileName)
plt.show()

# d = []
# l = [10, 100, 500, 1000, 10000, 20000, 50000, 80000, 100000]
# for i in l:
# 	d.append(np.mean(delay(angle, device1_positionMeasured, time, i)))
# print(d)
# print(time[int(np.ceil(d[-1]))])
# print(time[int(np.floor(d[-1]))])

# # print(np.mean(d))
# # print(np.median(d))
# # print(stats.mode(d))
# # plt.hist(d)
# plt.plot(l,d, 'bo')
# plt.show()
