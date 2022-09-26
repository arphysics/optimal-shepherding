import os
import numpy as np
import matplotlib.pyplot as plt
from herd_ODE_class import *
import time
from datetime import datetime
from aux_funcs_viz import *
plt.rcParams.update({'figure.max_open_warning': 0})
import seaborn as sns
sns.set()


data = np.loadtxt("data.out")

costdata = np.loadtxt("cost.out")

# old_data = np.loadtxt("old_data.out")

# old_area_array = old_data[:,5]


#H = [R, T, R', T', Q, A] // T = 'Theta'
R_array = data[:,0]
T_array = data[:,1]
R_prime_array = data[:,2]
T_prime_array = data[:,3]
Q_array = data[:,4]
A_array = data[:,5]
theta_dog = data[:,6]
uT = data[:,7]
uR = data[:, 8]
times = np.arange(0, len(R_array), 1)

delta_theta_dog_herd = np.cos(theta_dog-T_array)


plt.figure(figsize = (10,10))
#plt.plot(times, R_array, label = "R")
#plt.plot(times, delta_theta_dog_herd, label = "delta_theta_dog_herd")
plt.plot(times, A_array, '--', label = "Area")
#plt.plot(times, old_area_array, 'r--', label = "Old Area")
#plt.plot(times, theta_dog, '--', label = "theta_dog")
plt.plot(times, uT, label = "uT")
plt.plot(times, uR, label = "uR")
plt.plot(times, Q_array, label = "Q")
plt.plot(times, np.fmod(T_array-np.pi, 2*np.pi), label = "Theta")
plt.plot(times, T_prime_array, label = "Theta Prime")
plt.xlabel("time")
plt.legend()
#plt.show()

plt.savefig("fig_analysis_1.png")

os.system("open fig_analysis_1.png")