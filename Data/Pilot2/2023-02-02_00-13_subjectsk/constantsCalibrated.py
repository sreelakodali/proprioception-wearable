# Constants for Sensory Substitution Devce 
# Written by: Sreela Kodali (kodali@stanford.edu) 

BAUD_RATE = 4608000
DATASRC_SD = False # Where to save data, on SD card if true. Else on laptop
TRANSFER_RAW = False # save raw values if true. else process values with processing constants and calibration

## SYSTEM DIRECTORY PATHS ##
PATH_SD =  '/Volumes/PIEZO2/'
PATH_HOME = '/Users/Sreela/Documents/School/Stanford/Year3_2/PIEZO2/'
PATH_LAPTOP = PATH_HOME + 'Data/Pilot2/'
#PATH_LAPTOP = '/Users/Sreela/Documents/School/Stanford/Year3_2/PIEZO2/Data/systemEvaluation/'
#PATH_LAPTOP = '/Users/Sreela/Documents/School/Stanford/Year3_2/PIEZO2/Data/timing/'
PORT_NAME = "/dev/cu.usbmodem43098001"#"/dev/cu.usbmodem71181201"

## DATA PROCESSING CONSTANTS ##
ANGLE_MIN = 180
ANGLE_MAX = 40 # 0 for FLEX_SENSOR
ACTUATOR_POSITION_MIN = 0.0 # I should measure this
ACTUATOR_POSITION_MAX = 20.0
ACTUATOR_COMMAND_MIN = 47  
ACTUATOR_COMMAND_MAX = 139#130

# RUNTIME_LENGTH_ARM = 1000 # seconds #only for serialAngleArm.py
# RUNTIME_LENGTH = 10 # seconds #for readProcessSerial.py
# N_CORR = 20000 # computing the delay in processPlotData.py


# ## DEFAULT CALIBRATION VALUES ##
ANGLE_DATA_MIN = 40	# when using keyboard
ANGLE_DATA_MAX = 180
# ANGLE_DATA_MIN = 0   # when reading raw flex values
# ANGLE_DATA_MAX = 11600
# ANGLE_DATA_MIN = -25.48 # when calibrating flex sensor
# ANGLE_DATA_MAX = 95.24

# ACTUATOR_FEEDBACK_MAX = 988
# ACTUATOR_FEEDBACK_MIN = 145
# ZERO_FORCE = 0.00#2023-02-02_00-13_subjectsk
ACTUATOR_FEEDBACK_MAX = 979
ACTUATOR_FEEDBACK_MIN = 50
ZERO_FORCE = 255
USER_MIN_FORCE_DATA = 255
USER_MAX_FORCE_DATA = 255
USER_MIN_ACTUATOR_COMMAND = 84
USER_MAX_ACTUATOR_COMMAND = 107
USER_MIN_ACTUATOR_AVG = 84
USER_MAX_ACTUATOR_AVG = 107
