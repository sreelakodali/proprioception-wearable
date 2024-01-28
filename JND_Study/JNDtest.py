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

def staircase(nUp, nDown, nTrials):
	startPosition = 120 # actuator pwm unit
	reference = 80# 6 N
	inc = -5 # start increment
	
	wait = 5
	retract = 47
	packetA = 0
	packetB = 0
	rightStreak = 0
	answerKey[3]

	# stepType

	# start Value for method of limits
	test = startPosition

	for i in range(0,nTrials):

		# randomize order presented
		if (random.randrange(0,1)):
			packetA = reference #A will be reference
			packetB = test #B will be test target
		else:
			packetA = test #A will be test target
			packetB = reference #B will be reference

		# apply stimuli
		mcu.write(str(packetA).encode()) # Send poke A
		time.sleep(wait) # hold the poke
		mcu.write(str(retract).encode()) # then retract

		mcu.write(str(packetB).encode()) # Send poke B
		time.sleep(wait) # hold the poke
		mcu.write(str(retract).encode()) # then retract

		# find the real answer
		answerKey[0] = (A > B)
		answerKey[1] = (A == B)
		answerKey[2] = (A < B)

		# wait for user's input


		# check the answer

		# if answer wrong, reset streak and step up increment
		rightStreak = 0
		inc = abs(inc) + 1 # step up increment

		# if answer correct, add to right streak
		rightStreak = rightStreak + 1

		# step down increment if they get 3 right answers in a row
		if (rightStreak == 3):
			inc = (abs(inc) - 1)*-1
			rightStreak = 0
		
		# depending on answer, determine next step increment
		# and compute test value
		test = test + inc



# # connect with device
# mcu = serial.Serial(port=CONST.PORT_NAME, baudrate=CONST.BAUD_RATE, timeout=.1)


# # send actuator commands
# while (1):
# 	txt = input()
# 	print(txt)
# 	mcu.write(str(txt).encode())