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
onePoke = "2024-03-18_22-21"#"2024-01-30_20-47"


p = onePoke + "/"


N_TOTAL_TRIALS = 50
cut = 4 # to cut off the overshoot

for f in os.listdir(CONST.PATH_LAPTOP + p):
	if f.startswith('processed') and f.endswith('.csv'):
		processedData = pd.read_csv(CONST.PATH_LAPTOP + p + f, delimiter = ",", header=0).astype(float)
		command = processedData['actuator position, command'].tolist()
		force = processedData['force'].tolist()
		positionMeasured = processedData['actuator position, measured'].tolist()
		force1 = processedData['force1'].tolist()
		positionMeasured1 = processedData['actuator position, measured1'].tolist()



	elif f.startswith('trial') and f.endswith('.csv'):
		trialData = pd.read_csv(CONST.PATH_LAPTOP + p + f, delimiter = ",", header=0).astype(float)
		testValues = trialData['Test'].tolist()
		stepValues = trialData['stepSize'].tolist()

		#fix step Values 
		# Note: In the trial_*.csv file, the "test" values in the column are off. I've accidentally included 
		# the test for the next trial in the row, not the current, hence the fix needed
		fixedTestValues = []
		for i in range(len(stepValues)):
			if (stepValues[i] == 3):
				fixedTestValues.append(testValues[i] + stepValues[i])
			elif (stepValues[i] > 5):
				fixedTestValues.append(testValues[i] - round(stepValues[i]))
			elif (stepValues[i] == 0):
				fixedTestValues.append(testValues[i])

#print(fixedTestValues)

h = open(CONST.PATH_LAPTOP + "force_AND_Position_OfStairCase_onePoke_" + onePoke + ".csv", 'w+')
writer = csv.writer(h)
writer.writerow(["trialCount", "testCommand", "testCommandMM", "meanForce", "stdevForce", "meanPos", "stdevPos", "meanForce1", "stdevForce1", "meanPos1", "stdevPos1", "n"])

testValuesMM = [round(sk.mapFloat(i, 47, 139, 0.0, 20.0),2) for i in fixedTestValues] #commanded test Values
positionMeasuredMM = [round(sk.mapFloat(i, 986, 139, 0.0, 20.0),2) for i in positionMeasured]
positionMeasured1MM = [round(sk.mapFloat(i, 986, 139, 0.0, 20.0),2) for i in positionMeasured1]


#print(testValuesMM)


# NOTE: in V1 on Jan31, in "res_list", I find all the instances of that command, even from other trials.
# so in the forceOfStairCase_*.csv files, the meanForces could be across multiple trials 


print("--------------------------START --------------------------")

#print(len(fixedTestValues))
trialCount = 0
marker = 0
for test in fixedTestValues:
	# test = 120
	print(test)
	command2 = command[marker:]
	res_list = [i for i in range(len(command)) if command[i] == test]
	#print(" --- TEST: " + str(test) + "--- ")
	
	# I'd like to check how many contiguous pieces / trials in each list
	# if (len(res_list) > 18):
	
	# print(len(res_list))

	tc = 1
	trialStarts = []
	trialStarts.append(res_list[0])
	for j in range(1, len(res_list)-1):
		if ((res_list[j+1]-res_list[j]) > 1):
			trialStarts.append(res_list[j+1])
			tc = tc + 1
	
	if (tc != 1):

		trialStarts = [i for i in trialStarts if i > marker]
		# choose trial that's closest to marker and update marker
		diff = [i-marker for i in trialStarts]
		t = trialStarts[diff.index(min(diff))]
		#print(res_list.index(t))
		# print("before:")
		# print(res_list)

		res_list2 = []
		for j in range(res_list.index(t), len(res_list)-1):
			 if ((res_list[j+1]-res_list[j]) == 1):
			 	res_list2.append(res_list[j])
			 else:
			 	break
		res_list = res_list2

		#print("after:")
		
	
	marker = res_list[-1]
	print(res_list)
	#print(res_list[0])
	#print("marker: " + str(marker))
	#print(trialStarts)
	#print(tc)
	#print(len(res_list))

	# actuator 1
	res_force = [force[i] for i in res_list]
	res_force = res_force[cut:]
	meanForce = np.mean(res_force)
	stdevForce = np.std(res_force)
	
	res_pos = [positionMeasuredMM[i] for i in res_list]
	res_pos = res_pos[cut:]
	meanPos = np.mean(res_pos)
	stdevPos = np.std(res_pos)

	# actuator 2
	res_force1 = [force1[i] for i in res_list]
	res_force1 = res_force1[cut:]
	meanForce1 = np.mean(res_force1)
	stdevForce1 = np.std(res_force1)

	res_pos1 = [positionMeasured1MM[i] for i in res_list]
	res_pos1 = res_pos1[cut:]
	meanPos1 = np.mean(res_pos1)
	stdevPos1 = np.std(res_pos1)

	row = [trialCount+1, test, testValuesMM[trialCount], meanForce, stdevForce, meanPos, stdevPos, meanForce1, stdevForce1, meanPos1, stdevPos1, len(res_list)]
	writer.writerow(row)

	print(row)

	trialCount = trialCount + 1