	# Reading and Saving Serial Data from MCU
# Written by: Sreela Kodali (kodali@stanford.edu) 

import serial
import datetime
import csv
import os
import numpy as np
from scipy import signal

## CONSTANTS
PATH = '/Users/Sreela/Documents/School/Stanford/Year3_2/PIEZO2/JND_Study/bleData/' # change this to your path!
PORT_NAME = "/dev/cu.usbmodem161767201"#"/dev/cu.usbmodem131752901" # change this to Arduino/teeny's port
BAUD_RATE = 4608000
RUNTIME_LENGTH = 160#570 # secon4ds

setpoints = [1.0, 0.0, 3.0, 0.0, 6.0, 0.0, 10.0, 0.0, 15.0, 0.0, 21.0, 0.0];#14.0, 0.0, 16.0, 0.0, 18.0, 0.0, 20.0, 0.0
waitTime = 10

#DIRECTORY
fileName = str(datetime.datetime.now())[0:16] # default name is date and time
fileName = ((fileName.replace('/', '_')).replace(' ', '_')).replace(':','-')
p = PATH +fileName+'/'
if not (os.path.exists(p)):
	os.makedirs(p)
	print("New directory created: %s" % fileName)

mcu = serial.Serial(port=PORT_NAME, baudrate=BAUD_RATE, timeout=.1)
f = open(p + 'raw_' + fileName + '.csv', 'w+', encoding='UTF8', newline='')
writer = csv.writer(f)

forceGlobal = 0.0 # hold only for non zero
reachedBool = 0

twoPrevious = 0.0
previousPos = 0.0
currentPos = 0.0
fallBool = 0

# Read in serial data and save in csv
idxSetpoint = 0
lastWritten = datetime.datetime.now()
endTime = datetime.datetime.now() + datetime.timedelta(seconds=RUNTIME_LENGTH)
while (datetime.datetime.now() < endTime):

	now = datetime.datetime.now()
	value = mcu.readline()
	value = str(value, "utf-8").split(",")

	if (len(value) > 4):
		raw = [j.rstrip() for j in value]
		#print(raw)
		#print(value[0]) # can also print(value) too
		if (reachedBool == 1):
			raw = ["Reached!"] + raw
			reachedBool = reachedBool + 1
		# elif (fallBool == 1):
		# 	raw = ["Fell!"] + raw
		# 	fallBool = fallBool + 1
		writer.writerow(raw)
		forceGlobal = raw[2]
		# twoPrevious = previousPos
		# previousPos = currentPos
		# currentPos = int(raw[5])

	if (len(value) > 1):
		print(value)

	if (idxSetpoint):
		if ( (abs(float(forceGlobal) - setpoints[idxSetpoint-1]) <=0.13) and (reachedBool == 0) and (setpoints[idxSetpoint-1] > 0)):
			reachedTime = datetime.datetime.now()
			reachedBool = 1
		# elif ( (previousPos-currentPos) > 200):
		# 	fallTime = datetime.datetime.now()
		# 	fallBool = 1


	if((now - lastWritten).total_seconds()  >= waitTime):
		if (idxSetpoint and (setpoints[idxSetpoint-1] > 0) and (idxSetpoint < len(setpoints))):
			stimTime = (datetime.datetime.now() - reachedTime).total_seconds()
			outputStr = "STIM TIME for SETPOINT {}={}\n".format(setpoints[idxSetpoint-1], stimTime)
			print(outputStr)
			#f.write(outputStr)

			if (stimTime >= 8.0):
				mcu.write(str(setpoints[idxSetpoint]).encode())
				idxSetpoint = idxSetpoint+ 1
				reachedBool = 0
				fallBool = 0
				print("SETPOINT=" + str(idxSetpoint))
				lastWritten = datetime.datetime.now()

		elif(idxSetpoint < len(setpoints)):
			mcu.write(str(setpoints[idxSetpoint]).encode())
			idxSetpoint = idxSetpoint+ 1
			reachedBool = 0
			fallBool = 0
			print("SETPOINT=" + str(idxSetpoint))
			lastWritten = datetime.datetime.now()

f.close()