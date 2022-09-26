# optimal-shepherding
README updated 09/26/2022


## Repository for code files corresponding to Optimal shepherding and transport of a flock-- PNAS, (Ranganathan, Heyde, Gupta, and Mahadevan)


Current Status:
Code in current state can be run to reproduce the results in the Paper and can be used to explore herding behavior in several contexts. Further git commits to come with further comments and notes to make the code more accessible to a general, less computationally sophisticated audience.



Credits:
This is a general multi-agent simulator written by Aditya Ranganathan.

The code was advised by Anupam Gupta, Chris Rycroft, and Lakshminarayanan Mahadevan. 

All Rights Reserved. ©Aditya Ranganathan, 2022



## Notes for ABM Model

Simulation code is written in C++
Plotting code is written in Python 


*Plotting Individual Simulations:*

MOVIES are made using the "visualizer.py" program that reads in the "data.txt" output file as well as the "params.txt" from the C++ simulations and converts to a stacked time series of scatter plots using ffmpeg. Movies are saved as "output_movie.mp4" by default. 

TRACE plots that show the trajectory of animals and shepherd(s) over time are made using the "trajectory_plotter.py" program that also reads "data.txt" and "params.txt" to produce a trace of the animals' and shepherd(s)' center of mass over time along with snapshots of the animals and herders at three times (by default) which include the initial and final times.

*Creating A Phase Plot*

To activate the phase plotting code functions that can then be called by "make_movie,"

	1) activate herd_env: "conda activate herd_env"

	2) install the package: "pip install -e ."


##  Notes for ODE Model

