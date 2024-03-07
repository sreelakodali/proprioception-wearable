# processing some JND Test 
# Written by: Sreela Kodali (kodali@stanford.edu) 


import csv, os, datetime, sys, getopt, shutil
import numpy as np
import pandas as pd
import constants as CONST
import skFunctions as sk
import matplotlib
matplotlib.use("TkAgg")
from matplotlib import pyplot as plt


twoPoke = "2024-01-30_20-21/"
onePoke = "2024-01-30_20-47/"


p = twoPoke

for f in os.listdir(CONST.PATH_LAPTOP + p):
	if f.startswith('processed') and f.endswith('.csv'):
		data = pd.read_csv(CONST.PATH_LAPTOP + p + f, delimiter = ",", header=0).astype(float)

		sortedData = data.sort_values(by=["actuator position, command"])
		# commandPos = sortedData["actuator position, command"].tolist()
		# measuredPos = sortedData["actuator position, measured"].tolist()
		# force = sortedData['force'].tolist()
		
		#sortedData.to_csv(CONST.PATH_LAPTOP + 'bloop.csv')
		#print(sortedData)
		# for unique actuator position commands
		unique = sortedData["actuator position, command"].unique()

		print(unique)
		new = np.zeros((len(unique), 7)) # number of rows is number of unique values


		# for all the rows that are same command, average/group their measured command and force 
		j = 0
		measuredBuf = []
		forceBuf = []
		
		print("----------- UNIQUE VALUE:" + str(unique[j]))
		for i in range(0, sortedData.shape[0]):
			u = unique[j]	

			if (sortedData["actuator position, command"].iloc[i] != u):

				#print(measuredBuf)
				#print(forceBuf)

				meanMeasured = sum(measuredBuf)/len(measuredBuf)
				stdevMeasured = np.std(measuredBuf)
				nMeasured = len(measuredBuf)

				meanForce = sum(forceBuf)/len(forceBuf)
				stdevForce = np.std(forceBuf)
				nForce = len(forceBuf)

				new[j] = [u, meanMeasured, stdevMeasured, nMeasured, meanForce, stdevForce, nForce]
				print(new[j])
				j = j + 1
				print("----------- UNIQUE VALUE:" + str(unique[j]))
				measuredBuf = []
				forceBuf = []

			# add them to the buffer
			measuredBuf.append(sortedData["actuator position, measured"].iloc[i])
			forceBuf.append(sortedData["force"].iloc[i])


		meanMeasured = sum(measuredBuf)/len(measuredBuf)
		stdevMeasured = np.std(measuredBuf)
		nMeasured = len(measuredBuf)

		meanForce = sum(forceBuf)/len(forceBuf)
		stdevForce = np.std(forceBuf)
		nForce = len(forceBuf)

		new[j] = [u, meanMeasured, stdevMeasured, nMeasured, meanForce, stdevForce, nForce]
		print(new[j])

		
		print(" -- ALL DATA -- ")
		print(new)
		df = pd.DataFrame(new)
		df.to_csv(CONST.PATH_LAPTOP + 'bloop3.csv')






		#for i in np.unique(commandPos):
			# force
			# force
			#print(i)

			
		#force1 = data['force1'].tolist()

		#new = zip(commandPos, measuredPos, force)
		#print(list(new))

		print("voila! done")

