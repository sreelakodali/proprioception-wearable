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

	if (i == 1):
		tr.shape('/Users/Sreela/Documents/School/Stanford/Year3_2/PIEZO2/GUIFigures/keypadJND.gif')
		turtle.update()
