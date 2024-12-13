import subprocess, sys, datetime, socket, turtle, keyboard, time, asyncio
import skPilotGraphics as skG
import skPilotGraphics as skG
import skCalibrationFunctions as skC
import skBLESupport_JND as skB
EXPERIMENT_TEXT_0 = ["Welcome!", "Let's begin the experiment", "", "", "", "", "", "", "", "", "", "", "Please click the red key to continue."]
#CALIBRATION_TEXT_MAX_PRESSURE = ["Calibration: Max Pressure", "Please wear the device. The actuator will extend", "into your arm and apply pressure. When you first", "feel the device, click the screen. The device will", "pause and then continue to extend. When it is too", "uncomfortable, click on the screen and the", "actuator will retract. We'll do this at least 3 times.", "Click CALIBRATE to begin each round and", "DONE once you've completed at least 3 rounds.", "Calibrate", "Done"]


def loadASRValues():
  paramNames = ['Min1', 'Max1', 'Min2', 'Max2', 'Min3', 'Max3']
  param = [0.0] * len(paramNames)
  for i in range(0,len(paramNames)):
    print(paramNames[i] + "?")
    p = float(input())
    param[i] = p

  # compute average min
  avgMin = (param[0] + param[2] + param[4]) / 3.0
  avgMax = (param[1] + param[3] + param[5]) / 3.0
  rangeASR = avgMax - avgMin

  q1 = avgMin + rangeASR/4.0
  q2 = rangeASR/2.0 + avgMin
  q3 = avgMax - rangeASR/4.0

  return [avgMin, avgMax, q1, q2, q3]

# a, b, c, d, e = loadASRValues()
# print(str(a) + "," + str(b) + "," + str(c) + "," + str(d) + "," + str(e))


async def main():
  t = 1
  sc = turtle.Screen()
  tr = skB.initializeGUI(sc) # initialize GUI
  await skB.waitGUI(sc)

  # calibration min max force
  skB.calibrationMinMaxGUI(sc, tr)
  skG.initializeCalibrationWindow(sc, skB.CALIBRATION_TEXT3)

  await skB.waitSK(20)
  skB.instructionsGUI(sc, tr) # GUI for instructions


asyncio.run(main())


# server
# next create a socket object 
  
# calibrate = True
# def on_click(x, y):
#   global calibrate

#   if (calibrate):
#     if ((x < -190) and (x > -355) and (y > -250) and (y < -195)):
#       # send start BLE command to device 
#       await client1.write_gatt_char(rx_char1, ("c\n").encode(encoding="ascii"), response=False) 
      
#     # Done button
#     elif((x < 280) and (x > 117) and (y > -250) and (y < -195)):
#       # send 'done' BLE command to device
#       await client1.write_gatt_char(rx_char1, ("d\n").encode(encoding="ascii"), response=False)
#       calibrate = False

#     else:
#       # send 'screenclick' ble signal to device
#       await client1.write_gatt_char(rx_char1, ("z\n").encode(encoding="ascii"), response=False)

# sc = turtle.Screen()
# turtle.onscreenclick(on_click)
# skG.initializeCalibrationWindow(sc, CALIBRATION_TEXT_MAX_PRESSURE)
# skG.buttons(sc)
# # sc.tracer(0)
# # sc.title("Calibration")
# while (click != 3):
#   turtle.update()
#   time.sleep(.2)

#keyboard.wait('down')


# print ("Socket successfully created")
# s = socket.socket()
# port = 12344
# s.bind(('', port))
# s.listen(2) 
# c, addr = s.accept() 

# print ("socket binded to %s" %(port)) 
# print ('Got connection from', addr )
 
# endTime = datetime.datetime.now() + datetime.timedelta(seconds=10)
# while (datetime.datetime.now() < endTime):
 
#   data = input()
#   c.send(data.encode()) 
 
# c.close()















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