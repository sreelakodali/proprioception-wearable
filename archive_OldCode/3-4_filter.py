# Filtering & Plotting Noisy Resistive Flex Sensor Data
# Written by: Sreela Kodali (kodali@stanford.edu) 

import numpy as np
from numpy import sin, cos, pi, linspace
from numpy.random import randn
from scipy.signal import lfilter, lfilter_zi, filtfilt, butter
from matplotlib.pyplot import plot, legend, show, hold, grid, figure, savefig
import csv

with open('3-3_data.csv') as csv_file:
	originalData = np.loadtxt(csv_file, delimiter=",")

time = originalData[:,0]
angle = originalData[:,2]
actuatorPosition = originalData[:,4]
force = originalData[:,5]

# # Create an order 3 lowpass butterworth filter.
b, a = butter(3, 0.1)


# Use filtfilt to apply the filter.
filteredAngle = filtfilt(b, a, angle)
filteredActuatorPosition = filtfilt(b, a, actuatorPosition)
filteredForce = filtfilt(b, a, force)

np.savetxt('filteredAngle_v2.csv', filteredAngle, delimiter=',')
np.savetxt('filteredActuatorPosition_v2.csv', filteredActuatorPosition, delimiter=',')
np.savetxt('filteredForce_v2.csv', filteredForce, delimiter=',')

# Make the plot.
figure(figsize=(10,5))
hold(True)
# plot(time, force, 'b', linewidth=1.75, alpha=0.75)
plot(time, filteredAngle, 'b', linewidth=1.75)
plot(time, filteredActuatorPosition, 'r', linewidth=1.75)
plot(time, filteredForce, 'g', linewidth=1.75)
# legend(('noisy signal',
#         # 'lfilter, once',
#         # 'lfilter, twice',
#         'filtfilt'),
#         loc='best')
hold(False)
grid(True)
show()