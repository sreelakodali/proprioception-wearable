# Timing Analysis of Firmware
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

actuatorType = 1

measureDelay_force = True # switch
RUNTIME_LENGTH = 30 # seconds
material = "cow"

readRealTimeData = False
computeDelay = True
fileSrc = "MOST_RECENT"
fileSrcRecent = True

opts, args = getopt.getopt(sys.argv[1:],"",["realTime=","computeDelay=", "fileSrc=", "delayFrom=", "windowSize="])

for opt, arg in opts:
	if opt == "--realTime":
		if (arg == 'y'):
			readRealTimeData = True
		elif (arg == 'n'):
			realRealTimeData = False

	if opt == "--computeDelay":
		if (arg == 'y'):
			computeDelay = True
		elif (arg == 'n'):
			computeDelay = False

	if opt == "--fileSrc":
		fileSrc = arg
		if (arg == 'MOST_RECENT'):
			fileSrcRecent = True
		else:
			fileSrcRecent = False
	if opt == "--delayFrom":
		if (arg == 'force'):
			measureDelay_force = True
		elif (arg == 'pos'):
			measureDelay_force = False

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


	if (actuatorType == 2):
		sk.plot_timingAll(0, p, fileName, t2, positionCommand, [], force, actuatorType)
	if (actuatorType == 1):
		sk.plot_timingAll(0, p, fileName, t2, positionCommand, position, force, actuatorType)


	window_size = 200#120 # changed from 200
	edgeWindow = 30
	minThresh = 5  #5 for actuator position

	l = len(t2) / window_size 
	t_delay = []
	t_risingEdge = []
	correspondingCommands = []
	correspondingTimes = []
	if (not(measureDelay_force)): speed = []

	# i = 0
	# if (i >= 0):
	for i in range(math.floor(l)-1):#range(6):#
		print(i)
		t = t2[i*window_size:i*window_size+window_size]
		c = commandRaw[i*window_size:i*window_size+window_size]
		c_all = positionCommand[i*window_size:i*window_size+window_size]
		idx_startC, idx_endC,  deltaCommand = sk.findRisingEdge(c, t, 1, edgeWindow)

		# switch
		if (measureDelay_force):
			m = forceRaw[i*window_size:i*window_size+window_size]
			m_all =  force[i*window_size:i*window_size+window_size]
		else:
			m = positionRaw[i*window_size:i*window_size+window_size]
			m_all =  position[i*window_size:i*window_size+window_size]
		
		idx_startM, idx_endM, delta = sk.findRisingEdge(m, t, 1, edgeWindow)		

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
			#sk.plot_timingAll(0, p, fileName, t2, commandMapped, measuredMapped, idx_startC, idx_endM, i)
		#sk.plot_timingWindow(0, p, fileName, t, c_all, m_all, idx_startC, idx_endC, idx_startM, idx_endM, measureDelay_force) # switch force or position
			#sk.plot_timingWindow(0, p, fileName, t, command[i*window_size:i*window_size+200], m_all, idx_startC, idx_endC, idx_startM, idx_endM, measureDelay_force) # switch force or position

	print(sum(t_delay)/len(t_delay))
	print(stat.median(t_delay))
	print(t_risingEdge)
	if (not(measureDelay_force)): print(speed)
	#print(correspondingCommands)

	sk.plot_timingAnalysis(0, p, fileName, t_delay, t_risingEdge, [], correspondingCommands, 0)
	sk.plot_timingAnalysis(0, p, fileName, t_delay, t_risingEdge, [], correspondingTimes, 1)


# 	# Create new csv to store processed data
# 	f = open(p + 'processed_' + fileName[4:], 'w+', encoding='UTF8', newline='')
# 	writer = csv.writer(f)

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