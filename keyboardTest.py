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

mcu = serial.Serial(port=CONST.PORT_NAME, baudrate=CONST.BAUD_RATE, timeout=.1)


armAngle = 180

sc = turtle.Screen()
# Initialize GUI
sc.tracer(0)
sc.title("keyboard Arm")
skG.initializeSerial()



while True:
	k = keyboard.read_key()
	if k == 'left':
		armAngle = armAngle + 1
	elif k == 'right':
		armAngle = armAngle - 1

	if (armAngle > 180):
		armAngle = 180
	elif (armAngle < 30):
		armAngle = 30

	print(armAngle)

	if (armAngle < 100):
		print(str(0).encode())
		mcu.write(str(0).encode())

	print(str(armAngle).encode())
	mcu.write(str(armAngle).encode())


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

    
