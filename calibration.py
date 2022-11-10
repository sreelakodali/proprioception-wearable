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
from enum import Enum

#CALIBRATION_OPTIONS = Enum('CALIBRATION_OPTIONS', ['NONE', 'ZERO_FORCE', 'FLEX', 'MAX_PRESSURE', 'ACTUATOR'])

CALIBRATION_OPTIONS = {'NONE': 0, 'ZERO_FORCE': 1, 'FLEX': 2, 'MAX_PRESSURE': 3, 'ACTUATOR':4}

# # Wait for subject input
# print("Please input the subject number: ")
# nSubject = input()

# # # DIRECTORY
# fileName = str(datetime.datetime.now())[0:16] # default name is date and time
# fileName = ((fileName.replace('/', '_')).replace(' ', '_')).replace(':','-')
# fileName = fileName + "_subject" + str(nSubject)
# p = CONST.PATH_LAPTOP +fileName+'/'
# if not (os.path.exists(p)):
# 	os.makedirs(p)
# 	print("New directory created: %s" % fileName)

# # add current constants file's birthtime to its file name, copy it, add it to the archive
# t_oldConst = str(datetime.datetime.fromtimestamp(sk.getCreationTime(CONST.PATH_HOME+'constants.py')))[0:16]
# t_oldConst = ((t_oldConst.replace('/', '_')).replace(' ', '_')).replace(':','-')
# shutil.copy2(os.path.join(CONST.PATH_HOME,'constants.py'),os.path.join(CONST.PATH_HOME+'constantsArchive/',t_oldConst+'constants.py'))

# # create new constants file. write calibration values to new file
# shutil.copy2(os.path.join(CONST.PATH_HOME,'constantsCalibrationTemplate.py'),p)
# os.rename(p+'constantsCalibrationTemplate.py',p+'constantsCalibrated.py')
# #g = open(p + 'calibrationData' + '.py', 'w+', encoding='UTF8')
# g = open(p + 'constantsCalibrated.py', 'a', encoding='UTF8')

# g.write("#" + fileName + "\n")
# print("Created calibration file for subject and copied constants. Press button to begin calibration.")



opts, args = getopt.getopt(sys.argv[1:],"",["calibrate="])
mcu = serial.Serial(port=CONST.PORT_NAME, baudrate=CONST.BAUD_RATE, timeout=.1)

for opt, arg in opts:
	# if opt == "-n":
	# 	#actuatorType = int(arg)

	if opt == "--calibrate":
		calibrationMode = (CALIBRATION_OPTIONS[arg])
		
#mcu.write(bytes("hi",'utf-8'))
print(calibrationMode)
mcu.write(str(calibrationMode).encode())
		



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




# while (lineCount <= 5):

# 	value = (mcu.readline()).decode()
# 	value = value.strip()

# 	if (value):
# 		print(value)

# 		if ("Begin flex sensor calibration" in value):
# 			break

# 		if (value.isnumeric()):

# 			if (lineCount == 0):
# 				g.write("ACTUATOR_FEEDBACK_MAX = " + value + "\n")
# 			elif (lineCount == 1):
# 				g.write("ACTUATOR_FEEDBACK_MIN = " + value + "\n")
# 			elif (lineCount == 2):
# 				g.write("ZERO_FORCE = " + value + "\n")
# 			elif (lineCount== 3):
# 				g.write("USER_MAX_FORCE_DATA = " + value + "\n")
# 			elif (lineCount == 4):
# 				g.write("USER_MAX_ACTUATOR_COMMAND = " + value + "\n")
# 			lineCount = lineCount + 1
# 			#value = int(value)
# 			#f.write(value+"\n")


# # first just read the values
# min_AngleData = 500;
# max_AngleData = 500;
# endTime = datetime.datetime.now() + datetime.timedelta(seconds=10)
# while (datetime.datetime.now() < endTime):
# 	value = mcu.readline()
# 	value = str(value, "utf-8").split(",")

# 	# if valid data packet, convert to right units and write in csv
# 	#if (len(value) == len(dataFunc)):
# 	print(value)
# 	value = int(value[1])
		
# 	if (value < min_AngleData): min_AngleData = value
# 	if (value > max_AngleData): max_AngleData = value

# g.write("ANGLE_DATA_MIN = " + str(min_AngleData) + "\n")
# g.write("ANGLE_DATA_MAX = " + str(max_AngleData) + "\n")
# g.close()

# lineCount = lineCount + 2

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

# while (lineCount == 7):
# 	value = (mcu.readline()).decode()
# 	value = value.strip()

# 	if (value):
# 		print(value)

# 		if ("Calibrated" in value):
# 			break

# #g.close()

