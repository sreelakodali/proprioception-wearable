# Timing Analysis of Firmware
# Written by: Sreela Kodali (kodali@stanford.edu) 

import serial
import math
import datetime
import csv
import os
import numpy as np
import pandas as pd
from operator import itemgetter
from scipy import signal # import lfilter, lfilter_zi, filtfilt, butter
# from scipy.signal import lfilter, lfilter_zi, filtfilt, butter
import constants as CONST
import skFunctions as sk

#DIRECTORY
fileName = str(datetime.datetime.now())[0:16] # default name is date and time
fileName = ((fileName.replace('/', '_')).replace(' ', '_')).replace(':','-')
p = CONST.PATH_LAPTOP +fileName+'/'
if not (os.path.exists(p)):
	os.makedirs(p)
	print("New directory created: %s" % fileName)

mcu = serial.Serial(port=CONST.PORT_NAME, baudrate=CONST.BAUD_RATE, timeout=.1)
f = open(p + fileName + '.csv', 'w+', encoding='UTF8', newline='')
writer = csv.writer(f)
writer.writerow(['t1', 't2', 'command', 'measured'])

# Read in serial data and save in csv
endTime = datetime.datetime.now() + datetime.timedelta(seconds=CONST.RUNTIME_LENGTH)
while (datetime.datetime.now() < endTime):
	value = mcu.readline()
	value = str(value, "utf-8").split(",")
	print(value[0:4])
	writer.writerow(value[0:4])
f.close()


# # Find the most recent data directory
# allSubdirs = [CONST.PATH_LAPTOP+d for d in os.listdir(CONST.PATH_LAPTOP) if os.path.isdir(os.path.join(CONST.PATH_LAPTOP, d))]
# p = max(allSubdirs, key=os.path.getctime) + '/'
# fileName = [f for f in os.listdir(p) if (f.endswith('.csv'))]
# fileName = fileName[0]
# print("Newest data found: %s" % fileName)

# # Read in processsed data and plot data
# data = pd.read_csv(p + fileName, delimiter = ",").astype(float)
# t1 = list(map(sk.millisToSeconds, data['t1'].tolist()))
# t2 = list(map(sk.millisToSeconds, data['t2'].tolist()))
# commandMapped = list(map(sk.commandToPosition, data['command'].tolist()))
# measuredMapped = list(map(sk.feedbackToPosition, data['measured'].tolist()))
# command = data['command'].tolist()
# measured = data['measured'].tolist()

# #sk.plot_timingAll(0, p, fileName, t2, commandMapped, measuredMapped)

# window_size = 200
# edgeWindow = 30
# minThresh = 5

# l = len(t2) / window_size 
# t_delay = []
# t_risingEdge = []
# speed = []
# correspondingCommands = []

# # i = 0
# # if (i >= 0):
# for i in range(math.floor(l)-1):#range(6):#
# 	t = t2[i*window_size:i*window_size+200]
# 	c = command[i*window_size:i*window_size+200]
# 	m = measured[i*window_size:i*window_size+200]

# 	idx_startC, idx_endC,  deltaCommand = sk.findRisingEdge(c, t, 1, edgeWindow)
# 	idx_startM, idx_endM, deltaMeasured = sk.findRisingEdge(m, t, minThresh, edgeWindow)

# 	if (not((idx_startM == 0) and (idx_endM == 0))):
# 		td = t[idx_endM] - t[idx_endC]
# 		tRE = t[idx_endM] - t[idx_startM]
# 		s = sk.actuatorSpeed(deltaMeasured, tRE)


# 		t_delay.append(td)
# 		t_risingEdge.append(tRE)
# 		speed.append(s) # mm/s
# 		correspondingCommands.append(c[idx_endC])
# 		#sk.plot_timingWindow(0, p, fileName, t2[i*window_size:i*window_size+200], commandMapped[i*window_size:i*window_size+200], measuredMapped[i*window_size:i*window_size+200], idx_startC, idx_endC, idx_startM, idx_endM)

# #print(t_delay)
# #print(t_risingEdge)
# # print(speed)
# #print(correspondingCommands)
# sk.plot_timingAnalysis(0, p, fileName, t_delay, t_risingEdge, speed, correspondingCommands)



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