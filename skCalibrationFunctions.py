# Calibration Support functions
# Written by: Sreela Kodali (kodali@stanford.edu)

import os
import shutil
import datetime
import constants as CONST
import sys
import importlib
import csv
import skFunctions as sk
import turtle
import skPilotGraphics as skG
import random

CALIBRATION_TEXT_INTRO = ["Welcome! Click to begin."]
CALIBRATION_TEXT_ACTUATOR = ["Calibration: Actuator","Please don't wear the actuator. Make sure","power is on. Click CALIBRATE to begin", "and DONE once complete.", " ", " ", " ", " ", "Calibrate", "Done"] 
CALIBRATION_TEXT_MAX_PRESSURE = ["Calibration: Max Pressure", "Please wear the device.", "The actuator will extend into your arm and apply", "pressure. When it is too uncomfortable, click", "anywhere on the screen and the actuator will", "retract. We will do this at least 3 times.", " ", "Click CALIBRATE to begin each round and", "DONE once you've completed at least 3 rounds.", "Calibrate", "Done"]
CALIBRATION_TEXT_FLEX =["Calibration: Flex Sensor", "Please wear the device. Extend your arm in front", "of you with your palm facing up. Keep your arm", "horizontal with the table. Then slowly bend your", "elbow and slowly extend it again. Please repeat", "this a few times.", " ", "Click CALIBRATE to begin and DONE once", "complete.", " ", "Calibrate", "Done"]
CALIBRATION_TEXT_ZERO = ["Calibration complete!"]

CALIBRATION_TEXT = {'ACTUATOR':CALIBRATION_TEXT_ACTUATOR, 'MAX_PRESSURE': CALIBRATION_TEXT_MAX_PRESSURE, 'FLEX': CALIBRATION_TEXT_FLEX, 'NONE': CALIBRATION_TEXT_ZERO}#  'ZERO_FORCE': 1, 'NONE': 0}

def calibrateActuator(mcu, p, saveData):
	lineCount = 0
	if(saveData):
		g = open(p + 'constantsCalibrated.py', 'a', encoding='UTF8')
	while (lineCount < 2):
	#while (1):
		value = (mcu.readline()).decode()
		value = value.strip()

		if (value):
			print(value)

			if (value.isnumeric()):

				if (saveData):
					if (lineCount == 0):
						g.write("ACTUATOR_FEEDBACK_MAX = " + value + "\n")
					elif (lineCount == 1):
						g.write("ACTUATOR_FEEDBACK_MIN = " + value + "\n")
				
				lineCount = lineCount + 1
	if(saveData):
		g.close()

def calibrateMaxPressure(mcu, p, saveData):
	lineCount = 0
	if(saveData):
		g = open(p + 'constantsCalibrated.py', 'a', encoding='UTF8')
		h = open(p + 'maxForce' + '.csv', 'a', encoding='UTF8')
	mcu.write(str(5).encode()) # letting teensy know that max pressure reached
	while (lineCount < 4):
		value = (mcu.readline()).decode()
		value = value.strip()

		if (value):
			print(value)
			if(saveData):
				h.write(value+'\n')
			if (value.isnumeric()):
				if(saveData):
					if (lineCount == 0):
						g.write("ZERO_FORCE = " + value + "\n")
						h.write("ZERO_FORCE = " + value + "\n")
					elif (lineCount== 1):
						g.write("USER_MAX_FORCE_DATA = " + value + "\n")
						h.write("USER_MAX_FORCE_DATA = " + value + "\n")
					elif (lineCount == 2):
						g.write("USER_MAX_ACTUATOR_COMMAND = " + value + "\n")
						h.write("USER_MAX_ACTUATOR_COMMAND = " + value + "\n")
					elif (lineCount == 3):
						g.write("USER_MAX_ACTUATOR_AVG = " + value + "\n")
						h.write("USER_MAX_ACTUATOR_AVG = " + value + "\n")
				lineCount = lineCount + 1
	if(saveData):
		g.close()
		h.close()

def calibrateFlexSensor(mcu, p, sc, saveData): # FIX: update with save data
	TIME_LENGTH_READ = 30 #seconds
	if(saveData):
		g = open(p + 'constantsCalibrated.py', 'a', encoding='UTF8')

	# first just read the values
	min_AngleData = 500;
	max_AngleData = 500;

	value = mcu.readline()
	value = str(value, "utf-8").split(",")	
	value = float(value[0])
	min_AngleData = value
	max_AngleData = value

	endTime = datetime.datetime.now() + datetime.timedelta(seconds=TIME_LENGTH_READ)
	while (datetime.datetime.now() < endTime):
		value = mcu.readline()
		value = str(value, "utf-8").split(",")
		value = float(value[0])
		print(value)
			
		if (value < min_AngleData): min_AngleData = value
		if (value > max_AngleData): max_AngleData = value

	g.write("ANGLE_DATA_MIN = " + str(min_AngleData) + "\n")
	g.write("ANGLE_DATA_MAX = " + str(max_AngleData) + "\n")
	g.close()

	# # update constants file and reimport. then see if calibrated. 
	shutil.copy2(os.path.join(p + 'constantsCalibrated.py'),os.path.join(CONST.PATH_HOME,'constants.py'))
	

	importlib.reload(CONST) #constants as 
	importlib.reload(sk)

	# # now for flex arm
	dataFunc = {'time':sk.millisToSeconds, 'flex sensor':sk.computeAngle,'actuator position, command':sk.commandToPosition, \
				'actuator position, measured':sk.feedbackToPosition, 'force':sk.computeForce}


	skG.erase2(sc,'white')
	skG.initializeSerial()

	endTime = datetime.datetime.now() + datetime.timedelta(seconds=TIME_LENGTH_READ)
	while (datetime.datetime.now() < endTime):
		value = mcu.readline()
		value = str(value, "utf-8").split(",")

		# if valid data packet, convert to right units and write in csv
		
		data = float(value[0])
		serialAngle = sk.mapFloat(data, min_AngleData, max_AngleData, CONST.ANGLE_MIN, CONST.ANGLE_MAX)
		s = "Measured=" + str(serialAngle)
		print(s)
		turtle.undo()
		turtle.undo()
		skG.drawForearm(sc,serialAngle, skG.COLOR_SERIAL)

	skG.initializeCalibrationWindow(sc, CALIBRATION_TEXT['FLEX'])
	skG.buttons(sc)


def calibrateDone(mcu, p, saveData):
	# g = open(p + 'constantsCalibrated.py', 'a', encoding='UTF8')
	# g.close()
	# copy over new calibration file to constants.py

	if(saveData):
		shutil.copy2(os.path.join(p,'constantsCalibrated.py'),os.path.join(CONST.PATH_HOME,'constants.py'))
		importlib.reload(CONST) #constants as 
		importlib.reload(sk)

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
	t_oldConst = str(datetime.datetime.fromtimestamp(os.path.getmtime(CONST.PATH_HOME+'constants.py')))[0:16]
	t_oldConst = ((t_oldConst.replace('/', '_')).replace(' ', '_')).replace(':','-')
	print(t_oldConst)
	shutil.copy2(os.path.join(CONST.PATH_HOME,'constants.py'),os.path.join(CONST.PATH_HOME+'constantsArchive/',t_oldConst+'_constants.py'))

	# create new constants file. write calibration values to new file
	shutil.copy2(os.path.join(CONST.PATH_HOME,'constantsCalibrationTemplate.py'),p)
	os.rename(p+'constantsCalibrationTemplate.py',p+'constantsCalibrated.py')
	#g = open(p + 'calibrationData' + '.py', 'w+', encoding='UTF8')
	g = open(p + 'constantsCalibrated.py', 'a', encoding='UTF8')

	g.write("#" + fileName + "\n")
	print("Created calibration file for subject and copied constants. Click screen to begin calibration.")

	return p