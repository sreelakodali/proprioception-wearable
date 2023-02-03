# Pilot Keyboard Support functions
# Written by: Sreela Kodali (kodali@stanford.edu)
import skFunctions as sk
import csv


EXPERIMENT_TEXT_0 = ["Welcome!", "Let's begin the experiment", "", "", "", "", "", "", "", "", "", "", "Please click the blue key to continue."]
EXPERIMENT_TEXT_1 = ["Experiment", "Task: Match virtual arm's elbow angle with target", "angle. Use <- and -> keys to move virtual arm.", "", "First there will be a learning phase followed by a",  "test phase.", "", "", "", "", "", "", "Please click the blue key to continue."]
EXPERIMENT_TEXT_X = ["Experiment", "Task: Match virtual arm's elbow angle with target", "angle. Use <- and -> keys to move virtual arm.", "", "Target Angle", "Virtual Arm", "Haptic Device", "Arm Rest", "", "", "", "", "Please click the blue key to continue."]
EXPERIMENT_TEXT_2 = ["Learning 1: Explore", "Move virtual arm with keypad and observe haptic", "feedback. Virtual arm will be shown in orange.", "", "Pay close attention to the haptic feedback and", "how that corresponds to where the virtual arm is.", "You will have 1 minute to explore.", "", "", "", "", "", "Please click the blue key to begin learning 1"]
EXPERIMENT_TEXT = [EXPERIMENT_TEXT_0, EXPERIMENT_TEXT_1, EXPERIMENT_TEXT_2]

EXPERIMENT_TEXT_3 = ["Learning 1: Explore", ""]
EXPERIMENT_TEXT_4 = ["Learning 1: Explore", "Learning 1 complete.", "", "", "", "", "", "", "", "", "", "", "Please click the blue key to continue"]

def writeOutData(i,dataFunc, writer2, writer, nTrials, target, bookmark):
	i = str(i, "utf-8").split(",")
	if (len(i) == len(dataFunc)):
		raw = [j.rstrip() for j in i]
		raw = raw + [nTrials, target, bookmark]
		writer2.writerow(raw)

		newRow = sk.processNewRow(dataFunc, i)	
		newRow = newRow + [nTrials, target, bookmark]
		writer.writerow(newRow)	
		print(newRow)