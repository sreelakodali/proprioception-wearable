# FFT on sensor data
# Written by: Sreela Kodali (kodali@stanford.edu) 

from scipy.fft import fft, ifft, fftfreq

import sys, getopt
import pandas as pd
import constants as CONST
import skFunctions as sk
import numpy as np


# identify the data
def main(argv):
	inputfile = ''
	try:
		opts, args = getopt.getopt(argv,"hi:",["ifile="])
	except getopt.GetoptError:
		print('sensorNoiseAnalysis.py -i <inputfile>')
		sys.exit(2)
	
	for opt, arg in opts:
		if opt == '-h':
			print('sensorNoiseAnalysis.py -i <inputfile>')
			sys.exit()
		elif opt in ("-i", "--ifile"):
			p = arg


	data = pd.read_csv(CONST.PATH_LAPTOP + p + '/processed_' + p + '.csv', delimiter = ",").astype(float)
	# time = data['time'].tolist()
	# angle = data['flex sensor'].tolist() # angle
	# device1_positionCommand = data['actuator position, command'].tolist()
	# device1_positionMeasured = data['actuator position, measured'].tolist()
	# force  = data['force'].tolist()

	t_d = data['td'].tolist()
	time = data['time'].tolist()
	angle = data['flex sensor'].tolist() # angle

	unique = np.unique(np.array(t_d))

	idx_td = []
	noise = []
	fs = []
	for x in unique:
		idx_list = [idx for idx, val in enumerate(t_d) if val == x]
		idx_td.append(min(idx_list))

	idx_td.append(len(t_d)-1)
	# #print(angle)

	#sk.plot_Angle(0, p, p, time, angle)

	for i in range((len(idx_td))-1):
		t_dSplit = t_d[idx_td[i]:idx_td[i+1]]
		timeSplit = time[idx_td[i]:idx_td[i+1]]
		angleSplit = angle[idx_td[i]:idx_td[i+1]]

		N = len(angleSplit)
		timeLength = (timeSplit[-1]-timeSplit[0])*1e-6

		# print(N)
		# print(timeLength)
		print(N/timeLength)
		fs.append(N/timeLength)
		print(1000*timeLength/N)

		yF = fft(angleSplit)
		xF = fftfreq(N,(timeLength/N))
		noise.append(max(xF))

		# #print(np.abs(angleF))
		#sk.plot_Angle(1, p, p, timeSplit, angleSplit)
		# #sk.plot_System(0, p, p, time, angle, force, device1_positionMeasured, device1_positionCommand)
		#sk.plot_Noise(1, p, p, xF, np.abs(yF))
		# #sk.plot_Noise(0, p, p, xF, 2.0/N * np.abs(yf[0:N//2])

	# print(unique)
	# print(noise)
	sk.plot_Noise(1, p, p, unique, noise)
if __name__ == "__main__":
	main(sys.argv[1:])