import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression

I = np.array([-225, -200, -175, -150, -125, -100, -75, -50, 50, 75, 100, 125, 150, 175, 200, 225])
T = np.array([[2.83, 2.88, 2.86, 2.88, 2.83], 
              [3.12, 3.11, 3.15, 3.09, 3.13],
              [3.26, 3.24, 3.25, 3.22, 3.28],
              [3.55, 3.51, 3.50, 3.49, 3.51],
              [3.82, 3.73, 3.81, 3.83, 3.80],
              [4.19, 4.26, 4.23, 4.14, 4.24],
              [4.68, 4.62, 4.61, 4.69, 4.62],
              [5.69, 5.48, 5.55, 5.65, 5.55],
              [7.64, 7.66, 7.73, 7.68, 7.67],
              [5.84, 5.91, 5.83, 5.77, 5.88],
              [4.85, 4.86, 4.87, 4.92, 4.89],
              [4.39, 4.36, 4.30, 4.36, 4.37],
              [3.89, 3.92, 3.83, 3.89, 3.83],
              [3.58, 3.49, 3.54, 3.59, 3.54],
              [3.36, 3.33, 3.33, 3.33, 3.38],
              [3.14, 3.13, 3.16, 3.12, 3.11]])

# DATA 
# 5 - AVG
# 6 - INCA = STD / sqrt(5)
# 7 - INCB
# 8 - INCC

T /= 5
f = 1 / T
f_2 = f ** 2

d = {}
for i in range(len(I)):
    d[I[i]] = f_2[i]

data = pd.DataFrame(d)

avg = []
inca = []
incb = []
incc = []
cnt = 0
for x in data:
    avg.append(data[x].mean())
    inca.append(data[x].std() / np.sqrt(5))
    incb.append(0.01 / (2 * np.sqrt(3)))
    incc.append(np.sqrt(inca[cnt] ** 2 + incb[cnt] ** 2))
    cnt += 1

data.loc[len(data)] = avg
data.loc[len(data)] = inca
data.loc[len(data)] = incb
data.loc[len(data)] = incc

X = data.columns
Y = data.iloc[5]

fig, ax = plt.subplots()

ax.scatter(X, Y)
# ax.errorbar(X, Y, yerr=incc, fmt='-o', linestyle = '')
ax.grid(alpha = 0.3)

# plt.show()

x_dec = np.array(data.columns[:8]).reshape((-1, 1))
y_dec = np.array(data.iloc[5][:8])
x_inc = np.array(data.columns[8:]).reshape((-1, 1))
y_inc = np.array(data.iloc[5][8:])

reg_dec = LinearRegression()
reg_dec.fit(x_dec, y_dec)

reg_inc = LinearRegression()
reg_inc.fit(x_inc, y_inc)

coef_lin_dec = reg_dec.predict(np.array(0).reshape(-1, 1))
coef_lin_inc = reg_inc.predict(np.array(0).reshape(-1, 1))
y_dec_100 = reg_dec.predict(np.array(100).reshape(-1, 1))
y_inc_100 = reg_dec.predict(np.array(100).reshape(-1, 1))

coef_ang_dec = (y_dec_100 - coef_lin_dec) / 100
coef_ang_inc = (y_inc_100 + coef_lin_inc) / -100

print(coef_lin_dec, coef_lin_inc)
print(coef_ang_dec, coef_ang_inc)

x_cross = (coef_lin_dec - coef_lin_inc) / (coef_ang_inc - coef_ang_dec)
print(x_cross)

test_x_dec = np.linspace(-250, x_cross, 100).reshape((-1, 1))
test_y_dec = reg_dec.predict(test_x_dec)

test_x_inc = np.linspace(x_cross, 250, 100).reshape((-1, 1))
test_y_inc = reg_inc.predict(test_x_inc)

ax.plot(test_x_dec, test_y_dec)
ax.plot(test_x_inc, test_y_inc)
ax.axvline(x_cross, linestyle="--", marker = '.')
# ax.plot(reg_inc)
ax.set_xticks([-250, -200, -150, -100, -50, 0, float(x_cross), 50, 100, 150, 200, 250])

plt.show()
