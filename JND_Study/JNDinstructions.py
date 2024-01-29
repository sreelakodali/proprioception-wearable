# Instructions 
# Written by: Sreela Kodali (kodali@stanford.edu) 


import datetime, getopt, turtle, time, keyboard, random
import numpy as np
import constants as CONST
import skFunctions as sk
import skPilotGraphics as skG



# you'll have to say if poke 1 and poke 2 are =, poke 1 > poke 2, or poke 1 < poke 2

# here's a practice

# Questions?


INTRO_TEXT_0 = ["Welcome!", "Thank you for participating in this study. Please", "click the red key on the keypad to continue."]
#INTRO_TEXT_0 = ["Experimental Setup", "Please click the blue key on the keypad to", "continue."]
INTRO_TEXT_1 = ["Experimental Setup", "We're going to do a Just Noticeable Difference", "(JND) study today. You'll wear this device, and", "each trial you'll receive two pokes, A and then B.", "", "", "", "", "", "", "", "", "Please click the red key to continue."]
INTRO_TEXT_2 = ["Experimental Setup", "Please indicate whether the intensity of Poke A is", "either greater, equal, or less than Poke B by", "selecting either the >, =, or < keys.",  "", "", "", "", "", "", "", "","Please click the red key to continue."]
# Your goal is to match your arm to this angle.
INTRO_TEXT_7 = ["Questions?", "", "", "", "", "", "", "", "", "", "", "Please click the red key to continue."]
INTRO_TEXT_8 = ["Done Fín", "woohoo"]
INTRO_TEXT = [INTRO_TEXT_0, INTRO_TEXT_1,INTRO_TEXT_2, INTRO_TEXT_7, INTRO_TEXT_8]



i = 0
skipClickForNewText = 0
sc = turtle.Screen()
sc.tracer(0)
sc.title("Introduction")

skG.initializeWindow(sc, ["JND"])

tr = turtle.Turtle()
sc.addshape('/Users/Sreela/Documents/School/Stanford/Year3_2/PIEZO2/GUIFigures/keypadJND.gif')
sc.addshape('/Users/Sreela/Documents/School/Stanford/Year3_2/PIEZO2/GUIFigures/setup.gif')

for txt in INTRO_TEXT:

	if not(skipClickForNewText):
		keyboard.wait('down')
	else:
		skipClickForNewText = 0

	print(i)
	i = i + 1
	skG.initializeWindow(sc, txt)

	# if (i == 7):
	# 	skG.initializeWindow_MultiColor(sc,txt, 0)
	# 	tr.shape('/Users/Sreela/Documents/School/Stanford/Year3_2/PIEZO2/GUIFigures/setup.gif')
	# 	tr.goto(100,0)
	# 	tr.stamp()
	# 	turtle.update()
	# else:
	# 	skG.initializeWindow(sc, txt)

	if (i == 1):
		tr.shape('/Users/Sreela/Documents/School/Stanford/Year3_2/PIEZO2/GUIFigures/keypadJND.gif')
		turtle.update()

	# elif (i == 2):
	# 	skG.drawUpperArm()
	# 	skG.drawForearm(sc,120, skG.COLOR)
	# elif (i == 3):
	# 	skG.drawUpperArm_Serial()
	# 	skG.drawForearm(sc,120, skG.COLOR_SERIAL)
	# elif (i == 4):
	# 	tr.stamp()
	# 	turtle.update()
	# elif (i == 5):
	# 	skG.drawUpperArm_Serial()
	# 	skG.drawForearm(sc,armAngle, skG.COLOR_SERIAL)
	# 	while True:
	# 		k = keyboard.read_key()
	# 		if k == 'left':
				
	# 			armAngle = armAngle + sk.generateKeyboardInc()
	# 		elif k == 'right':
	# 			if (random.randrange(2)):
	# 				inc = 3
	# 			else:
	# 				inc = 1
	# 			print(inc)
	# 			armAngle = armAngle - sk.generateKeyboardInc()

	# 		elif k == 'up':
	# 			skipClickForNewText = 1
	# 			break

	# 		if (armAngle > 180):
	# 			armAngle = 180

	# 		if (armAngle < 30):
	# 			armAngle = 30
	# 		turtle.undo() # angle
	# 		turtle.undo() # dot
	# 		skG.drawForearm(sc,armAngle, skG.COLOR_SERIAL)

	# elif (i == 6):
	# 	armAngle = 180
	# 	test = [180, 165, 150, 135, 120, 60, 45]
	# 	#print(test)
	# 	skG.drawUpperArm()
	# 	skG.drawForearm(sc,armAngle, skG.COLOR_SERIAL)

	# 	for a in test:
	# 		# turtle.undo() # angle
	# 		# turtle.undo() # dot
	# 		skG.erase4(sc, 'white')
	# 		skG.drawForearm(sc,a, skG.COLOR)
	# 		skG.drawForearm(sc,armAngle, skG.COLOR_SERIAL)

	# 		while True:
	# 			k = keyboard.read_key()
	# 			if k == 'left':
	# 				armAngle = armAngle + 1.5*(random.randrange(10) + 1)
	# 			elif k == 'right':
	# 				armAngle = armAngle - 1.5*(random.randrange(10) + 1)

	# 			elif k == 'up':
	# 				skipClickForNewText = 1
	# 				break

	# 			if (armAngle > 180):
	# 				armAngle = 180

	# 			if (armAngle < 30):
	# 				armAngle = 30
	# 			turtle.undo() # angle
	# 			turtle.undo() # dot
	# 			skG.drawForearm(sc,armAngle, skG.COLOR_SERIAL)

