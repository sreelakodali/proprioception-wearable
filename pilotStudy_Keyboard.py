# Pilot Study
# Written by: Sreela Kodali (kodali@stanford.edu) 

import numpy as np
import turtle
import serial
import datetime
import sys
import csv
import os
import skFunctions as sk
import skPilotGraphics as skG
import random
import constants as CONST
import keyboard
import random

# update this!!
#sys.path.append('/Users/Sreela/Documents/School/Stanford/Year3_2/PIEZO2/Data/Pilot2/2022-09-19_11-03_subjectrachel')
# import constantsCalibrated as CONST
#print(CONST.ACTUATOR_FEEDBACK_MAX)

# Global Variables
t = 1
nTrials = 0
# N = 1
# M = 1
# A = 1
sc = turtle.Screen()
nTargetAngles = sk.generateAngles('TARGET', 1, 1, 0)
nHaptics = sk.generateAngles('HAPTICS',1,0,0)
nPractice = sk.generateAngles('PRACTICE',1,1,2)
nTest = sk.generateAngles('TEST',0,0,4)

trialAngles = nTargetAngles + nHaptics + nPractice + nTest #sk.generateRandomTrials(N, M, A) # Generate random trials
#N_TOTAL_TRIALS = len(trialAngles)

subjectAngleAttempts = []
armAngle = 180

def completeTrial(x,y):
	# skG.star(sc)
	# skG.deleteStar(sc)
	global nTrials, subjectAngleAttempts, armAngle, nPractice
	
	currentAngle = armAngle
	# wait and hold the angle for 10 seconds
	#if (nTrials in windowVisual):
	skG.drawForearm(sc,currentAngle, skG.COLOR_SERIAL)
	turtle.update()
	skG.delay(sc, 100)

	# update
	skG.erase(sc, 'white')
	nTrials = nTrials + 1
	subjectAngleAttempts.append(armAngle)
	if nTrials < len(nPractice):
		skG.drawForearm(sc,nPractice[nTrials], skG.COLOR) #FIX: should be nPractice
		skG.updateTrialLabel(sc, nTrials)
		skG.delay(sc, t)



# Initialize GUI
sc.tracer(0)
sc.title("Experiment Study")
armAngle = 180


# Initialize Serial reading and data saving

# default name is date and time
fileName = str(datetime.datetime.now())[0:16] 
fileName = ((fileName.replace('/', '_')).replace(' ', '_')).replace(':','-')
p = CONST.PATH_LAPTOP +fileName+'/'
if not (os.path.exists(p)):
	os.makedirs(p)
	print("New directory created: %s" % fileName)

# saving in most recent folder
allSubdirs = [CONST.PATH_LAPTOP+d for d in os.listdir(CONST.PATH_LAPTOP) if os.path.isdir(os.path.join(CONST.PATH_LAPTOP, d))]
p = max(allSubdirs, key=sk.getCreationTime) + '/'
print("Destination directory: %s" % p)


mcu = serial.Serial(port=CONST.PORT_NAME, baudrate=CONST.BAUD_RATE, timeout=.1)
f = open(p + "processed_" + fileName + '.csv', 'w+', encoding='UTF8', newline='')
h = open(p + "raw_" + fileName + '.csv', 'w+', encoding='UTF8', newline='')
g = open(p + "targetAngles_" + fileName + '.csv', 'w+', encoding='UTF8', newline='')
w = csv.writer(g)
for a in trialAngles:
	w.writerow([a])
g.close()
print("Trial angles saved.")
writer = csv.writer(f)
writer2 = csv.writer(h)
dataFunc = {'time':sk.millisToSeconds, 'flex sensor':sk.doNothing,'actuator position, command':sk.commandToPosition, \
			'actuator position, measured':sk.feedbackToPosition, 'force':sk.computeForce}

columnNames = list(dataFunc.keys())
columnNames.append("'Trial Number'") 
columnNames.append("'Target Angle'")
writer.writerow(columnNames)

# # Read in serial data and save in csv
# noVisual1 = list(range(20 + 10*(N + M + A), 30 + 10*(N + M + A)))
# realTimeVisual1 = list(range(30 + 10*(N + M + A), 40 + 10*(N + M + A)))
# noVisual2 = list(range(40 + 10*(N + M + A), 50 + 10*(N + M + A)))
# realTimeVisual2 = list(range(50 + 10*(N + M + A), 60 + 10*(N + M + A)))

# realTimeVisual = list(range(0,20)) + realTimeVisual1 + realTimeVisual2
# windowVisual = list(range(20, 20 + 10*(N + M + A)))
# noVisual = noVisual1 + noVisual2


# STAGE 0: INTRODUCTION

EXPERIMENT_TEXT_0 = ["Welcome!", "Let's begin the experiment", "", "", "", "", "", "", "", "", "", "", "Please click the blue key to continue."]
EXPERIMENT_TEXT_1 = ["Experiment", "Task: Match virtual arm's elbow angle with target", "angle. Use <- and -> keys to move virtual arm.", "", "First there will be a learning phase followed by a",  "test phase.", "", "", "", "", "", "", "Please click the blue key to continue."]
EXPERIMENT_TEXT_X = ["Experiment", "Task: Match virtual arm's elbow angle with target", "angle. Use <- and -> keys to move virtual arm.", "", "Target Angle", "Virtual Arm", "Haptic Device", "Arm Rest", "", "", "", "", "Please click the blue key to continue."]
EXPERIMENT_TEXT_2 = ["Learning 1: Explore", "Move virtual arm with keypad and observe haptic", "feedback. Virtual arm will be shown in orange.", "", "Pay close attention to the haptic feedback and", "how that corresponds to where the virtual arm is.", "You will have 1 minute to explore.", "", "", "", "", "", "Please click the blue key to begin learning 1"]
EXPERIMENT_TEXT = [EXPERIMENT_TEXT_0, EXPERIMENT_TEXT_1, EXPERIMENT_TEXT_2]


for txt in EXPERIMENT_TEXT:
	skG.initializeWindow(sc,txt)
	keyboard.wait('up')

# STAGE 1: LEARNING 1 EXPLORE
EXPERIMENT_TEXT_3 = ["Learning 1: Explore", ""]
EXPERIMENT_TEXT_4 = ["Learning 1: Explore", "Learning 1 complete.", "", "", "", "", "", "", "", "", "", "", "Please click the blue key to continue"]
skG.initializeWindow(sc,EXPERIMENT_TEXT_3)
skG.drawUpperArm_Serial()
tLEARN1 = 60
endTime = datetime.datetime.now() + datetime.timedelta(seconds=tLEARN1)
while (datetime.datetime.now() < endTime):
	value = mcu.readlines()

	for i in value:
		i = str(i, "utf-8").split(",")
		if (len(i) == len(dataFunc)):
			raw = [j.rstrip() for j in i]
			raw.append(nTrials)
			raw.append(nTrials)
			writer2.writerow(raw)

			newRow = sk.processNewRow(dataFunc, i)		
			newRow.append(nTrials)
			newRow.append(nTrials)
			writer.writerow(newRow)	
			print(newRow)                                                                                        
	
	turtle.undo() # angle
	turtle.undo() # dot
	skG.drawForearm(sc,armAngle, skG.COLOR_SERIAL)

	k = keyboard.read_key()
	if k == 'left':

		armAngle = armAngle + sk.generateKeyboardInc()
		armAngle = sk.sendAngle_PCToWearable(armAngle, mcu)

	elif k == 'right':

		armAngle = armAngle - sk.generateKeyboardInc()
		armAngle = sk.sendAngle_PCToWearable(armAngle, mcu)

	if (armAngle > 180):
		armAngle = 180

	if (armAngle < 40):
		armAngle = 40


armAngle = 180
sk.sendAngle_PCToWearable(armAngle, mcu)
skG.initializeWindow(sc,EXPERIMENT_TEXT_4)
keyboard.wait('up')


# STAGE 2: LEARNING 2 INTRO TO TARGETS

EXPERIMENT_TEXT_5 = ["Learning 2: Targets", "Practice moving your virtual arm to the target", "angles in blue. Once you've aligned your virtual", "arm with the target, click the blue keypad to", "receive the next target.","", "Pay close attention to the haptic feedback and", "how that corresponds to where the virtual arm is.",  "", "", "", "", "Please click the blue key to begin learning 2"]
EXPERIMENT_TEXT_6 = ["Learning 2: Targets", "Pay close attention to the haptic feedback.", ""]
EXPERIMENT_TEXT_7 = ["Learning 2: Targets", "Learning 2 complete.", "", "", "", "", "", "", "", "", "", "", "Please click the blue key to continue"]
skG.initializeWindow(sc,EXPERIMENT_TEXT_5)
keyboard.wait('up')

skG.initializeWindow(sc,EXPERIMENT_TEXT_6)

skG.drawUpperArm()
skG.drawForearm(sc,nTargetAngles[nTrials], skG.COLOR)
skG.initializeTrialLabel(sc,len(nTargetAngles))
skG.updateTrialLabel(sc, nTrials)
skG.delay(sc, t)
skG.buffer('white')
while (nTrials < len(nTargetAngles)):

	value = mcu.readlines()
	for i in value:
		i = str(i, "utf-8").split(",")
		if (len(i) == len(dataFunc)):
			raw = [j.rstrip() for j in i]
			raw.append(nTrials)
			raw.append(nTargetAngles[nTrials])
			writer2.writerow(raw)

			newRow = sk.processNewRow(dataFunc, i)		
			newRow.append(nTrials)
			newRow.append(nTargetAngles[nTrials])
			writer.writerow(newRow)	
			print(newRow)

	turtle.undo() # angle
	turtle.undo() # dot
	skG.drawForearm(sc,armAngle, skG.COLOR_SERIAL)

	k = keyboard.read_key()
	if k == 'left':
		armAngle = armAngle + sk.generateKeyboardInc()
		armAngle = sk.sendAngle_PCToWearable(armAngle, mcu)

	elif k == 'right':
		armAngle = armAngle - sk.generateKeyboardInc()
		armAngle = sk.sendAngle_PCToWearable(armAngle, mcu)

	elif k == 'up':
		skG.erase(sc, 'white')
		nTrials = nTrials + 1
		subjectAngleAttempts.append(armAngle)
		if nTrials < len(nTargetAngles):
			skG.drawForearm(sc, nTargetAngles[nTrials], skG.COLOR)
			skG.updateTrialLabel(sc, nTrials)
			skG.delay(sc, t)

	if (armAngle > 180):
		armAngle = 180

	if (armAngle < 40):
		armAngle = 40

armAngle = 180
sk.sendAngle_PCToWearable(armAngle, mcu)
skG.initializeWindow(sc,EXPERIMENT_TEXT_7)
keyboard.wait('up')


# STAGE 3: LEARNING 3 HAPTIC FEEDBACK PER TARGET

EXPERIMENT_TEXT_8 = ["Learning 3: Haptics", "Experience haptic feedback associated with each", "target angle for at least 10 seconds. After 10", "seconds, text will appear at the bottom indicating", "that you can click the blue key to move on.", "","Pay close attention to the haptic feedback and", "how that corresponds to where the virtual arm is.", "", "", "", "", "Please click the blue key to begin learning 3"]
EXPERIMENT_TEXT_9 = ["Learning 3: Haptics", "Pay close attention to the haptic feedback.", ""]
EXPERIMENT_TEXT_10 = ["Learning 3: Haptics", "Learning 3 complete.", "", "", "", "", "", "", "", "", "", "", "Please click the blue key to continue"]
skG.initializeWindow(sc,EXPERIMENT_TEXT_8)
keyboard.wait('up')

skG.initializeWindow(sc,EXPERIMENT_TEXT_9)
nTrials = 0
tLEARN3 = 10

skG.drawUpperArm()
skG.drawForearm(sc,nHaptics[nTrials], skG.COLOR)
sk.sendAngle_PCToWearable(nHaptics[nTrials], mcu)
skG.initializeTrialLabel(sc,len(nHaptics))
skG.updateTrialLabel(sc, nTrials)
skG.delay(sc, t)
endTime = datetime.datetime.now() + datetime.timedelta(seconds=tLEARN3)
skG.buffer('white')
while (nTrials < len(nHaptics)):

	value = mcu.readlines()
	for i in value:
		i = str(i, "utf-8").split(",")
		if (len(i) == len(dataFunc)):
			raw = [j.rstrip() for j in i]
			raw.append(nTrials)
			raw.append(nHaptics[nTrials])
			writer2.writerow(raw)

			newRow = sk.processNewRow(dataFunc, i)		
			newRow.append(nTrials)
			newRow.append(nHaptics[nTrials])
			writer.writerow(newRow)	
			print(newRow)

	if (datetime.datetime.now() > endTime):
		skG.writeClickToContinue(sc)
		k = keyboard.read_key()
		if k == 'up':
			skG.erase(sc, 'white')
			nTrials = nTrials + 1
			subjectAngleAttempts.append('0')
			if nTrials < len(nHaptics):
				skG.drawForearm(sc, nTargetAngles[nTrials], skG.COLOR)
				sk.sendAngle_PCToWearable(nHaptics[nTrials], mcu)
				skG.updateTrialLabel(sc, nTrials)
				endTime = datetime.datetime.now() + datetime.timedelta(seconds=tLEARN3)
				skG.delay(sc, t)

armAngle = 180
sk.sendAngle_PCToWearable(armAngle, mcu)
skG.initializeWindow(sc,EXPERIMENT_TEXT_10)
keyboard.wait('up')


# STAGE 4: LEARNING 4 Practice Test with Answers
#EXPERIMENT_TEXT_11 = ["Learning 4: Practice", "Match your virtual arm with a target angle using", "ONLY haptic feedback. The virtual arm (orange)", "will NOT be visible. When you think your virtual", "arm is at the target angle, click the blue key and", "your virtual arm (orange line) will appear for 10", "seconds to show you how your attempt was. Then", "the next target angle will be shown.", "", "", "", "", "Please click the blue key to begin learning 4"]
EXPERIMENT_TEXT_11 = ["Learning 4: Practice", "Match your virtual arm with a target angle using", "ONLY haptic feedback. The virtual arm (orange)", "will NOT be visible.", "", "When you think your virtual arm is at the target" , "angle, click the blue key and the true position of", "your virtual arm will appear for 10 seconds. Then", "the next target angle will be shown.", "", "", "", "Please click the blue key to begin learning 4"]
EXPERIMENT_TEXT_12 = ["Learning 4: Practice", "", ""]
EXPERIMENT_TEXT_13 = ["Learning 4: Practice", "Learning 4 complete.", "", "", "", "", "", "", "", "", "", "", "Please click the blue key to continue"]
skG.initializeWindow(sc,EXPERIMENT_TEXT_11)
keyboard.wait('up')

skG.initializeWindow(sc,EXPERIMENT_TEXT_12)
nTrials = 0
skG.drawUpperArm()
skG.drawForearm(sc,nPractice[nTrials], skG.COLOR)
skG.initializeTrialLabel(sc,len(nPractice))
skG.updateTrialLabel(sc, nTrials)
skG.delay(sc, t)
skG.buffer('white')

# skG.initializePilot(sc)
# skG.drawForearm(sc,trialAngles[nTrials], skG.COLOR)
# skG.updateTrialLabel(sc, nTrials)
# skG.delay(sc, t)
# skG.buffer('white')

while (nTrials < len(nPractice)):

	value = mcu.readlines()
	for i in value:
		i = str(i, "utf-8").split(",")
		if (len(i) == len(dataFunc)):
			raw = [j.rstrip() for j in i]
			raw.append(nTrials)
			raw.append(nPractice[nTrials])
			writer2.writerow(raw)

			newRow = sk.processNewRow(dataFunc, i)		
			newRow.append(nTrials)
			newRow.append(nPractice[nTrials])
			writer.writerow(newRow)	
			print(newRow)

	#s = "Measured=" + str(armAngle) + ", Target=" + str(trialAngles[nTrials])
	
	turtle.undo() # angle
	turtle.undo() # dot
	skG.drawForearm2(sc,armAngle, 'white')

	k = keyboard.read_key()
	if k == 'left':
		armAngle = armAngle + sk.generateKeyboardInc()
		armAngle = sk.sendAngle_PCToWearable(armAngle, mcu)

	elif k == 'right':
		armAngle = armAngle - sk.generateKeyboardInc()
		armAngle = sk.sendAngle_PCToWearable(armAngle, mcu)

	elif k == 'up':
		completeTrial(0,0)

	if (armAngle > 180):
		armAngle = 180

	if (armAngle < 40):
		armAngle = 40

armAngle = 180
sk.sendAngle_PCToWearable(armAngle, mcu)
skG.initializeWindow(sc,EXPERIMENT_TEXT_13)
keyboard.wait('up')

# STAGE 5: TEST
EXPERIMENT_TEXT_14 = ["Experiment: Test", "Match your virtual arm with a target angle. You", "may (or may not) receive haptic feedback. The", "virtual arm (orange) may (or may not) be visible.", "", "When you think your virtual arm is at the target" , "angle, click the blue key and the next target angle", "will be shown.", "", "", "", "WAIT. Experimenter will tell you when to click the", "blue key to begin."]
EXPERIMENT_TEXT_15 = ["Experiment: Test", "", ""]
EXPERIMENT_TEXT_16 = ["Experiment: Test", "WAIT. Experimenter will tell you when to click the", "blue key to continue.", ""]
EXPERIMENT_TEXT_17 = ["Experiment: Test", "Test complete. Experiment is done.", "", "", "", "", "", "", "", "", "", "", "Please click the blue key to continue"]
skG.initializeWindow(sc,EXPERIMENT_TEXT_14)
keyboard.wait('up')

skG.initializeWindow(sc,EXPERIMENT_TEXT_15)
nTrials = 0
skG.drawUpperArm()
skG.drawForearm(sc,nTest[nTrials], skG.COLOR)
skG.initializeTrialLabel(sc,len(nTest))
skG.updateTrialLabel(sc, nTrials)
skG.delay(sc, t)
skG.buffer('white')

visualFeedback = list(range(10,20)) + list(range(30,40))

while (nTrials < len(nTest)):

	value = mcu.readlines()
	for i in value:
		i = str(i, "utf-8").split(",")
		if (len(i) == len(dataFunc)):
			raw = [j.rstrip() for j in i]
			raw.append(nTrials)
			raw.append(nTest[nTrials])
			writer2.writerow(raw)

			newRow = sk.processNewRow(dataFunc, i)		
			newRow.append(nTrials)
			newRow.append(nTest[nTrials])
			writer.writerow(newRow)	
			print(newRow)


	#s = "Measured=" + str(armAngle) + ", Target=" + str(trialAngles[nTrials])
	
	if (nTrials in visualFeedback):
		turtle.undo() # angle
		turtle.undo() # dot
		skG.drawForearm(sc,armAngle, skG.COLOR_SERIAL)

	#elif (nTrials in noVisual + windowVisual):
	# else:
	# 	turtle.undo() # angle
	# 	turtle.undo() # dot
	# 	skG.drawForearm2(sc,armAngle, 'white')

	k = keyboard.read_key()
	if k == 'left':
		armAngle = armAngle + sk.generateKeyboardInc()
		armAngle = sk.sendAngle_PCToWearable(armAngle, mcu)

	elif k == 'right':
		armAngle = armAngle - sk.generateKeyboardInc()
		armAngle = sk.sendAngle_PCToWearable(armAngle, mcu)

	elif k == 'up':
		if (((nTrials+1) % 10) == 0):
			skG.initializeWindow(sc,EXPERIMENT_TEXT_16)
			armAngle = 180
			sk.sendAngle_PCToWearable(armAngle, mcu)
			keyboard.wait('up')
			skG.erase3(sc, 'white')
			skG.initializeTrialLabel(sc,len(nTest))


		skG.erase(sc, 'white')
		nTrials = nTrials + 1
		subjectAngleAttempts.append(armAngle)
		if nTrials < len(nTest):
			skG.drawForearm(sc, nTest[nTrials], skG.COLOR)
			skG.updateTrialLabel(sc, nTrials)
			skG.delay(sc, t)

	if (armAngle > 180):
		armAngle = 180

	if (armAngle < 40):
		armAngle = 40

armAngle = 180
sk.sendAngle_PCToWearable(armAngle, mcu)
skG.initializeWindow(sc,EXPERIMENT_TEXT_17)
keyboard.wait('up')

# 	# if I click then done with trial, store angle and move onto next

# 	# sc.onscreenclick(completeTrial)
# 	# turtle.listen()

f.close()
f = open(p + "subjectAngleAttempts_" + fileName + '.csv', 'w+', encoding='UTF8', newline='')
w = csv.writer(f)
for i in subjectAngleAttempts:
	w.writerow([i])
f.close()
print("Subject results saved.")
