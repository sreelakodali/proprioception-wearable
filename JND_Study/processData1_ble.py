import csv
import os
import datetime
import shutil
import numpy as np
import pandas as pd

# Purpose: removes extra commas or zeros in the data and text

### FOR SUBJECT 1, READ IN REVISED TARGET ANGLE AND COMPUTE ERROR WITH SUBJECT ATTEMPT
folder='subjectsk_2025-04-08_21-50'#'subject8_2025-02-17_17-42'
PATH = '/Users/Sreela/Documents/School/Stanford/Year3_2/PIEZO2/JND_Study/bleData/' # change this to your path!
PATH = PATH + folder + '/'
# Find the most recent data directory
# allSubdirs = [PATH+d for d in os.listdir(PATH) if os.path.isdir(os.path.join(PATH, d))]
# p = max(allSubdirs, key=sk.getCreationTime) + '/'
# fileName = [f for f in os.listdir(p) if (f.startswith('subjectAngleAttempts') and f.endswith('.csv'))]
# fileName = fileName[0]
fileName = "processed_device2_" + folder + ".csv" #processed_device1_subjectsk_2025-01-04_02-00.csv"#"processed_device1_subject1_2024-12-18_22-36.csv"
newFileName = "EXP_"+fileName
print("Newest data found: %s" % fileName)

#data = pd.read_csv(p + fileName, delimiter = "\n").astype(float)


n = open(PATH + newFileName, 'w+', encoding='UTF8', newline='')
writer = csv.writer(n)
limitArr = []
with open(PATH + fileName, 'r') as file:
    reader = csv.reader(file)
    for row in reader:
        #r = row.split(",")
        if (len(row) in [5, 6,7]):
            if (not(row[0] == '')):
                
                # if( ("LIMIT" in row[0])):
                #     row[0] = row[0].replace('LIMIT =', '')
                #     limitArr.append(row)
                writer.writerow(row)
                #print(row)

        # if (len(row) in [2,3]):
        #     if (not(row[0] == '')):
                
        #         if( ("LIMIT" in row[0])):
        #             row[0] = row[0].replace('LIMIT =', '')
        #             limitArr.append(row)
        #         writer.writerow(row)
        #         #print(row)

n.close()
#print(limitArr)