	# Reading and Saving Serial Data from MCU
# Written by: Sreela Kodali (kodali@stanford.edu) 

import serial
import datetime
import csv
import os
import numpy as np
from scipy import signal

## CONSTANTS
PATH = '/Users/Sreela/Documents/School/Stanford/Year3_2/PIEZO2/JND_Study/additionalData/' # change this to your path!
PORT_NAME = "/dev/cu.usbmodem131754901" # change this to Arduino/teeny's port
BAUD_RATE = 4608000
RUNTIME_LENGTH = 60 # seconds


#DIRECTORY
fileName = str(datetime.datetime.now())[0:16] # default name is date and time
fileName = ((fileName.replace('/', '_')).replace(' ', '_')).replace(':','-')
p = PATH +fileName+'/'
if not (os.path.exists(p)):
	os.makedirs(p)
	print("New directory created: %s" % fileName)

mcu = serial.Serial(port=PORT_NAME, baudrate=BAUD_RATE, timeout=.1)
f = open(p + 'raw_' + fileName + '.csv', 'w+', encoding='UTF8', newline='')
writer = csv.writer(f)

# Read in serial data and save in csv
endTime = datetime.datetime.now() + datetime.timedelta(seconds=RUNTIME_LENGTH)
while (datetime.datetime.now() < endTime):
	value = mcu.readline()
	value = str(value, "utf-8").split(",")
	if (len(value) == 4):
		raw = [j.rstrip() for j in value]
		print(raw)
		#print(value[0]) # can also print(value) too
		writer.writerow(raw)
f.close()