#python3

#import libraries
import numpy as np
import matplotlib.pyplot as plt
plt.rcParams.update({'figure.max_open_warning': 0})
import time
import os
from auxiliary_functions import *

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


#calculate mean sheep trajectory
xmeans = np.zeros(timesteps)
ymeans = np.zeros(timesteps)

#plot the trajectories
print('plotting trajectory')
alpha = 1
for i in range(timesteps):
    alpha = alpha -.9/timesteps
    index = num_particles*i
    tmp_x = xpart[index: index+num_particles]
    tmp_y = ypart[index: index+num_particles]
    xmeans[i] = np.mean(tmp_x)
    ymeans[i] = np.mean(tmp_y)

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


#calculate dog trajectory at each time step
xdogs = x_dogs[::num_particles][:-1]
ydogs = y_dogs[::num_particles][:-1]




#store variables
xs, ys, zs = colored_line(xmeans, ymeans, 0, linewidth = .5);
xd, yd, zd = colored_line(xdogs, ydogs, 1, linewidth = .2)

# make the plots
fig, ax = plt.subplots(figsize = (15,10))
ax.pcolormesh(xs, ys, zs, shading='gouraud', cmap='Blues', label = 'Sheep')
ax.pcolormesh(xd, yd, zd, shading='gouraud', cmap='Greys', label = 'Dogs')
ax.scatter(x_target, y_target, c = 'Orange', marker = 'D', s = 50, label = 'target')
alpha = 1
c_index = 0 #variable to select a color as a function of time


#set max time
maxtime = timesteps;

for i in range(int(maxtime)):
    index = num_particles*i
    tmp_x = xpart[index: index+num_particles]
    tmp_y = ypart[index: index+num_particles]
    if i%int(maxtime/3) == 0:
        if c_index ==0: 
            color = 'Purple'
        if c_index ==1:
            color = 'Cyan'
        if c_index ==2:
            color = 'Red'
        ax.scatter(tmp_x,tmp_y, c = color, s = 2, label = 'sheep at time '+ str(i))
        ax.scatter(x_dogs[index],y_dogs[index], c = color, s = 100, marker = '^', label = 'dog at time '+ str(i) )
        c_index +=1

    if i == maxtime-1:
        ax.scatter(tmp_x,tmp_y, c = 'Blue', s = 2, label = 'sheep at time '+ str(i))
        ax.scatter(x_dogs[index],y_dogs[index], c = 'Blue', s = 100, marker = '^', label = 'dog at time '+ str(i) )

ax.legend()
plt.title('Trajectories over time')
plt.xlabel('x motion')
plt.ylabel('y motion')
plt.xlim(-L,L)
plt.ylim(-L,L)
#plt.show()
plt.savefig('output_plot.pdf')

