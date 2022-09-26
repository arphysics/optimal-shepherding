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







#----------------colored line bit------------------------------


def colored_line(x, y, lab, z=None, linewidth=1, MAP='jet'):
    # this uses pcolormesh to make interpolated rectangles
    xl = len(x)
    [xs, ys, zs] = [np.zeros((xl,2)), np.zeros((xl,2)), np.zeros((xl,2))]

    # z is the line length drawn or a list of vals to be plotted
    if z == None:
        z = [0]

    for i in range(xl-1):
        # make a vector to thicken our line points
        dx = x[i+1]-x[i]
        dy = y[i+1]-y[i]
        perp = np.array( [-dy, dx] )
        unit_perp = (perp/np.linalg.norm(perp))*linewidth

        # need to make 4 points for quadrilateral
        xs[i] = [x[i], x[i] + unit_perp[0] ]
        ys[i] = [y[i], y[i] + unit_perp[1] ]
        xs[i+1] = [x[i+1], x[i+1] + unit_perp[0] ]
        ys[i+1] = [y[i+1], y[i+1] + unit_perp[1] ]

        if len(z) == i+1:
            z.append(z[-1] + (dx**2+dy**2)**0.5)     
        # set z values
        zs[i] = [z[i], z[i] ] 
        zs[i+1] = [z[i+1], z[i+1] ]
        
    return xs, ys, zs


#--------------------end def of colored line function----------


#clear folders before saving
print("Pre-Clearing directory test_plots")
os.system('rm test_plots/*')
print("Now saving plots in directory 'test_plots'")


#plot the fence boundary
if fence == 1:
    xwall, ywall, xt_array, yt_array = plot_fence(L, x_target, y_target, ld)

counterr = 0
for t in range(timesteps):
#for t in range(10):

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


        
        fig, (ax2, ax1) = plt.subplots(1,2, figsize = (16,8))
        ax1.set_aspect('equal')
        ax2.set_aspect('equal')
        title = 'System at time = ' + str(int(dat_times[index]))
        fig.suptitle(title)
        name = './test_plots/test_plot'+str(counterr).zfill(4)
        
        
        #set colormap----------------------

        #figure out the right size
        scale_sheep = 5*np.std(tmp_x)
        scale_dog = 1.2*np.sqrt((x_dogs[index, 0]-x_avg)**2 + (y_dogs[index, 0]-y_avg)**2) #hardcoded for 1 dog

        scale = np.max([scale_dog, scale_sheep])
        #---------------


        #-----------make CLONE VIEW----------------------------------


        clone_view = 1
        if clone_view == True:
            #generate color-map-------------------
            angle_array = np.linspace(-np.pi, np.pi, 500)
            #angle_array = [ii - tmp_target_angle for ii in angle_array]
            x_offset = scale-scale/4
            y_offset = scale-scale/4
            x_colors_p = scale/5*np.cos(angle_array)
            y_colors_p = scale/5*np.sin(angle_array)


            x_colors = x_colors_p*np.cos(tmp_herd_dog_angle)-y_colors_p*np.sin(tmp_herd_dog_angle)+x_offset
            y_colors = y_colors_p*np.cos(tmp_herd_dog_angle)+x_colors_p*np.sin(tmp_herd_dog_angle)+y_offset

            angle_colors = [colorator(p) for p in angle_array]
            ax1.scatter(x_colors, y_colors, color = angle_colors)


            ax1.scatter(tmp_x_2, tmp_y_2, c = tmp_theta, marker = ".")

            #plot dogs
            for dd in range(ndogs):
                tag = "Dog" + str(dd)
                #plt.plot(x_dogs[index,dd],y_dogs[index,dd], 'x', label = tag)

                x_dogs_2 = (x_dogs[index,dd]-rot_x_center)*np.cos(tmp_herd_dog_angle)-(y_dogs[index,dd]-rot_y_center)*np.sin(tmp_herd_dog_angle)
                y_dogs_2 = (y_dogs[index,dd]-rot_y_center)*np.cos(tmp_herd_dog_angle)+(x_dogs[index,dd]-rot_x_center)*np.sin(tmp_herd_dog_angle)


                ax1.plot(x_dogs_2,y_dogs_2, 'kX', markersize = 10, label = tag)
            

            #plot target
            #plt.plot(x_target, y_target, 'go', label = "Target")

            x_target_2 = (x_target-rot_x_center)*np.cos(tmp_herd_dog_angle)-(y_target-rot_y_center)*np.sin(tmp_herd_dog_angle)
            y_target_2 = (y_target-rot_y_center)*np.cos(tmp_herd_dog_angle)+(x_target-rot_x_center)*np.sin(tmp_herd_dog_angle)

            ax1.plot(x_target_2, y_target_2, 'gD', markersize = 20, label = "Target")

            
            #plot some shading in the clone view
            #hardcoded for one dog
            hist_time = 500
            blah = t+1
            if t > hist_time:
                early_timestep = blah-hist_time
            else:
                early_timestep = 0
            xdogs = x_dogs[::num_particles][early_timestep:blah]
            ydogs = y_dogs[::num_particles][early_timestep:blah]

            xdogs_clone = (xdogs-rot_x_center)*np.cos(tmp_herd_dog_angle)-(ydogs-rot_y_center)*np.sin(tmp_herd_dog_angle)
            ydogs_clone = (ydogs-rot_y_center)*np.cos(tmp_herd_dog_angle)+(xdogs-rot_x_center)*np.sin(tmp_herd_dog_angle)


            xd, yd, zd = colored_line(xdogs_clone, ydogs_clone, 1, linewidth = .02)

            #ax2.pcolormesh(xs, ys, zs, shading='gouraud', cmap='Blues', label = 'Sheep')
            ax1.pcolormesh(xd, yd, zd, shading='gouraud', cmap='Greys', label = 'Dogs', alpha = 0.2)


            #plt characteristics    
            #plt.legend()
            ax1.set_xlim(-1.5*scale,1.5*scale)
            ax1.set_ylim(-1.5*scale,1.5*scale)
            ax2.set_xlim(-L,3)
            ax2.set_ylim(-3,L)




        #---------------MAKE DRONE VIEW-----------------------

        drone_view = 1


        if drone_view == True:



            #-------------COLORED MESH----------------------
            #store variables

            #xmeans
            #xs, ys, zs = colored_line(xmeans, ymeans, 0, linewidth = scale/10);

            #hardcoded for one dog
            blah = t+1
            xdogs = x_dogs[::num_particles][:blah]
            ydogs = y_dogs[::num_particles][:blah]


            xd, yd, zd = colored_line(xdogs, ydogs, 1, linewidth = .05)

            #ax2.pcolormesh(xs, ys, zs, shading='gouraud', cmap='Blues', label = 'Sheep')
            ax2.pcolormesh(xd, yd, zd, shading='gouraud', cmap='Greys', label = 'Dogs', alpha = 0.2)

            tmp_herd_dog_angle = 0*np.arctan2(y_target-y_avg, x_target-x_avg)

            #plots the center of mass
            ax2.plot(x_avg,y_avg, 'r.', markersize = 3, label = "Herd CM") #herd CM

            angle_array = np.linspace(-np.pi, np.pi, 500)
            #angle_array = [ii - tmp_target_angle for ii in angle_array]
            x_offset = 1.75
            y_offset = 5.0
            x_colors_p = 0.75*np.cos(angle_array)
            y_colors_p = 0.75*np.sin(angle_array)


            x_colors = x_colors_p*np.cos(tmp_herd_dog_angle)-y_colors_p*np.sin(tmp_herd_dog_angle)+x_offset
            y_colors = y_colors_p*np.cos(tmp_herd_dog_angle)+x_colors_p*np.sin(tmp_herd_dog_angle)+y_offset

            angle_colors = [colorator(p) for p in angle_array]
            ax2.scatter(x_colors, y_colors, color = angle_colors)



            #plot the data
            ax2.scatter(tmp_x, tmp_y, c = tmp_theta, marker = ".")

            #make the box

            tmp_herd_dog_angle = (np.pi/2-np.arctan2(y_target, x_target))

            tmp_box_lines = np.linspace(-1,1, 100)
            tmp_box_zero = np.zeros(100)
            
            tmp_box_lines_x = tmp_box_lines+x_avg
            tmp_box_lines_y = tmp_box_zero+y_avg

            tmp_x_box_top = scale*((tmp_box_lines_x-x_avg)*np.cos(tmp_herd_dog_angle)-(tmp_box_lines_y+1-y_avg)*np.sin(tmp_herd_dog_angle))
            tmp_y_box_top = scale*((tmp_box_lines_y+1-y_avg)*np.cos(tmp_herd_dog_angle)+(tmp_box_lines_x-x_avg)*np.sin(tmp_herd_dog_angle))

            tmp_x_box_bot = scale*((tmp_box_lines_x-x_avg)*np.cos(tmp_herd_dog_angle)-(tmp_box_lines_y-1-y_avg)*np.sin(tmp_herd_dog_angle))
            tmp_y_box_bot = scale*((tmp_box_lines_y-1-y_avg)*np.cos(tmp_herd_dog_angle)+(tmp_box_lines_x-x_avg)*np.sin(tmp_herd_dog_angle))

            
            tmp_box_lines_y_2 = tmp_box_lines+y_avg
            tmp_box_lines_x_2 = tmp_box_zero+x_avg


            tmp_x_box_right = scale*((tmp_box_lines_x_2+1-x_avg)*np.cos(tmp_herd_dog_angle)-(tmp_box_lines_y_2-y_avg)*np.sin(tmp_herd_dog_angle))
            tmp_y_box_right = scale*((tmp_box_lines_y_2-y_avg)*np.cos(tmp_herd_dog_angle)+(tmp_box_lines_x_2+1-x_avg)*np.sin(tmp_herd_dog_angle))

            tmp_x_box_left = scale*((tmp_box_lines_x_2-1-x_avg)*np.cos(tmp_herd_dog_angle)-(tmp_box_lines_y_2-y_avg)*np.sin(tmp_herd_dog_angle))
            tmp_y_box_left = scale*((tmp_box_lines_y_2-y_avg)*np.cos(tmp_herd_dog_angle)+(tmp_box_lines_x_2-1-x_avg)*np.sin(tmp_herd_dog_angle))


            ax2.plot(tmp_x_box_top+x_avg, tmp_y_box_top+y_avg, 'k--', alpha = 0.25)
            ax2.plot(tmp_x_box_bot+x_avg, tmp_y_box_bot+y_avg, 'k--', alpha = 0.25)
            ax2.plot(tmp_x_box_right+x_avg, tmp_y_box_right+y_avg, 'k--', alpha = 0.25)
            ax2.plot(tmp_x_box_left+x_avg, tmp_y_box_left+y_avg, 'k--', alpha = 0.25)

            #plot dogs
            for dd in range(ndogs):
                tag = "Dog" + str(dd)
                ax2.plot(x_dogs[index,dd],y_dogs[index,dd], 'kX', markersize = 10, label = tag)
        

            #plot target
            ax2.plot(x_target, y_target, 'gD', markersize = 20, label = "Target")



        fig.savefig(name)
    
    if t%modder ==0:
      print("Currently saving plot # ", t, "out of", timesteps )

t1 = time.time()

print("Total time to make and save plots is", t1-t0)

#make movie
make_movie_clone()





