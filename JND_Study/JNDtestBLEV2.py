# JND Test - BLE Version
# Written by: Sreela Kodali (kodali@stanford.edu) 

import serial, datetime, csv, sys, getopt, os, shutil, turtle, random, time, keyboard, asyncio, threading
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
N_ACTUATORS = 1
trialCount = 0 # counter

# ------- CONSTANTS, DIRECTORY, & setting up files
PATH = '/Users/Sreela/Documents/School/Stanford/Year3_2/PIEZO2/JND_Study/bleData/' # change this to your path!
fileName = str(datetime.datetime.now())[0:16] # default name is date and time
fileName = ((fileName.replace('/', '_')).replace(' ', '_')).replace(':','-')
p = PATH +fileName+'/'
if not (os.path.exists(p)):
    os.makedirs(p)
    print("New directory created: %s" % fileName)

f, h, writer1 = skB.createDataFiles(p, fileName, 1)
if (N_ACTUATORS == 2):
	g, m, writer2 = skB.createDataFiles(p, fileName, 2)
n = open(p + 'trial_' + fileName + '.csv', 'w+', encoding='UTF8', newline='')
writer = csv.writer(n) # csv writer for trials
writer.writerow(["trialCount", "Test", "Reference", "A", "B", "answerKey", "userAnswer", "stepSize", "rightStreak"])


# ------- BLE values
databuf = ""
databuf2 = ""
linebuf = ""

# ------- SYSTEM & STAIRCASE values
# start=120, ref=80, startStep=-5, wait=5, retract=47, nUp=1, nDown=3, N_Trials=30
# start=120, ref=95, startStep=-5, wait=6, retract=47, nUp=1, nDown=3, N_Trials=10
startValue = 7.0
retractPos = 0.0
ref = 3.50
stepDown=0.3
nUp = 1
nDown = 2
N_TOTAL_TRIALS = 10#50
waitTime = 6 # seconds
stepSizeRatio = {1:0.2845, 2:0.5488, 3:0.7393 , 4:0.8415}
stepUp = stepDown/stepSizeRatio[nDown]

# ------- Display & GUI variables
t = 1
sc = turtle.Screen()


# async def waitA():
# 	await asyncio.sleep(0.01)

# def waitReadBLEData():
# 	while(1):
# 		waitA()



# ----- SUPPORTING FUNCTIONS
# default: staircase(120, 80, -5, 5, 47, 1, 3, 15)
def staircaseBLE(start, reference, stepDown, stepUp, wait, retract, nUp, nDown, N_Trials, clientArr, rx_charArr):
	# start = 120 # actuator pwm unit
	# reference = 80# 6 N
	# inc = -5 # start increment
	# wait = 5
	# retract = 47
	global writer
	global trialCount

	packetA = 0
	packetB = 0
	rightStreak = 0
	answerKey = 0
	userAnswer = 0
	test = 0
	trialCount = 0 # counter
	wrongCount = 0
	# stepType

	# start Value for method of limits
	test = start

	for i in range(0,N_Trials):

		# ---- READ AND PRINT/SAVE DATA
		# value = mcu.readlines()
		# for j in value:
		# 	#skP.writeOutData(j,dataFunc, 0, 0, trialCount)
		# 	skP.writeOutData(j,dataFunc, writer2, writer, trialCount)

		print("----- TRIAL #" + str(i) + " -----")
		print("test: " + str(test))
		print("rightStreak: " + str(rightStreak))

		# randomize order presented
		packetA, packetB = skB.randomizeStimuli(reference, test)

		# apply stimuli
		await skB.sendPoke(sc, packetA, retract, wait, clientArr, rx_charArr, 1)  # Send poke A
		await skB.sendPoke(sc, packetB, retract, wait, clientArr, rx_charArr, 0) # Send poke B

		# find the real answer
		# 1 means A > B, 2 means A == B, 3 means A < B
		answerKey = (packetA > packetB)*1 + (packetA == packetB)*2 + (packetA < packetB)*3
		print("The real answer is: " + str(answerKey))

		skB.displayAnswerOptionsGUI(sc)

		while(1):

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
					if trialCount < N_Trials:
						skG.updateTrialLabel(sc, trialCount)
						skG.delay(sc, t)

					break

		# check the answer. depending on answer, determine next test value
		# if answer wrong, reset streak and step up test value
		print("User answer is: " + str(userAnswer))

		if (answerKey != userAnswer):
			print("ANSWER WRONG!")
			rightStreak = 0
			writer.writerow([trialCount, test, reference, packetA, packetB, answerKey, userAnswer, stepUp, rightStreak])
			test = round((test + stepUp), 2) # step up test value if wrong
			print("stepSize: " + str(stepUp))
			# inc = abs(inc) + 1 
			userAnswer = 0
			wrongCount = wrongCount + 1
			print("reversals:" + str(wrongCount))
			# if (wrongCount == 2):
			# 	stepSize = stepSize2

		# if answer correct, add to right streak
		elif (answerKey == userAnswer):
			print("ANSWER RIGHT!")
			rightStreak = rightStreak + 1
			
			# step down test if they get nDown right answers in a row
			if ((rightStreak == nDown) or (wrongCount == 0)): # FIX: check logic of wrongCount  
				writer.writerow([trialCount, test, reference, packetA, packetB, answerKey, userAnswer, stepDown, rightStreak])
				test = round((test - stepDown), 2)
				userAnswer = 0
				# inc = (abs(inc) - 1)*-1
				rightStreak = 0
			else:
				writer.writerow([trialCount, test, reference, packetA, packetB, answerKey, userAnswer, 0, rightStreak])

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
    global f
    global linebuf
    global writer1
    global trialCount

    strData = data.decode("ascii")
    if (strData[-1] == "\n"):
        if (len(linebuf) != 0):
            print(linebuf)
            linebuf = ""
        linebuf += ("1,"+databuf+strData[:-2])

        outputStr = databuf+strData[:-2]
        skB.writeOutDataBLE(outputStr, writer1, f, trialCount, 0) # FIX: need to add trialCount
        databuf = ""

    else:
        databuf += strData

def handle_rx2(_: BleakGATTCharacteristic, data: bytearray):
    global databuf2
    global g
    global linebuf
    global writer2
    global trialCount

    strData = data.decode("ascii")
    if (strData[-1] == "\n"):

        if (len(linebuf) != 0):
            linebuf = linebuf + ", "
        linebuf = linebuf + ("2,"+databuf2+strData[:-2])
        if (linebuf[0] == ","):
            linebuf = linebuf[2:]
        print(linebuf)
        linebuf = ""

        #g.write(databuf2+strData)
        outputStr = databuf+strData[:-2]
        skB.writeOutDataBLE(outputStr, writer2, g, trialCount, 0) # FIX: need to add trialCount
        databuf2 = ""

    else:
        databuf2 += strData



async def main():

	tr = skB.initializeGUI(sc) # initialize GUI
	skB.instructionsGUI(sc, tr) # GUI for instructions


	# look for BLE devices 
	device1 = await BleakScanner.find_device_by_address(skB.addr_Adafruit1)

	if (N_ACTUATORS == 2):
		device2 = await BleakScanner.find_device_by_address(skBaddr_Adafruit2)
	#device = await BleakScanner.find_device_by_name(bleName)

	if ( (device1 is None) ) :
	    print("could not find device with address {}".format(skB.addr_Adafruit1))

	elif ( (N_ACTUATORS == 2) and (device2 is None) ):
		print("could not find device with address {}".format(skB.addr_Adafruit2))
	
	else:

	# if (True):
	# 	clientArr = []
	# 	rx_charArr = []	
		print(device1)
		if (N_ACTUATORS == 2):
			print(device2)

		# if devices found, proceed with JND gui
		skB.prepareExperimentGUI(sc, N_TOTAL_TRIALS)

		# if (True):
		async with BleakClient(device1.address) as client1:
			await client1.start_notify(skB.UART_TX_CHAR_UUID, handle_rx1)
			nus1 = client1.services.get_service(skB.UART_SERVICE_UUID)
			rx_char1 = nus1.get_characteristic(skB.UART_RX_CHAR_UUID)

			clientArr = [client1]
			rx_charArr = [rx_char1]

			if (N_ACTUATORS == 2):
				async with BleakClient(device2.address) as client2:
					await client2.start_notify(skB.UART_TX_CHAR_UUID, handle_rx2)
					nus2 = client2.services.get_service(skB.UART_SERVICE_UUID)
					rx_char2 = nus2.get_characteristic(skB.UART_RX_CHAR_UUID)

					clientArr.append(client2)
					rx_charArr.append(rx_char2)

					#loop = asyncio.get_running_loop()

			print("Connected!")
			#t1 = threading.Thread(target=staircaseBLE, args=(startValue, ref, stepDown, stepUp, waitTime, retractPos, nUp, nDown, N_TOTAL_TRIALS, clientArr, rx_charArr,))
			# t2 = threading.Thread(target=waitReadBLEData)
			#t1.start()

			# t2.join()
			while(1):
				await asyncio.sleep(0.01)
			# staircaseBLE(startValue, ref, stepDown, stepUp, waitTime, retractPos, nUp, nDown, N_TOTAL_TRIALS, clientArr, rx_charArr)
			#t1.join()
			skB.closeFiles([f, h, n])
			if (N_ACTUATORS == 2):
				skB.closeFiles([g, m])

asyncio.run(main())

