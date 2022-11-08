# Pilot Study
# Written by: Sreela Kodali (kodali@stanford.edu) 

import numpy as np
import turtle
import serial
import datetime
import csv
import os
import constants as CONST
import skFunctions as sk
import skPilotGraphics as skG
import random

t = 10
nTrials = 0
sc = turtle.Screen()
trialAngles = sk.generateRandomTrials() # Generate random trials
N_TOTAL_TRIALS = 2#len(trialAngles)

# def updateTrialLabel():
# 	global sc
# 	sc.tracer(0)
# 	turtle.penup()
# 	skG.removeTrialLabel(sc)
# 	turtle.goto(325,300)
# 	global nTrials
# 	turtle.write(nTrials+1, move=False, font=("Arial",36, "normal"))
# 	turtle.penup()

# Initialize GUI
sc.tracer(0)
sc.title("Pilot Study")
skG.initializePilot()

# Initialize Serial reading and data saving
fileName = str(datetime.datetime.now())[0:16] # default name is date and time
fileName = ((fileName.replace('/', '_')).replace(' ', '_')).replace(':','-')
p = CONST.PATH_LAPTOP +fileName+'/'
if not (os.path.exists(p)):
	os.makedirs(p)
	print("New directory created: %s" % fileName)
mcu = serial.Serial(port=CONST.PORT_NAME, baudrate=CONST.BAUD_RATE, timeout=.1)
if (CONST.TRANSFER_RAW): f = open(p + 'raw_' + fileName + '.csv', 'w+', encoding='UTF8', newline='')
else:
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
if (CONST.SHOW_ARM): skG.buffer('white')
serialAngleBuf = []
while (nTrials < N_TOTAL_TRIALS):
	value = mcu.readline()
	value = str(value, "utf-8").split(",")

	# if valid data packet, convert to right units and write in csv
	if (len(value) == len(dataFunc)):
		newRow = sk.processNewRow(value, nTrials)
		serialAngle = newRow[1]
		s = "Measured=" + str(serialAngle) + ", Target=" + str(trialAngles[nTrials])
		newRow.append(nTrials)
		newRow.append(trialAngles[nTrials])
		writer.writerow(newRow)
		print(s)
		if (CONST.SHOW_ARM): turtle.undo() # angle
		if (CONST.SHOW_ARM): turtle.undo() # dot
		if (CONST.SHOW_ARM): skG.drawForearm(sc,serialAngle, skG.COLOR_SERIAL)

		if ((serialAngle > (trialAngles[nTrials] - CONST.ANGLE_TOLERANCE)) and (serialAngle < (trialAngles[nTrials] + CONST.ANGLE_TOLERANCE))):
			serialAngleBuf.append(serialAngle)

			# looking for value being held
			if (len(serialAngleBuf) == CONST.ANGLE_CONSECUTIVE):
				skG.star(sc)
				skG.deleteStar(sc)
				skG.erase(sc, 'white')
				nTrials = nTrials + 1
				if nTrials == len(trialAngles):
					break
				skG.drawForearm(sc,trialAngles[nTrials], skG.COLOR)
				skG.updateTrialLabel(sc, nTrials)
				skG.delay(sc, t)
		else:
			serialAngleBuf = []
f.close()
