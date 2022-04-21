# Test Graphics
# Written by: Sreela Kodali (kodali@stanford.edu) 

import numpy as np
import turtle
import serial
import datetime
import csv
import os
import constants as CONST
import skFunctions as sk
import skPilotGraphics as skG

t = 10
nTrials = 0
sc = turtle.Screen()

def updateTrialLabel():
	global sc
	sc.tracer(0)
	turtle.penup()
	turtle.goto(325,300)
	global nTrials
	turtle.write(nTrials, move=False, font=("Arial",36, "normal"))
	nTrials = nTrials + 1
	turtle.penup()

# Initialize GUI
sc.tracer(0)
sc.title("Pilot Study")
skG.initialize()
skG.buffer()

trialAngles = range(30,180,15)

# # read angle from serial
for i in trialAngles:
	skG.deleteForearm(sc)
	skG.drawForearm(sc,i)
	updateTrialLabel()
	skG.delay(sc, t)

skG.star()
skG.deleteStar(sc)

for i in trialAngles:
	skG.deleteForearm(sc)
	skG.drawForearm(sc,i)
	updateTrialLabel()
	skG.delay(sc, t)
# skG.drawForearm(sc,30)
# updateTrialLabel()
# skG.delay(sc, t)
	#while(serialAngle != i);

# sc.onscreenclick(updateTrials)
# listen()

# done()