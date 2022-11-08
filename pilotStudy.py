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
sc = turtle.Screen()
trialAngles = sk.generateRandomTrials() # Generate random trials
N_TOTAL_TRIALS = len(trialAngles)
subjectAngleAttempts = []
serialAngle = 0

def completeTrial(x,y):
	# skG.star(sc)
	# skG.deleteStar(sc)
	global nTrials, subjectAngleAttempts, serialAngle
	
	# wait and hold the angle for 10 seconds
	if (nTrials < 50):
		skG.drawForearm(sc,serialAngle, skG.COLOR_SERIAL)
		skG.delay(sc, 10000)

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
# fileName = str(datetime.datetime.now())[0:16] 
# fileName = ((fileName.replace('/', '_')).replace(' ', '_')).replace(':','-')
# p = CONST.PATH_LAPTOP +fileName+'/'
# if not (os.path.exists(p)):
# 	os.makedirs(p)
# 	print("New directory created: %s" % fileName)

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

while (nTrials < N_TOTAL_TRIALS):
	value = mcu.readline()
	value = str(value, "utf-8").split(",")

	# if valid data packet, convert to right units and write in csv
	if (len(value) == len(dataFunc)):

		newRow = sk.processNewRow(value, nTrials)
		print(newRow)
		serialAngle = newRow[1]

		#serialAngle = sk.mapFloat(data, CONST.ANGLE_DATA_MIN, CONST.ANGLE_DATA_MAX, CONST.ANGLE_MIN, CONST.ANGLE_MAX)
		s = "Measured=" + str(serialAngle) + ", Target=" + str(trialAngles[nTrials])
		newRow.append(nTrials)
		newRow.append(trialAngles[nTrials])
		writer.writerow(newRow)
		print(s)
		turtle.undo() # angle
		turtle.undo() # dot
		if (nTrials > 80):
			skG.drawForearm(sc,serialAngle, skG.COLOR_SERIAL)
		else: skG.drawForearm2(sc,serialAngle, 'white')

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
