import numpy as np
import matplotlib.pyplot as plt
from scipy import interpolate, stats

def smooth(x, y):
	x_new = np.linspace(min(x), max(x), 100)
	bspline = interpolate.make_interp_spline(x, y)
	y_new = bspline(x_new)

	return x_new, y_new

def plot(x, y, ax):
	x, y = smooth(x, y)
	ax.plot(x, y)

V_r = [0.498, 1.005, 1.502, 1.966, 2.508, 3.004, 3.505, 4.013, 4.507, 5.073, 5.512, 6.000]
I_r = [-4.99, -9.92, -15.13, -19.73, -25.30, -31.05, -35.21, -40.29, -45.19, -50.80, -55.31, -60.2]

V_d = [0.504, 0.521, 0.550, 0.573, 0.600, 0.624, 0.650, 0.673, 0.701, 0.724, 0.749]
I_d = [-0.22, -0.31, -0.59, -0.90, -1.65, -2.67, -4.75, -7.92, -15.14, -25.96, -48.08]

I_r = list(map(abs, I_r))
I_d = list(map(abs, I_d))


fig, axis = plt.subplots(1, 3, figsize=(17, 5))
ax_r, ax_d, ax_g = axis

ax_r.scatter(V_r, I_r)
slope, intercept, r, p, std_err = stats.linregress(V_r, I_r)
print(f"Resistência (1/slope): {1/slope * 1e3}")
ax_r.plot(V_r, list(map(lambda x: slope * x + intercept, V_r)))
ax_r.set_ylabel("Corrente (mA)")
ax_r.set_xlabel("Voltagem (V)")
ax_r.set_title("Resistor de 99.2 Ω")

ax_d.scatter(V_d, I_d)
plot(V_d, I_d, ax_d)
ax_d.set_ylabel("Corrente (mA)")
ax_d.set_xlabel("Voltagem (V)")
ax_d.set_title("Diodo a favor (0 Ω)")

ax_g.scatter(V_d, list(map(np.log10, I_d)))
slope, intercept, r, p, std_err = stats.linregress(V_d, list(map(np.log10, I_d)))
ax_g.plot(V_d, list(map(lambda x: slope * x + intercept, V_d)))
ax_g.set_ylabel("Corrente (log10 mA)")
ax_g.set_xlabel("Voltagem (V)")
ax_g.set_title("Diodo a favor (0 Ω)")

for ax in axis:
	ax.grid(alpha=0.3)

plt.show()

