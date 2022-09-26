from aux_funcs_viz import *
from aux_funcs import *
plt.rcParams.update({'figure.max_open_warning': 0})
import time


def generate_trajectory_test():

	target_loc = [-45.0, 45.0]

	timesteps, dt, lR, lT, lA, lQ, f0, ls, gamma, omega, zeta, alpha, beta, delta, A0, Q0, ThetaGoal, modder, H, uR_mag, uT_mag, sample_number = load_params_auto()

	os.system("mv traj.in old_traj.in")

	# file_trajectory = open("traj.in", 'w')

	print("generate trajectory test: ", timesteps)

	# print(file_trajectory)

	times = np.linspace(0, timesteps, timesteps)
	x = np.array([tt/timesteps*target_loc[0] for tt in times])*np.abs(15/target_loc[0])
	y = np.array([tt/timesteps*target_loc[1] for tt in times])*np.abs(15/target_loc[1])
	theta = np.zeros(len(x))
	theta[1:] = [np.arctan2(y[tt]-y[tt-1], x[tt]-x[tt-1]) for tt in range(1, len(x))]

	np.savetxt("traj.in", (x, y, theta))



if __name__ == '__main__':

	tom = time.time()
	
	generate_trajectory_test()

	plot_herd_movie("data.out")

	tfm = time.time()

	print("Total time to create movie = ", tfm-tom)






