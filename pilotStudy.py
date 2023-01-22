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

# update this!!
#sys.path.append('/Users/Sreela/Documents/School/Stanford/Year3_2/PIEZO2/Data/Pilot2/2022-09-19_11-03_subjectrachel')
# import constantsCalibrated as CONST
#print(CONST.ACTUATOR_FEEDBACK_MAX)

# Global Variables
t = 10
nTrials = 0
N = 3
M = 3
A = 1
sc = turtle.Screen()
trialAngles = sk.generateRandomTrials(N, M, A) # Generate random trials
N_TOTAL_TRIALS = len(trialAngles)
subjectAngleAttempts = []
serialAngle = 0

def completeTrial(x,y):
	# skG.star(sc)
	# skG.deleteStar(sc)
	global nTrials, subjectAngleAttempts, serialAngle
	
	currentAngle = serialAngle
	# wait and hold the angle for 10 seconds
	if (nTrials in windowVisual):
		skG.drawForearm(sc,currentAngle, skG.COLOR_SERIAL)
		turtle.update()
		skG.delay(sc, 100)

	# update
	skG.erase(sc, 'white')
	nTrials = nTrials + 1
	subjectAngleAttempts.append(serialAngle)
	if nTrials < len(trialAngles):
		skG.drawForearm(sc,trialAngles[nTrials], skG.COLOR)
		skG.updateTrialLabel(sc, nTrials)
		skG.delay(sc, t)

# Initialize GUI
sc.tracer(0)
sc.title("Pilot Study")
skG.initializePilot()


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
dataFunc = {'time':sk.millisToSeconds, 'flex sensor':sk.computeAngle,'actuator position, command':sk.commandToPosition, \
			'actuator position, measured':sk.feedbackToPosition, 'force':sk.computeForce}

columnNames = list(dataFunc.keys())
columnNames.append('Trial Number')
columnNames.append('Target Angle')
writer.writerow(columnNames)

# Read in serial data and save in csv
skG.drawForearm(sc,trialAngles[nTrials], skG.COLOR)
skG.updateTrialLabel(sc, nTrials)
skG.delay(sc, t)
skG.buffer('white')




noVisual1 = list(range(20 + 10*(N + M + A), 30 + 10*(N + M + A)))
realTimeVisual1 = list(range(30 + 10*(N + M + A), 40 + 10*(N + M + A)))
noVisual2 = list(range(40 + 10*(N + M + A), 50 + 10*(N + M + A)))
realTimeVisual2 = list(range(50 + 10*(N + M + A), 60 + 10*(N + M + A)))

realTimeVisual = list(range(0,20)) + realTimeVisual1 + realTimeVisual2
windowVisual = list(range(20, 20 + 10*(N + M + A)))
noVisual = noVisual1 + noVisual2

while (nTrials < N_TOTAL_TRIALS):
	value = mcu.readline()
	value = str(value, "utf-8").split(",")

	# if valid data packet, convert to right units and write in csv
	if (len(value) == len(dataFunc)):

		newRow = sk.processNewRow(dataFunc, value)
		print(newRow)
		serialAngle = newRow[1]

		#serialAngle = sk.mapFloat(data, CONST.ANGLE_DATA_MIN, CONST.ANGLE_DATA_MAX, CONST.ANGLE_MIN, CONST.ANGLE_MAX)
		s = "Measured=" + str(serialAngle) + ", Target=" + str(trialAngles[nTrials])
		newRow.append(nTrials)
		newRow.append(trialAngles[nTrials])
		writer.writerow(newRow)
		print(s)

		# erase dot and angle
		
		# # erase dot and angle
		# skG.erase3(sc,'blue') # FIX ME LATER: undo if runs too long idle, will undo everythig

		if (nTrials in realTimeVisual):
			turtle.undo() # angle
			turtle.undo() # dot
			skG.drawForearm(sc,serialAngle, skG.COLOR_SERIAL)
		elif (nTrials in noVisual + windowVisual):
			turtle.undo() # angle
			turtle.undo() # dot
			skG.drawForearm2(sc,serialAngle, 'white')

		# if I click then done with trial, store angle and move onto next
		sc.onscreenclick(completeTrial)
		turtle.listen()
f.close()
f = open(p + "subjectAngleAttempts_" + fileName + '.csv', 'w+', encoding='UTF8', newline='')
w = csv.writer(f)
for i in subjectAngleAttempts:
	w.writerow([i])
f.close()
print("Subject results saved.")
