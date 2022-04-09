# Reading and Saving Serial Data from Sensory Substitution Devce 
# Written by: Sreela Kodali (kodali@stanford.edu) 

import serial
import datetime
import csv
import os
import numpy as np
from scipy import signal
import skFunctions as sk
import constants as CONST

## CONSTANTS
RUNTIME_LENGTH = 30 # seconds
PORT_NAME = "/dev/cu.usbmodem1101"

# DIRECTORY
fileName = str(datetime.datetime.now())[0:16] # default name is date and time
fileName = ((fileName.replace('/', '_')).replace(' ', '_')).replace(':','-')
p = CONST.PATH +fileName+'/'
if not (os.path.exists(p)):
	os.makedirs(p)
	print("New directory created")

dataFunc = {'time':sk.millisToSeconds, 'flex sensor':sk.computeAngle,'actuator position, command':sk.commandToPosition, \
			'actuator position, measured':sk.feedbackToPosition, 'force':sk.computeForce}
columnNames = list(dataFunc.keys())

mcu = serial.Serial(port=PORT_NAME, baudrate=57600, timeout=.1)
f = open(p + 'raw_' + fileName + '.csv', 'w+', encoding='UTF8', newline='')
writer = csv.writer(f)
writer.writerow(list(dataFunc.keys()))

# Read in serial data and save in csv
i = 0
endTime = datetime.datetime.now() + datetime.timedelta(seconds=RUNTIME_LENGTH)
while (datetime.datetime.now() < endTime):
	value = mcu.readline()
	value = str(value, "utf-8").split()

	# if valid data packet, convert to right units and write in csv
	if (len(value) == len(dataFunc)):
		newRow = processNewRow(value, i)
		print(newRow)
		writer.writerow(newRow)
	i = i + 1
	# writer.writerow(str(value, "utf-8").split(mcuDataDelimiter))
f.close()