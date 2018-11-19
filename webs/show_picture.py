import matplotlib.pyplot as plt
import numpy as np


# x1 = np.array(range(100, 1100, 100))
# y1 = np.array([1, 0.7, 0.933, 0.775, 0.68, 0.8, 0.757, 0.788, 0.711, 0.76])
# plt.plot(x1, y1, marker='o')
axes = plt.gca()
axes.set_ylim([0, 1])
x2 = np.array(range(1000, 5000, 500))
y2 = np.array([0.76, 0.82, 0.765, 0.792, 0.793, 0.803, 0.79, 0.807])
plt.plot(x2, y2, marker='o')
plt.xlabel('number of samples')
plt.ylabel('accuracy')
plt.show()