# actuator command to force mapping
# Written by: Sreela Kodali (kodali@stanford.edu) 

import csv, os, datetime, sys, getopt, shutil
import numpy as np
import pandas as pd
from sklearn.metrics import r2_score
import constants as CONST
import skFunctions as sk
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
import matplotlib
matplotlib.use("TkAgg")
from matplotlib import pyplot as plt

#import file

#p = input()
p = "2024-01-30_20-13_subjectsk813pm"
p = p + "/"
for f in os.listdir(CONST.PATH_LAPTOP + p):
	if f.startswith('maxForce') and f.endswith('.csv'):
		
		# if you need to generate the version without text

		g = open(CONST.PATH_LAPTOP + p + f, 'r')
		h = open(CONST.PATH_LAPTOP + p + "v2" + f, 'w+')
		reader = csv.reader(g)
		writer = csv.writer(h)

		for row in reader:
			print(row)
			if (len(row) == 3):
				writer.writerow(row)
			else:
				print("fin!")
				break
		
		g.close()
		h.close()
		break

data = pd.read_csv(CONST.PATH_LAPTOP + p + "v2" + f, delimiter = ",", header=None).astype(float)
x = data.iloc[:,0]
y = data.iloc[:,2]



# polyModel = np.poly1d(np.polyfit(x, y, 3))
# print(r2_score(y, polyModel(x)))
# plt.scatter(x, y)
# plt.plot(x, polyModel(x))
# plt.show()

#sk.plot_ForceDistance(0, p, p, x, y)


x1 = np.array(x).reshape((-1,1))
y1 = np.array(y)
linModel = LinearRegression().fit(x1, y1)
ypred= linModel.intercept_ + linModel.coef_ * x1
print(linModel.intercept_)
print(linModel.coef_)
print(r2_score(y,ypred))
# print(linModel.score(x1, y1))
plt.scatter(x1, y1)
plt.plot(x1, ypred)
plt.show()

poly = PolynomialFeatures(degree=2, include_bias=False)
poly_features = poly.fit_transform(x1)
polyModel2 = LinearRegression()
polyModel2.fit(poly_features,y)
ypred2 = polyModel2.predict(poly_features)
print(poly.get_feature_names())
print(polyModel2.intercept_)
print(polyModel2.coef_)

plt.scatter(x1, y1)
plt.plot(x1, ypred2)
plt.show()

print(r2_score(y, ypred2))