# Processing & Plotting Serial Data from Sensory Substitution Devce 
# Written by: Sreela Kodali (kodali@stanford.edu) 

import csv
import os
import numpy as np
import pandas as pd
from scipy import signal # import lfilter, lfilter_zi, filtfilt, butter
# from scipy.signal import lfilter, lfilter_zi, filtfilt, butter
import matplotlib.pyplot as plt
from operator import itemgetter
import skFunctions as sk
import constants as CONST

# Finding the most recent data directory
allSubdirs = [CONST.PATH+d for d in os.listdir(CONST.PATH) if os.path.isdir(os.path.join(CONST.PATH, d))]
p = max(allSubdirs, key=os.path.getctime) + '/'
fileName = [f for f in os.listdir(p) if f.endswith('.csv')]
fileName = fileName[0]

dataFunc = {'time':sk.millisToSeconds, 'flex sensor':sk.computeAngle,'actuator position, command':sk.commandToPosition, \
			'actuator position, measured':sk.feedbackToPosition, 'force':sk.computeForce}
columnNames = list(dataFunc.keys())

# Read in and plot data
data = pd.read_csv(p + fileName, delimiter = ",").astype(float)
time = data['time'].tolist()
angle = data['flex sensor'].tolist() # angle
device1_positionCommand = data['actuator position, command'].tolist()
device1_positionMeasured = data['actuator position, measured'].tolist()
force  = data['force'].tolist()

# plot
fig, ax1 = plt.subplots()
fig.subplots_adjust(right=0.75)

ax2 = ax1.twinx()
ax3 = ax1.twinx()
# ax4 = ax1.twinx()
plt.suptitle("Real-time Data " + fileName[4:-4], name='Arial', weight='bold')
ax1.set_xlabel("Time (s)", name='Arial')
plt.xticks(name='Arial')
plt.yticks(name='Arial')

ax1.set_ylabel("Angle (degrees)", name='Arial')
l1 = ax1.plot(time, angle, 'b', linewidth=1.75, label='Angle')
ax1.yaxis.label.set_color('b')
ax1.tick_params(axis='y', color='b')
#ax1.set_ylim(30,180)
ax3.spines['left'].set_color('b')

ax2.set_ylabel("Force (N)", name='Arial',)
l2 = ax2.plot(time, force, 'r', linewidth=1.75, label='Force')
ax2.yaxis.label.set_color('r')
ax2.spines['right'].set_color('r')
ax2.tick_params(axis='y', color='r')
ax2.set_ylim(0,15)

ax3.spines['right'].set_position(('axes',1.2))
ax3.set_ylabel("Actuator Position (mm)", name='Arial')
l3 = ax3.plot(time, device1_positionMeasured, 'g', linewidth=1.75, label='Actuator Position (Measured)')
ax3.yaxis.label.set_color('g')
ax3.spines['right'].set_color('g')
ax3.tick_params(axis='y', color='g')
ax3.set_ylim(0,20)

#l4 = ax2.plot(time, device1_positionCommand, color='orange', linewidth=1.75, label='Actuator Position (Command)')

t_d = sk.delay(angle, device1_positionMeasured, time)
print("Time delay between signals: " + str(t_d) + " s")

idx_peaksPositionMeasured, _ = signal.find_peaks(np.asarray(device1_positionMeasured), height=(7,20), distance=150)
idx_peaksPositionMeasured = idx_peaksPositionMeasured.tolist()

t_peaksPositionMeasured = list(itemgetter(*idx_peaksPositionMeasured)(time))
idx_peaksAngle = []
for t in t_peaksPositionMeasured:
	t = t - t_d
	idx_peaksAngle.append((np.abs(time-t)).argmin())
t_peaksAngle = list(itemgetter(*idx_peaksAngle)(time))

t_peakDelays = list(zip(t_peaksAngle, t_peaksPositionMeasured))

for d in t_peakDelays:
	ax1.axvspan(d[0], d[1], color='teal', alpha=0.5)
ax1.plot(time, angle,'bD',markevery=idx_peaksAngle)
ax3.plot(time, device1_positionMeasured,'gD',markevery=idx_peaksPositionMeasured)
plt.title("Time Delay = %.2f ms" % (t_d*1000), name='Arial')

l_all = l1+l2+l3#+l4
labels = [l.get_label() for l in l_all]

plt.grid(True)
ax1.legend(l_all, labels, loc=0)
plt.savefig(p +"fig_"+fileName[4:-4])
plt.show()