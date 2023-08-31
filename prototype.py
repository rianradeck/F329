import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression

I = np.array([-.225, -.200, -.175, -.150, -.125, -.100, -.075, -.050, .050, .075, .100, .125, .150, .175, .200, .225]) * 1e3
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


def ret_unc(res):
    return res / (2 * np.sqrt(3))

def tri_unc(res):
    return res / (2 * np.sqrt(6))

def calc_r(d):
    return d[0] / 2, d[1] / 2

def calc_m_i(m, r, L):
    val = {'m': m[0], 'r': r[0], 'L': L[0]}
    unc = {'m': m[1], 'r': r[1], 'L': L[1]}

    relative_unc = [
        unc['m'] * (val['r'] ** 2 / 4 + val['L'] ** 2 / 12),
        unc['r'] * val['r'] * val['m'] / 2,
        unc['L'] * val['m'] * val['L']  / 6
    ]

    return val['m'] * ((val['r'] ** 2 / 4) + (val['L'] ** 2 / 12)), np.sqrt(np.sum([x ** 2 for x in relative_unc]))

def calc_T(T):
    NUM_SAMPLES = 5
    
    T /= 5
    unc_T_i = np.sqrt(ret_unc(0.01) ** 2 + 0.25 ** 2)
    unc_T_i /= 5

    sd = T.std(axis=1)
    unc_A = T.std(axis=1) / np.sqrt(NUM_SAMPLES)
    print("############ UNCA ##########")
    print(unc_A)
    unc_B = np.sqrt(unc_T_i ** 2 / 5)
    unc_T = np.sqrt(unc_A ** 2 + unc_B ** 2)
    T = T.mean(axis=1)

    return T, unc_T

def print_variable(x, unc_x):
    for i in range(len(x)):
        print(x[i], unc_x[i])


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

m = 5.1863 * 1e-3
d = 0.55 * 1e-2
r = d / 2
R = (22.51 + 19.96) / 2
R *= 1e-2
L = 2.5 * 1e-2
Bt = 17.8 * 1e-6
mu0 = 4 * np.pi * 1e-7
# N = 140

# print(r, L, mi)


a = coef_ang_dec * 1e3
b = coef_lin_dec

mi = m * (((r ** 2) / 4) + ((L ** 2) / 12))
print("mi ->", mi)
Kmi = 4 * np.pi ** 2 * mi
mu = b * Kmi / Bt

print("Dipolo do imã:", mu)
print("Campo:", Bt)

N = a * Kmi * 5 ** (3/2) * R / (mu * mu0 * 8)

print(N)



plt.show()