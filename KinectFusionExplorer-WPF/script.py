import matplotlib.pyplot as plt
import numpy as np

t = np.linspace(0,2*np.pi,1000)
x = np.cos(t)
plt.plot(t,x)
plt.show()