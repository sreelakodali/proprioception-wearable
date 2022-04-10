# Processing & Plotting Serial Data from Sensory Substitution Devce 
# Written by: Sreela Kodali (kodali@stanford.edu) 

import csv
import os
import numpy as np
import pandas as pd
from scipy import signal # import lfilter, lfilter_zi, filtfilt, butter
# from scipy.signal import lfilter, lfilter_zi, filtfilt, butter
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

t_d = 0#sk.delay(angle, device1_positionMeasured, time)
print("Time delay between signals: " + str(t_d) + " s")

# idx_peaksPositionMeasured, _ = signal.find_peaks(np.asarray(device1_positionMeasured), height=(7,20), distance=150)
# idx_peaksPositionMeasured = idx_peaksPositionMeasured.tolist()

# t_peaksPositionMeasured = list(itemgetter(*idx_peaksPositionMeasured)(time))
# idx_peaksAngle = []
# for t in t_peaksPositionMeasured:
# 	t = t - t_d
# 	idx_peaksAngle.append((np.abs(time-t)).argmin())
# t_peaksAngle = list(itemgetter(*idx_peaksAngle)(time))

# t_peakDelays = list(zip(t_peaksAngle, t_peaksPositionMeasured))

# plot 1
sk.plot_OneTactor(1, fileName, time, angle, force, device1_positionMeasured, t_d)
#sk.plot_SingleTactor(0, fileName, time, angle, force, device1_positionMeasured, t_d, t_peakDelays, idx_peaksAngle, idx_peaksPositionMeasured)
#sk.plot_TwoTactor(0, fileName, time, angle, force, device1_positionMeasured, t_d, t_peakDelays, idx_peaksAngle, idx_peaksPositionMeasured)