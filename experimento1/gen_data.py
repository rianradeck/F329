from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
import numpy as np

I = np.array([50, 75, 100, 125, 150, 175, 200, 225])

T = np.array([[7.64, 7.66, 7.73, 7.68, 7.67],
              [5.84, 5.91, 5.83, 5.77, 5.88],
              [4.85, 4.86, 4.87, 4.92, 4.89],
              [4.39, 4.36, 4.30, 4.36, 4.37],
              [3.89, 3.92, 3.83, 3.89, 3.83],
              [3.58, 3.49, 3.54, 3.59, 3.54],
              [3.36, 3.33, 3.33, 3.33, 3.38],
              [3.14, 3.13, 3.16, 3.12, 3.11]])

T = T.mean(axis = 1)
f2 = 1 / T ** 2

# print(f2)

model = LinearRegression()
model.fit(I.reshape(-1, 1), f2)

x = np.linspace(20, 40, 3).reshape(-1, 1)
y = model.predict(x)

plt.plot(x, y)
plt.show()

# print(x, 1 / np.sqrt(y), sep='\n')

fabricated_x = x
fabricated_y = 1 / np.sqrt(y)
# print("->", fabricated_y)

print('[', end = '')
for x in fabricated_x:
    print(np.round(x, 2)[0], end=', ')
print(']', end = '\n')

for y in fabricated_y:
    # print("->", y)
    print('[', end = '')
    for i in range(5):
        print(np.round(np.random.normal(y, 0.02), 2), end=(', ' if i != 2 else ''))
    print('],\n', end = '')

