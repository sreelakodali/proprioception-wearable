# Timing Analysis of Actuator
# Written by: Sreela Kodali (kodali@stanford.edu) 

import serial
import sys
import getopt
import math
import statistics as stat
import datetime
import csv
import os
import numpy as np
import pandas as pd
from operator import itemgetter
from scipy import signal # import lfilter, lfilter_zi, filtfilt, butter
# from scipy.signal import lfilter, lfilter_zi, filtfilt, butter
from scipy.ndimage import median_filter
import constants as CONST
import skFunctions as sk


RUNTIME_LENGTH = 30 # seconds

actuatorType = 1
material = "cow"

readRealTimeData = False
computeDelay = True
fileSrc = "MOST_RECENT"
fileSrcRecent = True
measureDelay_force = True
showWindow = False

window_size = 200#120 # changed from 200
edgeWindow = 30
minThresh = 1  #5 for actuator position

# -a actuator type
# -displayWindow whether or not to display zoomed in windows measuring the delays between rising edges
opts, args = getopt.getopt(sys.argv[1:],"a:",["realTime","computeDelay", "fileSrc=", "measureFromPos", "windowSize=", "displayWindow"])

for opt, arg in opts:
	if opt == "-a":
		actuatorType = int(arg)

	if opt == "--realTime":
		readRealTimeData = True
		computeDelay = False

	if opt == "--computeDelay":
		computeDelay = True

	if opt == "--fileSrc":
		fileSrc = arg
		if (arg == 'MOST_RECENT'):
			fileSrcRecent = True
		else:
			fileSrcRecent = False

	if opt == "--measureFromPos":
		measureDelay_force = False

	if opt == "--windowSize":
		window_size = int(arg)

	if opt == "--displayWindow":
		showWindow = True

# Read data from serial
if (readRealTimeData == True):
	fileName = str(datetime.datetime.now())[0:16] # default name is date and time
	fileName = ((fileName.replace('/', '_')).replace(' ', '_')).replace(':','-')
	fileName = fileName+"_actuatorType"+str(actuatorType)+"_"+material
	p = CONST.PATH_LAPTOP +fileName+'/'
	if not (os.path.exists(p)):
		os.makedirs(p)
		print("New directory created: %s" % fileName)

	mcu = serial.Serial(port=CONST.PORT_NAME, baudrate=CONST.BAUD_RATE, timeout=.1)
	f = open(p + fileName + '.csv', 'w+', encoding='UTF8', newline='')
	writer = csv.writer(f)
	writer.writerow(['t1', 't2', 'command', 'force', 'position'])

	# Read in serial data and save in csv
	endTime = datetime.datetime.now() + datetime.timedelta(seconds=RUNTIME_LENGTH)
	while (datetime.datetime.now() < endTime):
		value = mcu.readline()
		value = str(value, "utf-8").split(",")
		print(value[0:5])
		writer.writerow(value[0:5])
	f.close()

if (computeDelay == True):
	if (fileSrcRecent == True):
		allSubdirs = [CONST.PATH_LAPTOP+d for d in os.listdir(CONST.PATH_LAPTOP) if os.path.isdir(os.path.join(CONST.PATH_LAPTOP, d))]
		p = max(allSubdirs, key=os.path.getctime) + '/'
		fileName = [f for f in os.listdir(p) if (f.endswith('.csv'))]
		fileName = fileName[0]
		print("Newest data found: %s" % fileName)

	else:
		fileName = fileSrc+".csv"
		p = "/Users/Sreela/Documents/School/Stanford/Year3_2/PIEZO2/Data/Timing/" + fileSrc + "/"
		print(fileName)

	# Read in processsed data and plot data
	data = pd.read_csv(p + fileName, delimiter = ",").astype(float)
	t1 = list(map(sk.millisToSeconds, data['t1'].tolist()))
	t2 = list(map(sk.millisToSeconds, data['t2'].tolist()))
	force = list(map(sk.computeForce, data['force'].tolist()))
	forceRaw = data['force'].tolist()
	commandRaw = data['command'].tolist()

	if (actuatorType == 2):
		positionCommand = list(map(sk.commandToPosition_Actuator2, data['command'].tolist()))
		position = []
	elif (actuatorType == 1):
		positionCommand = list(map(sk.commandToPosition, data['command'].tolist()))
		position = list(map(sk.feedbackToPosition, data['position'].tolist()))
		positionRaw = data['position'].tolist()

	# Filtering
	# order = 10
	# fs = 158       
	# cutoff = 2.5
	# force = sk.butter_lowpass_filter(force, cutoff, fs, order)
	# force = median_filter(force, 500)

	sk.plot_timingActuatorAll(0, p, fileName, t2, positionCommand, position, force, actuatorType)

	l = len(t2) / window_size 
	t_delay = []
	t_risingEdge = []
	correspondingCommands = []
	correspondingTimes = []
	if (not(measureDelay_force)): speed = []

	i = 1
	if (i >= 0):
	# for i in range(math.floor(l)-1):#range(6):#
		print(i)
		t = t2[i*window_size:i*window_size+window_size]
		c_raw = commandRaw[i*window_size:i*window_size+window_size]
		c = positionCommand[i*window_size:i*window_size+window_size]
		idx_startC, idx_endC,  deltaCommand = sk.findRisingEdge(c_raw, t, 1, edgeWindow, measureDelay_force)

		# switch
		if (measureDelay_force):
			m_raw = forceRaw[i*window_size+idx_endC:i*window_size+window_size]
			m =  force[i*window_size:i*window_size+window_size]
		else:
			m_raw = positionRaw[i*window_size+idx_endC:i*window_size+window_size]
			m =  position[i*window_size:i*window_size+window_size]
		
		idx_startM, idx_endM, delta = sk.findRisingEdge(m_raw, t, 1, 60, measureDelay_force)
		idx_startM = idx_startM + idx_endC
		idx_endM = idx_endM + idx_endC

		check1 = (idx_endC > idx_startC) and (idx_endM > idx_startM)
		check2 = (idx_startM > idx_startC)
		check3 = (not((idx_startM == 0) and (idx_endM == 0)))

		# optional fix: rising edge doesn't distinguish between rising and falling and looks at one signal at a time
		# so sometimes the edge found for measured signal is noise and before the command rising edge


		if (check1 and check2 and check3):
			td = t[idx_endM] - t[idx_endC]
			tRE = t[idx_endM] - t[idx_startM]
			if (not(measureDelay_force)): s = sk.actuatorSpeed(delta, tRE) # switch
			print("t_delay ="+str(td))
			print("t_risingEdge =" + str(tRE))
			t_delay.append(td)
			t_risingEdge.append(tRE)
			if (not(measureDelay_force)): speed.append(s) # mm/s # switch
			correspondingCommands.append(c[idx_endC])
			correspondingTimes.append(t[idx_endC])
		if (showWindow == True):
			sk.plot_timingActuatorWindow(0, p, fileName, t, c, m, idx_startC, idx_endC, idx_startM, idx_endM, measureDelay_force) # switch force or position

	if (len(t_delay) > 0):
		print(sum(t_delay)/len(t_delay))
		print(stat.median(t_delay))
	#print(t_risingEdge)
	if (not(measureDelay_force)): print(speed)
	#print(correspondingCommands)

	sk.plot_timingActuatorAnalysis(0, p, fileName, t_delay, t_risingEdge, [], correspondingCommands, 0)

	# # Create new csv to store processed data
	# f = open(p + 'processed_' + fileName[4:], 'w+', encoding='UTF8', newline='')
	# writer = csv.writer(f)

	# # Process each data row and save to new file
	# with open(p + fileName, 'r') as read_obj:
	# 	csv_reader = csv.reader(read_obj)
	# 	for row in csv_reader:
	# 		# if valid data packet, convert to right units and write in csv
	# 		if (len(row) == 4):
	# 			row[3] = row[3].strip()
	# 			#print(row)
	# 			writer.writerow(row)

	# 		i = i + 1
	# 		# if (i == 500):
	# 		# 	break
	# f.close()

# 	# change fileName to processed
# 	fileName = 'processed_' + fileName[4:]
# 	print("Newly processed data is in: %s" % fileName)