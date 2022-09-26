#python3
#import libraries-------------------------------------------------------
import numpy as np
import matplotlib.pyplot as plt
plt.rcParams.update({'figure.max_open_warning': 0})
import time
import os
from auxiliary_functions import *
import seaborn as sns
#from scipy.fft import fft, fftfreq
#testing the complex exponential version of this
import cmath
#sns.set()
sns.set_style('white')
from scipy.signal import savgol_filter


start = time.time()


#-------------BEGIN LOAD DATA-------------------------------------------------------------

for selector in range(3):
	print(selector)
	#set_up_directories
	parent_folder = '/Users/adityaranganathan/Dropbox/Harvard_Research/repos/herding_parent/herding_new/SI_videos/'
	sub_folders = ['droving_slow', 'mustering_slow', 'driving']
	archived_sub_folders = ['droving', 'mustering']
	change_dir_to = parent_folder + sub_folders[selector]
	os.chdir(change_dir_to)


	#load the parameter files

	L = 6 #size of domain to plot
	dt = 0.05 #manually setting the timestep size (should eventually be grabbed from load_params_auto)

	#start timing
	t0 = time.time()

	#import data files
	dat_field = np.loadtxt('data.txt') #x,y position data for herd and dogs
	#dat_field = np.loadtxt('driving_data_SIVid.txt') #x,y position data for herd and dogs

	#load info from parameter file
	driving_on, x_target, y_target, vs, vd, ls, ld, fence, num_particles, ndogs, modder = load_params_auto('params.txt')

	#load info from data file
	xpart, ypart, thetapart, x_dogs, y_dogs, dat_times, timesteps, times, = load_data(dat_field, num_particles)


	#sanity checks
	sanity_checks(dat_field, num_particles, ndogs, timesteps)

	#temporary function to load the data from the costdata file
	costdata_full_array = np.loadtxt('costdata.txt')
	l4_norm  = costdata_full_array[:,3]



	#-------begin theta extraction----------------------------------

	tComplex = np.zeros((len(thetapart), 2))
	tComplex_avg = np.zeros((timesteps, 2))
	dtComplex_avg = np.zeros((timesteps, 2))
	Theta_extract_avg = np.zeros(timesteps)
	ThetaDot_extract_avg = np.zeros(timesteps)

	#setup complex theta_arrays
	for pp in range(len(thetapart)):
	    tComplex[pp,0] = np.cos(thetapart[pp])
	    tComplex[pp,1] = np.sin(thetapart[pp])

	#take the average of theta over the agents
	for kk in range(timesteps):
	    index = num_particles*kk
	    temp_theta_Complex = tComplex[index:index+num_particles, :]
	    tComplex_avg[kk, :] = np.array([np.average(temp_theta_Complex[:,0]), 
	                                    np.average(temp_theta_Complex[:,1])])
	    dtComplex_avg[kk] = tComplex_avg[kk] - tComplex_avg[kk-1]

	    #extract theta and theta-dot
	    Theta_extract_avg[kk] = np.arctan2(tComplex_avg[kk, 1], tComplex_avg[kk, 0])#%(2*np.pi)
	    
	    ThetaDot_extract_avg[kk] = dtComplex_avg[kk,1]*tComplex_avg[kk, 0]
	    -dtComplex_avg[kk, 0]*tComplex_avg[kk,1]


	filter_Theta_extract_avg = savgol_filter(Theta_extract_avg, 101, 3)    
	filter_ThetaDot_extract_avg = savgol_filter(ThetaDot_extract_avg, 101, 3)


	if selector==0:
		#store the good data for use in the combined plots--DROVING ONLY
		droving_theta_1_stored = filter_Theta_extract_avg
		droving_dtheta_1_stored = filter_ThetaDot_extract_avg
	

	elif selector==1:
		#store the good data for use in the combined plots--MUSTERING ONLY
		mustering_theta_1_stored = filter_Theta_extract_avg #np.fmod(-1*Theta_extract_avg[6000:6300], 2*np.pi)
		mustering_dtheta_1_stored = ThetaDot_extract_avg #ThetaDot_extract_avg[6000:6300]


	# store and select the data for each case
	elif selector==2:
		#store the good data for use in the combined plots--MUSTERING ONLY
		driving_theta_1_stored = filter_Theta_extract_avg #Theta_extract_avg[100:300]
		driving_dtheta_1_stored = filter_ThetaDot_extract_avg #ThetaDot_extract_avg[100:300]


	else:
		print("No selector chosen")




#-------------------BEGIN PLOTTING-----------------------------------------------------

#data selection



plt.figure(figsize = (18,18))
#plt.title('$ \dot \Theta$ vs $\Theta$')

ls_all = 0.3

must_shift = np.average(np.fmod(-1*mustering_theta_1_stored, 2*np.pi))
drove_shift = np.average(droving_theta_1_stored)
drive_shift = np.average(driving_theta_1_stored)

plt.plot(driving_theta_1_stored-drive_shift, ls_all/3.0*driving_dtheta_1_stored/0.2, '.', label = 'driving') #driving case 1
plt.plot(droving_theta_1_stored - drove_shift, ls_all*droving_dtheta_1_stored/1.3, '--', label = 'droving') #droving
plt.plot(np.fmod(-1*mustering_theta_1_stored+np.pi, 2*np.pi)-must_shift, ls_all*mustering_dtheta_1_stored/0.4, '.', label = 'mustering') 




plt.legend(fontsize=30)
plt.title("Angular Velocity vs Average Herd Orientation", fontsize = 35)
plt.xlabel("$\Theta$", fontsize=35)
plt.ylabel("$ \dot \Theta$", fontsize=35)
plt.ylim(-0.03, 0.03)
plt.xlim(-1*np.pi, 1*np.pi)
plt.xticks(fontsize=25)
plt.yticks(fontsize=25)
plt.savefig("combined_theta_vs_thetadot_1.png")
plt.show()

#-------------------END PLOTTING------------------------------------------------------

end=time.time()

print("Total time to run was ", end-start)






