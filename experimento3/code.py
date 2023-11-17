import numpy as np
import matplotlib.pyplot as plt
from scipy import interpolate, stats

def smooth(x, y):
	x_new = np.linspace(min(x), max(x), 101)
	bspline = interpolate.make_interp_spline(x, y)
	y_new = bspline(x_new)

	return x_new, y_new

def plot(x, y, ax):
	nx, ny = smooth(x, y)
	ax.plot(nx, ny)
	return nx / ny * 1e3

def get_derivative(X, f):
	dx = 0.001
	return list(map(lambda x: (f(x + dx) - f(x)) / dx, X))

V_r = [0.498, 1.005, 1.502, 1.966, 2.508, 3.004, 3.505, 4.013, 4.507, 5.073, 5.512, 6.000]
u_Vr = [0.000920748970494492, 0.0014762064275251844, 0.0019001762198982144, 0.002298158755757893, 0.0027644555823284032, 0.003191970968957373, 0.003624284124715758, 0.004062978392345529, 0.004489816635082848, 0.004979072545832876, 0.005358663514969629, 0.0057807150653415434]
I_r = [-4.99, -9.92, -15.13, -19.73, -25.30, -31.05, -35.21, -40.29, -45.19, -50.80, -55.31, -60.2]
u_Ir = np.array([7.115900622315259e-06, 1.4231713412891179e-05, 2.175169054732682e-05, 2.8391214163305294e-05, 3.6430813423071774e-05, 4.473022142057128e-05, 5.0734663117701556e-05, 5.806701049936472e-05, 6.513955051784336e-05, 7.323688733600485e-05, 7.97465111567062e-05, 8.680461777271224e-05]) * 1e3

V_d = [0.504, 0.521, 0.550, 0.573, 0.600, 0.624, 0.650, 0.673, 0.701, 0.724, 0.749]
u_Vd = [0.0009311362234746681, 0.000960567367063168, 0.001010775280003754, 0.0010505968145138585, 0.0010973452814254346, 0.0011544256869399031, 0.0011762404799473053, 0.001195559875818299, 0.0012191051704699915, 0.0012384662557642283, 0.0012595306334768784]
I_d = [-0.22, -0.31, -0.59, -0.90, -1.65, -2.67, -4.75, -7.92, -15.14, -25.96, -48.08]
u_Id = [0.00031745604682643344, 0.0004473598570129719, 0.0008515050450036493, 0.0012989515034570512, 0.0023814832580417887, 0.0038537264444084944, 0.006855947844147202, 0.011431448727450663, 0.021852621086306027, 0.03746994586787745, 0.06939741575405865]

I_r = list(map(abs, I_r))
I_d = list(map(abs, I_d))


fig, axis = plt.subplots(2, 3, figsize=(17, 10))
(ax_r, ax_d, ax_g), (ax_r2, ax_d2, ax_g2) = axis

ax_r.scatter(V_r, I_r, s=10)
ax_r.errorbar(V_r, I_r, xerr=np.array(u_Vr)*10, yerr=u_Ir, capsize=0, ls='none', color='red', elinewidth=1.5)
slope, intercept, r, p, std_err = stats.linregress(V_r, I_r)
print(f"Resistência (1/slope): {1/slope * 1e3}")
ax_r.plot(V_r, list(map(lambda x: slope * x + intercept, V_r)))
R_r = get_derivative(V_r, lambda x: 1/slope*1e3 * x + intercept)
ax_r.set_ylabel("Corrente (mA)")
ax_r.set_xlabel("Voltagem (V)")
ax_r.set_title("Resistor de 99.2 Ω")

u_Rr = [(u_Ir[i]*1e-3 / u_Vr[i]) for i in range(len(u_Vr))]
ax_r2.scatter(V_r, R_r, s = 10)
ax_r2.errorbar(V_r, R_r, xerr=np.array(u_Vr)*10, yerr=u_Rr, capsize=0, ls='none', color='red', elinewidth=1.5)
ax_r2.plot(V_r, R_r)
ax_r2.set_yticks(np.linspace(99.5,100, 5))
ax_r2.set_ylabel("Resistência (Ω)")
ax_r2.set_xlabel("Voltagem (V)")
ax_r2.set_title("Resistor de 99.2 Ω")

ax_d.scatter(V_d, I_d, s=10)
print(u_Vd[-1], V_d[-1])
ax_d.errorbar(V_d, I_d, xerr=np.array(u_Vd)*3, yerr=u_Id, capsize=0, ls='none', color='red', elinewidth=1.5)
R_d = plot(V_d, I_d, ax_d)
ax_d.set_ylabel("Corrente (mA)")
ax_d.set_xlabel("Voltagem (V)")
ax_d.set_title("Diodo a favor (0 Ω)")

auxX = np.linspace(min(V_r), max(V_r), len(R_d))[::10]
auxY = R_d[::10]
print("############", list(auxX / auxY) )
ax_d2.scatter(np.linspace(min(V_r), max(V_r), len(R_d))[::10], R_d[::10], s=10)
ax_d2.errorbar(auxX, auxY, xerr=np.array(u_Vd)*100, yerr=u_Id, capsize=0, ls='none', color='red', elinewidth=1.5)
ax_d2.plot(np.linspace(min(V_r), max(V_r), len(R_d)), R_d)
ax_d2.set_ylabel("Resistência (Ω)")
ax_d2.set_xlabel("Voltagem (V)")
ax_d2.set_title("Diodo a favor (0 Ω)")


ax_g.scatter(V_d, list(map(np.log, I_d)), s=10)
ax_g.errorbar(V_d, list(map(np.log, I_d)), xerr=np.array(u_Vd)*3, yerr=np.abs(list(map(np.log, u_Id)))/100, capsize=0, ls='none', color='red', elinewidth=1.5)
slope, intercept, r, p, std_err = stats.linregress(V_d, list(map(np.log, I_d)))
ax_g.plot(V_d, list(map(lambda x: slope * x + intercept, V_d)))
ax_g.set_ylabel("Corrente (log mA)")
ax_g.set_xlabel("Voltagem (V)")
ax_g.set_title("Diodo a favor (0 Ω)")

auxX = np.linspace(min(V_r), max(V_r), len(R_d))[::10]
auxY = np.abs(list(map(np.log, R_d[::10])))
u_Rd = [(auxX[i]*1e-3 / auxY[i]) for i in range(len(auxX))]

ax_g2.scatter(np.linspace(min(V_r), max(V_r), len(R_d))[::10], list(map(np.log, R_d[::10])), s=10)
ax_g2.errorbar(auxX, auxY, xerr=np.abs(list(map(np.log, u_Rd)))/100, capsize=0, ls='none', color='red', elinewidth=1.5)
slope, intercept, r, p, std_err = stats.linregress(np.linspace(min(V_r), max(V_r), len(R_d))[::10], list(map(np.log, R_d[::10])))
ax_g2.plot(np.linspace(min(V_r), max(V_r), len(R_d))[::10], list(map(lambda x: slope * x + intercept, np.linspace(min(V_r), max(V_r), len(R_d))[::10])))
ax_g2.set_ylabel("Resistência (log Ω)")
ax_g2.set_xlabel("Voltagem (V)")
ax_g2.set_title("Diodo a favor (0 Ω)")

for _ax in axis:
	for ax in _ax:
		ax.grid(alpha=0.3)

plt.show()

