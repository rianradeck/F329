import numpy as np
from inc_lib import Num
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
from matplotlib.ticker import FormatStrFormatter
from tabulate import tabulate

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


def ret_unc(res):
    return res / (2 * np.sqrt(3))

def tri_unc(res):
    return res / (2 * np.sqrt(6))

def evalLine(x, a, b):
    return x * a + b

def get_coefs(x, y):
    if isinstance(y[0], Num):
        ymaxes = np.vectorize(lambda a: a.value + a.inc)(y) 
        ymins = np.vectorize(lambda a: a.value - a.inc)(y)

        xNoInc = np.vectorize(lambda x: x.value)(x)

        amax, bmax = get_coefs(xNoInc, ymaxes)
        amin, bmin = get_coefs(xNoInc, ymins)

        y0Min = evalLine(xNoInc[0], amin, bmin)
        y0Max = evalLine(xNoInc[0], amax, bmax)
        y1Min = evalLine(xNoInc[-1], amin, bmin)
        y1Max = evalLine(xNoInc[-1], amax, bmax)
    
        a1, b1 = get_coefs(np.array([xNoInc[0], xNoInc[-1]]), np.array([y0Min, y1Max]))
        a2, b2 = get_coefs(np.array([xNoInc[0], xNoInc[-1]]), np.array([y0Max, y1Min]))
        a = Num((a1 + a2) / 2)

        xm = x.mean()
        ym = y.mean()
        b = ym - a * xm

        return a, b

        #return Num((amax + amin) / 2, np.abs(amax - amin) / 2), Num((bmax + bmin) / 2, np.abs(bmax - bmin) / 2)

    #n = len(x)
    #xy = x * y
    #x2 = x * x
    #den = x2.sum() * n - x.sum() ** 2
    #a = (xy.sum() * n - x.sum() * y.sum()) / den
    #b = (y.sum() * x2.sum() - x.sum() * xy.sum()) / den
    xm = x.mean()
    ym = y.mean()
    a = ((x - xm) * (y - ym)).sum() / ((x - xm) ** 2).sum()
    b = ym - a * xm

    return a, b

def abline(slope, intercept, st, nd):
    """Plot a line from slope and intercept"""
    slope = slope.value
    intercept = intercept.value
    axes = plt.gca()
    x_vals = np.linspace(st, nd, 2)
    y_vals = intercept + slope * x_vals
    plt.plot(x_vals, y_vals, '--')

def plot(I, f2):
    a_dec, b_dec = get_coefs(I[:8], f2[:8])
    a_inc, b_inc = get_coefs(I[8:], f2[8:])

    x_cross = (b_dec - b_inc) / (a_inc - a_dec)
    
    ax = plt.gca()
    ax.axvline(x_cross.value, linestyle=":", marker = '.')

    abline(a_dec, b_dec, -.250, x_cross.value)
    abline(a_inc, b_inc, x_cross.value, .250)

    I_val = np.array([x.value for x in I])
    I_inc = np.array([x.inc for x in I])
    f2_val = np.array([x.value for x in f2])
    f2_inc = np.array([x.inc for x in f2])
    ax.scatter(I_val, f2_val)
    ax.errorbar(I_val, f2_val,
             yerr = f2_inc,
             xerr = I_inc,
             fmt ='o')

    ax.xaxis.set_major_formatter(FormatStrFormatter('%.2f'))
    ax.set_xticks([-.250, -.200, -.150, -.100, -.050, 0, x_cross.value, .050, .100, .150, .200, .250])
    ax.grid(alpha=0.3)
    plt.xlabel('$I$ ($A$)')
    plt.ylabel('$f^2$ $({Hz}^2)$')

    return a_dec, b_dec, a_inc, b_inc
    

def print_table(v, mag):
    table = []
    for x in v:
        table.append([x.value, x.inc, np.round(abs(x.inc / x.value) * 100, 2)])

    print(tabulate(table, headers=[f"Valor {mag}", f"Incerteza {mag}", "Incerteza relativa (%)"], tablefmt='fancy_grid'))

if __name__ == '__main__':

    # defining constants
    m = Num(5.1863e-3, ret_unc(1e-7))
    d = Num(0.55e-2, tri_unc(1e-3))
    r = d / 2
    R = (Num(22.51e-2, tri_unc(1e-3)) + Num(19.96e-2, tri_unc(1e-3))) / 2
    L = Num(2.5e-2, tri_unc(1e-3))
    mu0 = 4e-7 * np.pi
    N = 300

    print(f"Massa do imã: {m}")
    print(f"Raio do imã: {r}")
    print(f"Comprimento do imã: {L}")
    print(f"Raio da bobina: {R}")

    # Calculating f^2
    unc_T_i = np.sqrt(ret_unc(0.01) ** 2 + 0.150 ** 2)
    T = np.vectorize(lambda x: Num(x, unc_T_i))(T)
    T /= 5
    incA = T.std(axis = 1, ddof=1) / np.sqrt(T.shape[1])
    incA = np.vectorize(lambda x: Num(0, x.value))(incA)
    T = T.mean(axis = 1) + incA
    f2 = T ** -2

    # Calculating Inertial momentum
    mi = (r ** 2 / 4 + L ** 2 / 12) * m

    # Calculating I
    incIexat = I * 0.008 + 3 * 0.1
    incIres = 0.1 / (2 * np.sqrt(3))
    # incFlut = 1
    incI = np.sqrt(incIexat * incIexat + incIres * incIres)
    I = np.vectorize(lambda x: Num(x, 0))(I)
    I = I + np.vectorize(lambda x: Num(0, x))(incI)
    I /= 1e3

    print_table(I, 'A')
    print_table(f2, 's^-2')

    # Linear regression
    a_dec, b_dec, a_inc, b_inc = plot(I, f2)

    # Calculating mu
    Kmi = mi * 4 * np.pi ** 2
    mu = (Kmi * a_dec * (5 ** (3 / 2)) * R) / (8 * mu0 * N)

    # Calculating Bt
    Bt = b_dec * 8 * mu0 * N / (a_dec * (5 ** (3 / 2)) * R)

    print(f'a: {a_dec}\nb: {b_dec}')
    print("Campo -> ", Bt * 1e6)

    plt.show()
    
