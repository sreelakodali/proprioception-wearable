import subprocess, sys, datetime, socket

# server
# next create a socket object 
         
print ("Socket successfully created")


s = socket.socket()
port = 12345
s.bind(('', port))
s.listen(2) 
c, addr = s.accept() 

print ("socket binded to %s" %(port)) 
print ('Got connection from', addr )

# put the socket into listening mode 
    
print ("socket is listening")            

    
print ('Got connection from', addr )

 
# a forever loop until we interrupt it or 
# an error occurs 


endTime = datetime.datetime.now() + datetime.timedelta(seconds=10)
while (datetime.datetime.now() < endTime):
 
# Establish connection with client. 

  data = input()

  # send a thank you message to the client. encoding to send byte type. 
  c.send(data.encode()) 
 

c.close()















# # sender = subprocess.Popen(["python", "testB.py"], stdout=subprocess.PIPE, text=True)
# # receiver = subprocess.Popen(["python", "testA.py"], stdin=sender.stdout, stdout=sys.stdout, text=True)

# #Bprocess = subprocess.Popen(["python", "testB.py"], stdout=subprocess.PIPE, text=True)

# def waitSK(td):
# 	w = 0
# 	endTime = datetime.datetime.now() + datetime.timedelta(seconds=td)
# 	while (datetime.datetime.now() < endTime):
# 		w = w + 1

# Aprocess = subprocess.Popen(["python", "bleCentralJND_Adafruit1.py"], stdin=subprocess.PIPE, stdout=sys.stdout, text=True)



# # bleProcess = subprocess.Popen(["python", "testA.py"], stdin=sys.stdout, text=True)

# data = range(0,10)
# for i in data:
# 	s = "x" + str(i) + "\n"# +  #.encode(encoding="ascii")
# 	print(s)
# 	Aprocess.stdin.write(s)
# 	#out, _ = Aprocess.sendsignal()
# 	#print(out)
# 	waitSK(10)


# #bleProcess = subprocess.Popen(["python", "testA.py"], stdin=sys.stdin, text=True)
# # process2 = subprocess.Popen(["python", "testB.py"], stdin=bleProcess.stdout, text=True)

# # while(1):
# # 	sender.communicate()
# # 	out, _ = receiver.communicate()
# # 	print(out.decode("ascii").strip())
# # print(error)

# # while(1):
# # 	data = input()
# # 	out, _ = bleProcess.communicate()
# # 	print(out.decode("ascii").strip())

# # output, error = process2.communicate()

# # print(output)
# # print(error)