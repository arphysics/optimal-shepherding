#import elements
import numpy as np
from scipy import *
from aux_funcs import *
import matplotlib.pyplot as plt
from scipy.integrate import odeint
import os
import time
from datetime import datetime
#from aux_funcs_viz import *


# H = [R, T, R', T', Q, A] // T = 'Theta'


class ODE_Herd:

	species = "sheep"

	#timing variables/arrays
	current_time = 0 #stores the current time
	counterr = 0 #variable to count when to plot (this variable is affected by modder!)

	# #testing the import
	print("Importing parameters from param.in")
	timesteps, dt, lR, lT, lA, lQ, f0, ls, gamma, omega, zeta, alpha, beta, delta, A0, Q0, ThetaGoal, modder, H, uR_mag, uT_mag, sample_number = load_params_auto()

	#additional variables 
	theta_dog = 0

	# Q0 = 1.0/H[0] #sets the natural aspect ratio for the herd

	#optimization variables and arrays
	tmp_H = [0,0, 0, 0, 0, 0]
	tmp_system = tmp_H
	dog_velocities = [0,0]
	dog_velocities_tmp = [0,0]
	max_cost = exp(10)
	min_cost = max_cost
	tmp_cost = max_cost
	costdata_array = [0,0,0,0] #4 element cost_function
	final_cost_array = costdata_array #final 4 element cost function


	#other random arrays
	delta_theta_dog = 0
	final_theta_dog = 0
	old_uT = 0

	#derivative has no time dependence
	def dH_dt(self, H_temp=H, control = [0,0]):
		# 	Calculates the derivative of the vector H, which solves the diff. eqn. system dH/dt = f(H,t)
		# 	H = [R, T, R', T', Q, A] // T = 'Theta'
		# 	H_prime = [R', T', R'', T'', Q', A']


		#print("In dH_dt: ", control, "at t = ", self.current_time)

		uT, uR = control
		uT_avg = (uT+self.old_uT)/2.0 #takes the average of the last two values of uT
		force = self.f0*np.exp(-1.0*H_temp[0]/self.ls) #calculates the force

		H_prime = np.zeros(6)

		H_prime[0] = H_temp[2] #(adding in a control term for the dog to affect R')
		H_prime[1] = H_temp[3] #
		H_prime[2] = -1.0*self.lR*H_temp[2]+force-1.0*uR
		H_prime[3] = -1.0*self.lT*(H_temp[3] -1.0*(uT/H_temp[4])) #<--- modify this one
		# H_prime[3] = -1.0*self.lT*(H_temp[3] -1.0*(uT)) #<--- modify this one
		H_prime[4] = -1.0*self.lQ*(H_temp[4] - self.Q0 - self.omega*force)
		H_prime[5] = -1.0*self.lA*(H_temp[5]- self.A0 - self.gamma*force + self.zeta*uT_avg*uT_avg/self.H[0])

		#print(H_temp[4], self.Q0, self.omega*force, H_prime[4])


		#print(H_prime)

		return H_prime



	def rk4_update(self, control=[0,0]):

		control_input = control

		#print("Control (RK4): ", control_input, "at t = ", self.current_time)

		##RK4 Method
		k1 = self.dt * self.dH_dt(H_temp = self.H, control = control_input) 
		k2 = self.dt * self.dH_dt(H_temp = self.H + 0.5 * k1, control = control_input)
		k3 = self.dt * self.dH_dt(H_temp = self.H + 0.5 * k2, control = control_input)
		k4 = self.dt * self.dH_dt(H_temp = self.H + k3, control = control_input)

		Y = self.H + k1/6.0 + k2/3.0 + k3/3.0 + k4/6.0 

		return Y


	def calculate_cost(self):
		#H = [R, T, R', T', Q, A] // T = 'Theta'

		
		term_1 = np.abs(np.fmod(self.tmp_system[1]-self.ThetaGoal, 2*np.pi)) #angular term
		term_2 = self.tmp_system[5] #area term
		term_3 = np.abs(1.0*self.tmp_system[0] -1.0*self.ls) #distance term

		#calculate the total cost
		total_tmp_cost = self.alpha*term_1 + self.beta*term_2 + self.delta*term_3

		self.costdata_array = np.array([term_1, term_2, term_3, total_tmp_cost])

		return total_tmp_cost



	def cost_sampling_1(self):

		tmp_number = 0

		self.min_cost = self.max_cost

		options = np.linspace(-1.0, 1.0, self.sample_number)
		uT_options = self.uT_mag*options
		uR_options = self.uR_mag*options


		for uR in uR_options:
			for uT in uT_options:

				tmp_control = [uT, uR] #load the control variable

				self.tmp_system = self.rk4_update(control = tmp_control) #steps forward temporarily
				self.tmp_cost = self.calculate_cost() #calculates the cost for the temporary step forward

				#selects the parameters corresponding to the best value of the cost function
				if self.tmp_cost < self.min_cost:
					self.min_cost = self.tmp_cost
					self.dog_velocities = tmp_control
					self.final_cost_array = self.costdata_array
					#self.final_theta_dog = tdog_temp


				tmp_number+=1

		#print("Selected control: ", self.dog_velocities)

		np.savetxt(self.file_cost, [self.final_cost_array])




	#-------------------------------------DOG FUNCTIONS-------------------------------------------------------

	def update_dog(self):
		'''
		Can later move this into the cost and sampling so that there are fewer external functions to call.
		'''

		#return self.theta_dog+self.dog_velocities[0]*self.dt

		self.old_uT = self.dog_velocities[0]

		return self.theta_dog+self.dog_velocities[0]*self.dt

		






	def sanity_checks(self):

		if self.H[5] < 0:
			print("Area is negative! Abort abort abort!")
			return 1

		if self.H[0] < 0:
			print("R is negative! Abort abort abort!")
			return 1

		else:
			return 0


#----------------------------ADMIN FUNCTIONS----------------------------------------------

	def dump_data_to_file(self):

		#print("H = " , self.H, " at time = ", curr_time)

		tmp_dog_data = [self.theta_dog, self.dog_velocities[0], self.dog_velocities[1]]

		data_dump_array = np.concatenate(([int(self.current_time)], self.H, tmp_dog_data))

		np.savetxt(self.file1, [data_dump_array])


	def initialize_simulation(self):


		print("Clearing old folders and output")
		os.system("mv data.out old_data.out")
		self.file1 = open("data.out", "a")

		os.system("mv cost.out old_cost.out")
		self.file_cost = open("cost.out", "a")

		os.system("mv output_movie.mp4 old_output_movie.mp4")

		#testing the import
		#self.timesteps, self.dt, self.lR, self.lT, self.lA, self.lQ, self.f0, self.ls, self.gamma, self.omega, self.delta, self.A0, self.Q0, self.modder = load_params_auto()




