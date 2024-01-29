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


# Global Variables
t = 1
N_TOTAL_TRIALS = 15
sc = turtle.Screen()
# # connect with device
# mcu = serial.Serial(port=CONST.PORT_NAME, baudrate=CONST.BAUD_RATE, timeout=.1)

# Initialize GUI
sc.tracer(0)
sc.title("JND Study")
tr = turtle.Turtle()
turtle.hideturtle()
sc.addshape('/Users/Sreela/Documents/School/Stanford/Year3_2/PIEZO2/GUIFigures/keypadJND.gif')

# default: staircase(120, 80, -5, 5, 47, 1, 3, 15)
def staircase(start, reference, startInc, wait, retract, nUp, nDown, N_Trials):
	# start = 120 # actuator pwm unit
	# reference = 80# 6 N
	# inc = -5 # start increment
	# wait = 5
	# retract = 47

	packetA = 0
	packetB = 0
	rightStreak = 0
	answerKey = 0
	userAnswer = 0
	test = 0
	trialCount = 0 # counter
	# stepType

	# start Value for method of limits
	test = start
	inc = startInc

	for i in range(0,N_Trials):

		print("----- TRIAL #" + str(i) + " -----")
		print("test: " + str(test))
		print("inc: " + str(inc))
		print("rightStreak: " + str(rightStreak))

		# randomize order presented
		if (random.randrange(0,2)):
			packetA = reference #A will be reference
			packetB = test #B will be test target
		else:
			packetA = test #A will be test target
			packetB = reference #B will be reference

		# apply stimuli
		print("Receiving Poke A: " + str(packetA))
		skG.writeText(sc, -350, 230, "Poke A in progress", skG.COLOR)
		# mcu.write(str(packetA).encode()) # Send poke A
		time.sleep(wait) # hold the poke
		# mcu.write(str(retract).encode()) # then retract

		print("Receiving Poke B: " + str(packetB))
		skG.writeText(sc, -350, 180, "Poke B in progress", skG.COLOR)
		# mcu.write(str(packetB).encode()) # Send poke B
		time.sleep(wait) # hold the poke
		# mcu.write(str(retract).encode()) # then retract

		# find the real answer
		# 1 means A > B, 2 means A == B, 3 means A < B
		answerKey = (packetA > packetB)*1 + (packetA == packetB)*2 + (packetA < packetB)*3
		print("The real answer is: " + str(answerKey))

		skG.writeText(sc, -350,80, "Select your answer:", skG.COLOR)
		skG.writeText(sc, -350,30, "A > B             A == B             A < B ", skG.COLOR_RED)
		skG.writeText(sc, -350,-120, "Press the red key to confirm your answer", skG.COLOR)
		skG.writeText(sc, -350,-170, "and proceed to the next trial.", skG.COLOR_GREEN)

		while(1):

		# wait for user's input
			k = keyboard.read_key()
			if k == 'page up':
				userAnswer = 1
				skG.eraseLine(sc,-350,40)
				skG.writeText(sc, -350,30, "(A > B)           A == B             A < B ", skG.COLOR_RED)
			elif k == 'right':
				userAnswer = 2
				skG.eraseLine(sc,-350,40)
				skG.writeText(sc, -350,30, "A > B            (A == B)            A < B ", skG.COLOR_RED)
			elif k == 'page down':
				userAnswer = 3
				skG.eraseLine(sc,-350,40)
				skG.writeText(sc, -350,30, "A > B             A == B            (A < B)", skG.COLOR_RED)

			elif k == 'down':

				if (userAnswer == 0):
					skG.writeText(sc, -350,-20, "You have to choose an answer to proceed.", skG.COLOR)					
				else:
					skG.eraseLine(sc,-350,40)
					skG.erase(sc, 'white')
					#skG.eraseLine(sc,-350,-20)
					trialCount = trialCount + 1
					userAnswer = 0
					if trialCount < N_Trials:
						skG.updateTrialLabel(sc, trialCount)
						skG.delay(sc, t)

					break


		# check the answer. depending on answer, determine next step increment
		# if answer wrong, reset streak and step up increment
		print("User answer is: " + str(userAnswer))

		if (answerKey != userAnswer):
			print("ANSWER WRONG!")
			rightStreak = 0
			inc = abs(inc) + 1 # step up increment

		# if answer correct, add to right streak
		elif (answerKey == userAnswer):
			print("ANSWER RIGHT!")
			rightStreak = rightStreak + 1

			# step down increment if they get 3 right answers in a row
			if (rightStreak == 3):
				inc = (abs(inc) - 1)*-1
				rightStreak = 0
		
		# and compute test value
		test = test + inc

# STAGE 0: Introduction
EXPERIMENT_TEXT_0 = ["Welcome!", "Let's begin the experiment", "", "", "", "", "", "", "", "", "", "", "Please click the red key to continue."]
EXPERIMENT_TEXT_1 = ["Experiment", "Task: Identify whether Poke A feels more intense,", "the same, or less intense than Poke B.", "", "",  "", "", "", "", "", "Use >, =, and < keys to indicate your answer.", "And then click the red key to begin the next trial.", "Please click the red key to continue."]
EXPERIMENT_TEXT = [EXPERIMENT_TEXT_0, EXPERIMENT_TEXT_1]

skG.initializeWindow(sc,EXPERIMENT_TEXT_0)
keyboard.wait('down')
skG.initializeWindow(sc,EXPERIMENT_TEXT_1)
tr.shape('/Users/Sreela/Documents/School/Stanford/Year3_2/PIEZO2/GUIFigures/keypadJND.gif')
turtle.update()
keyboard.wait('down')


# STAGE 1: JND
EXPERIMENT_TEXT_3 = ["JND Study", ""]
skG.initializeWindow(sc,EXPERIMENT_TEXT_3)
skG.initializeTrialLabel(sc,N_TOTAL_TRIALS)
skG.updateTrialLabel(sc, 0)
skG.delay(sc, t)

# start=120, ref=80, startInc=-5, wait=5, retract=47, nUp=1, nDown=3, N_Trials=15
staircase(120, 80, -5, 5, 47, 1, 3, 15)

# # send actuator commands
# while (1):
# 	txt = input()
# 	print(txt)
# 	mcu.write(str(txt).encode())