import socket, sys, datetime, select, random

# def sendMySetpoints():
#     data = "x2"
#     s = data.encode(encoding="ascii")
    
#     w = 0
#     endTime = datetime.datetime.now() + datetime.timedelta(seconds=10)
#     while (datetime.datetime.now() < endTime):
#         w = w + 1
#     return(s)

keys = ['q1', 'q2']

nUpCount = 0
nDownCount = 0
for k in keys:
	for l in list(range(0,6)):
		# skB.instructionsGUI(sc, tr)
		# skB.prepareExperimentGUI(sc)

		rUp = random.randrange(0,2)
		if (rUp):
			nUpCount = nUpCount + 1
		else:
			nDownCount = nDownCount + 1
	
		if ((rUp == 1) and (nUpCount == 3)) :
			rUp = 0
		if ((rUp == 0) and (nDownCount == 3)):
			rUp = 1

		print(rUp)

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