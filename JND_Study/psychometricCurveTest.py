import numpy as np

import matplotlib   #FIX: fix for newer python environment
matplotlib.use("TkAgg")
from matplotlib import pyplot as plt
from fit_psyche.psychometric_curve import PsychometricCurve

# x = np.linspace(start=12, stop=16, num=6)
# y = (x > x.mean()).astype(float)
# y[2] = y[2] + np.abs(np.random.rand())
# y[3] = y[3] - np.abs(np.random.rand())

x = [0.75, 0,5, 0.25]
y = [0.9, 0.7, 0.5]

pc = PsychometricCurve(model='logit').fit(x, y)
pc.plot(x, y)
print(pc.score(x, y))
print(pc.coefs_)

#plt.scatter(x,y)
plt.show()

# fig, ax1 = plt.subplots()
# # plt.suptitle("Real-time Data " + fileName, name='Arial', weight='bold')
# # ax1.set_xlabel("Time (s)", name='Arial')
# # plt.xticks(name='Arial')
# # plt.yticks(name='Arial')

# # ax1.set_ylabel("Force (N)", name='Arial',)
# # #ax1.scatter(time, force)
# l1 = ax1.plot(x, y, 'r', linewidth=1.75)
# # ax1.yaxis.label.set_color('r')
# # ax1.tick_params(axis='y', color='r')
# # #ax1.set_ylim(-2,10)
# # #ax1.set_ylim(0,2)

# # plt.grid(True)
# # #ax1.legend(l_all, labels, loc=0)
# # if s==1: plt.savefig(p +"fig_"+fileName)
# plt.show()