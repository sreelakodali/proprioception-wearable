# keyboard test 
# Written by: Sreela Kodali (kodali@stanford.edu) 

import serial
import datetime
import csv
import sys
import os
import shutil
import numpy as np
import getopt
from scipy import signal
import constants as CONST
import skFunctions as sk
import turtle
import skPilotGraphics as skG
import random
import skCalibrationFunctions as skC
import time
import keyboard
import random

mcu = serial.Serial(port=CONST.PORT_NAME, baudrate=CONST.BAUD_RATE, timeout=.1)
dataFunc = {'time':sk.millisToSeconds, 'flex sensor':sk.computeAngle,'actuator position, command':sk.commandToPosition, \
			'actuator position, measured':sk.feedbackToPosition, 'force':sk.computeForce}


armAngle = 180

sc = turtle.Screen()
# Initialize GUI
sc.tracer(0)
sc.title("keyboard Arm")
skG.initializeSerial()


while True:
	value = mcu.readlines()

	for i in value:
		i = str(i, "utf-8").split(",")
		if (len(i) == len(dataFunc)):
			print(i)

	k = keyboard.read_key()
	if k == 'left':
		armAngle = armAngle + 1.5*random.randrange(10)
		armAngle = sk.sendAngle_PCToWearable(armAngle, mcu)

	elif k == 'right':
		armAngle = armAngle - 1.5*random.randrange(10)
		armAngle = sk.sendAngle_PCToWearable(armAngle, mcu)

	print(armAngle)
	
	turtle.undo()
	turtle.undo()
	skG.drawForearm(sc,armAngle, skG.COLOR_SERIAL)


# print("hiya pal")

# # keyboard.add_hotkey('left', extendArm)
# # keyboard.add_hotkey('right', flexArm)
# # while True:
# # 	keyboard.wait()

#     # keyboard.wait('left')
#     # print('left')

    
