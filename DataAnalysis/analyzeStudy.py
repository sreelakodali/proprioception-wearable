#analyze pilot results


import csv
import os
import datetime
import shutil
import numpy as np
import pandas as pd
from scipy import signal # import lfilter, lfilter_zi, filtfilt, butter
# from scipy.signal import lfilter, lfilter_zi, filtfilt, butter
from operator import itemgetter
import skFunctions as sk
import constants as CONST


### SEE WHEN TRIAL # CHANGES TO FIND DIFFERENT SECTIONS, IDENTIFY TARGET ANGLES AND SUBJECT ATTEMPTS

# # Find the most recent data directory
# allSubdirs = [CONST.PATH_LAPTOP+d for d in os.listdir(CONST.PATH_LAPTOP) if os.path.isdir(os.path.join(CONST.PATH_LAPTOP, d))]
# p = max(allSubdirs, key=sk.getCreationTime) + '/'
# fileName = [f for f in os.listdir(p) if (f.startswith('processed') and f.endswith('.csv'))]
# fileName = fileName[0]
# print("Newest data found: %s" % fileName)

# data = pd.read_csv(p + fileName, delimiter = ",").astype(float)

# nTrial = data['Trial Number'].tolist()
# targets = data['Target Angle'].tolist()
# time = data['time'].tolist()
# angle = data['flex sensor'].tolist()

# idx = [i for i in range(1,len(nTrial)) if nTrial[i]!=nTrial[i-1] ]
# idx1 = [165] + idx 
# idx2 = idx + [3340]

# nTrial_afterEachChange = [nTrial[i] for i in idx1]
# targets_afterEachChange = [targets[i] for i in idx1]
# angle_afterEachChange = [angle[i] for i in idx2]

# g = open(p + "WELP_TargetAngles" + fileName, 'w+', encoding='UTF8', newline='')
# w = csv.writer(g)
# for a in targets_afterEachChange:
# 	w.writerow([a])
# g.close()

# g = open(p + "WELP_SubjectAttempts" + fileName, 'w+', encoding='UTF8', newline='')
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

# Find the most recent data directory
allSubdirs = [CONST.PATH_LAPTOP+d for d in os.listdir(CONST.PATH_LAPTOP) if os.path.isdir(os.path.join(CONST.PATH_LAPTOP, d))]
p = max(allSubdirs, key=sk.getCreationTime) + '/'
fileName = [f for f in os.listdir(p) if (f.startswith('subjectAngleAttempts') and f.endswith('.csv'))]
fileName = fileName[0]
print("Newest data found: %s" % fileName)
data = pd.read_csv(p + fileName, delimiter = "\n").astype(float)
subjectAttempt = data['subject'].tolist()
#print(subjectAttempt)

fileName = [f for f in os.listdir(p) if (f.startswith('targetAngles') and f.endswith('.csv'))]
fileName = fileName[0]
print("Newest data found: %s" % fileName)
data1 = pd.read_csv(p + fileName, delimiter = "\n").astype(float)
target = data1['target'].tolist()
#print(target)

learning2 = list(range(0,20))
learning3 = list(range(20,30))
practice = list(range(30,70))

## UPDATE THESE RANGES
test_HnV = list(range(70,80)) # haptics, no visual
test_HV = list(range(80,90))
test_nHnV = list(range(90,100)) # no haptics, no visual
test_nHV = list(range(100,110)) # no haptics, visual
groups = [learning2, practice, test_HnV, test_HV, test_nHnV, test_nHV]
txt = ['learning2= ', 'practice= ', 'Test, Yes Haptic No Visual= ', 'Test, Yes Haptic Yes Visual= ', 'Test, No Haptic No Visual= ', 'Test, No Haptic Yes Visual= ']

print("---- MEAN ERROR -----")

for i in range(0,len(groups)):
	idx = groups[i]
	error = [target[i] - subjectAttempt[i] for i in idx]
	#print(error)
	avgError = sum(error) / len(error)
	# errorABS = [abs(target[i] - subjectAttempt[i]) for i in idx]
	# avgErrorABS = sum(errorABS) / len(errorABS)
	print(txt[i]+str(avgError))

print("---- MEAN ERROR (ABSOLUTE VALUE) -----")
for i in range(0,len(groups)):
	idx = groups[i]
	errorABS = [abs(target[i] - subjectAttempt[i]) for i in idx]
	avgErrorABS = sum(errorABS) / len(errorABS)
	print(txt[i]+str(avgErrorABS))

