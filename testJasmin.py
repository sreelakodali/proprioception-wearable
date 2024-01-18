# testing circuitPython for Jasmin

import serial
import datetime

PORT_NAME = "/dev/tty.usbmodem131755101"
BAUD_RATE = 115200
RUNTIME_LENGTH = 20  # second
WRITE_INC = 5

# -------------------------------------------------------------------------

def serialWrite(msg):
	adafruit.write(str(msg).encode())

def serialRead():
	value = (adafruit.readline()).decode()
	value = value.strip()
	return value

# -------------------------------------------------------------------------

# Task: Send serial data to adafruit every few seconds. Let's see if Adafruit reads it
print("~~ let's debug ~~")
adafruit = serial.Serial(port=PORT_NAME, baudrate=BAUD_RATE, timeout=.1)
counter = 0
endTime = datetime.datetime.now() + datetime.timedelta(seconds=RUNTIME_LENGTH)
r = []
for i in range(WRITE_INC, RUNTIME_LENGTH, WRITE_INC): r.append(datetime.datetime.now() + datetime.timedelta(seconds=i)) 

# serial will be open for RUNTIME_LENGTH
while (datetime.datetime.now() < endTime):

	# send message to adafruit via serial every WRITE_INC seconds
	if (counter < len(r)):
		if (datetime.datetime.now() > r[0+counter]):
			print("Checkpoint %i seconds. Type a message to adafruit:" % ((counter+1)*WRITE_INC))
			message = input()
			#message="10 20 30"
			print("sending: %s" % message)
			serialWrite(message)
			counter = counter + 1

	# read from adafruit to help us debug
	print(str(serialRead()))

print(" ~~~~~ done! ~~~~~~~")
	# may need to concatenate the message and play around with the string formating

	#received = ""
	# for x in range(0,(len(message))):
	# 	received = received + str(serialRead())
	# print(received)