# Supporting Functions for Sensory Substitution Devce 
# Written by: Sreela Kodali (kodali@stanford.edu) 

import numpy as np
from scipy import signal
import constants as CONST
#import calibration


## CALIBRATION
ACTUATOR_FEEDBACK_MIN = 9
ACTUATOR_FEEDBACK_MAX = 606
# zero force
# max position and force of user
# min position and force for user (detection)

## FUNCTIONS ##
# Offloading computation that isn't needed real-time to computer

# Function 0: Mapping float value x in different range 
def mapFloat(x, in_min, in_max, out_min, out_max):
	return (float) ((x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min)

# Function 1: millisecond --> second
def millisToSeconds(s):
	return s/1000

# Function 2: place holder for angle function
def computeAngle(data):
	return data #float(bin(data))
	#format(255, '008b')
# Function 3: Servo command (degrees) --> actuator position (mm)
def commandToPosition(c):
	return 0.22*c - 10.7

# Function 4: Feedback signal from actuator (1/1024th of V) to actuator position (mm)
def feedbackToPosition(f):
	return mapFloat(f, ACTUATOR_FEEDBACK_MIN, ACTUATOR_FEEDBACK_MAX, CONST.ACTUATOR_POSITION_MAX, CONST.ACTUATOR_POSITION_MIN)

# Function 5: Digital value from force sensor --> force measurement (N)
def computeForce(data):
	return (data - 256) * (45.0)/511

def processNewRow(val, loopIncrement):
	r = []
	for key in dataFunc:
		if (val[columnNames.index(key)].lstrip("-").rstrip().isnumeric()):
			x = dataFunc[key](float(val[columnNames.index(key)]))
			if (loopIncrement < 20 and key == 'time' and x > 2): #fixme
				break
			r.append(x)
	return r

def delay(angle, positionMeasured, timeArr):

	ind = np.random.choice(len(timeArr)-CONST.N_WINDOW, CONST.N_CORR)
	maxCorr = []
	for i in ind:
		a = angle[i:i+85]
		p = positionMeasured[i:i+85]
    
		n = len(a)
		c = signal.correlate(a, p, mode='same') / np.sqrt(signal.correlate(a, a, mode='same')[int(n/2)] * signal.correlate(p, p, mode='same')[int(n/2)])
		maxCorr.append(timeArr[i+np.argmax(c)] - timeArr[i])
		#maxCorr.append(np.argmax(c))
	return np.mean(maxCorr)