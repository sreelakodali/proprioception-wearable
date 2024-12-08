import sys, datetime

# def sendMySetpoints():
#     data = "x2"
#     s = data.encode(encoding="ascii")
    
#     w = 0
#     endTime = datetime.datetime.now() + datetime.timedelta(seconds=10)
#     while (datetime.datetime.now() < endTime):
#         w = w + 1
#     return(s)

data = range(0,10)

for i in data:
	s = str(i) + "\n" #.encode(encoding="ascii")
	sys.stdout.write(s)
	w = 0
	endTime = datetime.datetime.now() + datetime.timedelta(seconds=2)
	while (datetime.datetime.now() < endTime):
		w = w + 1


# while(1):
# 	# data = input()
# 	# #data = "sent: " + data + "\n"
# 	# sys.stdout.write(data)

# 	data = sys.stdin.buffer.readline()
# 	data = "B: " + data.decode("ascii")
# 	#data = "sent: " + data + "\n"
# 	sys.stdout.write(data)