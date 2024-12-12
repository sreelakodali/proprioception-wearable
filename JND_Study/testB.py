import socket, sys, datetime, select

# def sendMySetpoints():
#     data = "x2"
#     s = data.encode(encoding="ascii")
    
#     w = 0
#     endTime = datetime.datetime.now() + datetime.timedelta(seconds=10)
#     while (datetime.datetime.now() < endTime):
#         w = w + 1
#     return(s)



s = socket.socket()       
	 
# Define the port on which you want to connect 
port = 12344            
IPAddr = '10.34.86.113'#stanford  #'10.36.81.32' #eduroam   # kuppa #'10.0.0.64'
# connect to the server on local computer 
s.connect((IPAddr, port)) 
	 
while(1):

# receive data from the server and decoding to get the string.
	data = s.recv(1024).decode()
	if (data):
		print("Received:" + data)


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