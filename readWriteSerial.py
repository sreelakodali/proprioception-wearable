# Reading and Saving Serial Data from MCU 
# AND writing data to microcontroller
# Written by: Sreela Kodali (kodali@stanford.edu) 

import serial, datetime, csv, os, keyboard, time
import numpy as np
from scipy import signal

## CONSTANTS
PATH = '/Users/Sreela/Documents/School/Stanford/Year3_2/PIEZO2/JND_Study/additionalData/' # change this to your path!
PORT_NAME = "/dev/cu.usbmodem101" # change this to Arduino/teensy's port
BAUD_RATE = 115200
RUNTIME_LENGTH = 60 # if you want to collect data for fixed amount of time, set this time in seconds

WAIT = 5 # how long holding the poke
RETRACT = 10 # SOME COMMAND TO BRING POKER BACK TO NEUTRAL POSITION
COMMANDS = [1500, 1550, 1600, 1650, 1700, 1750]



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

i = 0
# Read in serial data and save in csv
endTime = datetime.datetime.now() + datetime.timedelta(seconds=RUNTIME_LENGTH)
#while (datetime.datetime.now() < endTime): # Uncomment if collecting data for fixed amount of time
while(1):

	value = mcu.readline()
	value = str(value, "utf-8").split()
	if (value):
		print(value[0]) # can also print(value) too
		writer.writerow(value)

	k = keyboard.read_key()
	if (k == 'up' and i < len(COMMANDS)):
		print("Sending stimulus: " + str(COMMANDS[i]))
		mcu.write(str(COMMANDS[i]).encode())
		time.sleep(WAIT)
		mcu.write(str(RETRACT).encode())
		i = i + 1
	elif (k == 'up' and i == len(COMMANDS)):
		break
f.close()