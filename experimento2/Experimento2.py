import matplotlib.pyplot as plt
import numpy as np
import math
from scipy import interpolate
from matplotlib import cbook, cm
from matplotlib.colors import LightSource
import mpl_toolkits.mplot3d.art3d as art3d

POINTS_PER_EXP = 35
POINTS_PER_LINE = 7
DIST = 2
NUMBER_OF_LINES = {"clean" : 5, "point" : 5, "circle" : 4}

data = open("Dados.txt")
points = {"clean" : [], "point" : [], "circle" : []}
exp = "clean"
cnt = 0
for l in data:
	coords = l.split(',')
	if len(coords) != 3:
		continue
	try:
		x = float(coords[0].replace("#", "").strip())
		y = float(coords[1])
		z = float(coords[2])
		
		points[exp].append((x, y, z))
		cnt += 1
		if cnt == POINTS_PER_EXP:
			exp = "point"
		if cnt == POINTS_PER_EXP * 2:
			exp = "circle"
	except:
		pass

# print(points)

def print7(v):
	for i in range(len(v)):
		if i % POINTS_PER_LINE == 0:
			print(" ")
		print(v[i], end=' ')
	print()


def get_aux_points():
	off = 0
	aux = {"clean" : [], "point" : [], "circle" : []}
	for exp in ["clean", "point", "circle"]:
		for j in range(0, 2 * (NUMBER_OF_LINES[exp] - 1), 2):
			j = j - off
			newp = []
			for i in range(POINTS_PER_LINE):
				p = np.array(points[exp][j * POINTS_PER_LINE + i]) + np.array(points[exp][i + (j + 1) * POINTS_PER_LINE])
				p = tuple(p / 2)

				if exp == "circle" and 14 - 2.5 <= p[0] and p[0] <= 14 + 2.5 and 9 - 2.5 <= p[1] and p[1] <= 9 + 2.5:
					newp = []
					break

				newp.append(p)
			if len(newp) == 0:
				off += 1
				continue
			points[exp] = points[exp][:(j + 1) * POINTS_PER_LINE] + newp + points[exp][(j + 1) * POINTS_PER_LINE:]
			NUMBER_OF_LINES[exp] += 1


		# NUMBER_OF_LINES[exp] = 2 * NUMBER_OF_LINES[exp] - 1

# get_aux_points()
# get_aux_points()
# get_aux_points()
# get_aux_points()

print(points)

def get_point(x1, y1, x2, y2, P):
	P = 1
	if x1 > x2:
		x1, x2 = x2, x1
		y1, y2 = y2, y1
	
	xm  = (x1 + x2) / 2
	ym = (y1 + y2) / 2

	if y1 == y2:
		return xm, ym, 0, 1/P


	m = (x1 - x2) / (y2 - y1)

	dx = 1
	dy = m
	theta = np.arctan(m)
	dx = 1/P * np.cos(theta)
	dy = 1/P * np.sin(theta)

	if abs(dy) != dy:
		dy, dx = abs(dy), -dx

	return xm, ym, dx, abs(dy)

def smooth(x, y):
	x_new = np.linspace(2, 26, 100)
	bspline = interpolate.make_interp_spline(x, y)
	y_new = bspline(x_new)

	return x_new, y_new

def plot(X, Y, idx, P):
	zipped_lists = zip(X, Y)
	sorted_pairs = sorted(zipped_lists)

	tuples = zip(*sorted_pairs)
	X, Y = [list(tuple) for tuple in  tuples]

	_idx = X.index(14.0)
	X = X[0:_idx] + X[_idx + 1:]
	Y = Y[0:_idx] + Y[_idx + 1:]

	for i in range(len(X) - 1):
		x0, y0, dx, dy = get_point(X[i], Y[i], X[i + 1], Y[i + 1], P)
		axis[idx].arrow(x0, y0, dx, dy, width=0.1)

	X, Y = smooth(X, Y)
	axis[idx].plot(X, Y, label=str(P) + ' V')

	return [], []

def f(idx, exp):
	X = []
	Y = []
	Z = []
	curX = []
	curY = []
	offset = 0
	for i in range(len(points[exp])):
		p = points[exp][i]
		if p[0] == 14.0 and curX:
			print(exp, idx, points[exp][i - 1][2])
			curX, curY = plot(curX, curY, idx, points[exp][i - 1][2])
			
		a = [p[0], p[0] + i % POINTS_PER_LINE * DIST * 2]
		b = [p[1], p[1]]
		c = [p[2], p[2]]
		X += a
		curX += a
		Y += b
		curY += b
		Z += c

	print(exp, idx, points[exp][-1][2])
	curX, curY = plot(curX, curY, idx, points[exp][-1][2])

	axis[idx].scatter(X, Y, s = 10)
	axis[idx].errorbar(X, Y, xerr = 0.25, yerr = 0.25, fmt='.', c = 'brown')

	X = np.array(X).reshape(NUMBER_OF_LINES[exp], 2 * POINTS_PER_LINE)
	Y = np.array(Y).reshape(NUMBER_OF_LINES[exp], 2 * POINTS_PER_LINE)
	Z = np.array(Z).reshape(NUMBER_OF_LINES[exp], 2 * POINTS_PER_LINE)
	ls = LightSource(270, 45)
	rgb = ls.shade(Z, cmap=cm.gist_earth, vert_exag=0.1, blend_mode='soft')
	surf = axis3d[idx].plot_surface(X, Z, Y, rstride=1, cstride=10, facecolors=rgb,
	                       linewidth=0, antialiased=True, shade=False)
	# axis3d[idx].plot_wireframe(X, Z, Y, rstride=10, cstride=10)
	pt = {"clean" : "Limpo", "point" : "Ponta", "circle" : "Aro"}
	axis[idx].set_title(pt[exp])

def build_grid(ax):
	for i in range(1, 28):
		ax.axvline(i, aa=1, ls='-', lw=.8, alpha=.25, c='gray')
	for i in range(1, 19):
		ax.axhline(i, aa=1, ls='-', lw=.8, alpha=.25, c='gray')


figure, axis1 = plt.subplots()
figure, axis2 = plt.subplots()
figure, axis3 = plt.subplots()
axis = [axis1, axis2, axis3]
figure, axis3d = plt.subplots(1, 3, subplot_kw=dict(projection='3d'))
f(0, "clean")
f(1, "point")
f(2, "circle")

for i in range(3):
	axis[i].set_aspect('equal', 'box')
	# axis[i].grid(alpha=0.3)
	build_grid(axis[i])
	axis[i].set_xticks(range(0, 29, 2))
	axis[i].set_yticks(list(range(0, 20, 2)))
	axis[i].set_xlabel("X")
	axis[i].set_ylabel("Y")
	axis[i].legend(bbox_to_anchor=(0.9, 1.0), loc='upper left')
	# axis[i].legend()

	axis3d[i].set_xlabel("X")
	axis3d[i].set_ylabel("Z - Potencial")
	axis3d[i].set_zlabel("Y")
	axis3d[i].set_xticks(range(0, 29, 1))
	axis3d[i].set_zticks(range(0, 20, 1))
	axis3d[i].set_box_aspect([28,20,19])

axis[1].add_artist(plt.Polygon(([14,3],[14.5,3],[14,5]), closed=True,fill=True)) 
axis[1].add_artist(plt.Rectangle((14, 0), .5, 3))

circle = plt.Circle((14, 9.5), 2.5, fill = False)
axis[2].add_artist(circle)


def data_for_cylinder_along_z(center_x,center_y,radius,height_z):
    z = np.linspace(0, height_z, 50)
    theta = np.linspace(0, 2*np.pi, 50)
    theta_grid, z_grid=np.meshgrid(theta, z)
    x_grid = radius*np.cos(theta_grid) + center_x
    y_grid = radius*np.sin(theta_grid) * (19/28) + center_y
    return x_grid,y_grid,z_grid

Xc,Yc,Zc = data_for_cylinder_along_z(14,9.5,2.5,4)

axis3d[2].plot_surface(Xc, Zc, Yc, alpha=1)

plt.show()
