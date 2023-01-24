# Instructions 
# Written by: Sreela Kodali (kodali@stanford.edu) 


import datetime
import numpy as np
import getopt
import constants as CONST
import skFunctions as sk
import turtle
import skPilotGraphics as skG
import time
import keyboard
import random




INTRO_TEXT_1 = ["Instructions", "This represents the elbow angle of an arm. This", "angle will change.", "", "", "", "", "", "", "", "", "", "Please click the blue key to continue."]
INTRO_TEXT_2 = ["Instructions", "This orange arm is your virtual arm. You will", "control your virtual arm with the keypad.", "", "", "", "", "", "", "", "", "","Please click the blue key to continue."]
# Your goal is to match your arm to this angle.
INTRO_TEXT_3 = ["Instructions", "To extend your virtual arm, click the <- key. To", "flex your virtual arm, click the -> key.", "", "", "", "", "", "", "", "", "","Please click the blue key to continue."]
INTRO_TEXT_4 = ["Instructions", "Try using the <- and -> keys to move your virtual", "arm.", "", "", "", "", "", "", "", "", "","Please click the blue key to continue."]
INTRO_TEXT_5 = ["Instructions", "Your goal is to match your virtual arm with a given", "target angle shown in blue. Try it out."]
INTRO_TEXT_6 = ["Done Fín", "woohoo"]
INTRO_TEXT = [INTRO_TEXT_1,INTRO_TEXT_2, INTRO_TEXT_3, INTRO_TEXT_4, INTRO_TEXT_5, INTRO_TEXT_6]
INTRO_TEXT_0 = ["Welcome!", "Thank you for participating in this study. Please", "click the blue key on the keypad to continue."]


i = 0
skipClickForNewText = 0
armAngle = 180
sc = turtle.Screen()
sc.tracer(0)
sc.title("Introduction")

skG.initializeWindow(sc, INTRO_TEXT_0)

tr = turtle.Turtle()
sc.addshape('/Users/Sreela/Documents/School/Stanford/Year3_2/PIEZO2/GUIFigures/keypad.gif')
tr.shape('/Users/Sreela/Documents/School/Stanford/Year3_2/PIEZO2/GUIFigures/keypad.gif')
turtle.update()

for txt in INTRO_TEXT:

	if not(skipClickForNewText):
		keyboard.wait('up')
	else:
		skipClickForNewText = 0

	i = i + 1
	skG.initializeWindow(sc, txt)

	if (i == 1):
		skG.drawUpperArm()
		skG.drawForearm(sc,120, skG.COLOR)
	if (i == 2):
		skG.drawUpperArm_Serial()
		skG.drawForearm(sc,120, skG.COLOR_SERIAL)
	if (i == 3):
		tr.stamp()
		turtle.update()
	if (i == 4):
		skG.drawUpperArm_Serial()
		skG.drawForearm(sc,armAngle, skG.COLOR_SERIAL)
		while True:
			k = keyboard.read_key()
			if k == 'left':
				armAngle = armAngle + 1.5*(random.randrange(10) + 1)
			elif k == 'right':
				armAngle = armAngle - 1.5*(random.randrange(10) + 1)

			elif k == 'up':
				skipClickForNewText = 1
				break

			if (armAngle > 180):
				armAngle = 180

			if (armAngle < 30):
				armAngle = 30
			turtle.undo() # angle
			turtle.undo() # dot
			skG.drawForearm(sc,armAngle, skG.COLOR_SERIAL)

	if (i == 5):
		armAngle = 180
		test = [180, 165, 150, 135, 120, 60, 45]
		print(test)
		skG.drawUpperArm()
		skG.drawForearm(sc,armAngle, skG.COLOR_SERIAL)

		for a in test:
			# turtle.undo() # angle
			# turtle.undo() # dot
			skG.erase4(sc, 'white')
			skG.drawForearm(sc,a, skG.COLOR)
			skG.drawForearm(sc,armAngle, skG.COLOR_SERIAL)

			while True:
				k = keyboard.read_key()
				if k == 'left':
					armAngle = armAngle + 1.5*(random.randrange(10) + 1)
				elif k == 'right':
					armAngle = armAngle - 1.5*(random.randrange(10) + 1)

				elif k == 'up':
					skipClickForNewText = 1
					break

				if (armAngle > 180):
					armAngle = 180

				if (armAngle < 30):
					armAngle = 30
				turtle.undo() # angle
				turtle.undo() # dot
				skG.drawForearm(sc,armAngle, skG.COLOR_SERIAL)

