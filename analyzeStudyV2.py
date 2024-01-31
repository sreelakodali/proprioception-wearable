#analyze pilot results V2


import csv, os, datetime, sys, getopt, shutil
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
# subjects = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16]
# #hapticsConditionsTest = [1, 0, 1, 1, 0, 1, 0, 1, 0, 1, 0, 0, 1, 0]
# hapticsConditionsTest = [1, 0, 1, 1, 0, 1, 0, 1, 0, 1, 0, 0, 1, 1, 0, 0]

subjects = [1, 3, 4, 5, 6, 7, 9, 10, 11, 12, 13, 14, 15, 16]
hapticsConditionsTest = [1, 1, 1, 0, 1, 0, 0, 1, 0, 0, 1, 1, 0, 0]
errorTotal = []
errorABSTotal =[]

# errorHnV = []
# errorHV = []

#for i in list(range(8,13)):

for i in list(range(0, len(subjects))):

	## COMPUTING ERROR
	p = "SUBJECT" + str(subjects[i]) + '/'
	#print(p)
# 	for f in os.listdir(CONST.PATH_LAPTOP + p):
# 		if f.startswith('subject') and f.endswith('.csv'):
# 			data0 = pd.read_csv(CONST.PATH_LAPTOP + p + f, delimiter = "\n", header=None).astype(float)
# 			subjectAttempt = [i[0] for i in data0.values.tolist()]
# 			#print(subjectAttempt)
# 		elif f.startswith('targetAngles') and f.endswith('.csv'):
# 			data1 = pd.read_csv(CONST.PATH_LAPTOP + p + f, delimiter = "\n", header=None).astype(float)
# 			target = [i[0] for i in data1.values.tolist()]
# 			#print(target)
# 		# elif f.startswith('processed') and f.endswith('.csv'):
# 		# 	data = pd.read_csv(CONST.PATH_LAPTOP + p + f, delimiter = ",").astype(float)
# 		# 	force = data['force'].tolist()
# 		# 	dist = data["actuator position, measured"].tolist()
# 		# 	time = data['time'].tolist()
# 		# 	nTrial = data["'Trial Number'"].tolist()
# 		# 	angle = data['flex sensor'].tolist()
# 		# 	targets = data["'Target Angle'"].tolist()

# 			# print(len(force))
# 			# print(len(dist))
# 			# print(len(time))

# 			# k = []
# 			# for z in list(range(0,len(dist))):
# 			# 	if ((dist[z]) > 0 and force[z]/dist[z] >= 0 and force[z]/dist[z] < 2):
# 			# 		k.append(force[z]/dist[z])
# 			# 	else:
# 			# 		k.append(0)
# 			# meanK = np.mean(k)
# 			# #print("k = %s" % meanK)
# 			# #print(force)
# 			# sk.plot_Force(0, p, p, time, k)
# 			#skD.plotStudyTest(0, p, time,targets,angle,force,nTrial)
# 	#print(hapticsConditionsTest[i-8])
# 	#if (hapticsConditionsTest[i-8]):

# 	#print(hapticsConditionsTest[i])
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

# 	#txt = ['1, 0, ', '1, 1, ', '0, 0, ', '0, 1, ']
# 	txt = ['Test, Yes Haptic No Visual  | ', 'Test, Yes Haptic Yes Visual | ', 'Test, No Haptic No Visual   | ', 'Test, No Haptic Yes Visual  | ']
# 	groups = [test_HnV, test_HV, test_nHnV, test_nHV]
# 	groups = [test_HnV]
# 	#txt = [txt[3]]
# 	#groups = [groups[3]]

# 	#print("----------------------------- MEAN ERROR     MEAN ERROR (ABS)-----")
# 	buff0 = []
# 	buff1 = []
# 	for r in range(0,len(groups)):
# 		error = [target[j] - subjectAttempt[j] for j in groups[r]]
# 		errorABS = [abs(target[j] - subjectAttempt[j]) for j in groups[r]]
# 		#print(error)
# 		avgError = sum(error) / len(error)
# 		buff0.append(avgError)
# 		avgErrorABS = sum(errorABS) / len(errorABS)
# 		buff1.append(avgErrorABS)
# 		#print(str(subjects[i]) + ", " + txt[r] + str(avgErrorABS))
# 		#writer.writerow([subjects[i], 0, 1, avgErrorABS])
# 		#print(txt[r]+str(avgError) + "          " + str(avgErrorABS))
# 		print(str(avgErrorABS))

# 	#print([subjects[i]] +  buff1 + [meanK])
# #	writer.writerow([subjects[i]] +  buff1 + [meanK])
# #file.close()
# 	errorTotal.append(buff0)
# 	errorABSTotal.append(buff1)


	# Force vs. Distance
	# maxForce =
	fileName = [f for f in os.listdir(CONST.PATH_LAPTOP + p) if (f.startswith('maxForce') and f.endswith('.csv'))]
	fileName = fileName[0]
	data = pd.read_csv(CONST.PATH_LAPTOP + p + fileName, delimiter = ",").astype(float)

	command = data['command'].tolist()
	force = data['force'].tolist()
	dist = [sk.mapFloat(i, 64, 139, 4, 20) for i in command]
	sk.plot_ForceDistance(0, p, p, dist, force)

	# processedData = 
	# data = pd.read_csv(CONST.PATH_LAPTOP + p + '/maxForce.csv', delimiter = ",").astype(float)

	# Force vs. Time


# errorTotal = np.array(errorTotal)
# errorABSTotal = np.array(errorABSTotal)
# #print(errorTotal)

# print(np.average(errorTotal,axis=0))
# stdError = np.std(errorTotal,axis=0)
# print(stdError/np.sqrt(np.size(errorTotal, 0)))

#file = open('error_notABS.csv','w+', encoding='UTF8', newline='')
#writer = csv.writer(file)
# for row in errorTotal: #list(range(0,14)):
# 	print(row)
# 	writer.writerow(row)

# file.close()
# print(errorABSTotal)
# print(np.average(errorABSTotal,axis=0))
# stdABSError = np.std(errorABSTotal,axis=0)
# print(stdABSError/np.sqrt(np.size(errorABSTotal, 0)))




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

