#include <iostream>
#include <cmath>
#include <cstdlib>
#include <omp.h>
using namespace std;

#include "herding.hh"

int main(){

    herding obj;

    //srand(obj.seed); //set a specific seed for debugging
    srand(omp_get_wtime()); //set a random seed for each simulation

    //read variables from param.txt file
    obj.read_params();


    //cout << "spread_weight: " << obj.spread_weight << endl;


    //initialize dynamic arrays
    obj.init_arrs_and_vars();


    //initialize files for data to be dumped
    FILE *fparticles;
    fparticles = fopen("data.txt", "w");
    FILE *fcost;
    fcost = fopen("costdata.txt", "w");

    //initialize dogs
    obj.initialize_dogs();
    //initialize sheep
    obj.initialize_sheep(fparticles);


    //initialize sheep positions and print to file
    printf("data.txt contains: \n time, particle, xpos, ypos, thetapos, xpos_dog, ypos_dog, theta_dog \n");
    printf("costdata.txt contains: \n time, dist_weight, dog_speed, herd_spread, xcm, ycm, xdog, ydog \n");

    //print location data to file
    obj.print_data_to_file(fparticles, 0);


    //timestepping

    for(int jj=1; jj<obj.timesteps; jj++) //loop over timesteps
    {


        //cout << "Timstep: " << jj<< "----------------------------------------" << endl;
        //run vicsek, cm attraction, hard repulsion force, and wall repulsion
        obj.sheep_step_no_dog();

        //find optimal dog movement
        obj.first_round();

        //propogate with optimal dog movement
        obj.final_round(jj);

        //break if herd CM is very close to target 
        if (obj.break_when_close() == 1) break;

        //print out the results for a particular interval of timesteps

        if(jj%obj.mod_dump_data == 0){

        	obj.print_cost_to_file(fcost, jj); //print cost data to cost file

            obj.print_data_to_file(fparticles, jj); // print cost data to data file
        }


    }


     
}
