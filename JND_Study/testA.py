import sys, socket, os
# import datetime
# import shutil
# import numpy as np
# import pandas as pd
# #from scipy import signal # import lfilter, lfilter_zi, filtfilt, butter
# # from scipy.signal import lfilter, lfilter_zi, filtfilt, butter
# from operator import itemgetter
import skFunctions as sk

PATH = '/Users/Sreela/Documents/School/Stanford/Year3_2/PIEZO2/JND_Study/bleData/' # change this to your path!

allSubdirs = [PATH+d for d in os.listdir(PATH) if os.path.isdir(os.path.join(PATH, d))]
#print(allSubdirs)
p = max(allSubdirs, key=sk.getCreationTime) + '/'

print("Newest folder found: %s" % p)
print("Is that correct?")
response = input()

if response in ["yes", "y", "Y", "YES"]:

	f = open(p + 'staircasingData.csv', 'w+', encoding='UTF8', newline='')
	print("Let's create a socket and get started.")
	# Create a socket object 
	s = socket.socket()         
	 
	# Define the port on which you want to connect 
	port = 12345            
	IPAddr = '10.0.0.64'# kuppa ##'10.34.86.113'#stanford  #'10.36.81.32' #eduroam   
	# connect to the server on local computer 
	s.connect((IPAddr, port)) 
	 
	while(1):

	# receive data from the server and decoding to get the string.
		data = s.recv(1024).decode()
		if (data):
			print(data)
			f.write(data)
			if (data == "DONE\n"):
				break
		# print (s.recv(1024).decode())
	# close the connection 
	s.close()  
	f.close()
else:
	print("Sorry, please check for problem.")
# while(1):
# 	data = sys.stdin.buffer.readline()
# 	if data:
# 		data = "A: " + data.decode("ascii")
# 		#data = "sent: " + data + "\n"
# 		sys.stdout.write(data)