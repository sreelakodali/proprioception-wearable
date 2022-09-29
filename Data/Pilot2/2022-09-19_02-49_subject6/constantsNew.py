# Constants for Sensory Substitution Devce 
# Written by: Sreela Kodali (kodali@stanford.edu) 

BAUD_RATE = 4608000
DATASRC_SD = False
TRANSFER_RAW = False

# Calibration
# ACTUATOR_FEEDBACK_MAX = 988
# ACTUATOR_FEEDBACK_MIN = 145
# ANGLE_DATA_MIN = 0
# ANGLE_DATA_MAX = 11600
# ZERO_FORCE = 0.00

# PILOT STUDY
# SHOW_ARM = True
# ANGLE_TOLERANCE = 12
# ANGLE_CONSECUTIVE = 15
#N_TOTAL_TRIALS = 60


RUNTIME_LENGTH_ARM = 1000 # seconds

# DATA Collection
PATH_SD =  '/Volumes/PIEZO2/'
PATH_LAPTOP = '/Users/Sreela/Documents/School/Stanford/Year3_2/PIEZO2/Data/Pilot2/'
#PATH_LAPTOP = '/Users/Sreela/Documents/School/Stanford/Year3_2/PIEZO2/Data/systemEvaluation/'
#PATH_LAPTOP = '/Users/Sreela/Documents/School/Stanford/Year3_2/PIEZO2/Data/timing/'
PORT_NAME = "/dev/cu.usbmodem71181201"
RUNTIME_LENGTH = 10 # seconds

## DATA PROCESSING CONSTANTS ##
ANGLE_MIN = 180
ANGLE_MAX = 40
ACTUATOR_POSITION_MIN = 4.0 # I should measure this
ACTUATOR_POSITION_MAX = 20.0
ACTUATOR_COMMAND_MIN = 46  
ACTUATOR_COMMAND_MAX = 139#130
N_CORR = 20000 # computing the delay

#2022-09-19_02-49_subject6
ACTUATOR_FEEDBACK_MAX = 807
ACTUATOR_FEEDBACK_MIN = 51
ZERO_FORCE = 124
ANGLE_DATA_MIN = 500
ANGLE_DATA_MAX = 12688

