import csv
import os
import datetime
import shutil
import numpy as np
import pandas as pd

### FOR SUBJECT 1, READ IN REVISED TARGET ANGLE AND COMPUTE ERROR WITH SUBJECT ATTEMPT
PATH = '/Users/Sreela/Documents/School/Stanford/Year3_2/PIEZO2/JND_Study/bleData/subjectsk_2025-01-04_02-00/' # change this to your path!
# Find the most recent data directory
# allSubdirs = [PATH+d for d in os.listdir(PATH) if os.path.isdir(os.path.join(PATH, d))]
# p = max(allSubdirs, key=sk.getCreationTime) + '/'
# fileName = [f for f in os.listdir(p) if (f.startswith('subjectAngleAttempts') and f.endswith('.csv'))]
# fileName = fileName[0]
fileName = "processed_device1_subjectsk_2025-01-04_02-00.csv"#"processed_device1_subject1_2024-12-18_22-36.csv"
newFileName = "NEW_processed_device1_subjectsk_2025-01-04_02-00.csv"
print("Newest data found: %s" % fileName)

#data = pd.read_csv(p + fileName, delimiter = "\n").astype(float)


n = open(PATH + newFileName, 'w+', encoding='UTF8', newline='')
writer = csv.writer(n)

with open(PATH + fileName, 'r') as file:
    reader = csv.reader(file)
    for row in reader:
        #r = row.split(",")
        if (len(row) == 3):
            if( not("LIMIT" in row[0])):
                writer.writerow(row)
            #n.write(row)
        #print(row)

n.close()