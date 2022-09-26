#python3

#import libraries
import numpy as np
import matplotlib.pyplot as plt
plt.rcParams.update({'figure.max_open_warning': 0})
import time
import os
from auxiliary_functions import *


#set user defined parameters

L = 6 #size of domain to plot

#start timing
t0 = time.time()

#import data files
dat_field = np.loadtxt('data.txt') #x,y position data for herd and dogs

#load info from parameter file
driving_on, x_target, y_target, vs, vd, ls, ld, fence, num_particles, ndogs, modder = load_params_auto('params.txt')

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
#for t in range(200):

#fork here
#for t in range(0,100):
    if t%modder == 0:
        counterr +=1
        
        #download particle data
        index = num_particles*t
        tmp_x = xpart[index: index+num_particles]
        tmp_y = ypart[index: index+num_particles]
        tmp_theta = thetapart[index: index+num_particles]


        #calculate the angle between the target and the dog (ONLY FOR 1 DOG)
        tmp_target_angle = np.arctan2(y_target-y_dogs[index,0], x_target-x_dogs[index,0])

        # set color info
        tmp_colors = tmp_theta - tmp_target_angle#%(2*np.pi) #colorator(tmp_theta)
        #print(np.max(tmp_colors), np.min(tmp_colors))
        #tmp_colors = np.transpose(tmp_colors)

        # plt.figure(figsize = (10,8))
        # title = "histogram at time = " + str(int(dat_times[index]))
        # plt.title(title)
        # plt.hist(tmp_colors)
        # name2 = str(t)+"_theta_pdf"
        # plt.savefig(name2)

        #plot herd CM
        x_avg = np.average(tmp_x)
        y_avg = np.average(tmp_y)

        plt.plot(x_avg,y_avg, y_avg, 'yo', label = "Herd CM") #herd CM

        plt.figure(figsize = (10,8))
        title = 'System at time = ' + str(int(dat_times[index]))
        plt.title(title)
        name = './test_plots/test_plot'+str(counterr).zfill(4)
        
        # # #plot particles:
        plt.scatter(tmp_x, tmp_y, c = tmp_theta, marker = ".")
        #print(np.max(tmp_theta), np.min(tmp_theta))
        plt.clim(-np.pi, np.pi)
        plt.colorbar()

        #plot an arrow for the standard deviation--------------------------------------------------
        #average_orientation = np.average(tmp_theta)
        #plt.quiver(x_avg, y_avg, np.cos(average_orientation), np.sin(average_orientation))

        #generate color-map-------------------
        #tmp_herd_dog_angle = (np.pi/2-np.arctan2(y_target, x_target))
        tmp_herd_dog_angle = 0*np.arctan2(y_target-y_avg, x_target-x_avg)

        angle_array = np.linspace(-np.pi, np.pi, 500)
        #angle_array = [ii - tmp_target_angle for ii in angle_array]
        x_offset = 2.0
        y_offset = 4.0
        x_colors_p = 0.75*np.cos(angle_array)
        y_colors_p = 0.75*np.sin(angle_array)


        x_colors = x_colors_p*np.cos(tmp_herd_dog_angle)-y_colors_p*np.sin(tmp_herd_dog_angle)+x_offset
        y_colors = y_colors_p*np.cos(tmp_herd_dog_angle)+x_colors_p*np.sin(tmp_herd_dog_angle)+y_offset

        angle_colors = [colorator(p) for p in angle_array]
        plt.scatter(x_colors, y_colors, color = angle_colors)



        #plot bounding box

        #dog-herd angle
        tmp_herd_dog_angle = (np.pi/2-np.arctan2(y_target, x_target))

        tmp_box_lines = np.linspace(-1,1, 100)
        tmp_box_zero = np.zeros(100)
        
        tmp_box_lines_x = tmp_box_lines+x_avg
        tmp_box_lines_y = tmp_box_zero+y_avg

        tmp_x_box_top = (tmp_box_lines_x-x_avg)*np.cos(tmp_herd_dog_angle)-(tmp_box_lines_y+1-y_avg)*np.sin(tmp_herd_dog_angle)
        tmp_y_box_top = (tmp_box_lines_y+1-y_avg)*np.cos(tmp_herd_dog_angle)+(tmp_box_lines_x-x_avg)*np.sin(tmp_herd_dog_angle)

        tmp_x_box_bot = (tmp_box_lines_x-x_avg)*np.cos(tmp_herd_dog_angle)-(tmp_box_lines_y-1-y_avg)*np.sin(tmp_herd_dog_angle)
        tmp_y_box_bot = (tmp_box_lines_y-1-y_avg)*np.cos(tmp_herd_dog_angle)+(tmp_box_lines_x-x_avg)*np.sin(tmp_herd_dog_angle)

        
        tmp_box_lines_y_2 = tmp_box_lines+y_avg
        tmp_box_lines_x_2 = tmp_box_zero+x_avg

        tmp_x_box_right = (tmp_box_lines_x_2+1-x_avg)*np.cos(tmp_herd_dog_angle)-(tmp_box_lines_y_2-y_avg)*np.sin(tmp_herd_dog_angle)
        tmp_y_box_right = (tmp_box_lines_y_2-y_avg)*np.cos(tmp_herd_dog_angle)+(tmp_box_lines_x_2+1-x_avg)*np.sin(tmp_herd_dog_angle)

        tmp_x_box_left = (tmp_box_lines_x_2-1-x_avg)*np.cos(tmp_herd_dog_angle)-(tmp_box_lines_y_2-y_avg)*np.sin(tmp_herd_dog_angle)
        tmp_y_box_left = (tmp_box_lines_y_2-y_avg)*np.cos(tmp_herd_dog_angle)+(tmp_box_lines_x_2-1-x_avg)*np.sin(tmp_herd_dog_angle)

        #print(tmp_x_box)

        plt.plot(tmp_x_box_top+x_avg, tmp_y_box_top+y_avg, 'k--')
        plt.plot(tmp_x_box_bot+x_avg, tmp_y_box_bot+y_avg, 'k--')
        plt.plot(tmp_x_box_right+x_avg, tmp_y_box_right+y_avg, 'k--')
        plt.plot(tmp_x_box_left+x_avg, tmp_y_box_left+y_avg, 'k--')


        #plt.plot(tmp_box_lines_x, tmp_box_lines_y)


        # plt.vlines(x_avg-1, y_avg-1, y_avg+1, colors = 'k', linestyles = 'dashed')
        # plt.vlines(x_avg+1, y_avg-1, y_avg+1, colors = 'k', linestyles = 'dashed')
        # plt.hlines(y_avg-1, x_avg-1, x_avg+1, colors = 'k', linestyles = 'dashed')
        # plt.hlines(y_avg+1, x_avg-1, x_avg+1, colors = 'k', linestyles = 'dashed')



        #plot arrows (quiver)------------------------------------
        # tmp_x_dir = np.cos(tmp_theta)
        # tmp_y_dir = np.sin(tmp_theta)
        # tmp_angles = [colorator(p) for p in tmp_colors]

        # #print(np.shape(tmp_angles))

        # #print(len(tmp_x_dir), len(tmp_y_dir), len(tmp_x), len(tmp_y))

        # plt.quiver(tmp_x, tmp_y, tmp_x_dir, tmp_y_dir, color = tmp_angles)
        # #plt.clim(0, 2*np.pi)
        # #plt.colorbar()



        #generate color-map-------------------
        # angle_array = np.linspace(-np.pi, np.pi, 500)
        # #angle_array = [ii - tmp_target_angle for ii in angle_array]
        # x_offset = 1
        # y_offset = 4
        # x_colors_p = 0.75*np.cos(angle_array)
        # y_colors_p = 0.75*np.sin(angle_array)

        # x_colors = x_colors_p*np.cos(tmp_target_angle)-y_colors_p*np.sin(tmp_target_angle)+x_offset
        # y_colors = y_colors_p*np.cos(tmp_target_angle)+x_colors_p*np.sin(tmp_target_angle)+y_offset

        # angle_colors = [colorator(p) for p in angle_array]
        # plt.scatter(x_colors, y_colors, color = angle_colors)




        #plot dogs
        for dd in range(ndogs):
            tag = "Dog" + str(dd)
            plt.plot(x_dogs[index,dd],y_dogs[index,dd], 'x', label = tag)
        

        #plot target
        plt.plot(x_target, y_target, 'go', label = "Target")

        #plot fence
        if fence ==1: 
            plt.plot(xt_array,xwall,'r--')
            plt.plot(ywall, yt_array,'r--')

        #plt characteristics    
        plt.legend()
        plt.xlim(-L,3)
        #plt.xlim(-2,26)
        plt.ylim(-3,L)
        #plt.ylim(-4,4)
        plt.savefig(name)
    if t%modder ==0:
      print("Currently saving plot # ", t, "out of", timesteps )

t1 = time.time()

print("Total time to make and save plots is", t1-t0)

#make movie
make_movie()





