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
import keyboard

CALIBRATION_OPTIONS = {'ACTUATOR':4, 'MAX_PRESSURE': 3, 'FLEX': 2, 'NONE': 0}
CALIBRATION_OPTIONS2 = {'ACTUATOR':4, 'MAX_PRESSURE': 3, 'NONE': 0}
CALIBRATION_FUNCTIONS = {'ACTUATOR':skC.calibrateActuator, 'MAX_PRESSURE': skC.calibrateMaxPressure, 'FLEX': skC.calibrateFlexSensor, 'ZERO_FORCE': 1, 'NONE': skC.calibrateDone}

calibrationSeq = CALIBRATION_OPTIONS.keys() # default

opts, args = getopt.getopt(sys.argv[1:],"m",["mode=", "custom="])
for opt, arg in opts:
	if opt in ["-m", "--mode"]:
		if arg == 'FLEX':
			calibrationSeq = CALIBRATION_OPTIONS.keys()
		if arg == 'KEY':
			calibrationSeq = CALIBRATION_OPTIONS2.keys()
			#calibrationSeq = (CALIBRATION_OPTIONS[arg])
	elif opt == "--custom":
		calibrationSeq = arg

print(calibrationSeq)

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

p = skC.calibrateNewSubject();

sc = turtle.Screen()
sc.tracer(0)
sc.title("Calibration")
turtle.onscreenclick(on_click, btn=1)
turtle.update()
skG.initializeCalibrationWindow(sc, skC.CALIBRATION_TEXT_INTRO)

for i in calibrationSeq:

	if not(skipClickForNewText): btn = waitforclick()
	else: skipClickForNewText = 0
	skG.initializeCalibrationWindow(sc, skC.CALIBRATION_TEXT[i])

	if i == 'NONE':
		waitforclick()
		print(i)
		mcu.write(str(CALIBRATION_OPTIONS[i]).encode())
		CALIBRATION_FUNCTIONS[i](mcu,p)

	else:	
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
				if i =='ACTUATOR':
					CALIBRATION_FUNCTIONS[i](mcu,p)
				elif i == 'FLEX':
					CALIBRATION_FUNCTIONS[i](mcu,p, sc)
			elif (btn == 1):
				if i == 'MAX_PRESSURE':
					CALIBRATION_FUNCTIONS[i](mcu,p)
	