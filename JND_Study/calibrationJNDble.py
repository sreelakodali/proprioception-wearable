# Calibration BLE
# Written by: Sreela Kodali (kodali@stanford.edu) 

import serial, datetime, csv, sys, getopt, os, shutil, turtle, random, time, keyboard
import numpy as np
from scipy import signal
import constants as CONST
import skFunctions as sk
import skPilotGraphics as skG
import skCalibrationFunctions as skC


# calibration commands for teensy
# 5 = 
# 4 = for max pressure calibration, click
# 3 = start filter calibration
# 2 = start max pressure calibration
# 1 = load in userMin and Max values
# 0 = done with calibration

CALIBRATION_OPTIONS = {'FILTER': 3, 'MAX_PRESSURE': 2, 'NONE': 0}
#CALIBRATION_FUNCTIONS = {'ACTUATOR':skC.calibrateActuator, 'MAX_PRESSURE': skC.calibrateMaxPressure, 'FLEX': skC.calibrateFlexSensor, 'ZERO_FORCE': 1, 'NONE': skC.calibrateDone}
calibrationSeq = CALIBRATION_OPTIONS.keys() # default
def on_click(x, y):
	global click

	# print(x)
	# print(y)

	# Repeat button
	if ((x < -190) and (x > -355) and (y > -250) and (y < -195)):
		click = 2
	# Done button
	elif((x < 280) and (x > 117) and (y > -250) and (y < -195)):
		click = 3
	else: click = 1


# opts, args = getopt.getopt(sys.argv[1:],"zms",["mode=", "userMax="])
# for opt, arg in opts:
# 	if opt == "--userMax":
# 		mcu.write(str(1).encode())
# 		mcu.write(str(arg).encode())
# 		value = (mcu.readline()).decode()
# 		value = value.strip()
# 		if (value):
# 			print(value)

# 	elif opt == "-z":
# 		print('NONE')
# 		mcu.write(str(CALIBRATION_OPTIONS['NONE']).encode())
# 		skipGUI = 1

# 	elif opt in ["-m", "--mode"]:
# 		if arg == 'FLEX':
# 			calibrationSeq = CALIBRATION_OPTIONS.keys()
# 		if arg == 'KEY':
# 			calibrationSeq = CALIBRATION_OPTIONS2.keys()
# 			#calibrationSeq = (CALIBRATION_OPTIONS[arg])
	
# 	elif opt == "-s":
# 		saveData = True	

# 	# elif opt == "--custom":
# 	# 	calibrationSeq = arg # fix not done



#print(calibrationSeq)




#----------------------------------------------------------------
def on_click(x, y):
	global click

	# print(x)
	# print(y)

	# Repeat button
	if ((x < -190) and (x > -355) and (y > -250) and (y < -195)):
		click = 2
	# Done button
	elif((x < 280) and (x > 117) and (y > -250) and (y < -195)):
		click = 3
	else: click = 1

def waitforclick(maxPressure):
	global click, mcu
	turtle.update()
	click = 0

	if(maxPressure and saveData):
		h = open(p + 'maxForce' + '.csv', 'a', encoding='UTF8')

	while not click:

		if (maxPressure):
			value = (mcu.readline()).decode()
			value = value.strip()

			if (value):
				print(value)

				if (saveData):
					# h = open(p + 'maxForce' + '.csv', 'w+', encoding='UTF8')
					h.write(value+ "\n")
					#h.close()

		turtle.update()
		time.sleep(.2)
	oldClick = click
	click = 0
	if(maxPressure and saveData):
		h.close()
	return oldClick
#----------------------------------------------------------------


if(not(skipGUI)):
	# Default mode
	# actuator, welcome, please wear device, max+zero, flex

	if(saveData):
		p = skC.calibrateNewSubject();
	else:
		p = ''
	sc = turtle.Screen()
	sc.tracer(0)
	sc.title("Calibration")
	turtle.onscreenclick(on_click, btn=1)
	turtle.update()
	skG.initializeCalibrationWindow(sc, skC.CALIBRATION_TEXT_INTRO)

	for i in calibrationSeq:

		if not(skipClickForNewText): btn = waitforclick(0)
		else: skipClickForNewText = 0
		skG.initializeCalibrationWindow(sc, skC.CALIBRATION_TEXT[i])

		if i == 'NONE':
			waitforclick(0)
			print(i)
			mcu.write(str(CALIBRATION_OPTIONS[i]).encode())
			#CALIBRATION_FUNCTIONS[i](mcu,p, saveData)

		else:	
			skG.buttons(sc)
			while(True):

				if (i == 'MAX_PRESSURE'):
					btn = waitforclick(1)
				else: btn = waitforclick(0)

				#btn = waitforclick()
				#print(btn)
				if (btn == 3): # done
					skipClickForNewText = 1
					break
				elif (btn == 2): # calibrate
					print(i)
					mcu.write(str(CALIBRATION_OPTIONS[i]).encode())
					if i =='ACTUATOR':
						CALIBRATION_FUNCTIONS[i](mcu,p, saveData)
					elif i == 'FLEX':
						CALIBRATION_FUNCTIONS[i](mcu,p, sc, saveData)
				elif (btn == 1): # clicking anywhere else on the screen
					if i == 'MAX_PRESSURE':
						mcu.write(str(5).encode())
						while(True):
							btn2 = waitforclick(1)
						# time.sleep(2)
						# btn2 = waitforclick(1)
							if (btn2 == 1):
								#print("bloop")
								CALIBRATION_FUNCTIONS[i](mcu,p, saveData)
								break
	