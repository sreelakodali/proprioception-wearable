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
N = 1
M = 1
A = 1
sc = turtle.Screen()
trialAngles = sk.generateRandomTrials(N, M, A) # Generate random trials
N_TOTAL_TRIALS = len(trialAngles)
subjectAngleAttempts = []
armAngle = 180

def completeTrial(x,y):
	# skG.star(sc)
	# skG.deleteStar(sc)
	global nTrials, subjectAngleAttempts, armAngle
	
	currentAngle = armAngle
	# wait and hold the angle for 10 seconds
	if (nTrials in windowVisual):
		skG.drawForearm(sc,currentAngle, skG.COLOR_SERIAL)
		turtle.update()
		skG.delay(sc, 100)

	# update
	skG.erase(sc, 'white')
	nTrials = nTrials + 1
	subjectAngleAttempts.append(armAngle)
	if nTrials < len(trialAngles):
		skG.drawForearm(sc,trialAngles[nTrials], skG.COLOR)
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
g = open(p + "trialAngles_" + fileName + '.csv', 'w+', encoding='UTF8', newline='')
w = csv.writer(g)
for a in trialAngles:
	w.writerow([a])
g.close()
print("Trial angles saved.")
writer = csv.writer(f)
dataFunc = {'time':sk.millisToSeconds, 'flex sensor':sk.doNothing,'actuator position, command':sk.commandToPosition, \
			'actuator position, measured':sk.feedbackToPosition, 'force':sk.computeForce}

columnNames = list(dataFunc.keys())
columnNames.append('Trial Number')
columnNames.append('Target Angle')
writer.writerow(columnNames)

# Read in serial data and save in csv
noVisual1 = list(range(20 + 10*(N + M + A), 30 + 10*(N + M + A)))
realTimeVisual1 = list(range(30 + 10*(N + M + A), 40 + 10*(N + M + A)))
noVisual2 = list(range(40 + 10*(N + M + A), 50 + 10*(N + M + A)))
realTimeVisual2 = list(range(50 + 10*(N + M + A), 60 + 10*(N + M + A)))

realTimeVisual = list(range(0,20)) + realTimeVisual1 + realTimeVisual2
windowVisual = list(range(20, 20 + 10*(N + M + A)))
noVisual = noVisual1 + noVisual2


nInfoSlides = 4
# initial instructions
sc.addshape('/Users/Sreela/Documents/School/Stanford/Year3_2/PIEZO2/GUIFigures/keypad.gif')
sc.addshape('/Users/Sreela/Documents/School/Stanford/Year3_2/PIEZO2/GUIFigures/setup.gif')
#skG.initializeWindow(sc, ["Experiment", "Task: Match virtual arm's elbow angle with target", "angle. Use <- and -> keys to move virtual arm.", "", "First there will be a learning phase",  " followed  by a test phase.", "", "", "", "", "", "", "Please click the blue key to continue."])
skG.initializeWindow_MultiColor(sc, ["Experiment", "Task: Match virtual arm's elbow angle with target", "angle. Use <- and -> keys to move virtual arm.", "", "Target Angle", "Virtual Arm", "Haptic Device", "Arm Rest", "", "", "", "", "Please click the blue key to continue."], 1)
tr = turtle.Turtle()
tr.goto(100,-50)
tr.shape('/Users/Sreela/Documents/School/Stanford/Year3_2/PIEZO2/GUIFigures/setup.gif')
turtle.update()
keyboard.wait('up')

skG.initializeWindow(sc, ["Experiment: Learning Part 1 of 2", "Explore: Move virtual arm and observe haptic", "feedback. Virtual arm is shown in orange.", "", "", "", "", "", "", "", "", "", "Please click the blue key to continue."])
keyboard.wait('up')

skG.initializePilot(sc)
skG.drawForearm(sc,trialAngles[nTrials], skG.COLOR)
skG.updateTrialLabel(sc, nTrials)
skG.delay(sc, t)
skG.buffer('white')

 

while (nTrials < N_TOTAL_TRIALS):

	value = mcu.readlines()
	for i in value:
		i = str(i, "utf-8").split(",")
		if (len(i) == len(dataFunc)):
			newRow = sk.processNewRow(dataFunc, i)		
			newRow.append(nTrials)
			newRow.append(trialAngles[nTrials])
			writer.writerow(newRow)	
			#print(i)

	s = "Measured=" + str(armAngle) + ", Target=" + str(trialAngles[nTrials])
	
	if (nTrials in realTimeVisual):
		turtle.undo() # angle
		turtle.undo() # dot
		skG.drawForearm(sc,armAngle, skG.COLOR_SERIAL)
	
	elif (nTrials in noVisual + windowVisual):
		turtle.undo() # angle
		turtle.undo() # dot
		skG.drawForearm2(sc,armAngle, 'white')

	k = keyboard.read_key()
	if k == 'left':
		if (random.randrange(2)):
			inc = 3
		else:
			inc = 1
		print(inc)

		armAngle = armAngle + inc#1.5*(random.randrange(10) + 1)
		armAngle = sk.sendAngle_PCToWearable(armAngle, mcu)

	elif k == 'right':
		if (random.randrange(2)):
			inc = 3
		else:
			inc = 1
		print(inc)
		armAngle = armAngle - inc#1.5*(random.randrange(10) + 1)
		armAngle = sk.sendAngle_PCToWearable(armAngle, mcu)

	elif k == 'up':
		completeTrial(0,0)



	# if I click then done with trial, store angle and move onto next

	# sc.onscreenclick(completeTrial)
	# turtle.listen()
f.close()
f = open(p + "subjectAngleAttempts_" + fileName + '.csv', 'w+', encoding='UTF8', newline='')
w = csv.writer(f)
for i in subjectAngleAttempts:
	w.writerow([i])
f.close()
print("Subject results saved.")
