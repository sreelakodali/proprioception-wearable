# Read, Process, Plot Serial Data
# Written by: Sreela Kodali (kodali@stanford.edu) 

import serial
import datetime
import csv
import os
import numpy as np
import constantsBrian as CONST
import bvFunctions as bv
import matplotlib
import matplotlib.animation as animation
matplotlib.use("TkAgg")
from matplotlib import pyplot as plt

# Step 1: Create new folder with the current time and date to save the data in
fileName = str(datetime.datetime.now())[0:16] # default name is date and time
fileName = ((fileName.replace('/', '_')).replace(' ', '_')).replace(':','-')
p = CONST.PATH_SAVEDATA +fileName+'/'
if not (os.path.exists(p)):
	os.makedirs(p)
	print("New directory created: %s" % fileName)

# Step 2: Create serial connection to microcontroller and new csv file
mcu = serial.Serial(port=CONST.PORT_NAME, baudrate=CONST.BAUD_RATE, timeout=.1)
if (CONST.TRANSFER_RAW): f = open(p + 'raw_' + fileName + '.csv', 'w+', encoding='UTF8', newline='')
else: f = open(p + "processed_" + fileName + '.csv', 'w+', encoding='UTF8', newline='')
writer = csv.writer(f)

# dataFunc = {'time':sk.millisToSeconds, 'flex sensor':sk.computeAngle,'dutyCycle command':sk.commandToPosition, \
# 			'force':sk.computeForce}

dataFunc = {'time':bv.millisToSeconds,'force':bv.computeForce, 'command':bv.command}

# Read in serial data and save in csv
# fig = plt.figure()
# ax = fig.add_subplot(1, 1, 1)
time = []
force = []
command = []
writer.writerow(list(dataFunc.keys()))

endTime = datetime.datetime.now() + datetime.timedelta(seconds=CONST.RUNTIME_LENGTH)
while (datetime.datetime.now() < endTime):
	bv.readData(mcu, f, writer, dataFunc, time, force, command)

# if you want to plot and not save the figure, change the 1 to 0 in following command
# Example: bv.plot_Force(0, p, fileName, time, force)
bv.plot_ForceCommand(1, p, fileName, time, force, command)

# ani = animation.FuncAnimation(fig, bv.animate, fargs=(mcu, f, writer, dataFunc, time, force, ax), interval=500)
# plt.show()

f.close()

