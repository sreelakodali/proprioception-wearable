#analyze pilot results V4


import csv
import os
import datetime
import sys, getopt
import shutil
import numpy as np
import pandas as pd
from scipy import signal # import lfilter, lfilter_zi, filtfilt, butter
# from scipy.signal import lfilter, lfilter_zi, filtfilt, butter
from operator import itemgetter
import skFunctions as sk
import skDataAnalysisFunctions as skD
import constants as CONST

# ##Give input file
# opts, args = getopt.getopt(sys.argv[1:],"i:",["ifile="])
# for opt, arg in opts:
# 	if opt in ("-i", "--ifile"):
# 		p = arg
# print(p)


#hapticsConditionsTest = [0, 1, 0, 0, 1]
subjects = [1, 3, 4, 5, 6, 7, 9, 10, 11, 12, 13, 14, 15, 16]
hapticsConditionsTest = [1, 1, 1, 0, 1, 0, 0, 1, 0, 0, 1, 1, 0, 0]
print(len(hapticsConditionsTest))
print(len(subjects))

targetAngles = list(range(45,15,180))
arr_HnV =  [[0] * len(targetAngles)] * len(subjects)
arr_HV = [[0] * len(targetAngles)] * len(subjects)
arr_nHnV = [[0] * len(targetAngles)] * len(subjects)
arr_nHV = [[0] * len(targetAngles)] * len(subjects)

data = []
for i in list(range(0, len(subjects))):
	subjectBuffer = []
	p = "SUBJECT" + str(subjects[i]) + '/'
	print(p)
	for f in os.listdir(CONST.PATH_LAPTOP + p):
		#if f.startswith('subject') and f.endswith('.csv'):
			# data0 = pd.read_csv(CONST.PATH_LAPTOP + p + f, delimiter = "\n", header=None).astype(float)
			# subjectAttempt = [i[0] for i in data0.values.tolist()]
			#print(subjectAttempt)
		# #elif f.startswith('targetAngles') and f.endswith('.csv'):
		# 	data1 = pd.read_csv(CONST.PATH_LAPTOP + p + f, delimiter = "\n", header=None).astype(float)
		# 	target = [i[0] for i in data1.values.tolist()]
			#print(target)

		if f.startswith('maxForce') and f.endswith('.csv'):
			file = open(CONST.PATH_LAPTOP +p+f,'r', encoding='UTF8', newline='')
			lines = file.readlines()
			for k in list(range(0,len(lines))):
				if 'ZERO' in lines[k]:
					z = int(lines[k-1])
					minVal = int(lines[k+1])
					maxVal = int(lines[k+3])
					subjectBuffer.append([subjects[i], (minVal - z)*(45/512), (maxVal - z)*(45/512)])

			if (subjectBuffer):
				l = len(subjectBuffer)
				subjectBuffer = np.array(subjectBuffer)
				#print(subjectBuffer)
				meanMin = sum(subjectBuffer[:,1])/len(subjectBuffer)
				stderrMin = np.std(subjectBuffer[:,1])/np.sqrt(l)
				meanMax = sum(subjectBuffer[:,2])/len(subjectBuffer)
				stderrMax = np.std(subjectBuffer[:,2])/np.sqrt(l)

				data.append([subjects[i], meanMin, stderrMin, meanMax, stderrMax])

print(data)
newF = open('minMaxForce_MeanSTDperSubject_16.csv','w+', encoding='UTF8', newline='')
writer = csv.writer(newF)
writer.writerows(data)
newF.close()
print("done yay")
			#force = [i[0] for i in data2.values.tolist()]
			#print(target)

			#print(str(max(force)))# + ", " + str(min(force)))
# 		# for this subject, extract the ones of that condition, 
# 	if (hapticsConditionsTest[i]):		
# 		test_HnV = list(range(70,80)) # haptics, no visual
# 		test_HV = list(range(80,90)) # haptics, yes visual
# 		test_nHnV = list(range(90,100)) # no haptics, no visual
# 		test_nHV = list(range(100,110)) # no haptics, visual

# 	else:
# 		test_nHnV = list(range(70,80)) # no haptics, no visual
# 		test_nHV = list(range(80,90)) # no haptics, visual
# 		test_HnV = list(range(90,100)) # haptics, no visual
# 		test_HV = list(range(100,110)) # haptics, yes visual


# 	#sort it in ascending order of target angles
# 	arr_HnV[i] = [s for _, s in sorted(zip( [target[k] for k in test_HnV], [force[k] for k in test_HnV]))]
# 	#print(arr_HnV)
# 	arr_HV[i] = [s for _,s in sorted(zip( [target[k] for k in test_HV], [force[k] for k in test_HV]))]
# 	arr_nHnV[i] = [s for _, s in sorted(zip( [target[k] for k in test_nHnV], [force[k] for k in test_nHnV]))]
# 	arr_nHV[i] = [s for _, s in sorted(zip( [target[k] for k in test_nHV], [force[k] for k in test_nHV]))]


# f = open('force_HnV.csv','w+', encoding='UTF8', newline='')
# writer = csv.writer(f)
# writer.writerows(arr_HnV)
# f.close()

# f = open('force_HV.csv','w+', encoding='UTF8', newline='')
# writer = csv.writer(f)
# writer.writerows(arr_HV)
# f.close()

# f = open('force_nHnV.csv','w+', encoding='UTF8', newline='')
# writer = csv.writer(f)
# writer.writerows(arr_nHnV)
# f.close()

# f = open('force_nHV.csv','w+', encoding='UTF8', newline='')
# writer = csv.writer(f)
# writer.writerows(arr_nHV)
# f.close()

# print("done, yay!")

	# txt = ['1, 0, ', '1, 1, ', '0, 0, ', '0, 1, ']
	# #txt = ['Test, Yes Haptic No Visual  | ', 'Test, Yes Haptic Yes Visual | ', 'Test, No Haptic No Visual   | ', 'Test, No Haptic Yes Visual  | ']
	# groups = [test_HnV, test_HV, test_nHnV, test_nHV]

	# #print("----------------------------- MEAN ERROR     MEAN ERROR (ABS)-----")
	# buff0 = []
	# buff1 = []
	# for r in range(0,len(groups)):
	# 	error = [target[j] - subjectAttempt[j] for j in groups[r]]
	# 	errorABS = [abs(target[j] - subjectAttempt[j]) for j in groups[r]]
	# 	#print(error)
	# 	avgError = sum(error) / len(error)
	# 	buff0.append(avgError)
	# 	avgErrorABS = sum(errorABS) / len(errorABS)
	# 	buff1.append(avgErrorABS)
	# 	print(str(subjects[i]) + ", " + txt[r] + str(avgErrorABS))
	# 	#print(txt[i]+str(avgError) + "          " + str(avgErrorABS))
	# 	#print(str(avgErrorABS))

	# errorTotal.append(buff0)
	# errorABSTotal.append(buff1)


# 	# Force vs. Distance
# 	# maxForce =
# 	fileName = [f for f in os.listdir(CONST.PATH_LAPTOP + p) if (f.startswith('maxForce') and f.endswith('.csv'))]
# 	fileName = fileName[0]
# 	data = pd.read_csv(CONST.PATH_LAPTOP + p + fileName, delimiter = "\n").astype(float)

# 	command = data['command'].tolist()
# 	force = data['force'].tolist()
# 	dist = [sk.mapFloat(i, 64, 139, 4, 20) for i in command]
# 	sk.plot_ForceDistance(0, p, p, dist, force)

# 	# processedData = 
# 	# data = pd.read_csv(CONST.PATH_LAPTOP + p + '/maxForce.csv', delimiter = ",").astype(float)

# 	# Force vs. Time


# print(errorTotal)
# print(errorABSTotal)





# ## COMBINE TIMES FOR PROCESSED FOR SUBJECT2 and SUBJECT3
# p1 = '2023-01-31_18-30'
# p2 = '2023-01-31_18-44'
# data = pd.read_csv(CONST.PATH_LAPTOP + 'SUBJECT3/processed_2023-01-31_18-xxRAW.csv', delimiter = ",").astype(float)
# data0 = pd.read_csv(CONST.PATH_LAPTOP + 'SUBJECT3/' + p1 + '/processed_' + p1 + '.csv', delimiter = ",").astype(float)
# data1 = pd.read_csv(CONST.PATH_LAPTOP + 'SUBJECT3/' + p2 + '/processed_' + p2 + '.csv', delimiter = ",").astype(float)

# time1 = data0['time'].tolist()
# endTime = time1[-1]
# print(endTime)
# revisedTime2 = [i + endTime for i in data1['time'].tolist()]
# #print(revisedTime2)
# newTime = time1 + revisedTime2
# data['time'] = newTime
# data.to_csv(CONST.PATH_LAPTOP + 'SUBJECT3/processed_2023-01-31_18-xx.csv')
# print("done")

## FINDING SUBJECT3's subject attempt angles
# p = '2023-01-31_18-30'
# data = pd.read_csv(CONST.PATH_LAPTOP + 'SUBJECT3/'+p + '/processed_' + p + '.csv', delimiter = ",").astype(float)

# # PLOT FORCE VS TIME
# for p in ['2023-01-30_19-34', '2023-01-31_14-03', '2023-01-31_14-23']:
# 	data = pd.read_csv(CONST.PATH_LAPTOP + p + '/processed_' + p + '.csv', delimiter = ",").astype(float)
# 	force = data['newForce'].tolist()
# 	time = data['time'].tolist()
# 	#print(force)
# 	sk.plot_Force(0, p, p, time, force)


# ## COMPUTING SUBJECT 2 ERROR
# p = '2023-01-31_14-23'
# data0 = pd.read_csv(CONST.PATH_LAPTOP + p + '/subjectAngleAttempts_' + p + '.csv', delimiter = "\n").astype(float)
# data1 = pd.read_csv(CONST.PATH_LAPTOP + p + '/targetAngles_' + p + '.csv', delimiter = "\n").astype(float)
# subjectAttempt = data0['subject'].tolist()
# target = data1['target'].tolist()

# ## UPDATE THESE RANGES
# test_nHnV = list(range(0,10)) # no haptics, no visual
# test_nHV = list(range(10,20)) # no haptics, visual
# test_HnV = list(range(20,30)) # haptics, no visual
# test_HV = list(range(30,40))  # haptics, visual

# groups = [test_nHnV, test_nHV, test_HnV, test_HV]
# txt = ['Test, No Haptic No Visual= ', 'Test, No Haptic Yes Visual= ', 'Test, Yes Haptic No Visual= ', 'Test, Yes Haptic Yes Visual= ']
# # groups = [test_HnV, test_HV, test_nHnV, test_nHV]
# # txt = ['Test, Yes Haptic No Visual= ', 'Test, Yes Haptic Yes Visual= ', 'Test, No Haptic No Visual= ', 'Test, No Haptic Yes Visual= ']

# print("---- MEAN ERROR -----")

# for i in range(0,len(groups)):
# 	idx = groups[i]
# 	error = [target[j] - subjectAttempt[j] for j in idx]
# 	#print(error)
# 	avgError = sum(error) / len(error)
# 	# errorABS = [abs(target[i] - subjectAttempt[i]) for i in idx]
# 	# avgErrorABS = sum(errorABS) / len(errorABS)
# 	print(txt[i]+str(avgError))

# print("---- MEAN ERROR (ABSOLUTE VALUE) -----")
# for i in range(0,len(groups)):
# 	idx = groups[i]
# 	errorABS = [abs(target[j] - subjectAttempt[j]) for j in idx]
# 	#print(errorABS)
# 	avgErrorABS = sum(errorABS) / len(errorABS)
# 	print(txt[i]+str(avgErrorABS))


# # FORCE VS DISTANCE FOR EACH SUBJECT
# calibrationFolders = ['2023-01-30_19-32_subject1', '2023-01-31_13-35_subject2', '2023-01-31_18-23_subject3']
# for p in calibrationFolders:
# 	data = pd.read_csv(CONST.PATH_LAPTOP + p + '/maxForce.csv', delimiter = ",").astype(float)
# 	#data = pd.read_csv(CONST.PATH_LAPTOP + p + '/processed_' + p + '.csv', delimiter = ",").astype(float)
# 	print("Data found: %s" % p)

# 	# Generated new force for subjects 1 and 2
# 	command = data['command'].tolist()
# 	force = data['force'].tolist()
# 	dist = [sk.mapFloat(i, 64, 130, 4, 20) for i in command]
# 	sk.plot_ForceDistance(0, p, p, dist, force)




# FIXING FORCE FOR SUBJECTS 1 and 2
# data = pd.read_csv(CONST.PATH_LAPTOP + p + '/processed_' + p + '.csv', delimiter = ",").astype(float)
# force = data['force'].tolist()
# data['newForce'] = [i + 45*255/512 for i in force] 
# data.to_csv(CONST.PATH_LAPTOP + p + '/processed2_NEWFORCE' + p + '.csv')




# # Find the most recent data directory
# allSubdirs = [CONST.PATH_LAPTOP+d for d in os.listdir(CONST.PATH_LAPTOP) if os.path.isdir(os.path.join(CONST.PATH_LAPTOP, d))]
# p = max(allSubdirs, key=sk.getCreationTime) + '/'
# fileName = [f for f in os.listdir(p) if (f.startswith('processed') and f.endswith('.csv'))]
# fileName = fileName[0]
# print("Newest data found: %s" % fileName)



### SEE WHEN TRIAL # CHANGES TO FIND DIFFERENT SECTIONS, IDENTIFY TARGET ANGLES AND SUBJECT ATTEMPTS
# data = pd.read_csv(p + fileName, delimiter = ",").astype(float)

# time = data['time'].tolist()
# angle = data['flex sensor'].tolist()
# nTrial = data['Trial Number'].tolist()
# targets = data['Target Angle'].tolist()


# idx = [i for i in range(1,len(nTrial)) if nTrial[i]!=nTrial[i-1] ]
# print(len(time))
# idx1 = [176] + idx 
# idx2 = idx + [len(time)-1]

# nTrial_afterEachChange = [nTrial[i] for i in idx1]
# targets_afterEachChange = [targets[i] for i in idx1]
# angle_afterEachChange = [angle[i] for i in idx2]

# g = open(CONST.PATH_LAPTOP + p + "/WELP_TargetAngles" + p + ".csv", 'w+', encoding='UTF8', newline='')
# #g = open(p + "WELP_TargetAngles" + fileName, 'w+', encoding='UTF8', newline='')
# w = csv.writer(g)
# for a in targets_afterEachChange:
# 	w.writerow([a])
# g.close()

# g = open(CONST.PATH_LAPTOP + 'SUBJECT3/'+p + "/WELP_SubjectAttempts" + p + ".csv", 'w+', encoding='UTF8', newline='')
# #g = open(p + "WELP_SubjectAttempts" + fileName, 'w+', encoding='UTF8', newline='')
# w = csv.writer(g)
# for a in angle_afterEachChange:
# 	w.writerow([a])
# g.close()
# print("New Trial angles saved.")

# print("nTrial")
# print(nTrial_afterEachChange)
# print("targets")
# print(targets_afterEachChange)
# print("Angle Attempts")
# print(angle_afterEachChange)


### FOR SUBJECT 1, READ IN REVISED TARGET ANGLE AND COMPUTE ERROR WITH SUBJECT ATTEMPT

# # Find the most recent data directory
# allSubdirs = [CONST.PATH_LAPTOP+d for d in os.listdir(CONST.PATH_LAPTOP) if os.path.isdir(os.path.join(CONST.PATH_LAPTOP, d))]
# p = max(allSubdirs, key=sk.getCreationTime) + '/'
# fileName = [f for f in os.listdir(p) if (f.startswith('subjectAngleAttempts') and f.endswith('.csv'))]
# fileName = fileName[0]
# print("Newest data found: %s" % fileName)

# data = pd.read_csv(p + fileName, delimiter = "\n").astype(float)
# subjectAttempt = data['subject'].tolist()
# #print(subjectAttempt)

# fileName = [f for f in os.listdir(p) if (f.startswith('targetAngles') and f.endswith('.csv'))]
# fileName = fileName[0]
# print("Newest data found: %s" % fileName)
# data1 = pd.read_csv(p + fileName, delimiter = "\n").astype(float)
# target = data1['target'].tolist()
# #print(target)

# learning2 = list(range(0,20))
# learning3 = list(range(20,30))
# practice = list(range(30,70))

# ## UPDATE THESE RANGES
# test_HnV = list(range(70,80)) # haptics, no visual
# test_HV = list(range(80,90))
# test_nHnV = list(range(90,100)) # no haptics, no visual
# test_nHV = list(range(100,110)) # no haptics, visual
# groups = [learning2, practice, test_HnV, test_HV, test_nHnV, test_nHV]
# txt = ['learning2= ', 'practice= ', 'Test, Yes Haptic No Visual= ', 'Test, Yes Haptic Yes Visual= ', 'Test, No Haptic No Visual= ', 'Test, No Haptic Yes Visual= ']

# print("---- MEAN ERROR -----")

# for i in range(0,len(groups)):
# 	idx = groups[i]
# 	error = [target[i] - subjectAttempt[i] for i in idx]
# 	#print(error)
# 	avgError = sum(error) / len(error)
# 	# errorABS = [abs(target[i] - subjectAttempt[i]) for i in idx]
# 	# avgErrorABS = sum(errorABS) / len(errorABS)
# 	print(txt[i]+str(avgError))

# print("---- MEAN ERROR (ABSOLUTE VALUE) -----")
# for i in range(0,len(groups)):
# 	idx = groups[i]
# 	errorABS = [abs(target[i] - subjectAttempt[i]) for i in idx]
# 	avgErrorABS = sum(errorABS) / len(errorABS)
# 	print(txt[i]+str(avgErrorABS))

