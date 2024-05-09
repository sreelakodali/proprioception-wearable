# Reading and Saving Serial Data from MCU
# Written by:
import serial
import datetime
import csv
import os
import sys
import glob
import threading
import numpy as np
from scipy import signal
# CONSTANTS
RUNTIME_LENGTH = 90  # second
PATH_DEST = "/Users/Sreela/Documents/School/Stanford/Year3_2/PIEZO2/"
PORT_NAME1 = "/dev/tty.usbmodem1101"
PORT_NAME2 = "/dev/tty.usbmodem101"
BAUD_RATE = 115200
# DIRECTORY
fileName = str(datetime.datetime.now())[0:16]  # default name is date and time
fileName = ((fileName.replace('/', '_')).replace(' ', '_')).replace(':', '-')
p = PATH_DEST + fileName+'/'
if not (os.path.exists(p)):
    os.makedirs(p)
    print("New directory created: %s" % fileName)
# Check the device connections for Windows or Linix
if sys.platform.startswith('win'):
    ports = ['COM%s' % (i + 1) for i in range(256)]
elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
    # this excludes your current terminal "/dev/tty"
    ports = glob.glob('/dev/tty[A-Za-z]*')
elif sys.platform.startswith('darwin'):
    ports = glob.glob('/dev/tty.*')
else:
    raise EnvironmentError('Unsupported platform')
result = []
for port in ports:
    try:
        s = serial.Serial(port)
        s.close()
        result.append(port)
    except (OSError, serial.SerialException):
        pass
print(result)
# Functions to run when setting up the threads
def arduinoClass():
    global arduino
    arduino = serial.Serial(port=PORT_NAME1, baudrate=BAUD_RATE, timeout=.1)
    print(str(datetime.datetime.now()))
    # print("Arduino On!")
def forcesensorClass():
    global force
    force = serial.Serial(port=PORT_NAME2, baudrate=BAUD_RATE, timeout=.1)
    print(str(datetime.datetime.now()))
    # print("Force On!")
# Starting up the Threads
thread_one = threading.Thread(target=arduinoClass, args=())
thread_two = threading.Thread(target=forcesensorClass, args=())
# Start the threads at the same time
thread_one.start()
thread_two.start()
# Join the Threads together
thread_one.join()
thread_two.join()
print("Done setting up the threads!")
f = open(p + 'raw_' + fileName + '.csv', 'w+', encoding='UTF8', newline='')
writer = csv.writer(f)
# Read in serial data and save in csv
endTime = datetime.datetime.now() + datetime.timedelta(seconds=RUNTIME_LENGTH)
while (datetime.datetime.now() < endTime):
    arduinoData = arduino.readline()
    forceData = force.readline()
    arduinoData = str(arduinoData, "utf-8").split()
    forceData = str(forceData, "utf-8").split()
    # if len(arduinoData) >= 1 or len(forceData) >= 1:
    print([arduinoData, forceData])
    # if len(arduinoData) >= 1 and len(forceData) >= 1:
    # print([[arduinoData[0], forceData[0]]])
    # print(arduinoData[0])
    # print(forceData[0])
    # # Check if the required data lists have the required elements
    # if len(arduinoData) >= 6 and len(forceData) >= 1:
    #     # For debugging
    #     print([arduinoData[2], arduinoData[6], arduinoData[9], forceData[0]])
    #     # Write the data into separate rows
    #     writer.writerows(
    #         [[arduinoData[2], arduinoData[6], arduinoData[9], forceData[0]]])
    #     # arduinoData[9] # Time
    #     # arduinoData[2] # Angle
    #     # arduinoData[6] # Speed
    #     # forceData[0]   # Force
f.close()