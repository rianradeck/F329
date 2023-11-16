import numpy as np
from math import sqrt
import matplotlib.pyplot as plt
from scipy.odr import *


V_r = np.array([0.498, 1.005, 1.502, 1.966, 2.508, 3.004, 3.505, 4.013, 4.507, 5.073, 5.512, 6.000])
I_r = np.array([-4.99, -9.92, -15.13, -19.73, -25.30, -31.05, -35.21, -40.29, -45.19, -50.80, -55.31, -60.2]) * 1e-3



def getTensRes(tens):
    if tens <= 0.6:
        return 0.1e-3
    elif tens <= 6:
        return 0.001
    else:
        return 0.01

def getTensExat(tens):
    d = getTensRes(tens) 
    if tens <= 0.6:
        return 0.6e-2 * tens + 2 * d
    elif tens <= 600:
        return 0.3e-2 * tens + 2 * d

def getTensUnc(tens):
    d = getTensRes(tens)
    ex = getTensExat(tens)
    uRes = d / (2 * sqrt(3))
    uExat = ex / (2 * sqrt(3))
    return sqrt(uRes ** 2 + uExat ** 2)

def getCurRes(cur):
    if cur <= 600e-6:
        return 0.1e-6
    elif cur <= 6000e-6:
        return 1e-6
    elif cur <= 60e-3:
        return 0.01e-3
    else:
        return 0.1e-3

def getCurExat(cur):
    d = getCurRes(cur) 
    if cur <= 60e-3:
        return 0.5e-2 * cur + 3 * d
    else:
        return 0.8e-2 * cur + 3 * d

def getCurUnc(cur):
    d = getCurRes(cur)
    ex = getCurExat(cur)
    uRes = d / (2 * sqrt(3))
    uExat = ex / (2 * sqrt(3))
    return sqrt(uRes ** 2 + uExat ** 2)

def printWithUnc(x, uX):
    for i in range(len(x)):
        print(f"{x[i]} ± {uX[i]}")

uV_r = np.array([getTensUnc(x) for x in V_r])
uI_r = np.array([getCurUnc(x) for x in I_r])

print("Resistor tension: (V):")
printWithUnc(V_r, uV_r)
print("Resistor current: (A):")
printWithUnc(I_r, uI_r)

def lin_func(p, x):
    a, b = p
    return a * x + b

model = Model(lin_func)
data = RealData(V_r, I_r, sx=uV_r, sy=uI_r)
odr = ODR(data, model, beta0 =[0., 1.])

out = odr.run()

out.pprint()

plt.scatter(V_r, I_r)
plt.show()
