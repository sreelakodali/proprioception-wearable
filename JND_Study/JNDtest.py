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


#staircase variables
# # start=120, ref=80, startStep=-5, wait=5, retract=47, nUp=1, nDown=3, N_Trials=30
startValue = 120
retractPos = 65
ref = 95

stepDown=3
nUp = 1
nDown = 2
N_TOTAL_TRIALS = 10#50
waitTime = 6

stepSizeRatio = {1:0.2845, 2:0.5488, 3:0.7393 , 4:0.8415}

stepUp = stepDown/stepSizeRatio[nDown]



# Global Variables
t = 1
sc = turtle.Screen()

# # connect with device
mcu = serial.Serial(port=CONST.PORT_NAME, baudrate=CONST.BAUD_RATE, timeout=.1)

# # Initialize GUI
sc.tracer(0)
sc.title("JND Study")
tr = turtle.Turtle()
turtle.hideturtle()
sc.addshape('/Users/Sreela/Documents/School/Stanford/Year3_2/PIEZO2/GUIFigures/keypadJND.gif')

# default name is date and time
fileName = str(datetime.datetime.now())[0:16] 
fileName = ((fileName.replace('/', '_')).replace(' ', '_')).replace(':','-')
p = CONST.PATH_LAPTOP +fileName+'/'
if not (os.path.exists(p)):
	os.makedirs(p)
	print("New directory created: %s" % fileName)

f = open(p + "processed_" + fileName + '.csv', 'w+', encoding='UTF8', newline='') # I guess let's append trialCount, 
g = open(p + "raw_" + fileName + '.csv', 'w+', encoding='UTF8', newline='') # I guess let's append trialCount, 
h = open(p + "trial_" + fileName + '.csv', 'w+', encoding='UTF8', newline='') # trialCount, test, reference, A, B, forceA_a0, forceA_a1, forceB_a0, forceB_a1, answerKey, userAnswer, inc, rightStreak
writer = csv.writer(f)
writer2 = csv.writer(g)
writer3 = csv.writer(h)
# # dataFunc = {'time':sk.millisToSeconds, 'flex sensor':sk.doNothing,'actuator position, command':sk.commandToPosition, \
# # 			'actuator position, measured':sk.feedbackToPosition, 'force':sk.computeForce}

dataFunc = {'time':sk.millisToSeconds, 'flex sensor':sk.doNothing,'actuator position, command':sk.doNothing, \
			'actuator position, measured':sk.doNothing, 'force':sk.computeForce, 'actuator position, command1':sk.doNothing,\
			'actuator position, measured1':sk.doNothing, 'force1':sk.computeForce}

columnNames = list(dataFunc.keys())
columnNames.append("TrialCounter")

writer.writerow(columnNames)
writer2.writerow(columnNames)
writer3.writerow(["trialCount", "Test", "Reference", "A", "B", "answerKey", "userAnswer", "stepSize", "rightStreak"])


# default: staircase(120, 80, -5, 5, 47, 1, 3, 15)
def staircase(start, reference, stepDown, stepUp, wait, retract, nUp, nDown, N_Trials):
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
	wrongCount = 0
	# stepType

	# start Value for method of limits
	test = start

	for i in range(0,N_Trials):

		value = mcu.readlines()
		for j in value:
			#skP.writeOutData(j,dataFunc, 0, 0, trialCount)
			skP.writeOutData(j,dataFunc, writer2, writer, trialCount)

		print("----- TRIAL #" + str(i) + " -----")
		print("test: " + str(test))
		print("rightStreak: " + str(rightStreak))


		# randomize order presented
		r = random.randrange(0,2)
		print("r: " + str(r))
		if (r == 1):
			packetA = reference #A will be reference
			packetB = test #B will be test target
		else:
			packetA = test #A will be test target
			packetB = reference #B will be reference
		
		# w = 0

		# apply stimuli
		print("Receiving Stimulus A: " + str(packetA))
		skG.writeText(sc, -350, 230, "Stimulus A in progress", skG.COLOR)
		mcu.write(str(packetA).encode()) # Send poke A
		# endTime = datetime.datetime.now() + datetime.timedelta(seconds=wait)
		# while (datetime.datetime.now() < endTime):
		# 	w = w + 1
		time.sleep(wait) # hold the poke
	
		mcu.write(str(retract).encode()) # then retract
		# endTime = datetime.datetime.now() + datetime.timedelta(seconds=wait/2)
		# while (datetime.datetime.now() < endTime):
		# 	w = w + 1
		time.sleep(wait) # wait


		print("Receiving Stimulus B: " + str(packetB))
		skG.writeText(sc, -350, 180, "Stimulus B in progress", skG.COLOR)
		mcu.write(str(packetB).encode()) # Send poke B
		# endTime = datetime.datetime.now() + datetime.timedelta(seconds=wait)
		# while (datetime.datetime.now() < endTime):
		# 	w = w + 1
		time.sleep(wait) # hold the poke
		mcu.write(str(retract).encode()) # then retract
		# endTime = datetime.datetime.now() + datetime.timedelta(seconds=wait/2)
		# while (datetime.datetime.now() < endTime):
		# 	w = w + 1
		time.sleep(wait/2) # wait

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
					if trialCount < N_Trials:
						skG.updateTrialLabel(sc, trialCount)
						skG.delay(sc, t)

					break


		# check the answer. depending on answer, determine next test value
		# if answer wrong, reset streak and step up test value
		print("User answer is: " + str(userAnswer))

		

		if (answerKey != userAnswer):
			print("ANSWER WRONG!")
			rightStreak = 0
			test = test + round(stepUp) # step up test value if wrong
			writer3.writerow([trialCount, test, reference, packetA, packetB, answerKey, userAnswer, stepUp, rightStreak])
			print("stepSize: " + str(stepUp))
			# inc = abs(inc) + 1 
			userAnswer = 0
			wrongCount = wrongCount + 1
			print("reversals:" + str(wrongCount))
			# if (wrongCount == 2):
			# 	stepSize = stepSize2

		# if answer correct, add to right streak
		elif (answerKey == userAnswer):
			print("ANSWER RIGHT!")
			rightStreak = rightStreak + 1
			userAnswer = 0
			
			# step down test if they get 3 right answers in a row
			if ((rightStreak == nDown) or (wrongCount == 0)):
				test = test - stepDown
				writer3.writerow([trialCount, test, reference, packetA, packetB, answerKey, userAnswer, stepDown, rightStreak])
				# inc = (abs(inc) - 1)*-1
				rightStreak = 0
			else:
				writer3.writerow([trialCount, test, reference, packetA, packetB, answerKey, userAnswer, 0, rightStreak])
	
	value = mcu.readlines()
	for j in value:
		#skP.writeOutData(j,dataFunc, 0, 0, trialCount)
		skP.writeOutData(j,dataFunc, writer2, writer, trialCount)	
		# # and compute test value
		# test = test + inc

# STAGE 0: Introduction
EXPERIMENT_TEXT_0 = ["Welcome!", "Let's begin the experiment", "", "", "", "", "", "", "", "", "", "", "Please click the red key to continue."]
EXPERIMENT_TEXT_1 = ["Experiment", "Task: Identify whether Stimulus A feels more,", "intense, the same, or less intense than Stimulus B.", "", "",  "", "", "", "", "", "Use >, =, and < keys to indicate your answer,", "and then click the red key to go to the next trial.", "Please click the red key to start."]
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



staircase(startValue, ref, stepDown, stepUp, waitTime, retractPos, nUp, nDown, N_TOTAL_TRIALS)


f.close()
g.close()
h.close()

# # send actuator commands
# while (1):
# 	txt = input()
# 	print(txt)
# 	mcu.write(str(txt).encode())

# 	value = mcu.readlines()
# 	for j in value:
# 		skP.writeOutData(j,dataFunc, 0, 0, 0)
	