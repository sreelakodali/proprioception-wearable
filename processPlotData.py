# Processing & Plotting Serial Data from Sensory Substitution Devce 
# Written by: Sreela Kodali (kodali@stanford.edu) 

import csv
import os
import datetime
import shutil
import numpy as np
import pandas as pd
from scipy import signal # import lfilter, lfilter_zi, filtfilt, butter
# from scipy.signal import lfilter, lfilter_zi, filtfilt, butter
from operator import itemgetter
import skFunctions as sk
import constants as CONST

# If SD card is the data source, create new folder, copy raw data over
if (CONST.DATASRC_SD):

	# Find the most recent data file on SD card
	newestFile = max([CONST.PATH_SD+d for d in os.listdir(CONST.PATH_SD) if (d.startswith('raw') and d.endswith('.csv'))], key=os.path.getctime)
	print(newestFile)
	print("Newest SD data found: %s" % newestFile)

	# Create new folder on local machine and copy raw data over
	timeStmp = str(datetime.datetime.now())[0:16] # default name is date and time
	timeStmp = ((timeStmp.replace('/', '_')).replace(' ', '_')).replace(':','-')
	p = CONST.PATH_LAPTOP +timeStmp+'/'
	if not (os.path.exists(p)):
		os.makedirs(p)
		print("New directory created: %s" % timeStmp)
	shutil.copyfile(newestFile, (p + 'raw_' + timeStmp + '.csv'))
	print("File copied.")

# Find the most recent data directory
allSubdirs = [CONST.PATH_LAPTOP+d for d in os.listdir(CONST.PATH_LAPTOP) if os.path.isdir(os.path.join(CONST.PATH_LAPTOP, d))]
p = max(allSubdirs, key=os.path.getctime) + '/'
print(p)
fileName = [f for f in os.listdir(p) if (f.startswith('processed') and f.endswith('.csv'))]
fileName = fileName[0]
print("Newest data found: %s" % fileName)

# If raw data, process
if fileName.startswith('raw_'):

	dataFunc = {'time':sk.millisToSeconds, 'flex sensor':sk.computeAngle,'actuator position, command':sk.commandToPosition, \
			'actuator position, measured':sk.feedbackToPosition, 'force':sk.computeForce}

	# Create new csv to store processed data
	f = open(p + 'processed_' + fileName[4:], 'w+', encoding='UTF8', newline='')
	writer = csv.writer(f)
	writer.writerow(list(dataFunc.keys()))

	# Process each data row and save to new file
	i = 0
	with open(p + fileName, 'r') as read_obj:
		csv_reader = csv.reader(read_obj)
		for row in csv_reader:
			# if valid data packet, convert to right units and write in csv
			if (sk.validPacket(row)):
				newRow = sk.processNewRow(row, i)
				#print(newRow)
				writer.writerow(newRow)
			i = i + 1
	f.close()

	# change fileName to processed
	fileName = 'processed_' + fileName[4:]
	print("Newly processed data is in: %s" % fileName)


# fileSrc = "MOST_RECENT"
# opts, args = getopt.getopt(sys.argv[1:],"",["fileSrc"])


# for opt, arg in opts:

# 	if opt == "--fileSrc":
# 		fileSrc = arg
# 		if (arg == 'MOST_RECENT'):
# 			fileSrcRecent = True
# 		else:
# 			fileSrcRecent = False

# Read in processsed data and plot data
data = pd.read_csv(p + fileName, delimiter = ",").astype(float)
time = data['time'].tolist()
angle = data['flex sensor'].tolist() # angle
device1_positionCommand = data['actuator position, command'].tolist()
device1_positionMeasured = data['actuator position, measured'].tolist()
force  = data['force'].tolist()

# trial = data['Trial Number'].tolist()
# targetAngle  = data['Target Angle'].tolist()

# t_diff = sk.evaluatePilotPerformance(time, trial, targetAngle)
# #print(t_diff)
# sk.plot_pilotResults(t_diff)
t_dCC, t_peakDelaysCC, idx_peaksAngleCC, idx_peaksPositionMeasuredCC = sk.delayCrossCorrelation(angle, device1_positionMeasured, time)
print("Time delay between signals (cross correlation): " + str(t_dCC*1000) + " ms")

t_dPP, t_peakDelaysPP, idx_peaksAnglePP, idx_peaksPositionMeasuredPP = sk.delayPeakToPeak(angle, device1_positionMeasured, time)
print("Time delay between signals (peak to peak): " + str(t_dPP*1000) + " ms")
#print(t_peakDelaysPP)

# t_dCC_command, _ , _ , _ = sk.delayCrossCorrelation(device1_positionCommand, device1_positionMeasured, time)
# print("Time delay between signals (cross correlation): " + str(t_dCC_command*1000) + " ms")

# t_dPP_command, _ , _ , _ = sk.delayPeakToPeak(device1_positionCommand, device1_positionMeasured, time)
# print("Time delay between signals (peak to peak): " + str(t_dPP_command*1000) + " ms")
# #print(t_peakDelaysPP)

# plot
# x=9
# y=90
# sk.plot_System(0, p, fileName, time[x:y], angle[x:y], force[x:y], device1_positionMeasured[x:y], device1_positionCommand[x:y])
sk.plot_System(0, p, fileName, time, angle, force, device1_positionMeasured, device1_positionCommand)
sk.plot_SystemWithDelay(0, p, fileName, time, angle, force, device1_positionMeasured, t_dCC, t_peakDelaysCC, idx_peaksAngleCC, idx_peaksPositionMeasuredCC)
#sk.plot_TwoTactor(0, p, fileName, time, angle, force, device1_positionMeasured, t_d, t_peakDelays, idx_peaksAngle, idx_peaksPositionMeasured)