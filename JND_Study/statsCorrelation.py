import csv
import os
import datetime
import shutil
import numpy as np
import scipy.stats as stats
import pandas as pd

PATH = '/Users/Sreela/Documents/School/Stanford/Year3_2/PIEZO2/JND_Study/bleData/' # change this to your path!
fileName = "OverallData_ALL.csv"
df = pd.read_csv(PATH+fileName)

#label1="circumfrence" #'', 'JNDRef2_1', 'JNDRef2_2', 'JNDRatio2_2-1', 'JNDRef4_1', 'JNDRef4_2', 'JNDRatio4_2-1'
labelArr = ["Stiffness2", "StiffnessTotal", "ASR1", "ASR2"]#list(df.columns)
#labelArr = labelArr[1:]#["avgMax2", "JNDRatio4_2-1"]#
print(labelArr)
#labelArr = ["circumfrence", "StiffnessTotal", "Elbow length"]
counter = 0
completed = []
for j in labelArr:
	for l in labelArr:	
		# Pearson correlation

		if j!= l:

			myTuple = (j,l)
			myTuple2 = (l,j)

			if not( (myTuple in completed) or (myTuple2 in completed)):
				completed.append(myTuple)
				completed.append(myTuple2)

				#spearman_corr, p_value = stats.spearmanr(df[j], df[l])

				pearson_corr, p_value = stats.pearsonr(df[j], df[l])
				if (1):
				#if ( (p_value < 0.09) and (p_value > 0.00005)):
					counter += 1
					#print("{} vs. {} Pearson correlation={:.3f} P-value={:.4f}".format(j, l, pearson_corr, p_value))
					print("{}, {}, {}, {:.3f}, {:.4f}".format(counter,j, l, pearson_corr, p_value))
			# print(f"Pearson correlation: {pearson_corr:.3f}")
			# print(f"P-value: {p_value:.4f}")