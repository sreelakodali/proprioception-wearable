# Pilot Study
# Written by: Sreela Kodali (kodali@stanford.edu) 

from turtle import *

COLOR = '#51A0DC'
ELBOW_SIZE = 100
PEN_SIZE = 50
ARM_LENGTH = 300
HAND_SIZE = 120

def setForearm(screen, angle, time):
	drawForearm(screen, angle)
	delay(screen, time)
	#deleteForearm(screen)
	penup()

def drawUpperArm():
	goto(0,0)
	penup()
	goto(ARM_LENGTH,-(ARM_LENGTH)/2)
	pendown()
	backward(ARM_LENGTH)
	dot(ELBOW_SIZE)
	right(180)
	update()

def drawForearm(screen, angle):
	screen.tracer(0)
	goto(0, -(ARM_LENGTH)/2)
	seth(180)
	pendown()
	left(angle)
	backward(ARM_LENGTH)
	dot(HAND_SIZE)
	update()

def deleteForearm(screen):
	screen.tracer(0)
	undo() # angle
	undo() # dot
	undo() #backward arm length
	undo() # ?
	undo() #backward arm length
	undo() # ?
	undo() # ?
	update()

def delay(screen, time):
	screen.tracer(1,time)
	goto(0, -(ARM_LENGTH)/2)
	dot(ELBOW_SIZE)
	update()

def removeTrialLabel():
	penup()
	goto(345,320)
	dot(50, 'white')
	goto(325,300)

def initialize():
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
	
def buffer():
	penup()
	goto(0,-250)
	dot(50, 'blue')
	dot(50, 'blue')
	dot(50, 'blue')
	dot(50, 'blue')
	dot(50, 'blue')
	dot(50, 'blue')
	dot(50, 'blue')
	penup()

def star():
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
