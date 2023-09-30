import matplotlib.pyplot as plt
import numpy as np

zenerData = np.loadtxt('AnalogExperiment1//Test//1N4148.csv', delimiter=',')
zenerData[:,1] = zenerData[:,1] * 0.0048828125
zenerData[:,2] = zenerData[:,2] * 0.0048828125


i = zenerData[:,1]/1000
v = zenerData[:,2] - zenerData[:,1]

fig, ax = plt.subplots()
ax.scatter(v,i*1000, marker='.', s = 1)

plt.title('BAT85 Schottky diode I-V characteristics')
plt.xlabel('Votage(V)')
plt.ylabel('Current(mA)')
plt.show()
