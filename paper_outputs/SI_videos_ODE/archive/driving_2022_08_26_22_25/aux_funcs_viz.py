import os
from collections import OrderedDict
import numpy as np
import matplotlib.pyplot as plt
from aux_funcs import *

def plot_herd_snapshot(temp_H, curr_time, temp_counterr, loc_arrays, traj_array = [0,0,0]):

  '''
  Q=a/b; a = Q*b; a = A/(pi*b). => Qb = A/(pi*b) ==> b = sqrt(A/(pi*Q))

  Q = aR/b; A = pi*aRb ==>  Qb/R = A/(pi*R*b) ==> b = sqrt(A/Qpi) AND a = Qb/R
  '''

  model_2 = False


  x_shift = traj_array[0]
  y_shift = traj_array[1]
  theta_shift = traj_array[2]

  #parameters
  R = temp_H[0]
  if model_2 == True:
    b = np.sqrt(temp_H[5]/(np.pi*temp_H[4])) #(trying the new definition of the `ellipse')
    a = temp_H[4]*b
  else:
    #b = np.sqrt(temp_H[5]/(np.pi*temp_H[4]*temp_H[0]))
    b = np.sqrt(temp_H[5]/(np.pi*temp_H[4]))

    a = temp_H[4]*b/temp_H[0]
  
  # a = temp_H[4]*b
  theta = temp_H[1]+theta_shift +np.pi#modifying theta to deal with any rotations in the prescribed/overlayed herd trajectory

  #print("R, b, a, theta: ", R, " , ", b, " , ", " , ", a, " , ", theta)
  #print("R, b, a, theta: ", R, " , ", b, " , ", " , ", a, " , ", theta)


  #set arrays

  if model_2 == True:
    a_scale = 0.01/R
    phi_array = np.arange(-a/R+a_scale, a/R-a_scale, a_scale)
  else:
    phi_array = np.arange(-a, a, 0.001)

  #phi_array = np.arange(-a/R, a/R, 0.001/R)*R #<---------DON'T USE THIS ONE!!
  r_array_1 = np.zeros(len(phi_array))
  r_array_2 = np.zeros(len(phi_array))

  #create shape
  for kk in range(len(phi_array)):
    if model_2 == True:
      r_array_1[kk] = R+b*np.sqrt(1-(phi_array[kk]*R)**2/a**2)
      r_array_2[kk] = R-b*np.sqrt(1-(phi_array[kk]*R)**2/a**2)
    else:
      r_array_1[kk] = R+b*np.sqrt(1-(phi_array[kk])**2/a**2)
      r_array_2[kk] = R-b*np.sqrt(1-(phi_array[kk])**2/a**2)

  phi_array_sum = np.concatenate((phi_array, phi_array))
  r_array_sum = np.concatenate((r_array_1, r_array_2))


  x = np.array([np.cos(phi_array_sum[kk])*r_array_sum[kk] for kk in range(len(r_array_sum))])
  y = np.array([np.sin(phi_array_sum[kk])*r_array_sum[kk] for kk in range(len(r_array_sum))])

  x_centered = x - R
  y_centered = y

  theta_rot = theta#+np.pi
  x_rot = np.array([np.cos(theta_rot)*x_centered[ii]-np.sin(theta_rot)*y_centered[ii] for ii in range(len(x))])
  y_rot = np.array([np.sin(theta_rot)*x_centered[ii]+np.cos(theta_rot)*y_centered[ii] for ii in range(len(x))])



  x_rot_corr = np.cos(theta_rot)*R
  y_rot_corr = np.sin(theta_rot)*R

  #---------------------------plotting in the herd frame------------------------------------

  theta_dog_plot = theta
  r_dog_plot = -1.0*R

  x_dog = r_dog_plot*np.cos(theta_dog_plot)+x_shift
  y_dog = r_dog_plot*np.sin(theta_dog_plot)+y_shift

  loc_arrays.append([x_dog, y_dog, x_shift, y_shift])


  #-----------------------------DEFINE FIGURE HERE-------------------------------------------
  max_plot_radius = 20

  fig = plt.figure(figsize = (16,8))
  ax1 = fig.add_subplot(122, projection = 'polar')
  ax2 = fig.add_subplot(121)
  #ax3 = fig.add_subplot(221)

  title = 'System at time = ' + str(curr_time)
  fig.suptitle(title)
  plot_name = './test_plots/test_plot'+str(temp_counterr).zfill(4)


  #plot from the Dog Frame
  ax1.plot(phi_array_sum+theta, r_array_sum, '.', label = 'herd (polar)')
  ax1.plot(0,0, 'ro', markersize = 5, label = 'dog position')
  ax1.set_ylim(0, max_plot_radius) #only use this one for polar
  ax1.legend(loc='upper left')



  #Plot from the herd frame
  ax2.plot(x_rot+x_shift, y_rot+y_shift, '.', label = 'herd (x,y), with rotation')
  ax2.plot(x_dog, y_dog, 'rx', label = 'dog')
  ax2.set_ylim(-max_plot_radius, max_plot_radius)
  ax2.set_xlim(-max_plot_radius, max_plot_radius)
  ax2.legend(loc='upper right')
  tmp_x_array = np.array([loc_arrays[tt][0] for tt in range(len(loc_arrays))])
  tmp_y_array = np.array([loc_arrays[tt][1] for tt in range(len(loc_arrays))])
  xd, yd, zd = colored_line(tmp_x_array[-500:], tmp_y_array[-500:], 1, linewidth = .2)
  ax2.pcolormesh(xd, yd, zd, shading='gouraud', cmap='Greys', label = 'Dogs', alpha = 0.2)
  ax2.plot(-15.0, 15.0, 'gD', markersize = 20, label = "Target")
  #ax2.grid()



  # fig.legend()
  fig.savefig(plot_name)


  return loc_arrays



def plot_herd_movie(filename):

  os.system("mv output_movie.mp4 old_output_movie.mp4")

  timesteps, dt, lR, lT, lA, lQ, f0, ls, gamma, omega, zeta, alpha, beta, delta, A0, Q0, ThetaGoal, modder, H, uR_mag, uT_mag, sample_number = load_params_auto()

  loc_arrays = []

  # H = [R, T, R', T', Q, A] // T = 'Theta'

  trajectory_data = np.loadtxt("traj.in")

  print("Shape of trajectory data: ", np.shape(trajectory_data))

  data = np.loadtxt(filename)
  temp_counterr = 0

  times = data[:,0]
  max_time = int(np.max(times))

  #print(max_time)


  for kk in range(max_time):

    if kk%modder == 0:
      temp_H = data[kk, 1:7]

      temp_traj_array = trajectory_data[:, kk]

      #print("Temp H at time ", kk, ": ", temp_H)
      loc_arrays = plot_herd_snapshot(temp_H, kk, temp_counterr, loc_arrays, traj_array = temp_traj_array)
      #loc_arrays = plot_herd_snapshot(temp_H, kk, temp_counterr, loc_arrays)
      #plot_herd_snapshot(temp_H, kk, temp_counterr)

      temp_counterr +=1


  make_movie()


def make_movie():
  '''
  This function converts the images saved in a temp folder to an mp4 movie using ffmpeg. 

  The name is hardcoded here, but should eventually be changed to be moplar (and so two make_movie functions are no longer required)
  '''

  #hardcoded name for the output movie file
  print("Making a movie! Movie will be called 'output_movie.mp4'") 
  
  #run ffmpeg
  os.system("ffmpeg -loglevel panic -y -r 15 -f image2 -s 1920x1080 -start_number 0 -i ./test_plots/test_plot%04d.png -vframes 1000 -vcodec libx264 -crf 10  -pix_fmt yuv420p output_movie.mp4")
  
  #clear the saved images from temp folder
  print("Movie made...clearing individual plots")
  os.system('rm test_plots/*') #hardcoded temp folder name
  
  #open the created movie
  os.system("open output_movie.mp4")



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




