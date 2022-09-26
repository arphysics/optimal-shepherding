#import elements
import numpy as np
import matplotlib.pyplot as plt
import os
import time
from datetime import datetime



temp_H = [5.0, 0.0, 0, 0, 1, 2.5]

theta_shift = 0

R = temp_H[0]
#b = np.sqrt(temp_H[5]/(temp_H[4]*temp_H[0]))
b = np.sqrt(temp_H[5]/(np.pi*temp_H[4])) #(trying the new definition of the `ellipse')
a = temp_H[4]*b
theta = temp_H[1]+theta_shift +np.pi

phi_array = np.arange(-a, a, 0.1)
phi_array_R = np.arange(-a/R, a/R, 0.1/R)

r_array_1 = np.zeros(len(phi_array))
r_array_2 = np.zeros(len(phi_array))

r_array_1_R = np.zeros(len(phi_array))
r_array_2_R = np.zeros(len(phi_array))


for kk in range(len(phi_array)):
	r_array_1[kk] = R+b*np.sqrt(1-(phi_array[kk])**2/a**2)
	r_array_2[kk] = R-b*np.sqrt(1-(phi_array[kk])**2/a**2)

for kk in range(len(phi_array_R)):
	r_array_1_R[kk] = R+b*np.sqrt(1-(phi_array_R[kk]*R)**2/a**2)
	r_array_2_R[kk] = R-b*np.sqrt(1-(phi_array_R[kk]*R)**2/a**2)



phi_array_sum = np.concatenate((phi_array, phi_array))
r_array_sum = np.concatenate((r_array_1, r_array_2))

phi_array_sum_R = np.concatenate((phi_array_R, phi_array_R))
r_array_sum_R = np.concatenate((r_array_1_R, r_array_2_R))

print("No divide by R: ", r_array_1)
print("With divide by R: ", r_array_1_R)


max_plot_radius = 20

fig = plt.figure(figsize = (16,8))
ax1 = fig.add_subplot(122, projection = 'polar')

ax1.plot(phi_array_sum+theta, r_array_sum, '.', label = 'herd (no R)')
ax1.plot(phi_array_sum_R+theta, r_array_sum_R, '.', label = 'herd (corrected by R)')
ax1.set_ylim(0, max_plot_radius) #only use this one for polar
ax1.legend(loc='upper left')

fig.savefig("test.png")

os.system("open test.png")