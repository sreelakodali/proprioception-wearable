# Mini Pilot Study for mulitple actuators
# Written by: Sreela Kodali (kodali@stanford.edu) 

import numpy as np
import serial
import datetime
import sys
import csv
import os
import skFunctions as sk
import skPilotGraphics as skG
import skPilotKeyboardFunctions as skP
import random
import constants as CONST
import keyboard
import random

p = "/dev/cu.usbmodem131755101"
baud_rate = 4608000
mcu = serial.Serial(port=p, baudrate=baud_rate, timeout=.1)

c = 0
while(1):
	k = keyboard.read_key()
	if k == 'left':
		if (c == 0):
			c = c + 1
			print("beep")
			mcu.write(str(4).encode())
		else:
			c = 0
	elif k == 'right':
		if (c == 0):
			c = c + 1
			print("boop")
			mcu.write(str(5).encode())
		else:
			c = 0