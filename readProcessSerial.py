# Read and Process Serial Data
# Written by: Sreela Kodali (kodali@stanford.edu) 

import serial
import datetime
import csv
import os
import sys, getopt
import numpy as np
from scipy import signal
import constants as CONST
import skFunctions as sk

# DIRECTORY
fileName = str(datetime.datetime.now())[0:16] # default name is date and time
fileName = ((fileName.replace('/', '_')).replace(' ', '_')).replace(':','-')
p = CONST.PATH_LAPTOP +fileName+'/'
if not (os.path.exists(p)):
	os.makedirs(p)
	print("New directory created: %s" % fileName)

mcu = serial.Serial(port=CONST.PORT_NAME, baudrate=CONST.BAUD_RATE, timeout=.1)
if (CONST.TRANSFER_RAW): f = open(p + 'raw_' + fileName + '.csv', 'w+', encoding='UTF8', newline='')
else: f = open(p + "processed_" + fileName + '.csv', 'w+', encoding='UTF8', newline='')
writer = csv.writer(f)

dataFunc = {'time':sk.millisToSeconds, 'flex sensor':sk.computeAngle,'actuator position, command':sk.commandToPosition, \
			'actuator position, measured':sk.feedbackToPosition, 'force':sk.computeForce}


plotOn = False
savePlot = 0
noiseAnalysis = ' '

# if plot on

opts, args = getopt.getopt(sys.argv[1:],"ps",["txt=","noise="])

for opt, arg in opts:
	if opt == '-p':
		plotOn = True
		# create arrays to hold data
		time = []
		angle = []
		device1_positionCommand = []
		device1_positionMeasured = []
		force = []
	elif opt == '-s':
		savePlot = 1

	elif opt == '--txt':
		g = open(p + "notes" + fileName + '.txt', 'w+', encoding='UTF8', newline='')
		g.write(str(arg))
		g.close()

	elif opt == '--noise':
		noiseAnalysis = arg

# Read in serial data and save in csv
if (not(CONST.TRANSFER_RAW)): writer.writerow(list(dataFunc.keys()))
endTime = datetime.datetime.now() + datetime.timedelta(seconds=CONST.RUNTIME_LENGTH)
while (datetime.datetime.now() < endTime):
	value = mcu.readline()
	value = str(value, "utf-8").split(",")

	if (not(CONST.TRANSFER_RAW)):
		# if valid data packet, convert to right units and write in csv
		#print(len(value))
		if (len(value) == len(dataFunc)):
			newRow = sk.processNewRow(dataFunc, value)
			print(newRow)
			writer.writerow(newRow)
			if (plotOn):
				time.append(newRow[0])
				angle.append(newRow[1])
				device1_positionCommand.append(newRow[2])
				device1_positionMeasured.append(newRow[3])
				force.append(newRow[4])

	else:
		print(value)
		writer.writerow(value)

f.close()


if (plotOn): sk.plot_System(savePlot, p, fileName, time, angle, force, device1_positionMeasured, device1_positionCommand)
if (noiseAnalysis in ('FLEX', 'flex', 'flexSensor', 'angle')):
	from scipy.fft import fft, ifft, fftfreq

	N = len(angle)
	timeLength = time[-1]-time[0]
	yF = fft(angle)
	xF = fftfreq(N,(timeLength/N))
	sk.plot_Noise(savePlot, p, fileName, xF, np.abs(yF))
