# Pilot Keyboard Support functions
# Written by: Sreela Kodali (kodali@stanford.edu)
import skFunctions as sk
import csv

def writeOutData(i,dataFunc, writer2, writer, trialCount):
	i = str(i, "utf-8").split(",")
	if (len(i) == 8): # hardcoded, length of packet from device
		raw = [j.rstrip() for j in i]
		raw = raw + [trialCount]
		writer2.writerow(raw)

		newRow = sk.processNewRow(dataFunc, i)	
		newRow = newRow + [trialCount]
		writer.writerow(newRow)	
		print(newRow)