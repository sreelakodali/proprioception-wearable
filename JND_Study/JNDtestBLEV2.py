# JND Test - BLE Version
# Written by: Sreela Kodali (kodali@stanford.edu) 

import serial, datetime, csv, sys, getopt, os, shutil, turtle
import random, time, keyboard, asyncio, socket, re, statistics
import numpy as np
from collections import deque
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
import skBLESupport_JND as skB

# ------------
N_ACTUATORS = 2
trialCount = 0 # counter

# ------- CONSTANTS, DIRECTORY, & setting up files
PATH = '/Users/Sreela/Documents/School/Stanford/Year3_2/PIEZO2/JND_Study/bleData/' # change this to your path!

print("Welcome to the study! Please enter subject number:")
nSubject = input()
nSubject = "subject" + nSubject + "_"
fileName = str(datetime.datetime.now())[0:16] # default name is date and time
fileName = ((fileName.replace('/', '_')).replace(' ', '_')).replace(':','-')
fileName = nSubject + fileName
p = PATH +fileName+'/'
if not (os.path.exists(p)):
    os.makedirs(p)
    print("New directory created: %s" % fileName)

f, h = skB.createDataFiles(p, fileName, 1)
#if (N_ACTUATORS == 2):
g, m = skB.createDataFiles(p, fileName, 2)

# ------- BLE values
databuf = ""
databuf2 = ""
linebuf = ""

# ----- Global Force Values, for holding... let's see
force1Global = 0.0
force2Global = 0.0
tStim = 4.0 # sets the actual stimulation time. 4-1-25: maybe make it 6-8 seconds
MIN_TRIALS = 12

# ------- Display & GUI variables
t = 1
sc = turtle.Screen()
calibrate = 1
waitTime = 10 # seconds
retractPos = 0.0

async def waitSK_setpointTimer(td, s, c, n):
	global force1Global
	global force2Global
	global tStim
	reachedBool = False
	w = 0

	endTime = datetime.datetime.now() + datetime.timedelta(seconds=td)
	while (datetime.datetime.now() < endTime):
		#print(force1Global)
		# reached setpoint. note the time

		if (n == 1):
			if ( (abs(float(force1Global) - s) <= 0.15) and (reachedBool ==False) and s > 0):
				reached = datetime.datetime.now()
				c.send(("REACHED FORCE " + str(s) + "\n").encode())
				reachedBool = True
				break
		elif (n == 2):
			if ( (abs(float(force2Global) - s) <= 0.15) and (reachedBool ==False) and s > 0):
				reached = datetime.datetime.now()
				c.send(("REACHED FORCE " + str(s) + "\n").encode())
				reachedBool = True
				break

		await asyncio.sleep(0.01)
		w = w + 1

	if (reachedBool == False):
		reached = datetime.datetime.now()
	stimTime = (datetime.datetime.now() - reached).total_seconds()
	c.send(("Stim time = " + str(stimTime) + "s \n").encode())
	while ( (stimTime < tStim) and (s > 0) and (reachedBool == True)): # 
		await asyncio.sleep(0.01)
		w = w + 1
		stimTime = (datetime.datetime.now() - reached).total_seconds()
	c.send(("Final Stim time = " + str(stimTime) + "s \n").encode())


async def methodOfConstantStimuli(reference, inc1, inc2, inc3, l, c, nAct, avgMin, avgMax, wait, retract, client1, rx_char1, client2, rx_char2):
	global trialCount
	global fileName
	global p
	nWrong = 0
	nRight = 0

	trialCount = 0
	staircaseFileName = skB.initializeTrialFiles(p, fileName, str(reference), l)
	c.send((("ACTUATOR#= {}, REFERENCE={}\n").format(nAct, reference)).encode())

	# step 1: generate 8 values for comparisons
	comparisonValues = [reference - inc3, reference - inc2, reference - inc1, reference + inc3, reference + inc2, reference + inc1]

	# step 2: randomize order for experiment, 10 times per value
	
	experimentStimuli = []
	for j in comparisonValues:
		for i in range(0,10):
			experimentStimuli.append(j)
	random.shuffle(experimentStimuli)
	stimuliStack = deque(experimentStimuli)
	c.send((str(stimuliStack)).encode())

	for i in range(0, len(experimentStimuli)):
		graphIcon = 0
		await asyncio.sleep(0.01)
		test = stimuliStack.pop() #testArr[trialCount]

		c.send( ( "----- TRIAL #" + str(trialCount) + " -----\n").encode())
		c.send(("test: " + str(test) + "\n" ).encode())

		packetA, packetB, r = skB.randomizeStimuli(reference, test, c)
		# if r == 1, A=ref, B=test
		# if r== 0, A=test, B=ref

		# send stimuli A
		c.send(("Receiving Stimulus A: " + str(packetA) + "\n").encode())
		skG.writeText(sc, -350, 230, "Stimulus A in progress", skG.COLOR)

		await skB.sendSetpoint(packetA, client1, rx_char1, 1) 	
		if (nAct == 2):
			await skB.sendSetpoint(packetA, client2, rx_char2, 2) 	
		#await skB.waitSK(wait) 	# hold the poke	
		await waitSK_setpointTimer(wait, packetA, c, 1) # device1

		await skB.sendSetpoint(retract, client1, rx_char1, 1)
		if (nAct == 2):
			await skB.sendSetpoint(retract, client2, rx_char2, 2)
		await skB.waitSK(2) 	# retract

		# send stimuli B
		c.send(("Receiving Stimulus B: " + str(packetB) + "\n").encode())
		skG.writeText(sc, -350, 180, "Stimulus B in progress", skG.COLOR)

		await skB.sendSetpoint(packetB, client1, rx_char1, 1) 	
		if (nAct == 2):
			await skB.sendSetpoint(packetB, client2, rx_char2, 2) 	
		#await skB.waitSK(wait) 	# hold the poke	
		await waitSK_setpointTimer(wait, packetB, c, 1) #device 1

		await skB.sendSetpoint(retract, client1, rx_char1, 1)
		if (nAct == 2):
			await skB.sendSetpoint(retract, client2, rx_char2, 2)
		await skB.waitSK(2) 	# retract	

		# find the real answer
		# 1 means A > B, 2 means A == B, 3 means A < B
		answerKey = (packetA > packetB)*1 + (packetA == packetB)*2 + (packetA < packetB)*3
		c.send(("The real answer is: " + str(answerKey) + "\n").encode())

		skB.displayAnswerOptionsGUI2AFC(sc)
		userAnswer = 0
		while(1):
			await asyncio.sleep(0.01)
		# wait for user's input
			k = keyboard.read_key()

			if k == 'page up':
				userAnswer = 1
				skB.updateUserAnswerGUI2AFC(sc, userAnswer)

			elif k == 'page down':
				userAnswer = 3
				skB.updateUserAnswerGUI2AFC(sc, userAnswer)

			elif k == 'down':

				if (userAnswer == 0):
					skG.writeText(sc, -350,-20, "You have to choose an answer to proceed.", skG.COLOR)					
				else:
					skG.eraseLine(sc,-350,40)
					skG.erase(sc, 'white')
					#skG.eraseLine(sc,-350,-20)
					trialCount = trialCount + 1
					#if trialCount < N_Trials:
					skG.updateTrialLabel(sc, trialCount)
					skG.delay(sc, t)
					break
			
		# check the answer. depending on answer, determine next test value
		# if answer wrong, reset streak and step up test value
		c.send(("User answer is: " + str(userAnswer)+ "\n").encode())
		await asyncio.sleep(0.01)

		if (userAnswer == answerKey):
			nRight = nRight + 1
		else:
			nWrong = nWrong + 1
		# if test < ref

		n = open(staircaseFileName, 'a', encoding='UTF8', newline='')
		n.write(str(trialCount) + "," + str(test) + "," + str(reference) + "," + str(packetA) + "," + str(packetB)+ "," + str(answerKey)+ "," + str(userAnswer)+ "," + str(nRight) + "," + str(nWrong) + "," + str(r) + "\n")
		n.close()
		userAnswer = 0

	c.send(("DONE\n").encode())


# provide staircasing parameters: going up or down (bounds); reference, nUP, nDown, retract, wait, c, clients and rxchars
async def staircase2AFC(Xo, l, c, nAct, nDown, avgMin, avgMax, key, reference, wait, retract, client1, rx_char1, client2, rx_char2):
	#global writer
	global trialCount
	global fileName
	global p
	#global n
	packetA = 0
	packetB = 0
	rightStreak = 0
	answerKey = 0
	userAnswer = 0
	test = 0
	trialCount = 0 # counter
	reversals = 0
	nWrong = 0
	nRight = 0
	increment = 0

	localDir = 1 # 1 is increasing. 0 is decreasing. starts increasing
	staircaseFileName = skB.initializeTrialFiles(p, fileName, key, l)

	# we are assuming nUp, nDown: 2:1
	testArr = [] # [0.0] * 50
	Ldb = 2 #db
	Xo = round(Xo, 2)
	testArr.append(Xo)
	
	c.send((("ACTUATOR#= {}, QUARTILE={}\n").format(nAct, key)).encode())
	c.send(("STAIRCASE " + key + "\n").encode())
	c.send(("INITIAL VALUE= " + str(Xo) + "\n").encode())
	c.send(("REFERENCE= " + str(reference) + "\n").encode())
	
	keepGoing = True
	while (keepGoing):
		graphIcon = 0
		await asyncio.sleep(0.01)
		test = testArr[trialCount]

		c.send( ( "----- TRIAL #" + str(trialCount) + " -----\n").encode())
		c.send(("test: " + str(test) + "\n" ).encode())
		c.send(("rightStreak: " + str(rightStreak) + "\n").encode())

		packetA, packetB, r = skB.randomizeStimuli(reference, test, c)
		# if r == 1, A=ref, B=test
		# if r== 0, A=test, B=ref

		# send stimuli A
		c.send(("Receiving Stimulus A: " + str(packetA) + "\n").encode())
		skG.writeText(sc, -350, 230, "Stimulus A in progress", skG.COLOR)

		await skB.sendSetpoint(packetA, client1, rx_char1, 1) 	
		if (nAct == 2):
			await skB.sendSetpoint(packetA, client2, rx_char2, 2) 	
		#await skB.waitSK(wait) 	# hold the poke	
		await waitSK_setpointTimer(wait, packetA, c, 1) # device1

		await skB.sendSetpoint(retract, client1, rx_char1, 1)
		if (nAct == 2):
			await skB.sendSetpoint(retract, client2, rx_char2, 2)
		await skB.waitSK(2) 	# retract

		# send stimuli B
		c.send(("Receiving Stimulus B: " + str(packetB) + "\n").encode())
		skG.writeText(sc, -350, 180, "Stimulus B in progress", skG.COLOR)

		await skB.sendSetpoint(packetB, client1, rx_char1, 1) 	
		if (nAct == 2):
			await skB.sendSetpoint(packetB, client2, rx_char2, 2) 	
		#await skB.waitSK(wait) 	# hold the poke	
		await waitSK_setpointTimer(wait, packetB, c, 1) #device 1

		await skB.sendSetpoint(retract, client1, rx_char1, 1)
		if (nAct == 2):
			await skB.sendSetpoint(retract, client2, rx_char2, 2)
		await skB.waitSK(2) 	# retract	

		# find the real answer
		# 1 means A > B, 2 means A == B, 3 means A < B
		answerKey = (packetA > packetB)*1 + (packetA == packetB)*2 + (packetA < packetB)*3
		c.send(("The real answer is: " + str(answerKey) + "\n").encode())

		skB.displayAnswerOptionsGUI2AFC(sc)

		while(1):
			await asyncio.sleep(0.01)
		# wait for user's input
			k = keyboard.read_key()

			if k == 'page up':
				userAnswer = 1
				skB.updateUserAnswerGUI2AFC(sc, userAnswer)

			elif k == 'page down':
				userAnswer = 3
				skB.updateUserAnswerGUI2AFC(sc, userAnswer)

			elif k == 'down':

				if (userAnswer == 0):
					skG.writeText(sc, -350,-20, "You have to choose an answer to proceed.", skG.COLOR)					
				else:
					skG.eraseLine(sc,-350,40)
					skG.erase(sc, 'white')
					#skG.eraseLine(sc,-350,-20)
					trialCount = trialCount + 1
					#if trialCount < N_Trials:
					skG.updateTrialLabel(sc, trialCount)
					skG.delay(sc, t)
					break
			
		# check the answer. depending on answer, determine next test value
		# if answer wrong, reset streak and step up test value
		c.send(("User answer is: " + str(userAnswer)+ "\n").encode())
		await asyncio.sleep(0.01)

		if (userAnswer == answerKey):
			nRight = nRight + 1
		else:
			nWrong = nWrong + 1
		# if test < ref

		## if r == 1, A=ref, B=test. --> to have ref > test, answer 1
		# if r== 0, A=test, B=ref. --> to have test < ref, answer 3
		
		# if (increasing):
		# 	condition1 = ((r==0) and (userAnswer==1)) or ((r==1) and (userAnswer==3))
		# 	condition3 = ((r==0) and (userAnswer==3)) or ((r==1) and (userAnswer==1))

		# if TEST > reference, needs to be correct N times before reducing.
		if ((r==0) and (userAnswer==1)) or ((r==1) and (userAnswer==3)):
			
			c.send(("User said TEST is greater than REFERENCE\n").encode())
			graphIcon = 3
			rightStreak = rightStreak + 1

			# if greater N times in a row, reduce it to the last less value
			if (rightStreak == nDown):
				rightStreak = 0
				newTest = test - increment	#increment = increment * -1

				# # if its a direction change, then reversal
				if (localDir==1):
					reversals = reversals + 1 # reversals
					Ldb = Ldb / 2 # Ldb is reduced
					if (Ldb <= 0.5):
						Ldb = 0.5
					c.send(("reversals:" + str(reversals)+ "\n").encode())
				localDir = 0

			else:
				newTest = test
				#localDir = 2 # keep the same
		
		# if TEST < reference, increase by the exponential factor
		elif ((r==0) and (userAnswer==3)) or ((r==1) and (userAnswer==1)):
			
			c.send(("User said TEST is less than REFERENCE\n").encode())
			graphIcon = 1
			rightStreak = 0

			newTest = test * 10 ** (Ldb/20)
			increment = newTest - test
			localDir = 1
			
		# updated termination conditions
		if (trialCount > MIN_TRIALS):

			# precomputation for condition #2
			equalityCheckVal = testArr[-10]
			nEqualityCheck = 0
			for j in testArr[-10:]:
				if (j==equalityCheckVal):
					nEqualityCheck = nEqualityCheck + 1

			# precomputation for condition #3
			diffVal = np.diff(np.array(testArr))
			diffVal = diffVal[diffVal != 0]

			# Condition #1: less than 2dB
			# the range of the most recent 10 values
			#if (abs(statistics.mean(testArr[-10:]) - reference) <  10**(0.1)):
			if ( (max(testArr[-10:]) - min(testArr[-10:])) <  1.2):#10**(2/20)
				keepGoing = False
				c.send(("Termination Condition #1 Reached: range of last 10 < 2 dB").encode())
			#npTestArr = np.array(testArr[-10:])

			# Condition #2: if the last 10 values are the exact same
			elif (nEqualityCheck == 10):
				keepGoing = False
				c.send(("Termination Condition #2 Reached: last 10 values the same").encode())
			
			# Condition #3: if the increment is smaller than the resolution of the system
			elif (min(abs(diffVal)) < skB.SYSTEM_MIN_RESOLUTION):
				keepGoing = False 
				c.send(("Termination Condition #3 Reached: increments are less than the system resolution").encode())

		# round and bound next value and append to array
		newTest = round(newTest, 2)
		if (newTest > avgMax):
			newTest = avgMax
		elif (newTest < avgMin):
			newTest = avgMin
		testArr.append(newTest)

		n = open(staircaseFileName, 'a', encoding='UTF8', newline='')
		n.write(str(trialCount) + "," + str(test) + "," + str(reference) + "," + str(packetA) + "," + str(packetB)+ "," + str(answerKey)+ "," + str(userAnswer)+ "," + str(reversals)+ "," + str(graphIcon) + "," + str(nRight) + "," + str(nWrong) + "," + str(r) + "\n")
		n.close()
		userAnswer = 0

	c.send(("DONE\n").encode())

async def orderingPairsSendStimuli(sc, c,k, v1, v2, c1, rx1, c2, rx2, wait):
	skB.orderedPairsGUI(sc)
	c.send(("Applying pair: " + str(v1) + ", " + str(v2) + "\n" ).encode())
	txt = "Stimulus " + str(k) + " in progress"
	skG.writeText(sc, -350, 230, txt, skG.COLOR)
	await skB.sendSetpoint(v1, c1, rx1, 1) 	
	await skB.sendSetpoint(v2, c2, rx2, 2)
	if (v2 > v1):
		await waitSK_setpointTimer(wait, v2, c, 2)
	else:
		await waitSK_setpointTimer(wait, v1, c, 1)
	#await skB.waitSK(wait) 	# hold the poke	

	await skB.sendSetpoint(0.0, c1, rx1, 1)
	await skB.sendSetpoint(0.0, c2, rx2, 2)
	await skB.waitSK(2) 	# hold the poke
	skG.writeText(sc, -350, 180, "Stimulus done.", skG.COLOR)
	c.send(("STIMULUS PAIR APPLIED, DONE\n").encode())

async def orderingPairs(sc, c, avgMin, avgMax, q2, wait, c1, rx1, c2, rx2):
	
	value1 = 0.0
	value2 = 0.0

	validKeys = ['7', '8', '9', '4', '5', '6', '1', '2', '3']
	random.shuffle(validKeys)

	c.send( ( "--- ORDERING PAIRS TASK ----\n").encode())
	c.send((" KEYS ORDER: " + str(validKeys) + "\n").encode())
	while (1):
		
		await asyncio.sleep(0.1)	
		k = keyboard.read_key()

		if k == validKeys[0]: # 00
			#await client1.write_gatt_char(rx_char1, ("c\n").encode(encoding="ascii"), response=False)
			value1 = avgMin
			value2 = avgMin
			c.send(("STIMULI PAIR: MIN, MIN\n").encode())
			await orderingPairsSendStimuli(sc, c, k, value1, value2, c1, rx1, c2, rx2, wait)

		elif k == validKeys[1]: # 01
			value1 = avgMin
			value2 = q2
			c.send(("STIMULI PAIR: MIN, MID\n").encode())
			await orderingPairsSendStimuli(sc, c, k, value1, value2, c1, rx1, c2, rx2, wait)

		elif k == validKeys[2]: # 02
			value1 = avgMin
			value2 = avgMax
			c.send(("STIMULI PAIR: MIN, MAX\n").encode())
			await orderingPairsSendStimuli(sc, c, k, value1, value2, c1, rx1, c2, rx2, wait)

		elif k == validKeys[3]: # 10
			value1 = q2
			value2 = avgMin
			c.send(("STIMULI PAIR: MID, MIN\n").encode())
			await orderingPairsSendStimuli(sc, c, k, value1, value2, c1, rx1, c2, rx2, wait)

		elif k == validKeys[4]: # reduce actuator position
			value1 = q2
			value2 = q2
			c.send(("STIMULI PAIR: MID, MID\n").encode())
			await orderingPairsSendStimuli(sc, c, k, value1, value2, c1, rx1, c2, rx2, wait)

		elif k == validKeys[5]: # reset 
			value1 = q2
			value2 = avgMax
			c.send(("STIMULI PAIR: MID, MAX\n").encode())
			await orderingPairsSendStimuli(sc, c, k, value1, value2, c1, rx1, c2, rx2, wait)

		elif k == validKeys[6]: # indicate limit
			value1 = avgMax
			value2 = avgMin
			c.send(("STIMULI PAIR: MAX, MIN\n").encode())
			await orderingPairsSendStimuli(sc, c, k, value1, value2, c1, rx1, c2, rx2, wait)

		elif k == validKeys[7]: # reduce actuator position
			value1 = avgMax
			value2 = q2
			c.send(("STIMULI PAIR: MAX, MID\n").encode())
			await orderingPairsSendStimuli(sc, c, k, value1, value2, c1, rx1, c2, rx2, wait)

		elif k == validKeys[8]: # indicate limit
			value1 = avgMax
			value2 = avgMax
			c.send(("STIMULI PAIR: MAX, MAX\n").encode())
			await orderingPairsSendStimuli(sc, c, k, value1, value2, c1, rx1, c2, rx2, wait)

		elif k == 'down':
			break



async def quickScan():
    devices = await BleakScanner.discover()
    #print(len(devices))
    for dev in devices:
        # if (dev.name == bleName):
        print(dev)

# TIP: you can get this function and more from the ``more-itertools`` package.
def sliced(data: bytes, n: int) -> Iterator[bytes]:
    """
    Slices *data* into chunks of size *n*. The last slice may be smaller than
    *n*.
    """
    return takewhile(len, (data[i : i + n] for i in count(0, n)))

# printing the data received from BLE uart. for packets that
# get separated, they're concatenated accordingly with newline
# character as demarker of end of packet
def handle_rx1(_: BleakGATTCharacteristic, data: bytearray):
    global databuf
    global f, h
    global linebuf
    global calibrate
    global trialCount
    global force1Global

    strData = data.decode("ascii")
    #commaCount = strData.count(',')
    remove = ["K", "c", "z", "d", "v", "w", "ERROR", "OK"]
    for r in remove:
    	strData = re.sub(r,"",strData)
    #packet = strData.split(",")
    # and not(strData[0] in ["x", "y", "O", "E"])

    # find a substring, starts with x or y and ends with \n    

    # remove = ["OK", "ERROR"]
    # for txt in remove:
    # 	strData.replace(txt, "")

    # find the x's and y's

    if (len(strData) ):
	    if ((strData[-1] == "\n")):
	        if (len(linebuf)):
	            print(linebuf)
	            linebuf = ""
	        if (calibrate):
	        	linebuf += (databuf+strData[:-2])
	        else:
	        	linebuf += ("1,"+databuf+strData[:-2])

	        outputStr = databuf+strData[:-2]
	        arr = outputStr.split(",")
	        if (len(arr) >= 6):
	        	force1Global = arr[2]
	        skB.writeOutDataBLE(outputStr, f, h, trialCount, 0)
	        databuf = ""

	    else:
	        databuf += strData

def handle_rx2(_: BleakGATTCharacteristic, data: bytearray):
    global databuf2
    global g, m
    global linebuf
    global trialCount
    global force2Global

    strData = data.decode("ascii")
    #commaCount = strData.count(',')

    remove = ["K", "c", "z", "d", "v", "w", "ERROR", "OK"]
    for r in remove:
    	strData = re.sub(r,"",strData)

    # remove = ["OK", "ERROR"]
    # for txt in remove:
    # 	strData.replace(txt, "")

    if (len(strData)):
	    if ((strData[-1] == "\n")):

	        if (len(linebuf) != 0):
	            linebuf = linebuf + ", "
	        linebuf = linebuf + ("2,"+databuf2+strData[:-2])
	        if (linebuf[0] == ","):
	            linebuf = linebuf[2:]
	        print(linebuf)
	        linebuf = ""

	        outputStr = databuf2+strData[:-2]
	        arr = outputStr.split(",")
	        if (len(arr) >= 6):
	        	force2Global = arr[2]
	        skB.writeOutDataBLE(outputStr, g, m, trialCount, 0)
	        databuf2 = ""

	    else:
	        databuf2 += strData



async def main():

	# write the staircasse data via socket
	nASR = 2
	s = socket.socket()
	port = 12345
	s.bind(('', port))
	s.listen(2)
	print("Waiting to connect to client to print JND data...")
	c, addr = s.accept()

	tr = skB.initializeGUI(sc) # initialize GUI
	device1 = await BleakScanner.find_device_by_address(skB.addr_Adafruit1) 	# look for BLE devices 
	if ( (device1 is None) ) :
	    print("could not find device with address {}".format(skB.addr_Adafruit1))
	
	else:
		print(device1)
		async with BleakClient(device1.address) as client1:
			await client1.start_notify(skB.UART_TX_CHAR_UUID, handle_rx1)
			nus1 = client1.services.get_service(skB.UART_SERVICE_UUID)
			rx_char1 = nus1.get_characteristic(skB.UART_RX_CHAR_UUID)

			global client2
			global rx_char2

			client2 = 0
			rx_char2 = 0

			print("Connected!")
			global calibrate
			await skB.waitGUI(sc) 	# Calibration Filter: wait for filter to stabilize


			skB.device2GUI(sc)
			device2 = await BleakScanner.find_device_by_address(skB.addr_Adafruit2)
			if (device2 is None):
				print("could not find device with address {}".format(skB.addr_Adafruit2))
			else:
				print(device2)
				async with BleakClient(device2.address) as client2:
					await client2.start_notify(skB.UART_TX_CHAR_UUID, handle_rx2)
					nus2 = client2.services.get_service(skB.UART_SERVICE_UUID)
					rx_char2 = nus2.get_characteristic(skB.UART_RX_CHAR_UUID)
					await skB.waitGUI(sc) # Calibration Filter: wait for filter to stabilize

					# calibration min max force
					skB.calibrationMinMaxGUI(sc, tr)
					skG.initializeCalibrationWindow(sc, skB.CALIBRATION_TEXT3)
					while (calibrate):
						
						k = keyboard.read_key()

						if k == 'page up': # increase actuator position
							await client1.write_gatt_char(rx_char1, ("c\n").encode(encoding="ascii"), response=False)
							if (nASR == 2):
								await client2.write_gatt_char(rx_char2, ("c\n").encode(encoding="ascii"), response=False)

						elif k == 'right': # indicate limit
							await client1.write_gatt_char(rx_char1, ("z\n").encode(encoding="ascii"), response=False)
							if (nASR == 2):
								await client2.write_gatt_char(rx_char2, ("z\n").encode(encoding="ascii"), response=False)

						elif k == 'page down': # reduce actuator position
							await client1.write_gatt_char(rx_char1, ("w\n").encode(encoding="ascii"), response=False)
							if (nASR == 2):
								await client2.write_gatt_char(rx_char2, ("w\n").encode(encoding="ascii"), response=False)

						elif k == 'up': # reset 
							await client1.write_gatt_char(rx_char1, ("v\n").encode(encoding="ascii"), response=False)
							if (nASR == 2):
								await client2.write_gatt_char(rx_char2, ("v\n").encode(encoding="ascii"), response=False)		

						elif k == 'down': # complete

							if (calibrate == 1):
								calibrate = calibrate + 1
								skG.initializeCalibrationWindow(sc, skB.CALIBRATION_TEXT4)
							else:
								await client1.write_gatt_char(rx_char1, ("d\n").encode(encoding="ascii"), response=False)
								if (nASR == 2):
									await client2.write_gatt_char(rx_char2, ("d\n").encode(encoding="ascii"), response=False)		
								calibrate = 0

						await asyncio.sleep(0.1)

					await skB.waitSK(3)

			# avgMin, avgMax, q1, q2, q3 = skB.loadASRValues(c);
			# quartiles = {"q2": q2, "q1":q1, }#, # , 
			# XoArr = {"q1": [skB.generateInitialValue(avgMin, q1), skB.generateInitialValue(avgMin, q1)], "q2": [skB.generateInitialValue(avgMin, q2), skB.generateInitialValue(avgMin, q2)]}
			# keys = list(quartiles.keys())
			# random.shuffle(keys)
			
			# skB.device2GUI(sc)
			# device2 = await BleakScanner.find_device_by_address(skB.addr_Adafruit2)
			# if (device2 is None):
			# 	print("could not find device with address {}".format(skB.addr_Adafruit2))
			# else:
			# 	print(device2)
			# 	async with BleakClient(device2.address) as client2:
			# 		await client2.start_notify(skB.UART_TX_CHAR_UUID, handle_rx2)
			# 		nus2 = client2.services.get_service(skB.UART_SERVICE_UUID)
			# 		rx_char2 = nus2.get_characteristic(skB.UART_RX_CHAR_UUID)



					# nDown = 2
					# actuatorOrder = [1,2] # 1
					# random.shuffle(actuatorOrder)

					# refArr = [2, 4, 7]					
					# random.shuffle(refArr)

					# #c.send(("Quartile Order: " + str(keys) + " N_Actuator Order: " + str(actuatorOrder) + "  Ok?\n").encode())
					# c.send(("Reference Order: " + str(refArr) + " N_Actuator Order: " + str(actuatorOrder) + "  Ok?\n").encode())					
					# while(1):
					# 	k = keyboard.read_key()
					# 	if k == 'y':
					# 		c.send(("Confirmed.\n").encode())
					# 		break
					# 	elif k == 'n':
					# 		random.shuffle(keys)
					# 		random.shuffle(refArr)
					# 		random.shuffle(actuatorOrder)
					# 		#c.send(("Quartile Order: " + str(keys) + " N_Actuator Order: " + str(actuatorOrder) + "  Ok?\n").encode())
					# 		c.send(("Reference Order: " + str(refArr) + " N_Actuator Order: " + str(actuatorOrder) + "  Ok?\n").encode())	
					# 	await asyncio.sleep(0.1)


					# method of constant stimuli
					inc = 0.3
					n = 2
					r = 4.0
					skB.instructionsGUI2(sc, tr, 1)
					skB.prepareExperimentGUI(sc, 1)
					await methodOfConstantStimuli(r, inc, 2*inc, 3*inc, 1, c, n, 0, 10, waitTime, 0.0, client1, rx_char1, client2, rx_char2)
					# for n in actuatorOrder:
					# 	for r in refArr:

					# 		if (r == 7):
					# 			inc = 0.5
					# 		elif (r in [2,4]):
					# 			inc = 0.3
					# 		skB.instructionsGUI2(sc, tr, 1)
					# 		skB.prepareExperimentGUI(sc, 1)
					# 		await methodOfConstantStimuli(r, inc, 2*inc, 3*inc, 1, c, n, avgMin, avgMax, waitTime, 0.0, client1, rx_char1, client2, rx_char2)

					# # staircasing, 2 up 1 down
					# nParts = 0
					# for n in actuatorOrder:
					# 	for k in keys:
					# 		nParts = nParts + 1

					# 		if k == "q2":
					# 			for l in list(range(0,2)):
					# 				skB.instructionsGUI2(sc, tr, (nParts-1)*2 + l)
					# 				skB.prepareExperimentGUI(sc, l)
					# 				#print ("this is staircase" + str(k))
					# 				c.send(("TRIAL#" + str(l) + "\n").encode())
					# 				await staircase2AFC((XoArr[k])[l], l, c, n, nDown, avgMin, avgMax, k, quartiles[k], waitTime, 0.0, client1, rx_char1, client2, rx_char2)
					# 				#await staircaseNewBLE(l, c, n, rUp, avgMin, avgMax, k, quartiles[k], waitTime, 0.0, client1, rx_char1, client2, rx_char2)

					# skB.orderedPairsInstructionsGUI(sc, tr)
					# skB.orderedPairsGUI(sc)
					# await orderingPairs(sc, c, avgMin, avgMax, q2, waitTime, client1, rx_char1, client2, rx_char2)

asyncio.run(main())

