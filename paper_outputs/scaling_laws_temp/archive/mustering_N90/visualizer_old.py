#python3

#import libraries
import numpy as np
import matplotlib.pyplot as plt
plt.rcParams.update({'figure.max_open_warning': 0})
import time
import os
from auxiliary_functions import *


#set user defined parameters

L = 10 #size of domain to plot
#modder = 3 #how often to convert frames to video

#start timing
t0 = time.time()

#import data files
dat_field = np.loadtxt('data.txt') #x,y position data for herd and dogs
parameters = np.loadtxt('params.txt') #info from parameter file (change function when params changes)

#load info from parameter file
driving_on, x_target, y_target, vs, vd, ls, ld, fence, num_particles, ndogs, modder = load_params(parameters)

#load info from data file
xpart, ypart, thetapart, x_dogs, y_dogs, dat_times, timesteps, times, = load_data(dat_field, num_particles)


#sanity checks
sanity_checks(dat_field, num_particles, ndogs, timesteps)


#-----------------------end sanity checks------------------------


#clear folders before saving
print("Pre-Clearing directory test_plots")
os.system('rm test_plots/*')
print("Now saving plots in directory 'test_plots'")


#plot the fence boundary
if fence == 1:
    xwall, ywall, xt_array, yt_array = plot_fence(L, x_target, y_target, ld)

counterr = 0
for t in range(timesteps):
#for t in range(2000):

#fork here
#for t in range(0,100):
    if t%modder == 0:
        counterr +=1
        
        #download particle data
        index = num_particles*t
        tmp_x = xpart[index: index+num_particles]
        tmp_y = ypart[index: index+num_particles]
        tmp_theta = thetapart[index: index+num_particles]

        # set color info
        tmp_colors = tmp_theta #%(2*np.pi) #colorator(tmp_theta)
        #print(np.max(tmp_colors), np.min(tmp_colors))
        #tmp_colors = np.transpose(tmp_colors)

        # plt.figure(figsize = (10,8))
        # title = "histogram at time = " + str(int(dat_times[index]))
        # plt.title(title)
        # plt.hist(tmp_colors)
        # name2 = str(t)+"_theta_pdf"
        # plt.savefig(name2)

        plt.figure(figsize = (10,8))
        title = 'System at time = ' + str(int(dat_times[index]))
        plt.title(title)
        name = './test_plots/test_plot'+str(counterr).zfill(4)
        
        #plot particles:
        plt.scatter(tmp_x, tmp_y, c = tmp_colors, marker = ".")
        #print(np.max(tmp_theta), np.min(tmp_theta))
        plt.clim(-np.pi, np.pi)
        plt.colorbar()

        #plot dogs
        for dd in range(ndogs):
            tag = "Dog" + str(dd)
            plt.plot(x_dogs[index,dd],y_dogs[index,dd], 'x', label = tag)
        plt.plot(np.average(tmp_x),np.average(tmp_y), 'yo', label = "Herd CM") #herd CM
        plt.plot(x_target, y_target, 'go', label = "Target")

        #plot fence
        if fence ==1: 
            plt.plot(xt_array,xwall,'r--')
            plt.plot(ywall, yt_array,'r--')

        #plt characteristics    
        plt.legend()
        plt.xlim(-L,L)
        #plt.xlim(-2,26)
        plt.ylim(-L,L)
        #plt.ylim(-4,4)
        plt.savefig(name)
    if t%modder ==0:
      print("Currently saving plot # ", t, "out of", timesteps )

t1 = time.time()

print("Total time to make and save plots is", t1-t0)

#make movie
make_movie()





