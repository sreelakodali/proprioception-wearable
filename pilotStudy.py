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

t = 10
nTrials = 0
sc = turtle.Screen()
trialAngles = range(30,180,15) # Generate trial angles

def updateTrialLabel():
	global sc
	sc.tracer(0)
	turtle.penup()
	turtle.goto(325,300)
	global nTrials
	turtle.write(nTrials+1, move=False, font=("Arial",36, "normal"))
	turtle.penup()

# Initialize GUI
sc.tracer(0)
sc.title("Pilot Study")
skG.initialize()

# Initialize Serial reading and data saving
fileName = str(datetime.datetime.now())[0:16] # default name is date and time
fileName = ((fileName.replace('/', '_')).replace(' ', '_')).replace(':','-')
p = CONST.PATH_LAPTOP +fileName+'_PILOT/'
# if not (os.path.exists(p)):
# 	os.makedirs(p)
# 	print("New directory created: %s" % fileName)
mcu = serial.Serial(port=CONST.PORT_NAME, baudrate=CONST.BAUD_RATE, timeout=.1)
# if (CONST.TRANSFER_RAW): f = open(p + 'raw_' + fileName + '.csv', 'w+', encoding='UTF8', newline='')
# else: f = open(p + "processed_" + fileName + '.csv', 'w+', encoding='UTF8', newline='')
# writer = csv.writer(f)
dataFunc = {'time':sk.millisToSeconds, 'flex sensor':sk.computeAngle,'actuator position, command':sk.commandToPosition, \
			'actuator position, measured':sk.feedbackToPosition, 'force':sk.computeForce}
# writer.writerow(list(dataFunc.keys()))

# Read in serial data and save in csv
skG.drawForearm(sc,trialAngles[nTrials])
updateTrialLabel()
skG.delay(sc, t)
serialAngleBuf = []
while (nTrials < CONST.N_TOTAL_TRIALS):
	value = mcu.readline()
	value = str(value, "utf-8").split(",")

	# if valid data packet, convert to right units and write in csv
	#print(len(value))
	if (len(value) == len(dataFunc)):
		newRow = sk.processNewRow(value, nTrials)
		serialAngle = newRow[1]
		#s = "Time=" + str(newRow[0]) + ", Measured=" + str(serialAngle) + ", Target=" + str(trialAngles[nTrials])
		newRow.append(nTrials)
		print(newRow)
		#writer.writerow(newRow)
		#print(s)
		if ((serialAngle > (trialAngles[nTrials] - CONST.ANGLE_TOLERANCE)) and (serialAngle < (trialAngles[nTrials] + CONST.ANGLE_TOLERANCE))):
			serialAngleBuf.append(serialAngle)

			# looking for value being held
			if (len(serialAngleBuf) == 32):
				skG.star()
				skG.deleteStar(sc)
				skG.deleteForearm(sc)
				nTrials = nTrials + 1
				if nTrials == len(trialAngles):
					break
				skG.drawForearm(sc,trialAngles[nTrials])
				updateTrialLabel()
				skG.delay(sc, t)
		else:
			serialAngleBuf = []
#f.close()



