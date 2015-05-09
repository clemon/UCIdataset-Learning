import matplotlib.pyplot as plt
import numpy as np

N = 10
x = []
y = []
for i in range(700):
    x.append(i)
    y.append(i)


plt.scatter(x, y, c=x, alpha=0.5)

plt.show()