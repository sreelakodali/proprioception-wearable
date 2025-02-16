import csv
import os
import datetime
import shutil
import numpy as np
import pandas as pd
import matplotlib   #FIX: fix for newer python environment
matplotlib.use("TkAgg")
from matplotlib import pyplot as plt

# Purpose: Process and plots data for a subject

nSubject = 7
calibrationDir = 
dataDir = []

# for each directory in dataDir, will read all the trial*.csv. if data isn't empty then, plots it


folder='subject3_2025-01-30_20-23'
PATH = '/Users/Sreela/Documents/School/Stanford/Year3_2/PIEZO2/JND_Study/bleData/' # change this to your path!
PATH = PATH + folder + '/'
# Find the most recent data directory
# allSubdirs = [PATH+d for d in os.listdir(PATH) if os.path.isdir(os.path.join(PATH, d))]
# p = max(allSubdirs, key=sk.getCreationTime) + '/'
# fileName = [f for f in os.listdir(p) if (f.startswith('subjectAngleAttempts') and f.endswith('.csv'))]
# fileName = fileName[0]
fileName = "processed_device1_" + folder + ".csv" #processed_device1_subjectsk_2025-01-04_02-00.csv"#"processed_device1_subject1_2024-12-18_22-36.csv"
newFileName = "NEW_"+fileName
print("Newest data found: %s" % fileName)

#data = pd.read_csv(p + fileName, delimiter = "\n").astype(float)


n = open(PATH + newFileName, 'w+', encoding='UTF8', newline='')
writer = csv.writer(n)

with open(PATH + fileName, 'r') as file:
    reader = csv.reader(file)
    for row in reader:
        #r = row.split(",")
        if (len(row) in [2,3]):
            if (not(row[0] == '')):
                
                if( ("LIMIT" in row[0])):
                    row[0] = row[0].replace('LIMIT =', '')
                writer.writerow(row)
                #print(row)

n.close()