import matplotlib.pyplot as plt
import numpy as np

zenerData = np.loadtxt('AnalogExperiment1\Test\Test1.csv', delimiter=',')
zenerData[:,1] = zenerData[:,1] * 0.0048828125
zenerData[:,2] = zenerData[:,2] * 0.0048828125


i = zenerData[:,1]/1000
v = zenerData[:,2]

fig, ax = plt.subplots()
ax.scatter(v,i, marker='.', s = 1)

plt.title('Exprimet Zener diode I-V characteristics')
plt.xlabel('Votage(V)')
plt.ylabel('Current(A)')
plt.show()

