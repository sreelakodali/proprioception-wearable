# Calibration 
# Written by: Sreela Kodali (kodali@stanford.edu) 

import serial
import datetime
import csv
import sys
import os
import shutil
import numpy as np
import getopt
from scipy import signal
import constants as CONST
import skFunctions as sk
import turtle
import skPilotGraphics as skG
import random
import skCalibrationFunctions as skC
import time

#CALIBRATION_OPTIONS = {'ACTUATOR':4, 'MAX_PRESSURE': 3, 'FLEX': 2, 'ZERO_FORCE': 1, 'NONE': 0}
CALIBRATION_OPTIONS = {'ACTUATOR':4, 'MAX_PRESSURE': 3, 'NONE': 0}
CALIBRATION_FUNCTIONS = {'ACTUATOR':skC.calibrateActuator, 'MAX_PRESSURE': skC.calibrateMaxPressure, 'FLEX': 2, 'ZERO_FORCE': 1, 'NONE': skC.calibrateDone}

opts, args = getopt.getopt(sys.argv[1:],"",["mode="])
for opt, arg in opts:
	if opt == "--mode": calibrationMode = (CALIBRATION_OPTIONS[arg])

mcu = serial.Serial(port=CONST.PORT_NAME, baudrate=CONST.BAUD_RATE, timeout=.1)
click = 0
lineCount = 0
skipClickForNewText = 0

#----------------------------------------------------------------
def on_click(x, y):
	global click

	# print(x)
	# print(y)

	# Repeat button
	if ((x < -190) and (x > -355) and (y > -250) and (y < -195)):
		click = 2
	# Done button
	elif((x < 280) and (x > 117) and (y > -250) and (y < -195)):
		click = 3
	else: click = 1

def waitforclick():
    global click
    turtle.update()
    click = 0
    while not click:
        turtle.update()
        time.sleep(.2)
    oldClick = click
    click = 0
    return oldClick
#----------------------------------------------------------------



# Default mode
# actuator, welcome, please wear device, max+zero, flex

g = skC.calibrateNewSubject();

sc = turtle.Screen()
sc.tracer(0)
sc.title("Calibration")
turtle.onscreenclick(on_click, btn=1)
turtle.update()
skG.initializeCalibrationWindow(sc, skC.CALIBRATION_TEXT_INTRO)

for i in CALIBRATION_OPTIONS.keys():

	if not(skipClickForNewText): btn = waitforclick()
	else: skipClickForNewText = 0
	skG.initializeCalibrationWindow(sc, skC.CALIBRATION_TEXT[i])
	
	if i == 'MAX_PRESSURE':
		skG.buttons(sc)
		while(True):	
			btn = waitforclick()
			#print(btn)

			if (btn == 3): # done
				skipClickForNewText = 1
				break

			elif (btn == 2): # calibrate
				print(i)
				mcu.write(str(CALIBRATION_OPTIONS[i]).encode())

			elif (btn == 1):
				CALIBRATION_FUNCTIONS[i](mcu,g)

	else:
		waitforclick()
		print(i)
		mcu.write(str(CALIBRATION_OPTIONS[i]).encode())
		CALIBRATION_FUNCTIONS[i](mcu,g)



# pressure = True
# while (pressure):
# 	mcu.write(str(CALIBRATION_OPTIONS['MAX_PRESSURE']).encode())
# 	skC.calibrateMaxPressure(mcu, g)

# 	print("Repeat?")
# 	response = input()
# 	pressure = (response in ("y","yes","Yes", "Y", "1"))



# calibrationSeq = [4, 3]
# for i in calibrationSeq:
# 	calibrationMode = i
# 	print(calibrationMode)
# 	mcu.write(str(calibrationMode).encode())

# print(calibrationMode)
# mcu.write(str(calibrationMode).encode())
		



def calibrateFlexSensor_Read():
	TIME_LENGTH_READ = 30 #seconds

	# first just read the values
	min_AngleData = 500;
	max_AngleData = 500;
	#endTime = datetime.datetime.now() + datetime.timedelta(seconds=TIME_LENGTH_READ)
	while (datetime.datetime.now() < endTime):
		value = mcu.readline()
		value = str(value, "utf-8").split(",")

		# if valid data packet, convert to right units and write in csv
		#if (len(value) == len(dataFunc)):
		print(value)
		value = int(value[1])
			
		if (value < min_AngleData): min_AngleData = value
		if (value > max_AngleData): max_AngleData = value

	g.write("ANGLE_DATA_MIN = " + str(min_AngleData) + "\n")
	g.write("ANGLE_DATA_MAX = " + str(max_AngleData) + "\n")
	g.close()

	lineCount = lineCount + 2

#def calibrateFlexSensor_Map():


# # update constants file and reimport. then see if calibrated. 
# shutil.copy2(os.path.join(p + 'constantsCalibrated.py'),os.path.join(CONST.PATH_HOME,'constants.py'))
# import constants as CONST
# import skFunctions as sk

# # then with the calibrated values, overwrite the old constants file. maybe add it to the archive in case


# # now for flex arm
# dataFunc = {'time':sk.millisToSeconds, 'flex sensor':sk.computeAngle,'actuator position, command':sk.commandToPosition, \
# 			'actuator position, measured':sk.feedbackToPosition, 'force':sk.computeForce}

# sc = turtle.Screen()
# sc.tracer(0)
# sc.title("SerialArm")
# skG.initializeSerial()

# endTime = datetime.datetime.now() + datetime.timedelta(seconds=10)
# while (datetime.datetime.now() < endTime):
# 	value = mcu.readline()
# 	value = str(value, "utf-8").split(",")

# 	# if valid data packet, convert to right units and write in csv
# 	if (len(value) == len(dataFunc)):
# 		data = int(value[1])
# 		serialAngle = sk.mapFloat(data, min_AngleData, max_AngleData, CONST.ANGLE_MIN, CONST.ANGLE_MAX)
# 		s = "Measured=" + str(serialAngle)
# 		print(s)
# 		turtle.undo()
# 		turtle.undo()
# 		skG.drawForearm(sc,serialAngle, skG.COLOR_SERIAL)

# 	# if (not(CONST.TRANSFER_RAW)):
# 	# 	# if valid data packet, convert to right units and write in csv
# 	# 	#print(len(value))
# 	# 	if (len(value) == len(dataFunc)):
# 	# 		newRow = sk.processNewRow(value, i)
# 	# 		print(newRow)
# 	# 		writer.writerow(newRow)
# 	# 	i = i + 1

# 	# else:
# 	# 	print(value)
# 		# writer.writerow(value)

# sc.bye()

# while(1): 
# 	msg = input()
# 	mcu.write(bytes(msg,'utf-8'))

# lineCount = 0
# calibrationOn = True
# calibrationMode = 
# #endTime = datetime.datetime.now() + datetime.timedelta(seconds=120)
# #while (datetime.datetime.now() < endTime):

# # Read in calibration mode, then decide
# while (calibrationOn):

# 	value = (mcu.readline()).decode()
# 	if (value.strip()): print(value)









# while (lineCount == 7):
# 	value = (mcu.readline()).decode()
# 	value = value.strip()

# 	if (value):
# 		print(value)

# 		if ("Calibrated" in value):
# 			break

# #g.close()

