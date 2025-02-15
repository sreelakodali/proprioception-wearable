# JND Test - BLE Version
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
import skPilotKeyboardFunctions as skP


# ------- CONSTANTS, DIRECTORY, & setting up files
PATH = '/Users/Sreela/Documents/School/Stanford/Year3_2/PIEZO2/JND_Study/bleData/' # change this to your path!
fileName = str(datetime.datetime.now())[0:16] # default name is date and time
fileName = ((fileName.replace('/', '_')).replace(' ', '_')).replace(':','-')
p = PATH +fileName+'/'
if not (os.path.exists(p)):
    os.makedirs(p)
    print("New directory created: %s" % fileName)
f = open(p + 'raw_device1_' + fileName + '.csv', 'w+', encoding='UTF8', newline='')
g = open(p + 'raw_device2_' + fileName + '.csv', 'w+', encoding='UTF8', newline='')
h = open(p + 'processed_device1_' + fileName + '.csv', 'w+', encoding='UTF8', newline='')
m = open(p + 'processed_device2_' + fileName + '.csv', 'w+', encoding='UTF8', newline='')
n = open(p + 'trial_device2_' + fileName + '.csv', 'w+', encoding='UTF8', newline='')
writer1 = csv.writer(h)
writer2 = csv.writer(m)
writer = csv.writer(n) # csv writer for trials

# data packet structure, length 6
# time, setpoint, set - err, filtered force value, commandedActuatorPos, measuredActuatorPos
dataFunc = {'time':sk.millisToSeconds, 'setpoint':sk.doNothing,'set-err':sk.doNothing, \
			'filteredRawForce':sk.doNothing, 'commandedActuatorPos':sk.doNothing, \
			'measuredActuatorPos':sk.doNothing} #sk.feedbackToPosition, sk.commandToPosition

columnNames = list(dataFunc.keys())
columnNames.append("TrialCounter")
columnNames = str(columnNames) + "\n"
f.write(columnNames)
g.write(columnNames)
h.write(columnNames)
m.write(columnNames)
writer.writerow(["trialCount", "Test", "Reference", "A", "B", "answerKey", "userAnswer", "stepSize", "rightStreak"])

# ------- BLE values
addr_Adafruit1 = "026B8104-5A8F-E8AF-518E-B778DB1C9CE2"
addr_Adafruit2 = "380FFB6A-AB04-7634-8A6C-C8E255F7A26C"
UART_SERVICE_UUID = "6e400001-b5a3-f393-e0a9-e50e24dcca9e"
UART_RX_CHAR_UUID = "6e400002-b5a3-f393-e0a9-e50e24dcca9e" # 2, RX write
UART_TX_CHAR_UUID = "6e400003-b5a3-f393-e0a9-e50e24dcca9e" # 3, TX notify
name = "Adafruit Bluefruit LE"
databuf = ""
databuf2 = ""
linebuf = ""


# ------- SYSTEM & STAIRCASE values
# # start=120, ref=80, startStep=-5, wait=5, retract=47, nUp=1, nDown=3, N_Trials=30
N_ACTUATORS = 1
startValue = 120
retractPos = 65
ref = 95
stepDown=3
nUp = 1
nDown = 2
N_TOTAL_TRIALS = 10#50
waitTime = 6
stepSizeRatio = {1:0.2845, 2:0.5488, 3:0.7393 , 4:0.8415}
stepUp = stepDown/stepSizeRatio[nDown]

# ------- Display & GUI variables
t = 1
sc = turtle.Screen()
EXPERIMENT_TEXT_0 = ["Welcome!", "Let's begin the experiment", "", "", "", "", "", "", "", "", "", "", "Please click the red key to continue."]
EXPERIMENT_TEXT_1 = ["Experiment", "Task: Identify whether Stimulus A feels more,", "intense, the same, or less intense than Stimulus B.", "", "",  "", "", "", "", "", "Use >, =, and < keys to indicate your answer,", "and then click the red key to go to the next trial.", "Please click the red key to start."]
EXPERIMENT_TEXT = [EXPERIMENT_TEXT_0, EXPERIMENT_TEXT_1]
EXPERIMENT_TEXT_3 = ["JND Study", ""]
# sc.tracer(0)
# sc.title("JND Study")
# tr = turtle.Turtle()
# turtle.hideturtle()
# sc.addshape('/Users/Sreela/Documents/School/Stanford/Year3_2/PIEZO2/GUIFigures/keypadJND.gif')

# ----- SUPPORTING FUNCTIONS
# default: staircase(120, 80, -5, 5, 47, 1, 3, 15)
def staircaseBLE(start, reference, stepDown, stepUp, wait, retract, nUp, nDown, N_Trials, nAct):
	# start = 120 # actuator pwm unit
	# reference = 80# 6 N
	# inc = -5 # start increment
	# wait = 5
	# retract = 47

	global writer
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
		r = random.randrange(0,2)
		print("r: " + str(r))
		if (r == 1):
			packetA = reference #A will be reference
			packetB = test #B will be test target
		else:
			packetA = test #A will be test target
			packetB = reference #B will be reference
		
		w = 0

		# apply stimuli
		print("Receiving Stimulus A: " + str(packetA))
		skG.writeText(sc, -350, 230, "Stimulus A in progress", skG.COLOR)

		# Send poke A
		await client1.write_gatt_char(rx_char1, skP.formatBLEPacket(packetA,1)) 
		if (nAct == 2):
	        await client2.write_gatt_char(rx_char2, skP.formatBLEPacket(packetA,2))
		
        # hold the poke
		endTime = datetime.datetime.now() + datetime.timedelta(seconds=wait)
		while (datetime.datetime.now() < endTime):
			w = w + 1
		#time.sleep(wait) 
	
		# then retract
		await client1.write_gatt_char(rx_char1, skP.formatBLEPacket(retract,1)) 
		if (nAct == 2):
        	await client2.write_gatt_char(rx_char2, skP.formatBLEPacket(retract,2))
		
		# wait
		endTime = datetime.datetime.now() + datetime.timedelta(seconds=wait/2)
		while (datetime.datetime.now() < endTime):
			w = w + 1
		#time.sleep(wait) # wait

		# apply stimuli
		print("Receiving Stimulus B: " + str(packetB))
		skG.writeText(sc, -350, 180, "Stimulus B in progress", skG.COLOR)
		
		# Send poke B
        await client1.write_gatt_char(rx_char1, skP.formatBLEPacket(packetB,1))
        if (nAct == 2):
        	await client2.write_gatt_char(rx_char2, skP.formatBLEPacket(packetB,2))

         # hold the poke
		endTime = datetime.datetime.now() + datetime.timedelta(seconds=wait)
		while (datetime.datetime.now() < endTime):
			w = w + 1
		#time.sleep(wait)

		# then retract
		await client1.write_gatt_char(rx_char1, skP.formatBLEPacket(retract,1))
		if (nAct == 2):
        	await client2.write_gatt_char(rx_char2, skP.formatBLEPacket(retract,2))

        # wait
		endTime = datetime.datetime.now() + datetime.timedelta(seconds=wait/2)
		while (datetime.datetime.now() < endTime):
			w = w + 1
		#time.sleep(wait/2) # wait

		# find the real answer
		# 1 means A > B, 2 means A == B, 3 means A < B
		answerKey = (packetA > packetB)*1 + (packetA == packetB)*2 + (packetA < packetB)*3
		print("The real answer is: " + str(answerKey))

		skG.writeText(sc, -350,80, "Select your answer:", skG.COLOR)
		skG.writeText(sc, -350,30, "A > B             A == B             A < B ", skG.COLOR_RED)
		skG.writeText(sc, -350,-120, "Press the red key to confirm your answer", skG.COLOR)
		skG.writeText(sc, -350,-170, "and proceed to the next trial.", skG.COLOR_GREEN)

		while(1):

		# wait for user's input
			k = keyboard.read_key()

			if k == 'page up':
				userAnswer = 1
				skG.eraseLine(sc,-350,40)
				skG.writeText(sc, -350,30, "(A > B)           A == B             A < B ", skG.COLOR_RED)
			elif k == 'right':
				userAnswer = 2
				skG.eraseLine(sc,-350,40)
				skG.writeText(sc, -350,30, "A > B            (A == B)            A < B ", skG.COLOR_RED)
			elif k == 'page down':
				userAnswer = 3
				skG.eraseLine(sc,-350,40)
				skG.writeText(sc, -350,30, "A > B             A == B            (A < B)", skG.COLOR_RED)

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
			test = test + round(stepUp) # step up test value if wrong
			writer3.writerow([trialCount, test, reference, packetA, packetB, answerKey, userAnswer, stepUp, rightStreak])
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
			userAnswer = 0
			
			# step down test if they get 3 right answers in a row
			if ((rightStreak == nDown) or (wrongCount == 0)):
				test = test - stepDown
				writer.writerow([trialCount, test, reference, packetA, packetB, answerKey, userAnswer, stepDown, rightStreak])
				# inc = (abs(inc) - 1)*-1
				rightStreak = 0
			else:
				writer.writerow([trialCount, test, reference, packetA, packetB, answerKey, userAnswer, 0, rightStreak])

async def quickScan():
    devices = await BleakScanner.discover()
    #print(len(devices))
    for dev in devices:
        # if (dev.name == name):
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

    strData = data.decode("ascii")
    if (strData[-1] == "\n"):
        if (len(linebuf) != 0):
            print(linebuf)
            linebuf = ""
        linebuf += ("1,"+databuf+strData[:-2])

        #print("1,"+databuf+strData[:-2], end=",", flush=True)
        f.write(databuf+strData) # FIX: raw doesn't include trialCount
        skP.writeOutDataBLE(databuf+strData, dataFunc, writer1, 0, 0) # FIX: need to add trialCount
        
        databuf = ""
    else:
        databuf += strData

def handle_rx2(_: BleakGATTCharacteristic, data: bytearray):
    global databuf2
    global g
    global linebuf
    global writer2

    strData = data.decode("ascii")
    if (strData[-1] == "\n"):

        if (len(linebuf) != 0):
            linebuf = linebuf + ", "
        linebuf = linebuf + ("2,"+databuf2+strData[:-2])
        if (linebuf[0] == ","):
            linebuf = linebuf[2:]
        print(linebuf)
        linebuf = "" # FIX: may not need linebuf for printing data...tbd

        g.write(databuf2+strData)
        skP.writeOutDataBLE(databuf+strData, dataFunc, writer2, 0, 0) # FIX: need to add trialCount
        databuf2 = ""
    else:
        databuf2 += strData



async def main():

	# initialize GUI
	sc.tracer(0)
	sc.title("JND Study")
	tr = turtle.Turtle()
	turtle.hideturtle()
	sc.addshape('/Users/Sreela/Documents/School/Stanford/Year3_2/PIEZO2/GUIFigures/keypadJND.gif')

	# GUI for instructions
	skG.initializeWindow(sc,EXPERIMENT_TEXT_0)
	keyboard.wait('down')
	skG.initializeWindow(sc,EXPERIMENT_TEXT_1)
	tr.shape('/Users/Sreela/Documents/School/Stanford/Year3_2/PIEZO2/GUIFigures/keypadJND.gif')
	turtle.update()
	keyboard.wait('down')

	# look for BLE devices 
    device1 = await BleakScanner.find_device_by_address(addr_Adafruit1)

    if (N_ACTUATORS == 2):
    	device2 = await BleakScanner.find_device_by_address(addr_Adafruit2)
    #device = await BleakScanner.find_device_by_name(name)

    if ( (device1 is None) or ((N_ACTUATORS == 2) and (device2 is None)) ) :
        print("could not find device with name {}".format(name))

    # elif ( (N_ACTUATORS == 2) and (device2 is None) ):
    # 	print("could not find device with name {}".format(name))
    
    else:
        print(device1)
        if (N_ACTUATORS == 2):
        	print(device2)

        # if devices found, proceed with JND gui
        skG.initializeWindow(sc,EXPERIMENT_TEXT_3)
		skG.initializeTrialLabel(sc,N_TOTAL_TRIALS)
		skG.updateTrialLabel(sc, 0)
		skG.delay(sc, t)

        async with BleakClient(device1.address) as client1:
        	await client1.start_notify(UART_TX_CHAR_UUID, handle_rx1)
            nus1 = client1.services.get_service(UART_SERVICE_UUID)
            rx_char1 = nus1.get_characteristic(UART_RX_CHAR_UUID)

            if (N_ACTUATORS == 2):
	            async with BleakClient(device2.address) as client2:
	            	await client2.start_notify(UART_TX_CHAR_UUID, handle_rx2)
	                nus2 = client2.services.get_service(UART_SERVICE_UUID)
	                rx_char2 = nus2.get_characteristic(UART_RX_CHAR_UUID)
	                #loop = asyncio.get_running_loop()

            print("Connected!")
            staircaseBLE(startValue, ref, stepDown, stepUp, waitTime, retractPos, nUp, nDown, N_TOTAL_TRIALS, N_ACTUATORS)

			f.close()
			g.close()
			h.close()
			m.close()
			n.close()

asyncio.run(main())

