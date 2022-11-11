# Calibration Support functions
# Written by: Sreela Kodali (kodali@stanford.edu)

import os
import shutil
import datetime
import constants as CONST
import sys
import csv
import skFunctions as sk
import turtle
import skPilotGraphics as skG
import random

def calibrateActuator(mcu, g):
	lineCount = 0
	while (lineCount < 2):
	#while (1):
		value = (mcu.readline()).decode()
		value = value.strip()

		if (value):
			print(value)

			if (value.isnumeric()):

				if (lineCount == 0):
					g.write("ACTUATOR_FEEDBACK_MAX = " + value + "\n")
				elif (lineCount == 1):
					g.write("ACTUATOR_FEEDBACK_MIN = " + value + "\n")
				lineCount = lineCount + 1

def calibrateMaxPressure(mcu, g):
	lineCount = 0
	while (lineCount < 3):
		value = (mcu.readline()).decode()
		value = value.strip()

		if (value):
			print(value)

			if (value.isnumeric()):
				if (lineCount == 0):
					g.write("ZERO_FORCE = " + value + "\n")
				elif (lineCount== 1):
					g.write("USER_MAX_FORCE_DATA = " + value + "\n")
				elif (lineCount == 2):
					g.write("USER_MAX_ACTUATOR_COMMAND = " + value + "\n")
				lineCount = lineCount + 1


def calibrateNewSubject():
	# Wait for subject input
	print("Please input the subject number: ")
	nSubject = input()

	# Create new folder with subject number and date-time
	fileName = str(datetime.datetime.now())[0:16] # default name is date and time
	fileName = ((fileName.replace('/', '_')).replace(' ', '_')).replace(':','-')
	fileName = fileName + "_subject" + str(nSubject)
	p = CONST.PATH_LAPTOP +fileName+'/'
	if not (os.path.exists(p)):
		os.makedirs(p)
		print("New directory created: %s" % fileName)

	# add current constants file's birthtime to its file name, copy it, add it to the archive
	t_oldConst = str(datetime.datetime.fromtimestamp(sk.getCreationTime(CONST.PATH_HOME+'constants.py')))[0:16]
	t_oldConst = ((t_oldConst.replace('/', '_')).replace(' ', '_')).replace(':','-')
	shutil.copy2(os.path.join(CONST.PATH_HOME,'constants.py'),os.path.join(CONST.PATH_HOME+'constantsArchive/',t_oldConst+'constants.py'))

	# create new constants file. write calibration values to new file
	shutil.copy2(os.path.join(CONST.PATH_HOME,'constantsCalibrationTemplate.py'),p)
	os.rename(p+'constantsCalibrationTemplate.py',p+'constantsCalibrated.py')
	#g = open(p + 'calibrationData' + '.py', 'w+', encoding='UTF8')
	g = open(p + 'constantsCalibrated.py', 'a', encoding='UTF8')

	g.write("#" + fileName + "\n")
	print("Created calibration file for subject and copied constants. Press button to begin calibration.")

	return g