# processing some JND Test 2 
# Written by: Sreela Kodali (kodali@stanford.edu) 


import csv, os, datetime, sys, getopt, shutil
import numpy as np
import pandas as pd
import constants as CONST
import skFunctions as sk
import matplotlib
matplotlib.use("TkAgg")
from matplotlib import pyplot as plt


twoPoke = "force_AND_Position_OfStairCase_twoPoke_2024-01-30_20-21"
onePoke = "force_AND_Position_OfStairCase_onePoke_2024-01-30_20-47"


p = twoPoke


for f in os.listdir(CONST.PATH_LAPTOP):
	if f.startswith(p) and f.endswith('.csv'):
		data = pd.read_csv(CONST.PATH_LAPTOP + f, delimiter = ",", header=0).astype(float)

		force = data["meanForce"].tolist()
		measuredPos = data["meanPos"].tolist()
		command = data["testCommand"].tolist()

		stepSizes = np.zeros((len(force)-1, 3))
		for i in range(0, len(force)-1):

			stepSizes[i] = [(command[i+1]-command[i]), (measuredPos[i+1]-measuredPos[i]), (force[i+1]-force[i])]
			#print(stepSizes[i])

#print(stepSizes)

stepSizes = stepSizes[stepSizes[:, 0].argsort()]
print(stepSizes)

# u = np.unique(stepSizes[:,0])
# j = 0
# measuredBuf = []
# forceBuf = []
# new = np.zeros((len(u), 6))

# for i in range(0, len(stepSizes)):
# 	if (stepSizes[i,0] == u[j]):
# 		measuredBuf.append(stepSizes[i,1])
# 		forceBuf.append(stepSizes[i,2])
# 	else:

# 		#print(measuredBuf)
# 		#print(forceBuf)
# 		meanMeasured = sum(measuredBuf)/len(measuredBuf)
# 		stdevMeasured = np.std(measuredBuf)
# 		#nMeasured = len(measuredBuf)

# 		meanForce = sum(forceBuf)/len(forceBuf)
# 		stdevForce = np.std(forceBuf)
# 		n = len(forceBuf)

# 		new[j] = [u[j], meanMeasured, stdevMeasured, meanForce, stdevForce, n]
# 		#print(new[j])
# 		measuredBuf = []
# 		forceBuf = []

# 		j = j + 1
# 		if (stepSizes[i,0] == u[j]):
# 			measuredBuf.append(stepSizes[i,1])
# 			forceBuf.append(stepSizes[i,2])

# #print(measuredBuf)
# #print(forceBuf)

# meanMeasured = sum(measuredBuf)/len(measuredBuf)
# stdevMeasured = np.std(measuredBuf)

# meanForce = sum(forceBuf)/len(forceBuf)
# stdevForce = np.std(forceBuf)
# n = len(forceBuf)

# new[j] = [u[j], meanMeasured, stdevMeasured, meanForce, stdevForce, n]
# print(new)