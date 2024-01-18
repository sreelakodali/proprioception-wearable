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

t = 100
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
skG.initializePilot()
skG.buffer('white')

trialAngles = range(30,180,15)

# # read angle from serial
for i in trialAngles:
	skG.deleteForearm(sc, 7)
	skG.drawForearm(sc,i, skG.COLOR)
	updateTrialLabel()
	skG.delay(sc, t)

skG.star(sc)
skG.deleteStar(sc)

skG.erase(sc, skG.COLOR_SERIAL)
skG.delay(sc, t)
for i in trialAngles:
	skG.deleteForearm(sc, 7)
	skG.drawForearm(sc,i, skG.COLOR)
	updateTrialLabel()
	skG.delay(sc, t)
# skG.drawForearm(sc,30)
# updateTrialLabel()
# skG.delay(sc, t)
	#while(serialAngle != i);

sc.onscreenclick(updateTrialLabel)
listen()

# done()