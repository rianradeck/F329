import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import interpolate

df = pd.read_csv("dados2.csv")

df["clear"] = np.round(df["clear"]  / df["clear"].max() * 3.95, 2)

for col in df.columns:	
	for i in range(len(df[col])):
		df[col].iloc[i] = 4 - df[col].iloc[i]

print(df)

def smooth(x, y):
	x_new = np.linspace(0, 19, 1000)
	bspline = interpolate.make_interp_spline(x, y)
	y_new = bspline(x_new)

	return x_new, y_new

pt = {"clear" : "Limpo", "point" : "Ponta", "circle" : "Aro"}
def f(exp, idx):
	x = np.linspace(0, 20, len(df[exp]))
	y = np.array(df[exp][::-1])
	y[np.isnan(y)] = 0
			
	print(x, y, sep='\n')
	x, y = smooth(x, y)

	axis.plot(x, y, label=pt[exp])

figure, axis = plt.subplots()

f("clear", 0)
f("point", 1)
f("circle", 2)

# for i in range(3):
# axis.set_aspect('equal', 'box')
axis.set_xticks(np.arange(0, 20, 1))
axis.set_yticks(np.arange(0, 4.5, 0.5))
axis.grid(alpha=.3)
axis.legend(prop={'size':20})
axis.set_xlabel("Y (cm)")
axis.set_ylabel("Pot (V)")
axis.set_title("Potencial ao longo do eixo de simetria")


plt.show()