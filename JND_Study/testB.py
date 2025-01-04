import socket, sys, datetime, select, random
from collections import deque

# def sendMySetpoints():
#     data = "x2"
#     s = data.encode(encoding="ascii")
    
#     w = 0
#     endTime = datetime.datetime.now() + datetime.timedelta(seconds=10)
#     while (datetime.datetime.now() < endTime):
#         w = w + 1
#     return(s)

keys = ['q1', 'q2']


for k in keys:
	print(k)
	nUpCount = 0
	nDownCount = 0
	for l in list(range(0,6)):
		# skB.instructionsGUI(sc, tr)
		# skB.prepareExperimentGUI(sc)

		rUp = random.randrange(0,2)
		if (rUp):
			nUpCount = nUpCount + 1
		else:
			nDownCount = nDownCount + 1
	
		if ((rUp == 1) and (nUpCount > 3)) :
			rUp = 0
			nDownCount = nDownCount + 1
		if ((rUp == 0) and (nDownCount > 3)):
			rUp = 1
			nUpCount = nUpCount + 1

		print(rUp)
	print("nUpCount = " + str(nUpCount))
	print("nDownCount = " + str(nDownCount))


actuatorOrder = [1,2]
random.shuffle(actuatorOrder)

for n in actuatorOrder:
	for k in keys:

		nUpCount = 0
		nDownCount = 0
		print(" ")
		for l in list(range(0,6)):
			# skB.instructionsGUI(sc, tr)
			# skB.prepareExperimentGUI(sc)

			rUp = random.randrange(0,2)
			if (rUp):
				nUpCount = nUpCount + 1
			else:
				nDownCount = nDownCount + 1

			if ((rUp == 1) and (nUpCount > 3)) :
				rUp = 0
				nDownCount = nDownCount + 1
			elif ((rUp == 0) and (nDownCount > 3)):
				rUp = 1
				nUpCount = nUpCount + 1
			#print ("this is staircase" + str(k))
			print("actuator#= {}, increasing= {}, quartile={}, trial#={}".format(n, rUp, k, l))

actuatorOrder = [1,2]
random.shuffle(actuatorOrder)

for n in actuatorOrder:
	for k in keys:
		
		rUpStack = deque()
		rUpArr = [0, 0, 0, 1, 1, 1]
		random.shuffle(rUpArr)
		for r in rUpArr:
			rUpStack.append(r)
		print(" ")
		for l in list(range(0,6)):
			# skB.instructionsGUI(sc, tr)
			# skB.prepareExperimentGUI(sc)
			rUp = rUpStack.pop()
			#print ("this is staircase" + str(k))
			print("actuator#= {}, increasing= {}, quartile={}, trial#={}".format(n, rUp, k, l))



			#await staircaseNewBLE(c, n, rUp, avgMin, avgMax, k, quartiles[k], waitTime, 0.0, client1, rx_char1, client2, rx_char2)
# data = range(0,10)

# for i in data:
# 	s = str(i) + "\n" #.encode(encoding="ascii")
# 	sys.stdout.write(s)
# 	w = 0
# 	endTime = datetime.datetime.now() + datetime.timedelta(seconds=2)
# 	while (datetime.datetime.now() < endTime):
# 		w = w + 1


# while(1):
# 	# data = input()
# 	# #data = "sent: " + data + "\n"
# 	# sys.stdout.write(data)

# 	data = sys.stdin.buffer.readline()
# 	data = "B: " + data.decode("ascii")
# 	#data = "sent: " + data + "\n"
# 	sys.stdout.write(data)