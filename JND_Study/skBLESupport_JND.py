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


def writeOutDataBLE(i, writer, trialCount, verbose):
	i = str(i, "utf-8").split(",")
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

def wait(td):
	w = 0
	endTime = datetime.datetime.now() + datetime.timedelta(seconds=td)
	while (datetime.datetime.now() < endTime):
		w = w + 1
	#time.sleep(td)

def sendSetpoint(value, client, rx_char, idx):
	await client.write_gatt_char(rx_char, formatBLEPacket(value,idx)) 

def sendPoke(sc, h, value, retract, wait, clientArr, rx_charArr):
	print("Receiving Stimulus: " + str(packetA))
	skG.writeText(sc, -350, h, "Stimulus A in progress", skG.COLOR)

	# Send poke A and wait
	for k in range(0,len(clientArr)):
		sendSetpoint(value, clientArr[k], rx_charArr[k], k) 	
	wait(wait) 	# hold the poke	

	# Retract and wait
	for k in range(0,len(clientArr)):
		sendSetpoint(retract, clientArr[k], rx_charArr[k], k) 	
	wait(wait/2) 	# hold the poke
