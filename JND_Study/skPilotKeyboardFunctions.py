# Pilot Keyboard Support functions
# Written by: Sreela Kodali (kodali@stanford.edu)
import skFunctions as sk
import csv

def writeOutData(i,dataFunc, writer2, writer, trialCount):
	i = str(i, "utf-8").split(",")
	if (len(i) == 8): # hardcoded, length of packet from device
		raw = [j.rstrip() for j in i]
		raw = raw + [trialCount]
		writer2.writerow(raw)

		newRow = sk.processNewRow(dataFunc, i)	
		newRow = newRow + [trialCount]
		writer.writerow(newRow)	
		print(newRow)


def writeOutData2(i,dataFunc, writer2, writer, trialCount, verbose):
	i = str(i, "utf-8").split(",")
	if (len(i) == 8): # hardcoded, length of packet from device
		raw = [j.rstrip() for j in i]
		raw = raw + [trialCount]
		writer2.writerow(raw)

		newRow = sk.processNewRow(dataFunc, i)	
		newRow = newRow + [trialCount]
		writer.writerow(newRow)
		if (verbose):
			print(newRow)

def writeOutDataBLE(i,dataFunc, writer, trialCount, verbose):
	i = str(i, "utf-8").split(",")
	if (len(i) == len(dataFunc)): 
		# raw = [j.rstrip() for j in i]
		# raw = raw + [trialCount]	
		#writer2.writerow(raw)

		newRow = sk.processNewRow(dataFunc, i)	
		newRow = newRow + [trialCount]
		writer.writerow(newRow)
		if (verbose):
			print(newRow)

def formatBLEPacket(value, nAct):
	if (nAct == 1):
		buf = str("x")+str(value) 
	else:
		buf = str("y")+str(value)
	return buf.encode()

# default: staircase(120, 80, -5, 5, 47, 1, 3, 15)
def staircaseBLE(start, reference, stepDown, stepUp, wait, retract, nUp, nDown, N_Trials, nAct):
	# start = 120 # actuator pwm unit
	# reference = 80# 6 N
	# inc = -5 # start increment
	# wait = 5
	# retract = 47

	packetA = 0
	packetB = 0
	rightStreak = 0
	answerKey = 0
	userAnswer = 0
	test = 0
	trialCount = 0 # counter
	wrongCount = 0
	# stepType

	# start Value for method of limits
	test = start

	for i in range(0,N_Trials):

		# ---- READ AND PRINT/SAVE DATA
		# value = mcu.readlines()
		# for j in value:
		# 	#skP.writeOutData(j,dataFunc, 0, 0, trialCount)
		# 	skP.writeOutData(j,dataFunc, writer2, writer, trialCount)

		print("----- TRIAL #" + str(i) + " -----")
		print("test: " + str(test))
		print("rightStreak: " + str(rightStreak))

		# randomize order presented
		r = random.randrange(0,2)
		print("r: " + str(r))
		if (r == 1):
			packetA = reference #A will be reference
			packetB = test #B will be test target
		else:
			packetA = test #A will be test target
			packetB = reference #B will be reference
		
		w = 0

		# apply stimuli
		print("Receiving Stimulus A: " + str(packetA))
		skG.writeText(sc, -350, 230, "Stimulus A in progress", skG.COLOR)

		# Send poke A
		await client1.write_gatt_char(rx_char1, formatBLEPacket(packetA,1)) 
		if (nAct == 2):
	        await client2.write_gatt_char(rx_char2, formatBLEPacket(packetA,2))
		
        # hold the poke
		endTime = datetime.datetime.now() + datetime.timedelta(seconds=wait)
		while (datetime.datetime.now() < endTime):
			w = w + 1
		#time.sleep(wait) 
	
		# then retract
		await client1.write_gatt_char(rx_char1, formatBLEPacket(retract,1)) 
		if (nAct == 2):
        	await client2.write_gatt_char(rx_char2, formatBLEPacket(retract,2))
		
		# wait
		endTime = datetime.datetime.now() + datetime.timedelta(seconds=wait/2)
		while (datetime.datetime.now() < endTime):
			w = w + 1
		#time.sleep(wait) # wait

		# apply stimuli
		print("Receiving Stimulus B: " + str(packetB))
		skG.writeText(sc, -350, 180, "Stimulus B in progress", skG.COLOR)
		
		# Send poke B
        await client1.write_gatt_char(rx_char1, formatBLEPacket(packetB,1))
        if (nAct == 2):
        	await client2.write_gatt_char(rx_char2, formatBLEPacket(packetB,2))

         # hold the poke
		endTime = datetime.datetime.now() + datetime.timedelta(seconds=wait)
		while (datetime.datetime.now() < endTime):
			w = w + 1
		#time.sleep(wait)

		# then retract
		await client1.write_gatt_char(rx_char1, formatBLEPacket(retract,1))
		if (nAct == 2):
        	await client2.write_gatt_char(rx_char2, formatBLEPacket(retract,2))

        # wait
		endTime = datetime.datetime.now() + datetime.timedelta(seconds=wait/2)
		while (datetime.datetime.now() < endTime):
			w = w + 1
		#time.sleep(wait/2) # wait

		# find the real answer
		# 1 means A > B, 2 means A == B, 3 means A < B
		answerKey = (packetA > packetB)*1 + (packetA == packetB)*2 + (packetA < packetB)*3
		print("The real answer is: " + str(answerKey))

		skG.writeText(sc, -350,80, "Select your answer:", skG.COLOR)
		skG.writeText(sc, -350,30, "A > B             A == B             A < B ", skG.COLOR_RED)
		skG.writeText(sc, -350,-120, "Press the red key to confirm your answer", skG.COLOR)
		skG.writeText(sc, -350,-170, "and proceed to the next trial.", skG.COLOR_GREEN)

		while(1):

		# wait for user's input
			k = keyboard.read_key()

			if k == 'page up':
				userAnswer = 1
				skG.eraseLine(sc,-350,40)
				skG.writeText(sc, -350,30, "(A > B)           A == B             A < B ", skG.COLOR_RED)
			elif k == 'right':
				userAnswer = 2
				skG.eraseLine(sc,-350,40)
				skG.writeText(sc, -350,30, "A > B            (A == B)            A < B ", skG.COLOR_RED)
			elif k == 'page down':
				userAnswer = 3
				skG.eraseLine(sc,-350,40)
				skG.writeText(sc, -350,30, "A > B             A == B            (A < B)", skG.COLOR_RED)

			elif k == 'down':

				if (userAnswer == 0):
					skG.writeText(sc, -350,-20, "You have to choose an answer to proceed.", skG.COLOR)					
				else:
					skG.eraseLine(sc,-350,40)
					skG.erase(sc, 'white')
					#skG.eraseLine(sc,-350,-20)
					trialCount = trialCount + 1
					if trialCount < N_Trials:
						skG.updateTrialLabel(sc, trialCount)
						skG.delay(sc, t)

					break


		# check the answer. depending on answer, determine next test value
		# if answer wrong, reset streak and step up test value
		print("User answer is: " + str(userAnswer))

		if (answerKey != userAnswer):
			print("ANSWER WRONG!")
			rightStreak = 0
			test = test + round(stepUp) # step up test value if wrong
			writer3.writerow([trialCount, test, reference, packetA, packetB, answerKey, userAnswer, stepUp, rightStreak])
			print("stepSize: " + str(stepUp))
			# inc = abs(inc) + 1 
			userAnswer = 0
			wrongCount = wrongCount + 1
			print("reversals:" + str(wrongCount))
			# if (wrongCount == 2):
			# 	stepSize = stepSize2

		# if answer correct, add to right streak
		elif (answerKey == userAnswer):
			print("ANSWER RIGHT!")
			rightStreak = rightStreak + 1
			userAnswer = 0
			
			# step down test if they get 3 right answers in a row
			if ((rightStreak == nDown) or (wrongCount == 0)):
				test = test - stepDown
				writer3.writerow([trialCount, test, reference, packetA, packetB, answerKey, userAnswer, stepDown, rightStreak])
				# inc = (abs(inc) - 1)*-1
				rightStreak = 0
			else:
				writer3.writerow([trialCount, test, reference, packetA, packetB, answerKey, userAnswer, 0, rightStreak])
	
	# value = mcu.readlines()
	# for j in value:
	# 	#skP.writeOutData(j,dataFunc, 0, 0, trialCount)
	# 	skP.writeOutData(j,dataFunc, writer2, writer, trialCount)	
	# 	# # and compute test value
	# 	# test = test + inc