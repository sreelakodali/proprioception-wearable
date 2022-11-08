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

# Finding the most recent data file on SD card
newestFile = max([CONST.PATH+d for d in os.listdir(CONST.PATH) if (d.startswith('raw') and d.endswith('.csv'))], key=os.path.getctime)
print(newestFile)
print("Newest data found: %s" % newestFile)

# Create new folder on local machine and copy raw data over
fileName = str(datetime.datetime.now())[0:16] # default name is date and time
fileName = ((fileName.replace('/', '_')).replace(' ', '_')).replace(':','-')
p = CONST.PATH_LAPTOP +fileName+'/'
if not (os.path.exists(p)):
	os.makedirs(p)
	print("New directory created: %s" % fileName)
shutil.copyfile(newestFile, (p + 'raw_' + fileName + '.csv'))
print("File copied.")

dataFunc = {'time':sk.millisToSeconds, 'flex sensor':sk.computeAngle,'actuator position, command':sk.commandToPosition, \
			'actuator position, measured':sk.feedbackToPosition, 'force':sk.computeForce}

# Create new csv to store processed data
f = open(p + 'processed_' + fileName + '.csv', 'w+', encoding='UTF8', newline='')
writer = csv.writer(f)
writer.writerow(list(dataFunc.keys()))

# Process each data row and save to new file
i = 0
with open(p + 'raw_' + fileName + '.csv', 'r') as read_obj:
	csv_reader = csv.reader(read_obj)
	for row in csv_reader:
		# if valid data packet, convert to right units and write in csv
		if (len(row) == len(dataFunc)):
			# for j in range(0,len(row)):
			# 	print(row[j])
			newRow = sk.processNewRow(row, i)
			#print(newRow)
			writer.writerow(newRow)
		i = i + 1
f.close()

# Read in processsed data and plot data
data = pd.read_csv(p + 'processed_' + fileName + '.csv', delimiter = ",").astype(float)
time = data['time'].tolist()
angle = data['flex sensor'].tolist() # angle
device1_positionCommand = data['actuator position, command'].tolist()
device1_positionMeasured = data['actuator position, measured'].tolist()
force  = data['force'].tolist()

t_d = 0#sk.delay(angle, device1_positionMeasured, time)
# print("Time delay between signals: " + str(t_d*1000) + " ms")

# idx_peaksPositionMeasured, _ = signal.find_peaks(np.asarray(device1_positionMeasured), height=(7,20), distance=150)
# idx_peaksPositionMeasured = idx_peaksPositionMeasured.tolist()

# t_peaksPositionMeasured = list(itemgetter(*idx_peaksPositionMeasured)(time))
# idx_peaksAngle = []
# for t in t_peaksPositionMeasured:
# 	t = t - t_d
# 	idx_peaksAngle.append((np.abs(time-t)).argmin())
# t_peaksAngle = list(itemgetter(*idx_peaksAngle)(time))

# t_peakDelays = list(zip(t_peaksAngle, t_peaksPositionMeasured))

# plot 1
sk.plot_OneTactor(0, p, fileName, time, angle, force, device1_positionMeasured, t_d)
#sk.plot_SingleTactor(1, p, fileName, time, angle, force, device1_positionMeasured, t_d, t_peakDelays, idx_peaksAngle, idx_peaksPositionMeasured)
#sk.plot_TwoTactor(0, p, fileName, time, angle, force, device1_positionMeasured, t_d, t_peakDelays, idx_peaksAngle, idx_peaksPositionMeasured)