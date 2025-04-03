import socket, sys, datetime, select, random
from collections import deque
import skBLESupport_JND as skB


def changeScalePolyfit(s):
	ls = 13.3 - 2.83* (s ** 1) + 0.264* (s ** 2) - 0.0108*(s ** 3) + 0.000106*(s ** 4);
	#ls = 13.309610778443160 -3.142974745776060* (s ** 1) + 0.329362743111748* (s ** 2) - 0.015300291353016*(s ** 3) + 0.0002598774881315157*(s ** 4);
	return ls


# the probability will progressively decrease with magnitude until
def simulatedSubjectResponse(a, b):
	diff = float(a)-float(b)
	pA=0
	pB=0
	pEqual=0

	if (abs(diff) > 1):
		pA = 1
		pEqual = 0
		if(diff < 0):
			pA = 1 - pA - pEqual

	elif (abs(diff) < 0.4):
		pEqual=0.4
		pA = 0.3

	elif (abs(diff) < 0.6):
		pEqual=0.3
		pA = 0.5
		if(diff < 0):
			pA = 1 - pA - pEqual

	elif (abs(diff) <= 1):
		pEqual = 0.15
		pA = 0.75
		if(diff < 0):
			pA = 1 - pA - pEqual

	pB = 1-pA-pEqual

	print("pA={}, pEqual={}, pB={}".format(pA, pEqual, pB))

	response = random.choices([1, 2, 3], weights=[pA, pEqual, pB])
	response = response[0]
	print("response={}".format(response))
	return response

# while (1):
# 	print("min?")
# 	A = float(input())
# 	print("max?")
# 	B = float(input())

# 	asr = (B - A)
# 	q1 = A + asr/4
# 	q2 = A + asr/2
# 	q3 = A + (3* asr/4)

# 	print("ASR={},  q1={}, q2={}, q3={}".format(asr, q1, q2, q3))

# 	print("ref?")
# 	C = float(input())
# 	Xo = skB.generateInitialValue(A, B, C);
# 	print("Xo={}".format(Xo))
# 	#print("scale is {}".format(changeScalePolyfit(float(setpoint))))

while (1):
	print("setpoint?")
	s = float(input())
	print("scale is {}".format(changeScalePolyfit(float(s))))


# comparisonValues = [10-3, 10-2, 10-1, 10, 10+1, 10+2, 10+3]
# experimentStimuli = []
# for j in comparisonValues:
# 	for i in range(0,10):
# 		experimentStimuli.append(j)
# random.shuffle(experimentStimuli)
# stack = deque(experimentStimuli)

# print(experimentStimuli)


# def sendMySetpoints():
#     data = "x2"
#     s = data.encode(encoding="ascii")
    
#     w = 0
#     endTime = datetime.datetime.now() + datetime.timedelta(seconds=10)
#     while (datetime.datetime.now() < endTime):
#         w = w + 1
#     return(s)

# keys = ['q1', 'q2']



# for k in keys:
# 	print(k)
# 	nUpCount = 0
# 	nDownCount = 0
# 	for l in list(range(0,6)):
# 		# skB.instructionsGUI(sc, tr)
# 		# skB.prepareExperimentGUI(sc)

# 		rUp = random.randrange(0,2)
# 		if (rUp):
# 			nUpCount = nUpCount + 1
# 		else:
# 			nDownCount = nDownCount + 1
	
# 		if ((rUp == 1) and (nUpCount > 3)) :
# 			rUp = 0
# 			nDownCount = nDownCount + 1
# 		if ((rUp == 0) and (nDownCount > 3)):
# 			rUp = 1
# 			nUpCount = nUpCount + 1

# 		print(rUp)
# 	print("nUpCount = " + str(nUpCount))
# 	print("nDownCount = " + str(nDownCount))


# actuatorOrder = [1,2]
# random.shuffle(actuatorOrder)

# for n in actuatorOrder:
# 	for k in keys:

# 		nUpCount = 0
# 		nDownCount = 0
# 		print(" ")
# 		for l in list(range(0,6)):
# 			# skB.instructionsGUI(sc, tr)
# 			# skB.prepareExperimentGUI(sc)

# 			rUp = random.randrange(0,2)
# 			if (rUp):
# 				nUpCount = nUpCount + 1
# 			else:
# 				nDownCount = nDownCount + 1

# 			if ((rUp == 1) and (nUpCount > 3)) :
# 				rUp = 0
# 				nDownCount = nDownCount + 1
# 			elif ((rUp == 0) and (nDownCount > 3)):
# 				rUp = 1
# 				nUpCount = nUpCount + 1
# 			#print ("this is staircase" + str(k))
# 			print("actuator#= {}, increasing= {}, quartile={}, trial#={}".format(n, rUp, k, l))

# actuatorOrder = [1,2]
# random.shuffle(actuatorOrder)

# for n in actuatorOrder:
# 	for k in keys:
		
# 		rUpStack = deque()
# 		rUpArr = [0, 0, 0, 1, 1, 1]
# 		random.shuffle(rUpArr)
# 		for r in rUpArr:
# 			rUpStack.append(r)
# 		print(" ")
# 		for l in list(range(0,6)):
# 			# skB.instructionsGUI(sc, tr)
# 			# skB.prepareExperimentGUI(sc)
# 			rUp = rUpStack.pop()
# 			#print ("this is staircase" + str(k))
# 			print("actuator#= {}, increasing= {}, quartile={}, trial#={}".format(n, rUp, k, l))



# 			#await staircaseNewBLE(c, n, rUp, avgMin, avgMax, k, quartiles[k], waitTime, 0.0, client1, rx_char1, client2, rx_char2)
# # data = range(0,10)

# # for i in data:
# # 	s = str(i) + "\n" #.encode(encoding="ascii")
# # 	sys.stdout.write(s)
# # 	w = 0
# # 	endTime = datetime.datetime.now() + datetime.timedelta(seconds=2)
# # 	while (datetime.datetime.now() < endTime):
# # 		w = w + 1


# # while(1):
# # 	# data = input()
# # 	# #data = "sent: " + data + "\n"
# # 	# sys.stdout.write(data)

# # 	data = sys.stdin.buffer.readline()
# # 	data = "B: " + data.decode("ascii")
# # 	#data = "sent: " + data + "\n"
# # 	sys.stdout.write(data)