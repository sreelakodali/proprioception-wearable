# Supporting Functions for Sensory Substitution Device -- Brian's Version
# Written by: Sreela Kodali (kodali@stanford.edu) 

import constantsBrian as CONST
import matplotlib
import matplotlib.animation as animation
matplotlib.use("TkAgg")
from matplotlib import pyplot as plt


def processNewRow(dataFunc, val):
	columnNames = list(dataFunc.keys())
	r = []
	for key in dataFunc:
		if (val[columnNames.index(key)].lstrip("-").rstrip().isnumeric()): # negatives removed otherwise seen as char
			x = dataFunc[key](float(val[columnNames.index(key)]))
			r.append(x)
	return r

#  millisecond --> second
def millisToSeconds(s):
	return s/1000

def command(c):
	return c

def computeForce(data):
	return round(((data - 255) * (45.0)/512) - CONST.ZERO_FORCE, 2)

def plot_ForceCommand(s, p, fileName, time, force, command):
	fig, ax1 = plt.subplots()
	ax2 = ax1.twinx()

	plt.suptitle("Real-time Data " + fileName, name='Arial', weight='bold')
	ax1.set_xlabel("Time (s)", name='Arial')
	plt.xticks(name='Arial')
	plt.yticks(name='Arial')

	ax1.set_ylabel("Force (N)", name='Arial',)
	l1 = ax1.plot(time, force, 'r', linewidth=1.75, label='Force')
	ax1.yaxis.label.set_color('r')
	ax1.tick_params(axis='y', color='r')
	ax1.set_ylim(0,25)

	ax2.set_ylabel("Hoxel Command (PWM Duty %)", name='Arial',)
	l2 = ax2.plot(time, command, 'g', linewidth=1.75, label='command')
	ax2.yaxis.label.set_color('g')
	ax2.spines['right'].set_color('g')
	ax2.tick_params(axis='y', color='g')
	ax2.set_ylim(0,100)

	plt.grid(True)
	#ax1.legend(l_all, labels, loc=0)
	if s==1: plt.savefig(p +"fig_"+fileName)
	plt.show()


def readData (mcu, f, writer, dataFunc, time, force, command):
	value = mcu.readline()
	value = str(value, "utf-8").split(",")
	if (len(value) == len(dataFunc)):
		newRow = processNewRow(dataFunc, value)
		time.append(newRow[0])
		force.append(newRow[1])
		command.append(newRow[2])
		print(newRow)
		writer.writerow(newRow)


# def animate (mcu, f, writer, dataFunc, time, force, ax):
# 	value = mcu.readline()
# 	value = str(value, "utf-8").split(",")
# 	if (len(value) == len(dataFunc)):
# 		newRow = processNewRow(dataFunc, value)
# 		time.append(newRow[0])
# 		force.append(newRow[1])
# 		print(newRow)
# 		writer.writerow(newRow)

# 		# # limit
# 		time = time[-20:]
# 		force = force[-20:]

#     	# clear
# 		ax.clear()
# 		ax.plot(time, force)

# 		#plot format
# 		plt.suptitle("Real-time Data " + fileName, name='Arial', weight='bold')
# 		ax.set_xlabel("Time (s)", name='Arial')
# 		plt.xticks(name='Arial')
# 		plt.yticks(name='Arial')
# 		ax.set_ylabel("Force (N)", name='Arial',)
# 		ax.yaxis.label.set_color('r')
# 		ax.tick_params(axis='y', color='r')
# 		ax.set_ylim(0,25)


# Mapping float value x in different range 
def mapFloat(x, in_min, in_max, out_min, out_max):
	return (float) ((x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min)

# Computing angle from flex sensor data
def computeAngle(data):
	#a = 180 - float(data)/64.0 #float(data)
	#return a
	#if a > 90: return a
	#else: return a - 0.2*(90-a)
	 
	return mapFloat(data, CONST.ANGLE_DATA_MIN, CONST.ANGLE_DATA_MAX, CONST.ANGLE_MIN, CONST.ANGLE_MAX) # NEEDS CALIBRATED VAL