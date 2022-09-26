#import elements
#import numpy as np
#import matplotlib.pyplot as plt
import os
from herd_ODE_class import *
from visualizer import *
import time
from datetime import datetime
from aux_funcs_viz import *
plt.rcParams.update({'figure.max_open_warning': 0})


if __name__ == '__main__':

	to = time.time()
	
	herd = ODE_Herd() #can later convert this to take in input/init parameters

	herd.initialize_simulation()

	herd.dump_data_to_file()

	#herd.plot_herd(0)
	

	for tt in range(1, herd.timesteps):

		herd.current_time = tt #set the internal class variable to the current time
		#print("currently simulating timestep ", herd.current_time)

		#----------------------adding in the optimization and sampling---------------------

		herd.cost_sampling_1() #this version uses both uR and uT
		#herd.cost_sampling_2() #this version only controls uT


		#----------------------end optimization and sampling-----------------------------

		temp_vector = herd.rk4_update(control = herd.dog_velocities)
		herd.H = temp_vector

		herd.theta_dog = herd.update_dog()

		# temp_vector = herd.rk4_update()
		# herd.H = temp_vector

		herd.dump_data_to_file()

		# if tt%herd.modder == 0:
		# 	herd.plot_herd(tt)

		#herd.calculate_cost()

		if herd.sanity_checks() == 1:
			break


	tf = time.time()

	print("Total time to run main = ", tf-to)

	#make_movie()


	tom = time.time()
	generate_trajectory_test()
	# plot_herd_movie("data.out")

	tfm = time.time()

	print("Total time to create movie = ", tfm-tom)







