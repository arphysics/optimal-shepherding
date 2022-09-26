#python3

'''
I do believe this code works!! And this should be the formulation that is finally used...but this comment 
needs to be checked. 08/09/21 --A.R. 


'''


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


#--------------------end def of colored line function----------


#clear folders before saving
print("Pre-Clearing directory test_plots")
os.system('rm test_plots/*')
print("Now saving plots in directory 'test_plots'")


#set up necessary arrays
avg_polarization_1 = np.zeros(timesteps)
std_polarization_1 = np.zeros(timesteps)
temp_time_counter_1 = np.zeros(timesteps)
n_std_width = 2.0
#error_up_1 = []
#error_down_1 = []


counterr = 0
for t in range(timesteps):
#for t in range(10):

#fork here
#for t in range(0,100):
    if t%modder == 0:
        
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

        #plot herd CM
        x_avg = np.average(tmp_x)
        y_avg = np.average(tmp_y)

        #dog-herd angle
        tmp_herd_dog_angle = (np.pi/2-np.arctan2(y_target-y_avg, x_target-x_avg))
        #tmp_herd_dog_angle = -np.pi/6

        rot_x_center = x_avg
        rot_y_center = y_avg


        #rotate positions about x_avg and y_avg
        tmp_x_2 = (tmp_x-rot_x_center)*np.cos(tmp_herd_dog_angle)-(tmp_y-rot_y_center)*np.sin(tmp_herd_dog_angle)
        tmp_y_2 = (tmp_y-rot_y_center)*np.cos(tmp_herd_dog_angle)+(tmp_x-rot_x_center)*np.sin(tmp_herd_dog_angle)


        
        fig, (ax1, ax2) = plt.subplots(1,2, figsize = (24,12))
        ax1.set_aspect(timesteps/2.0)
        ax2.set_aspect(2.0/num_particles)
        title = 'System at time = ' + str(int(dat_times[index]))
        fig.suptitle(title)
        name = './test_plots/test_plot'+str(counterr+1).zfill(4)

        
        
        #set colormap----------------------
        #---------------


        #-----------make polarization plots----------------------------------
        #print(counterr)
        avg_polarization_1[counterr] = np.average(np.cos(tmp_theta))
        std_polarization_1[counterr] = np.std(np.cos(tmp_theta))
        temp_time_counter_1[counterr] = t
        tmp_error_up = avg_polarization_1[:counterr] + n_std_width*std_polarization_1[:counterr]
        tmp_error_down = avg_polarization_1[:counterr] - n_std_width*std_polarization_1[:counterr]

        ax1.fill_between(temp_time_counter_1[:counterr], tmp_error_down, tmp_error_up, alpha=0.5, edgecolor='k', facecolor='#7EFF99', label = '2 std bound')
        ax1.plot(temp_time_counter_1[:counterr], avg_polarization_1[:counterr], 'red', label = 'average polarization')
        ax1.legend()
        ax1.set_ylim(-1.5, 1.5)
        ax1.set_xlim(0, timesteps)
        ax1.set_xlabel('time')
        ax1.set_ylabel('average polarization (cos(theta))')
        ax1.title.set_text('Polarization over time')



        #---------------MAKE HISTOGRAM PLOTS-----------------------
        ax2.hist(np.cos(tmp_theta))
        ax2.set_xlim(-1.5, 1.5)
        ax2.set_ylim(0, num_particles)
        ax2.title.set_text("Histogram of orientations over time")
        ax2.set_ylabel('count')
        ax2.set_xlabel('polarization {cos(theta)}')



        fig.savefig(name)

        counterr +=1
    
    if t%modder ==0:
      print("Currently saving plot # ", t, "out of", timesteps )

t1 = time.time()

print("Total time to make and save plots is", t1-t0)

#----------MAKE MOVIE

#hardcoded name for the output movie file
print("Making a movie! Movie will be called 'output_movie_polarization.mp4'") 

#run ffmpeg
os.system("ffmpeg -loglevel panic -y -r 15 -f image2 -s 1920x1080 -start_number 1 -i ./test_plots/test_plot%04d.png -vframes 1000 -vcodec libx264 -crf 10  -pix_fmt yuv420p output_movie_polarization.mp4")

#clear the saved images from temp folder
print("Movie made...clearing individual plots")
os.system('rm test_plots/*') #hardcoded temp folder name

#open the created movie
os.system("open output_movie_polarization.mp4")



