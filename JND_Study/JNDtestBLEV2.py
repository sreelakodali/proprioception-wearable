# JND Test - BLE Version
# Written by: Sreela Kodali (kodali@stanford.edu) 

import serial, datetime, csv, sys, getopt, os, shutil, turtle
import random, time, keyboard, asyncio, socket, re, statistics
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

f, h, writer1 = skB.createDataFiles(p, fileName, 1)
if (N_ACTUATORS == 2):
	g, m, writer2 = skB.createDataFiles(p, fileName, 2)

# ------- BLE values
databuf = ""
databuf2 = ""
linebuf = ""

# ------- SYSTEM & STAIRCASE values
# start=120, ref=80, startStep=-5, wait=5, retract=47, nUp=1, nDown=3, N_Trials=30
# start=120, ref=95, startStep=-5, wait=6, retract=47, nUp=1, nDown=3, N_Trials=10
startValue = 12.0
retractPos = 0.0
ref = 6.0
stepDown=0.4
# nUp = 1
# nDown = 2
#N_TOTAL_TRIALS = 50
waitTime = 6 # seconds
# stepSizeRatio = {1:0.2845, 2:0.5488, 3:0.7393 , 4:0.8415}
# stepUp = stepDown/stepSizeRatio[nDown]

# ------- Display & GUI variables
t = 1
sc = turtle.Screen()
calibrate = True

# async def waitA():
# 	await asyncio.sleep(0.01)

# def waitReadBLEData():
# 	while(1):
# 		waitA()


# provide staircasing parameters: going up or down (bounds); reference, nUP, nDown, retract, wait, c, clients and rxchars
async def staircaseNewBLE(c, nAct, increasing, avgMin, avgMax, key, reference, wait, retract, client1, rx_char1, client2, rx_char2):
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


	skB.initializeTrialFiles(p, fileName, key)

	# we are assuming nUp, nDown: 2:1

	testArr = [] # [0.0] * 50
	Ldb = 4 #db
	Xo = skB.generateInitialValue(increasing, avgMin, avgMax, reference)

	# FIX since some people's force range won't allow for 3.0 difference
	while (abs(Xo - reference) < (avgMax-avgMin)/6):
		Xo = skB.generateInitialValue(increasing, avgMin, avgMax, reference)

	Xo = round(Xo, 2)
	c.send(("STAIRCASE " + key + "\n").encode())
	c.send(("INITIAL VALUE= " + str(Xo) + "\n").encode())
	c.send(("REFERENCE= " + str(reference) + "\n").encode())

	# response = input()
	testArr.append(Xo)

	keepGoing = True
	# statistics.mean(testArr[-10:]) < 1.0

	while (keepGoing): # FIX, last 10 are less than 0.5
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
		await skB.sendSetpoint(packetA, client2, rx_char2, 2) 	
		await skB.waitSK(wait) 	# hold the poke	

		await skB.sendSetpoint(retract, client1, rx_char1, 1)
		await skB.sendSetpoint(retract, client2, rx_char2, 2)
		await skB.waitSK(wait/2) 	# hold the poke

		# send stimuli B
		c.send(("Receiving Stimulus B: " + str(packetB) + "\n").encode())
		skG.writeText(sc, -350, 180, "Stimulus B in progress", skG.COLOR)

		await skB.sendSetpoint(packetB, client1, rx_char1, 1) 	
		await skB.sendSetpoint(packetB, client2, rx_char2, 2) 	
		await skB.waitSK(wait) 	# hold the poke	

		await skB.sendSetpoint(retract, client1, rx_char1, 1)
		await skB.sendSetpoint(retract, client2, rx_char2, 2)
		await skB.waitSK(wait/2) 	# hold the poke	

		# find the real answer
		# 1 means A > B, 2 means A == B, 3 means A < B
		answerKey = (packetA > packetB)*1 + (packetA == packetB)*2 + (packetA < packetB)*3
		c.send(("The real answer is: " + str(answerKey) + "\n").encode())

		skB.displayAnswerOptionsGUI(sc)

		while(1):
			await asyncio.sleep(0.01)
		# wait for user's input
			k = keyboard.read_key()

			if k == 'page up':
				userAnswer = 1
				skB.updateUserAnswerGUI(sc, userAnswer)

			elif k == 'right':
				userAnswer = 2
				skB.updateUserAnswerGUI(sc, userAnswer)

			elif k == 'page down':
				userAnswer = 3
				skB.updateUserAnswerGUI(sc, userAnswer)

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

		# if test < ref

		## if r == 1, A=ref, B=test. --> to have ref > test, answer 1
		# if r== 0, A=test, B=ref. --> to have test < ref, answer 3

		## for decreasing staircase
		# if test > ref, decrease. blue x
		# if r == 1, A=ref, B=test --> if ref < test, answer 3. user says reduce. blue x
		# if r == 0, A=test, B=ref --> if test > ref, answer 1. user says decrease. blue x
		# if test < ref, increase. green o
		## if r==1, A=ref, B=test. ref > test, answer1. user says increase
		## if r==0, A=test, B=ref. test < ref, answer 3. user says decrease

		
		# test more than reference
		# test > ref, ref < test
		# r=0, answer1 r=1answer3

		# if (increasing):
		# 	condition1 = ((r==0) and (userAnswer==1)) or ((r==1) and (userAnswer==3))
		# 	condition3 = ((r==0) and (userAnswer==3)) or ((r==1) and (userAnswer==1))
		# else:
		# 	condition1 = (((r==0) and (userAnswer==1)) or ((r==1) and (userAnswer==3))) # test > ref, decrease
		# 	condition3 = (((r==0) and (userAnswer==3)) or ((r==1) and (userAnswer==1))) # test < ref, increase. reversal

		if ((r==0) and (userAnswer==1)) or ((r==1) and (userAnswer==3)):
			
			c.send(("User said TEST is greater than REFERENCE\n").encode())
			
			if (increasing):
				reversals = reversals + 1 # reversals
				rightStreak = 0
				graphIcon = 3
				newTest = testArr[trialCount-2] # next value is the previous one
				Ldb = Ldb / 2 # Ldb is reduced
				# if (Ldb <= 0.5):
				# 	Ldb = 0.5
				c.send(("reversals:" + str(reversals)+ "\n").encode())
			else:
				graphIcon = 1
				if (userAnswer == answerKey):
					rightStreak = rightStreak + 1

				if (rightStreak == 2):
					# change the stimulus pattern
					newTest = test *  (2 - 10 ** (Ldb/20))
					rightStreak = 0
				else:
					newTest = test

		#same as reference
		elif (userAnswer == 2):
			graphIcon = 2
			c.send(("User said TEST equals REFERENCE\n").encode())
			rightStreak = 0
			# compute next step using previous test
			if (increasing):
				newTest = testArr[trialCount-2] * (10 **(Ldb/20))
			else:
				newTest = testArr[trialCount-2] * (2 - 10 ** (Ldb/20))

		# test less than reference
		# test < ref,  ref > test. 
		# r=0, answer3 r=1, answer1
		elif ((r==0) and (userAnswer==3)) or ((r==1) and (userAnswer==1)):
			
			c.send(("User said TEST is less than REFERENCE\n").encode())

			if (increasing):
				graphIcon = 1
				if (userAnswer == answerKey):
					rightStreak = rightStreak + 1

				if (rightStreak == 2):
					# change the stimulus pattern
					newTest = test * 10 ** (Ldb/20)
					rightStreak = 0
				else:
					newTest = test
			else:
				reversals = reversals + 1 # reversals
				rightStreak = 0
				graphIcon = 3
				newTest = testArr[trialCount-2] # next value is the previous one
				Ldb = Ldb / 2 # Ldb is reduced
				# if (Ldb <= 0.5):
				# 	Ldb = 0.5
				c.send(("reversals:" + str(reversals)+ "\n").encode())
		
		if (trialCount > 14):
			npTestArr = np.array(testArr[-10:])
			if (abs(statistics.mean(testArr[-10:]) - reference) <  10**(0.1)):
				keepGoing = False
			elif ( sum(abs(np.gradient(npTestArr, 1))) < 0.3 ):
				keepGoing = False
		newTest = round(newTest, 2)
		if (newTest > avgMax):
			newTest = avgMax
		elif (newTest < avgMin):
			newTest = avgMin
		testArr.append(newTest)
		n = open(p + 'trial' + key + "_" + fileName + '.csv', 'a', encoding='UTF8', newline='')
		n.write(str(trialCount-1) + "," + str(test) + "," + str(reference) + "," + str(packetA) + "," + str(packetB)+ "," + str(answerKey)+ "," + str(userAnswer)+ "," + str(reversals)+ "," + str(graphIcon) + "\n")
		n.close()
		#writer.writerow([trialCount-1, test, reference, packetA, packetB, answerKey, userAnswer, reversals, rightStreak])
		#trialCount = trialCount + 1

	c.send(("DONE\n").encode())

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
    #global writer1
    global trialCount

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
	        #skB.writeOutDataBLE(outputStr, writer1, f, trialCount, 0) # FIX: need to add trialCount
	        skB.writeOutDataBLE(outputStr, h, f, trialCount, 0) # FIX: need to add trialCount
	        databuf = ""

	    else:
	        databuf += strData

def handle_rx2(_: BleakGATTCharacteristic, data: bytearray):
    global databuf2
    global g, m
    global linebuf
    #global writer2
    global trialCount

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

	        #g.write(databuf2+strData)
	        outputStr = databuf+strData[:-2]
	        skB.writeOutDataBLE(outputStr, m, g, trialCount, 0) # FIX: need to add trialCount
	        #skB.writeOutDataBLE(outputStr, writer2, g, trialCount, 0) # FIX: need to add trialCount
	        databuf2 = ""

	    else:
	        databuf2 += strData



async def main():

	# write the staircase data via socket
	s = socket.socket()
	port = 12346
	s.bind(('', port))
	s.listen(2)
	print("Waiting to connect to client to print JND data...")
	c, addr = s.accept()

	tr = skB.initializeGUI(sc) # initialize GUI
	#skB.instructionsGUI(sc, tr) # GUI for instructions

	# look for BLE devices 
	device1 = await BleakScanner.find_device_by_address(skB.addr_Adafruit1)

	# if (N_ACTUATORS == 2):
	# 	device2 = await BleakScanner.find_device_by_address(skB.addr_Adafruit2)
	# #device = await BleakScanner.find_device_by_name(bleName)

	if ( (device1 is None) ) :
	    print("could not find device with address {}".format(skB.addr_Adafruit1))

	# elif ( (N_ACTUATORS == 2) and (device2 is None) ):
	# 	print("could not find device with address {}".format(skB.addr_Adafruit2))
	
	else:

	# if (True):
	# 	clientArr = []
	# 	rx_charArr = []	
		print(device1)
		# if (N_ACTUATORS == 2):
		# 	print(device2)

		# if (True):
		async with BleakClient(device1.address) as client1:
			await client1.start_notify(skB.UART_TX_CHAR_UUID, handle_rx1)
			nus1 = client1.services.get_service(skB.UART_SERVICE_UUID)
			rx_char1 = nus1.get_characteristic(skB.UART_RX_CHAR_UUID)

			global client2
			global rx_char2

			client2 = 0
			rx_char2 = 0
			# clientArr = [client1]
			# rx_charArr = [rx_char1]

					#loop = asyncio.get_running_loop()

			print("Connected!")
			global calibrate
			# Calibration Filter: wait for filter to stabilize
			await skB.waitGUI(sc)

			# calibration min max force
			skB.calibrationMinMaxGUI(sc, tr)
			skG.initializeCalibrationWindow(sc, skB.CALIBRATION_TEXT3)
			
			while (calibrate):
				
				k = keyboard.read_key()

				if k == 'page up': # increase actuator position
					await client1.write_gatt_char(rx_char1, ("c\n").encode(encoding="ascii"), response=False)

				elif k == 'right': # indicate limit
					await client1.write_gatt_char(rx_char1, ("z\n").encode(encoding="ascii"), response=False)

				elif k == 'page down': # reduce actuator position
					await client1.write_gatt_char(rx_char1, ("w\n").encode(encoding="ascii"), response=False)

				elif k == 'up': # reset 
					await client1.write_gatt_char(rx_char1, ("v\n").encode(encoding="ascii"), response=False)		

				elif k == 'down': # complete
					await client1.write_gatt_char(rx_char1, ("d\n").encode(encoding="ascii"), response=False)		
					calibrate = False

				await asyncio.sleep(0.1)

			await skB.waitSK(3)

			avgMin, avgMax, q1, q2, q3 = skB.loadASRValues(c);
			quartiles = {"q1": q1, "q2": q2, "q3": q3}
			keys = list(quartiles.keys())
			random.shuffle(keys)


			if (N_ACTUATORS == 2):
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
				# 		clientArr.append(client2)
				# 		rx_charArr.append(rx_char2)
				# 		print("Connected!")

						# Calibration Filter: wait for filter to stabilize
						await skB.waitGUI(sc)

						skB.instructionsGUI(sc, tr) # GUI for instructions
						skB.prepareExperimentGUI(sc) # proceed with JND gui
						directionIncreasing = True
						await staircaseNewBLE(c, N_ACTUATORS, directionIncreasing, avgMin, avgMax, 'q2', q2, waitTime, retractPos, client1, rx_char1, client2, rx_char2)

						# for k in keys:
						# 	skB.instructionsGUI(sc, tr)
						# 	skB.prepareExperimentGUI(sc)
						# 	#print ("this is staircase" + str(k))
						# 	await staircaseNewBLE(c, N_ACTUATORS, 1, avgMin, avgMax, k, quartiles[k], waitTime, retractPos, client1, rx_char1, client2, rx_char2)

			else:
			# for k in keys:
			# 	skB.instructionsGUI(sc, tr)
			# 	skB.prepareExperimentGUI(sc)
			# 	#print ("this is staircase" + str(k))
			# 	await staircaseNewBLE(c, N_ACTUATORS, 1, avgMin, avgMax, k, quartiles[k], waitTime, retractPos, client1, rx_char1, client2, rx_char2)

			skB.instructionsGUI(sc, tr) # GUI for instructions
			skB.prepareExperimentGUI(sc) # proceed with JND gui
			directionIncreasing = True
			await staircaseNewBLE(c, N_ACTUATORS, directionIncreasing, avgMin, avgMax, 'q2', q2, waitTime, retractPos, client1, rx_char1, client2, rx_char2)
			
			skB.closeFiles([f, h])
			if (N_ACTUATORS == 2):
				skB.closeFiles([g, m])

asyncio.run(main())

