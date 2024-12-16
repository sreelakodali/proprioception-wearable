# BLE support functions for JND experiment
# Written by: Sreela Kodali (kodali@stanford.edu) 

import serial, datetime, csv, sys, getopt, os, shutil, turtle, random, time, keyboard, asyncio, socket, re
import numpy as np
#from scipy import signal
from bleak import BleakScanner, BleakClient
from itertools import count, takewhile
from typing import Iterator
from bleak.backends.characteristic import BleakGATTCharacteristic
from bleak.backends.device import BLEDevice
from bleak.backends.scanner import AdvertisementData
import constants as CONST
import skFunctions as sk
import skPilotGraphics as skG
import skCalibrationFunctions as skC

# data packet structure, length 6
# time, setpoint, set - err, filtered force value, commandedActuatorPos, measuredActuatorPos
dataFunc = {'time':sk.millisToSeconds, 'setpoint':sk.doNothing,'set-err':sk.doNothing, \
			'filteredRawForce':sk.doNothing, 'commandedActuatorPos':sk.doNothing, \
			'measuredActuatorPos':sk.doNothing} #sk.feedbackToPosition, sk.commandToPosition


EXPERIMENT_TEXT_0 = ["Welcome!", "Let's begin the experiment", "", "", "", "", "", "", "", "", "", "", "Please click the red key to continue."]
EXPERIMENT_TEXT_1 = ["Experiment", "Task: Identify whether Stimulus A feels more,", "intense, the same, or less intense than Stimulus B.", "", "",  "", "", "", "", "", "Use >, =, and < keys to indicate your answer,", "and then click the red key to go to the next trial.", "Please click the red key to proceed."]
EXPERIMENT_TEXT = [EXPERIMENT_TEXT_0, EXPERIMENT_TEXT_1]
EXPERIMENT_TEXT_3 = ["JND Study", ""]
EXPERIMENT_TEXT_2 = ["Initializing", "Please wait 20 seconds until we begin"]
EXPERIMENT_TEXT_4 = ["", "Please click the red key to start."]
#CALIBRATION_TEXT1 = ["Calibration", "Please indicate your minimum detection and", "maximum comfortable pressures. Controls are:", "", "", "", "", "", "", "", "> and < extend and retract the device", "8 retracts the device all the way and please use", "= to indicate when you feel a min/max pressure.", "Click the red key for more details."]
CALIBRATION_TEXT1 = ["Calibration", "Please indicate your minimum detection and", "maximum comfortable pressures. Controls are:", "", "8 retracts the", "device fully", "", "> and < increase", "decrease", "pressure", "", "Please use = to indicate when you feel a min/max", "pressure. Click the red key for more details."]

#CALIBRATION_TEXT2 = ["Calibration: Procedure", "Press > to extend the device into your arm and", "apply pressure. When you first feel contact, click =.", "", "Then continue to press > to apply increasing", "pressure. When you've reached your maximum", "comfortable pressure, click =. You may use >", "and < keys to increase/decrease pressure and", "hone into your maximum comfortable pressure.", "Then click 8 to retract the device. We'll repeat this", "process 3x. When done, click the red key."]

CALIBRATION_TEXT3 = ["Calibration: Procedure", "1. Apply pressure with >", "2. When you first feel contact, click =.",  "3. Continue to press > to apply more pressure.", "4. Use > and < keys to hone into your", "maximum comfortable pressure.", "5. Click = when you've reached your maximum", "comfortable pressure.", "6. Click 8 to retract the device.", "", "We'll repeat this process 3x. After 3x, please", "click the red key to move onto the next task."]


addr_Adafruit1 = "026B8104-5A8F-E8AF-518E-B778DB1C9CE2"
addr_Adafruit2 = "380FFB6A-AB04-7634-8A6C-C8E255F7A26C"
UART_SERVICE_UUID = "6e400001-b5a3-f393-e0a9-e50e24dcca9e"
UART_RX_CHAR_UUID = "6e400002-b5a3-f393-e0a9-e50e24dcca9e" # 2, RX write
UART_TX_CHAR_UUID = "6e400003-b5a3-f393-e0a9-e50e24dcca9e" # 3, TX notify
bleName = "Adafruit Bluefruit LE"


t = 1

#initial value is randomized 
def generateInitialValue(increasing, minValue, maxValue, reference):
	if (increasing): # 
		Xo = random.uniform(minValue, reference); #initial value less than reference
	else:
		Xo = random.uniform(reference, maxValue); # initial value is greater than reference
	Xo = round(Xo, 2)

	return Xo

def initializeGUI(sc):
	sc.tracer(0)
	sc.title("JND Study")
	tr = turtle.Turtle()
	turtle.hideturtle()
	sc.addshape('/Users/Sreela/Documents/School/Stanford/Year3_2/PIEZO2/GUIFigures/keypadJND.gif')
	skG.initializeWindow(sc,EXPERIMENT_TEXT_0)
	keyboard.wait('down')
	return tr

def instructionsGUI(sc, tr):
	# skG.initializeWindow(sc,EXPERIMENT_TEXT_0)
	# keyboard.wait('down')
	#turtle.pendown()
	#tr.shape('/Users/Sreela/Documents/School/Stanford/Year3_2/PIEZO2/GUIFigures/keypadJND.gif')
	#skG.erase5(sc)
	skG.initializeWindow(sc,EXPERIMENT_TEXT_1)
	tr.shape('/Users/Sreela/Documents/School/Stanford/Year3_2/PIEZO2/GUIFigures/keypadJND.gif')
	turtle.update()
	#turtle.penup()
	keyboard.wait('down')

def calibrationMinMaxGUI(sc, tr):
	skG.initializeWindow(sc,CALIBRATION_TEXT1) # EXPERIMENT_TEXT_0
	tr.shape('/Users/Sreela/Documents/School/Stanford/Year3_2/PIEZO2/GUIFigures/keypadJND.gif')
	turtle.update()
	keyboard.wait('down')
	# skG.initializeWindow(sc,CALIBRATION_TEXT2) # EXPERIMENT_TEXT_0
	# turtle.update()
	#keyboard.wait('down')

async def waitGUI(sc):
	skG.initializeWindow(sc,EXPERIMENT_TEXT_2)
	await waitSK(20)
	
def initializeTrialFiles(p, fileName, key):
	n = open(p + 'trial' + key + "_" + fileName + '.csv', 'w+', encoding='UTF8', newline='')
	writer = csv.writer(n) # csv writer for trials
	writer.writerow(["trialCount", "Test", "Reference", "A", "B", "answerKey", "userAnswer", "reversals", "graphIcon"])
	n.close()

def loadASRValues(c):
	print("LOAD ASR VALUES")
	c.send(("LOAD ASR VALUES\n").encode())

	paramNames = ['Min1', 'Max1', 'Min2', 'Max2', 'Min3', 'Max3']
	param = [0.0] * len(paramNames)
	for i in range(0,len(paramNames)):
		print(paramNames[i] + "?")
		p = input()
		remove = ["\x1b", "B", "A", "C", "\[5~", "\[", "R", "\^"]
		for r in remove:
			p = re.sub(r,"",p)
		param[i] = float(p)

  	# compute average min
	avgMin = round(((param[0] + param[2] + param[4]) / 3.0), 2)
	avgMax = round(((param[1] + param[3] + param[5]) / 3.0), 2)
	rangeASR = avgMax - avgMin

	q1 = round((avgMin + rangeASR/4.0), 2)
	q2 = round((rangeASR/2.0 + avgMin), 2)
	q3 = round((avgMax - rangeASR/4.0), 2)

	for i in range(0,len(paramNames)):
		print(paramNames[i] + " "+ str(param[i]))
		c.send((paramNames[i] + " "+ str(param[i]) + "\n").encode())


	print("avgMin " + str(avgMin))
	print("avgMax " + str(avgMax))
	print("q1 " + str(q1))
	print("q2 " + str(q2))
	print("q3 " + str(q3))

	c.send(("avgMin " + str(avgMin) + "\n").encode())
	c.send(("avgMax " + str(avgMax) + "\n").encode())
	c.send(("q1 " + str(q1) + "\n").encode())
	c.send(("q2 " + str(q2) + "\n").encode())
	c.send(("q3 " + str(q3) + "\n").encode())

	return [avgMin, avgMax, q1, q2, q3]

def prepareExperimentGUI(sc):
	skG.initializeWindow(sc,EXPERIMENT_TEXT_3)
	#skG.initializeTrialLabel(sc, n)
	skG.updateTrialLabel(sc, 0)
	skG.delay(sc, t)

def closeFiles(arr):
	for i in arr:
		i.close()

def randomizeStimuli(ref, test, c):
	r = random.randrange(0,2)
	c.send(("r: " + str(r)+ "\n").encode())
	if (r == 1):
		return (ref, test, r)
	else:
		return (test, ref, r)

def createDataFiles(p, name, idx_Act):
	f = open(p + 'raw_device' + str(idx_Act) + '_' + name + '.csv', 'w+', encoding='UTF8', newline='')
	h = open(p + 'processed_device' + str(idx_Act) + '_' + name + '.csv', 'w+', encoding='UTF8', newline='')
	writer = csv.writer(h)

	columnNames = list(dataFunc.keys())
	columnNames.append("TrialCounter\n")
	#columnNames = str(columnNames) + "\n"
	for k in [f, h]:
		for i in columnNames:
			if (i == "TrialCounter\n"):
				k.write(str(i))
			else:
				k.write(str(i) + ",")
			#k.write(columnNames)

	return (f, h, writer)

def writeOutDataBLE(i, writer, f, trialCount, verbose):
	
	# if it has the word SETPOINT, write it 
	s = i.split(",")
	if "SETPOINT" in i:
		f.write(i+ "\n")
		writer.write(i+ "\n")
	elif (len(s) > 2):
		f.write(i+"," + str(trialCount) + "\n")
		writer.write(i+"," + str(trialCount) + "\n")
	
	# if (len(i) == len(dataFunc)): 
	# 	# raw = [j.rstrip() for j in i]
	# 	# raw = raw + [trialCount]	
	# 	#writer2.writerow(raw)

	# 	newRow = sk.processNewRow(dataFunc, i)	
	# 	newRow = newRow + [trialCount]
	# 	writer.writerow(newRow)
	# 	if (verbose):
	# 		print(newRow)

def formatBLEPacket(value, nAct):
	if (nAct == 1):
		buf = str("x")+str(value)+"\n" 
	else:
		buf = str("y")+str(value)+"\n"
	return buf.encode(encoding="ascii")

def updateUserAnswerGUI(sc, userAnswer):
	skG.eraseLine(sc,-350,40)
	if (userAnswer == 1):		
		skG.writeText(sc, -350,30, "(A > B)           A == B             A < B ", skG.COLOR_RED)
	elif (userAnswer == 2):
		skG.writeText(sc, -350,30, "A > B            (A == B)            A < B ", skG.COLOR_RED)
	elif (userAnswer == 3):
		skG.writeText(sc, -350,30, "A > B             A == B            (A < B)", skG.COLOR_RED)

def displayAnswerOptionsGUI(sc):
	skG.writeText(sc, -350,80, "Select your answer:", skG.COLOR)
	skG.writeText(sc, -350,30, "A > B             A == B             A < B ", skG.COLOR_RED)
	skG.writeText(sc, -350,-120, "Press the red key to confirm your answer", skG.COLOR)
	skG.writeText(sc, -350,-170, "and proceed to the next trial.", skG.COLOR_GREEN)

async def waitSK(td):
	w = 0
	endTime = datetime.datetime.now() + datetime.timedelta(seconds=td)
	while (datetime.datetime.now() < endTime):
		await asyncio.sleep(0.01)
		w = w + 1
	#time.sleep(td)

async def sendSetpoint(value, client, rx_char, idx):
	await client.write_gatt_char(rx_char, formatBLEPacket(value,idx), response=False) 

async def sendPoke(sc, c, value, retract, wait, client, rx_char, stimulus1, idx_Act):

	if (stimulus1):
		outputStr = "Receiving Stimulus A: "
		outputStr2 = "Stimulus A in progress"
		h = 230
	else:
		outputStr = "Receiving Stimulus B: "
		outputStr2 = "Stimulus B in progress"
		h = 180
	c.send((outputStr + str(value) + "\n").encode())
	skG.writeText(sc, -350, h, outputStr2, skG.COLOR)

	# Send poke A and wait
	# for k in range(0,len(clientArr)):
	# 	await sendSetpoint(value, clientArr[k], rx_charArr[k], k+1)
	await sendSetpoint(value, client, rx_char, idx_Act) 	
	await waitSK(wait) 	# hold the poke	

	# Retract and wait
	# for k in range(0,len(clientArr)):
	# 	await sendSetpoint(retract, clientArr[k], rx_charArr[k], k+1)
	await sendSetpoint(retract, client, rx_char, idx_Act) 	
	await waitSK(wait/2) 	# hold the poke
