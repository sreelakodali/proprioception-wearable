# JND Test 
# Written by: Sreela Kodali (kodali@stanford.edu) 


import serial, datetime, csv, sys, getopt, os, shutil, turtle, random, time, keyboard
import numpy as np
from scipy import signal
import constants as CONST
import skFunctions as sk
import skPilotGraphics as skG
import skCalibrationFunctions as skC
import skPilotGraphics as skG
import skPilotKeyboardFunctions as skP

# Global Variables
# t = 1
# sc = turtle.Screen()

# # connect with device
mcu = serial.Serial(port="/dev/cu.usbmodem1101", baudrate=115200, timeout=.1)

# # Initialize GUI
# sc.tracer(0)
# sc.title("JND Study")
# tr = turtle.Turtle()
# turtle.hideturtle()
# sc.addshape('/Users/Sreela/Documents/School/Stanford/Year3_2/PIEZO2/GUIFigures/keypadJND.gif')


# # STAGE 0: Introduction
# EXPERIMENT_TEXT_0 = ["Welcome!", "Let's send commands to the motor", "", "", "", "", "", "", "", "", "", "", "Please click the red key to continue."]


# skG.initializeWindow(sc,EXPERIMENT_TEXT_0)
# keyboard.wait('down')
# skG.initializeWindow(sc,EXPERIMENT_TEXT_0)
# tr.shape('/Users/Sreela/Documents/School/Stanford/Year3_2/PIEZO2/GUIFigures/keypadJND.gif')
# turtle.update()
# keyboard.wait('down')


# skG.initializeWindow(sc,'vine time')
# skG.initializeTrialLabel(sc,N_TOTAL_TRIALS)
# skG.updateTrialLabel(sc, 0)
# skG.delay(sc, t)

while(1):
	value = mcu.readline()
	if (value):
		print(value)
	# for j in value:
	# 	#skP.writeOutData(j,dataFunc, 0, 0, trialCount)
	# 	print(j)

	k = keyboard.read_key()
	if k == 'down':
		#print("key pressed")
		mcu.write(str(9).encode())
		time.sleep(0.5)


# # send actuator commands
# while (1):
# 	txt = input()
# 	print(txt)
# 	mcu.write(str(txt).encode())

# 	value = mcu.readlines()
# 	for j in value:
# 		skP.writeOutData(j,dataFunc, 0, 0, 0)
	