# Plotting Serial Data from Sensory Substitution Device
# Written by: Sreela Kodali (kodali@stanford.edu) 

import sys, getopt
import pandas as pd
import constants as CONST
import skFunctions as sk

def main(argv):
	inputfile = ''
	try:
		opts, args = getopt.getopt(argv,"hi:",["ifile="])
	except getopt.GetoptError:
		print('plot.py -i <inputfile>')
		sys.exit(2)
	
	for opt, arg in opts:
		if opt == '-h':
			print('plot.py -i <inputfile>')
			sys.exit()
		elif opt in ("-i", "--ifile"):
			p = arg


	data = pd.read_csv(CONST.PATH_LAPTOP + p + '/processed_' + p + '.csv', delimiter = ",").astype(float)
	time = data['time'].tolist()
	angle = data['flex sensor'].tolist() # angle
	device1_positionCommand = data['actuator position, command'].tolist()
	device1_positionMeasured = data['actuator position, measured'].tolist()
	force  = data['force'].tolist()

	sk.plot_System(0, p, p, time, angle, force, device1_positionMeasured, device1_positionCommand)



if __name__ == "__main__":
	main(sys.argv[1:])