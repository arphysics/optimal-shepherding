# herding_new


## What is this?

The code described here was designed to explore the herding phenomenon via agent-based simulations. Results corresponding to this code are described in the paper "Optimal Herding of Self Propelled Agents," by Alexander Heyde, Aditya Ranganathan, Anupam Gupta, and Lakshminarayanan Mahadevan. 

###Credits:

The code listed here was written by Aditya Ranganathan, and only possible thanks to the generous advice of Anupam Gupta, Chris Rycroft, and Lakshminarayanan Mahadevan. 

## How do I run the code?

All code to run simulations is written in C++ using an object oriented approach. Plotting is done using python (see below).

### Running the C++ Code:

The C++ code is designed to be object oriented and is written in a modular fashion with function definitions distributed over several files and grouped by their function within the broader project goals. This modular approach limits the file size of any file and allows for easier edits and modifications to the code. It does, however, also require an understanding of the high level structure in order to handle efficiently. The steps below are designed to allow you to efficiently start running the code for yourself and get a 30,000ft view of the code files and structure. For more detail, don't hesitate to dive into the comments (which are less detailed than I'd like) or shoot me an email (aditya_ranganathan@g.harvard.edu) with any questions. 

	
	(1) First, set your system config. If running Mac with the GNU compiler, the existing config.mk file should work. If running Linux, you might need to the config.mk file in the repository home folder to reflect your favorite C compiler. 

	(2) Enter the subdirectory labelled "code" within the repository. This subdirectory contains several code files vaguely organized by their purpose in the code. A quick list and description of each is below (in reverse order):

		* simulate --> is the compiled C file (to create the simulate file, run the "make" command)
		* simulate.cc --> generates the objects and runs the simulation
		* herding.hh --> defines the "herding" class and necessary variables and arrays 
		* herd.cc --> defines the functions necessary to initialize the system, load the parameter file, print the data to a file, as well 
			as a few other miscellaneous functions (like calculating average positions)
		* timestepping.hh --> defines the functions necessary to step the simulation forward in time
		* forces.hh --> defines the functions governing the interaction between agents both internally and externally with the shepherd
		* cost_and_sampling.hh --> defines the functions that carry out the optimization calculations during the simulation
		* params.txt --> sets the parameters for the simulation (and is designed so that editing the param file doesn't require a "make" command 	before running a new simulation)
		* data.txt --> the code outputs the positions of every agent and shepherd to this file which is the main data file for the simulation
		* costdata.txt --> outputs the results optimization at each timestep which is useful for analysis and debugging

### Generating Plots and Videos

Plotting code notes:

MOVIES are made using the "visualizer.py" program that reads in the "data.txt" output file as well as the "params.txt" from the C++ simulations and converts to a stacked time series of scatter plots using ffmpeg. Movies are saved as "output_movie.mp4" by default. 

TRACE plots that show the trajectory of animals and shepherd(s) over time are made using the "trajectory_plotter.py" program that also reads "data.txt" and "params.txt" to produce a trace of the animals' and shepherd(s)' center of mass over time along with snapshots of the animals and herders at three times (by default) which include the initial and final times.

##Caveats on *this* version of the code

These caveats are in no particular order

* The code in this repository corresponds to the state of this multi-agent mult-shepherd simulator at the time the paper described above was submitted. The careful peruser of the code will notice parameters and functions that point to capabilities not currently present in the code (like multiple shepherds or a variety of boundary conditions). This is on purpose, to provide the reader with an accurate representation of the code used to generate the data and results described in the "Optimal Herding of Self Propelled Agents" paper. Once the broader multi-agent simulator is complete, it will be available for open source use on the arphysics github page. Check back in a few months if the extra features are of interest!

* In the paper which this code supports, the terms agents and shepherd are used. In the comments within the code, agents and sheep as well as shepherd and dog are used interchangeably. 

* This README was last updated on  02/23/2022



Files to delete in public version: 

* todo.txt
* tmpdata.txt 
* visualizer.py
* visualizer_new.py
* visualizer_old.py






Structure: 









©Aditya Ranganathan, 2022
