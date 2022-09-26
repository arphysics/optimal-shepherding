#ifndef HO_HERDING_HH
#define HO_HERDING_HH

#include <iostream>
#include <cmath>
#include <cstdlib>
using namespace std;


class herding {
	public:
		//functions in the class for setup
		void read_params(); //reads in and sets varaibles based on param file
		void print_params(); //prints value of params
		void init_arrs_and_vars(); //initializes dynamic arrays
		void initialize_dogs(); //initialize position of dogs
		void initialize_sheep(FILE*); //initialize position of sheep
		void print_data_to_file(FILE*, int); //prints data to file
		void print_cost_to_file(FILE*, int); //outputs the results optimization at each timestep which is useful for analysis and debugging

		//functions in class for forces
		double viscek(int); //propogates agents according to the vicsek model
		double dog_direction(int); //sets direction of the dog to herd CM
		void dog_repulsor(double [], double, int); //propogates according to dog-repulsion
		double sheep_attractor(int); //propogates according to CM attraction
		void fence_repulsor(double [], int, double); //for case of active fence, triggers fence repulsion
		void sheep_repulsor(int); //calculates soft-shell repulsion for sheep

		//timestepping
		void sheep_step_no_dog(); //moves the sheep forward according to vicsek, CM attraction, and local repulsion terms (ignoring dog)
		void propogate_herd(int, double, int); //moves the herd by including the effects of the dog
		void test_propogate_sheep(); //tentatively moves the herd forward but does not switch pointers; used in optimization tests
		void first_round(); //calculates the cost function for iterations equal to the sample number and chooses the optimal dog behavior
		void final_round(int); //moves the entire system forward by one timestep per the optimal dog behavior

		//cost function
		void cost_function(int); //evaluates the objective function given the state of the system
		int break_when_close();  //ends the simulation when the herd is close enough to the target


		//helper functions
		void avg_loc(double [], double []); //calculates the center of mass position of the herd



	private: 
		
		//define parameter variables (see the param file for what each of these parameters means)
	    double v, v_dog, dt, r, ls, ld, eta, alpha, beta, gamma, delta, x_target, y_target, dog_range;
	    double bound, grid_spacing, xd_start, yd_start, dist_weight, spread_weight, coll_weight_factor;
	    double max_spread_X, min_spread_X;  
	    double dist_weight_factor, speed_weight_factor, dog_dist_factor;
	    bool fence, driving_on;


//--------------------NEED TO CLEAN THIS UP BEFORE PROCEEDING
	    double xd2; double yd2; //temporary location of a single dog for next timestep


	    // //Additional temporary arrays / variables
	    double pos_avg[2] = {}; //temporary array to store the average position of the sheep herd for that timestep
	    double ssrf[2] = {}; //array to store sheep-sheep repulsion force
	    double cost_function_val[4] = {}; //array to store the cost function values and parameters
	    double dog_sample_angle; //make this array


	    double sheep_spread2, sheep_spread_final, dist_weight_2;
	    double v_dog_tmp, max_spread, min_spread, xcm_final, ycm_final;


//--------------------NEED TO CLEAN THIS UP FOR MAX EFFICIENCY BETWEEN PUBLIC AND PRIVATE (02/08/2021) 
//--------------------update (02/24/2022) still should be cleaned up for better efficiency, but works fine as isas is

	public:
	//arrays in the class
		double* x; //temporary array to store x positions of sheep for a single timestep
	    double* y; //temporary array to store y positions of sheepfor a single timestep
	    double* theta; //temporary array to store angles for a single timestep

	    double* x2; //temporary array to store x positions for next  timestep
	    double* y2; //temporary array to store y positions for next timestep
	    double* theta2; //temporary array to store angles for next timestep

	    double* x_test; //temporary array to store sampling positions for next  timestep
	    double* y_test; //temporary array to store sampling positions for next timestep


	    //dog(s)
	    double* xdogs; //array to store x positions of dogs
	    double* ydogs; //array to store y positions of dogs
	    double* xdogsf; //temporary array to store x positions of dogs
	    double* ydogsf; //temporary array to store y positions of dogs

	    //some more parameters that are defined in the parameter file
	    int timesteps, num_agents, num_dogs, L, sample_number, mod_dump_data;

	   	double seed = 1231.12;

	   	//double seed = srand(omp_get_wtime())1231.12; --> random seed is now being implemented in simulate.cc

	private: 
		//extra functions that are private
		double rand_float(); //function to generate random value -1 to 1
};





#endif