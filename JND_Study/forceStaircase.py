# force of staircase
# Written by: Sreela Kodali (kodali@stanford.edu) 

import csv, os, datetime, sys, getopt, shutil
import numpy as np
import pandas as pd
import constants as CONST
import skFunctions as sk
import matplotlib
matplotlib.use("TkAgg")
from matplotlib import pyplot as plt


twoPoke = "2024-01-30_20-21"
onePoke = "2024-01-30_20-47"


p = twoPoke + "/"


N_TOTAL_TRIALS = 50
cut = 4

for f in os.listdir(CONST.PATH_LAPTOP + p):
	if f.startswith('processed') and f.endswith('.csv'):
		processedData = pd.read_csv(CONST.PATH_LAPTOP + p + f, delimiter = ",", header=0).astype(float)
		command = processedData['actuator position, command'].tolist()
		force = processedData['force'].tolist()
		force1 = processedData['force1'].tolist()

	elif f.startswith('trial') and f.endswith('.csv'):
		trialData = pd.read_csv(CONST.PATH_LAPTOP + p + f, delimiter = ",", header=0).astype(float)
		testValues = trialData['Test'].tolist()
		stepValues = trialData['stepSize'].tolist()

		#fix step Values
		fixedTestValues = []
		for i in range(len(stepValues)):
			if (stepValues[i] == 3):
				fixedTestValues.append(testValues[i] + stepValues[i])
			elif (stepValues[i] > 5):
				fixedTestValues.append(testValues[i] - round(stepValues[i]))
			elif (stepValues[i] == 0):
				fixedTestValues.append(testValues[i])

#print(fixedTestValues)

h = open(CONST.PATH_LAPTOP + "forceOfStairCase_twoPoke_" + twoPoke + ".csv", 'w+')
writer = csv.writer(h)
writer.writerow(["trialCount", "testCommand", "meanForce", "stdevForce", "meanForce1", "stdevForce1"])

trialCount = 1
for test in fixedTestValues:
	# test = 120
	res_list = [i for i in range(len(command)) if command[i] == test]

	# actuator 1
	res_force = [force[i] for i in res_list]
	res_force = res_force[cut:]
	meanForce = np.mean(res_force)
	stdevForce = np.std(res_force)

	# actuator 2
	res_force1 = [force1[i] for i in res_list]
	res_force1 = res_force1[cut:]
	meanForce1 = np.mean(res_force1)
	stdevForce1 = np.std(res_force1)

	row = [trialCount, test, meanForce, stdevForce, meanForce1, stdevForce1]
	writer.writerow(row)

	print(str(trialCount) + ", " + str(test) + ", " + str(meanForce) + ", " + str(stdevForce) + ", " +  str(meanForce1) + ", " + str(stdevForce1))

	trialCount = trialCount + 1