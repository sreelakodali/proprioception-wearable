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
PORT_NAME = "/dev/cu.usbmodem71181201"

## DATA PROCESSING CONSTANTS ##
ANGLE_MIN = 180
ANGLE_MAX = 40
ACTUATOR_POSITION_MIN = 4.0 # I should measure this
ACTUATOR_POSITION_MAX = 20.0
ACTUATOR_COMMAND_MIN = 46  
ACTUATOR_COMMAND_MAX = 139#130

# RUNTIME_LENGTH_ARM = 1000 # seconds #only for serialAngleArm.py
# RUNTIME_LENGTH = 10 # seconds #for readProcessSerial.py
# N_CORR = 20000 # computing the delay in processPlotData.py

# ## DEFAULT CALIBRATION VALUES ##
# ACTUATOR_FEEDBACK_MAX = 988
# ACTUATOR_FEEDBACK_MIN = 145
# ANGLE_DATA_MIN = 0
# ANGLE_DATA_MAX = 11600
# ZERO_FORCE = 0.00#2022-11-10_22-12_subjecttestagain
