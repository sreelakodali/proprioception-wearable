import csv
import os
import datetime
import shutil
import numpy as np
import pandas as pd


folder= 'subject5_2025-04-26_16-01'#'subject5_2025-04-26_17-17'#'subject8_2025-02-17_17-42'
PATH = '/Users/Sreela/Documents/School/Stanford/Year3_2/PIEZO2/JND_Study/bleData/' # change this to your path!
PATH = PATH + folder + '/'
fileName = "trial1_4_subject5_2025-04-26_16-01_16-11.csv"#"trial1_4_subject5_2025-04-26_17-17_17-19.csv"#"trial1_4_" + folder + ".csv" #processed_device1_subjectsk_2025-01-04_02-00.csv"#"processed_device1_subject1_2024-12-18_22-36.csv"
newFileName = "modified_"+fileName

data = pd.read_csv(PATH + fileName, delimiter = ",").astype(float)
#data = data.sort_values(by=['Test'])
testValues = np.unique(data['Test'])
col = data.columns.values

nCount = 8
for t in testValues:
    buf = data.loc[data['Test'] == t]
    buf = buf.iloc[0:nCount, :]

    if t == testValues[0]:
        newData = buf.values
    else:
        newData = np.concatenate((newData,buf.values), axis=0)
print(newData)

n = open(PATH + newFileName, 'w+', encoding='UTF8', newline='')
writer = csv.writer(n, delimiter=',')
writer.writerows(newData)
n.close()