# Pilot Study
# Written by: Sreela Kodali (kodali@stanford.edu) 

from turtle import *

COLOR = '#51A0DC'
COLOR_SERIAL = '#A8F3A3'
ELBOW_SIZE = 100
PEN_SIZE = 50
ARM_LENGTH = 300
HAND_SIZE = 120

def setForearm(screen, angle, time):
	drawForearm(screen, angle)
	delay(screen, time)
	penup()

def drawUpperArm():
	goto(0,0)
	penup()
	goto(ARM_LENGTH,-(ARM_LENGTH)/2)
	pendown()
	backward(ARM_LENGTH)
	dot(ELBOW_SIZE)
	penup()
	right(180)
	update()

def drawForearm(screen, angle, c):
	penup()
	screen.tracer(0)
	color(c, c)
	goto(0, -(ARM_LENGTH)/2)
	seth(180)
	pendown()
	left(angle)
	backward(ARM_LENGTH)
	dot(HAND_SIZE)
	update()

def deleteForearm(screen, r):
	screen.tracer(0)
	for i in range(0,r):
		undo()
	update()

def delay(screen, time):
	screen.tracer(1,time)
	goto(0, -(ARM_LENGTH)/2)
	dot(ELBOW_SIZE)
	update()

def removeTrialLabel(screen):
	screen.tracer(0)
	penup()
	goto(345,320)
	dot(50, 'white')
	#goto(325,300)

def initializePilot():
	hideturtle()
	color(COLOR, COLOR)
	pensize(PEN_SIZE)
	penup()
	goto(-350,300)
	write("Pilot Study", move=False, font=("Arial",48, "normal"))
	goto(200,300)
	write("Trial #: ", move=False, font=("Arial",36, "normal"))
	# drawing initial arm
	drawUpperArm()
	penup()

def initializeSerial():
	hideturtle()
	color(COLOR_SERIAL, COLOR_SERIAL)
	pensize(40)
	penup()
	goto(-350,300)
	write("Serial Data", move=False, font=("Arial",48, "normal"))
	# drawing initial arm
	drawUpperArm()
	penup()
	
def buffer(c):
	penup()
	goto(0,-250)
	dot(50, c)
	dot(50, c)
	dot(50, c)
	dot(50, c)
	dot(50, c)
	dot(50, c)
	dot(50, c)
	penup()

def star(screen):
	screen.tracer(1,10)
	penup()
	goto(-50,100)
	pendown()
	pencolor('#F3D139')
	pensize(25)
	for i in range(5):
		forward(100)
		right(144)

def deleteStar(screen):
	screen.tracer(0)
	for i in range(14):
		undo()
	update()

def updateTrialLabel(screen, nTrials):
	screen.tracer(0)
	penup()
	removeTrialLabel(screen)
	goto(325,300)
	write(nTrials+1, move=False, font=("Arial",36, "normal"))
	penup()

def erase(screen, c):
	#screen.tracer(1,10)
	#showturtle()
	screen.tracer(0)
	begin_fill()
	color(c, c)
	penup()
	goto(-350,270)
	pendown()
	seth(180)
	backward(700)
	right(90)
	backward(370)
	right(90)
	backward(350)
	left(90)
	backward(100)
	right(90)
	backward(350)
	right(90)
	backward(470)
	end_fill()
	penup()
	seth(0)
	color(COLOR, COLOR)
	drawUpperArm()
	update()
