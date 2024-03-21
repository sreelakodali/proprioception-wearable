# trial by trial view for JND study
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
onePoke = "2024-01-30_20-47/" #"2024-03-18_22-21/"


p = onePoke

N_TOTAL_TRIALS = 50

for f in os.listdir(CONST.PATH_LAPTOP + p):
	if f.startswith('processed') and f.endswith('.csv'):
		data = pd.read_csv(CONST.PATH_LAPTOP + p + f, delimiter = ",", header=0).astype(float)
		nTrials = data['TrialCounter'].tolist()
		time = data['time'].tolist()
		force = data['force'].tolist()
		force1 = data['force1'].tolist()

		for i in range(1,N_TOTAL_TRIALS+1):
		#i = 1	
			a = nTrials.index(i)
			b = len(nTrials) - 1 - nTrials[::-1].index(i)

			print(a)
			print(b)
			#print(time[a])

			fig, axs = plt.subplots(2)
			fig.suptitle('Force in Trial #' + str(i))
			axs[0].plot(time[a:b+1], force[a:b+1])
			axs[1].plot(time[a:b+1], force1[a:b+1])
			axs[0].set_ylim(-2,14)
			axs[1].set_ylim(-2,14)
			plt.show()
			


		 