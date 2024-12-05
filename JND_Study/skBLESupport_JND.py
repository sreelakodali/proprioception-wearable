# BLE support functions for JND experiment
# Written by: Sreela Kodali (kodali@stanford.edu) 

import serial, datetime, csv, sys, getopt, os, shutil, turtle, random, time, keyboard, asyncio
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
EXPERIMENT_TEXT_1 = ["Experiment", "Task: Identify whether Stimulus A feels more,", "intense, the same, or less intense than Stimulus B.", "", "",  "", "", "", "", "", "Use >, =, and < keys to indicate your answer,", "and then click the red key to go to the next trial.", "Please click the red key to start."]
EXPERIMENT_TEXT = [EXPERIMENT_TEXT_0, EXPERIMENT_TEXT_1]
EXPERIMENT_TEXT_3 = ["JND Study", ""]

addr_Adafruit1 = "026B8104-5A8F-E8AF-518E-B778DB1C9CE2"
addr_Adafruit2 = "380FFB6A-AB04-7634-8A6C-C8E255F7A26C"
UART_SERVICE_UUID = "6e400001-b5a3-f393-e0a9-e50e24dcca9e"
UART_RX_CHAR_UUID = "6e400002-b5a3-f393-e0a9-e50e24dcca9e" # 2, RX write
UART_TX_CHAR_UUID = "6e400003-b5a3-f393-e0a9-e50e24dcca9e" # 3, TX notify
bleName = "Adafruit Bluefruit LE"


t = 1

def initializeGUI(sc):
	sc.tracer(0)
	sc.title("JND Study")
	tr = turtle.Turtle()
	turtle.hideturtle()
	sc.addshape('/Users/Sreela/Documents/School/Stanford/Year3_2/PIEZO2/GUIFigures/keypadJND.gif')

	return tr

def instructionsGUI(sc, tr):
	skG.initializeWindow(sc,EXPERIMENT_TEXT_0)
	keyboard.wait('down')
	skG.initializeWindow(sc,EXPERIMENT_TEXT_1)
	tr.shape('/Users/Sreela/Documents/School/Stanford/Year3_2/PIEZO2/GUIFigures/keypadJND.gif')
	turtle.update()
	keyboard.wait('down')


def prepareExperimentGUI(sc, n):
	skG.initializeWindow(sc,EXPERIMENT_TEXT_3)
	skG.initializeTrialLabel(sc, n)
	skG.updateTrialLabel(sc, 0)
	skG.delay(sc, t)

def closeFiles(arr):
	for i in arr:
		i.close()

def randomizeStimuli(ref, test):
	r = random.randrange(0,2)
	print("r: " + str(r))
	if (r == 1):
		return (ref, test)
	else:
		return (test, ref)

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
	f.write(i+"," + str(trialCount) + "\n")

	i = i.split(",")
	if (len(i) == len(dataFunc)): 
		# raw = [j.rstrip() for j in i]
		# raw = raw + [trialCount]	
		#writer2.writerow(raw)

		newRow = sk.processNewRow(dataFunc, i)	
		newRow = newRow + [trialCount]
		writer.writerow(newRow)
		if (verbose):
			print(newRow)

def formatBLEPacket(value, nAct):
	if (nAct == 1):
		buf = str("X")+str(value) 
	else:
		buf = str("Y")+str(value)
	return buf.encode()

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

def waitSK(td):
	w = 0
	endTime = datetime.datetime.now() + datetime.timedelta(seconds=td)
	while (datetime.datetime.now() < endTime):
		w = w + 1
	#time.sleep(td)

async def sendSetpoint(value, client, rx_char, idx):
	await client.write_gatt_char(rx_char, formatBLEPacket(value,idx)) 

def sendPoke(sc, value, retract, wait, clientArr, rx_charArr, stimulus1):

	if (stimulus1):
		outputStr = "Receiving Stimulus A: "
		outputStr2 = "Stimulus A in progress"
		h = 230
	else:
		outputStr = "Receiving Stimulus B: "
		outputStr2 = "Stimulus B in progress"
		h = 180
	print(outputStr + str(value))
	skG.writeText(sc, -350, h, outputStr2, skG.COLOR)

	# Send poke A and wait
	for k in range(0,len(clientArr)):
		sendSetpoint(value, clientArr[k], rx_charArr[k], k) 	
	waitSK(wait) 	# hold the poke	

	# Retract and wait
	for k in range(0,len(clientArr)):
		sendSetpoint(retract, clientArr[k], rx_charArr[k], k)
	waitSK(wait/2) 	# hold the poke
