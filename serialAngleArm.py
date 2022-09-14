# serial angle Study
# Written by: Sreela Kodali (kodali@stanford.edu) 

import numpy as np
import turtle
import serial
import datetime
import csv
import os
import constants as CONST
import skFunctions as sk
import skPilotGraphics as skG
import random

# t = 1
# nTrials = 0
sc = turtle.Screen()

# Initialize GUI
sc.tracer(0)
sc.title("SerialArm")
skG.initializeSerial()

# Initialize Serial reading and data saving
fileName = str(datetime.datetime.now())[0:16] # default name is date and time
fileName = ((fileName.replace('/', '_')).replace(' ', '_')).replace(':','-')
p = CONST.PATH_LAPTOP +fileName+'/'
if not (os.path.exists(p)):
	#os.makedirs(p)
	print("New directory created: %s" % fileName)
mcu = serial.Serial(port=CONST.PORT_NAME, baudrate=CONST.BAUD_RATE, timeout=.1)

dataFunc = {'time':sk.millisToSeconds, 'flex sensor':sk.computeAngle,'actuator position, command':sk.commandToPosition, \
			'actuator position, measured':sk.feedbackToPosition, 'force':sk.computeForce}

endTime = datetime.datetime.now() + datetime.timedelta(seconds=CONST.RUNTIME_LENGTH_ARM)
while (datetime.datetime.now() < endTime):
	value = mcu.readline()
	value = str(value, "utf-8").split(",")

	# if valid data packet, convert to right units and write in csv
	if (len(value) == len(dataFunc)):
		newRow = sk.processNewRow(value, 0)
		serialAngle = newRow[1]
		s = "Measured=" + str(serialAngle)
		print(s)
		turtle.undo()
		turtle.undo()
		skG.drawForearm(sc,serialAngle, skG.COLOR_SERIAL)