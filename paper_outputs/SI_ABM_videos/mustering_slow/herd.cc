#include <cstdio>
#include <cmath>
#include <cstdlib>
#include <iostream>
#include <fstream>
#include <string>
using namespace std;

#include "herding.hh"
#include "forces.hh"
#include "timestepping.hh"


void herding::read_params(){

    /* 
    Function reads in the parameter file. 
    Unfortunately this function IS SENSITIVE TO ORDER so be VERY CAREFUL when editing or adding to the param file

    */
    
    double a;
    string b;

    ifstream myfile;
    myfile.open("params.txt");

    myfile >>a >> b; timesteps = a;
    myfile >>a >> b; num_agents = a;
    myfile >>a >> b; num_dogs = a;
    myfile >>a >> b; L = a;
    myfile >>a >> b; sample_number = a;
    myfile >>a >> b; v = a;
    myfile >>a >> b; v_dog = a;
    myfile >>a >> b; dt = a;
    myfile >>a >> b; r = a;
    myfile >>a >> b; ls = a;
    myfile >>a >> b; ld = a;
    myfile >>a >> b; eta = a;
    myfile >>a >> b; alpha = a;
    myfile >>a >> b; beta = a;
    myfile >>a >> b; gamma = a;
    myfile >>a >> b; delta = a;
    myfile >>a >> b; x_target = a;
    myfile >>a >> b; y_target = a;
    myfile >>a >> b; dog_range = a;
    myfile >>a >> b; bound = a;
    myfile >>a >> b; grid_spacing = a;
    myfile >>a >> b; xd_start = a;
    myfile >>a >> b; yd_start = a;
    myfile >>a >> b; dist_weight = a;
    myfile >>a >> b; spread_weight = a;
    myfile >>a >> b; coll_weight_factor = a;
    myfile >>a >> b; max_spread_X = a;
    myfile >>a >> b; min_spread_X = a;
    myfile >>a >> b; dist_weight_factor = a;
    myfile >>a >> b; speed_weight_factor = a;
    myfile >>a >> b; driving_on = a;
    myfile >>a >> b; dog_dist_factor = a;
    myfile >>a >> b; fence = a;
    myfile >>a >> b; mod_dump_data = a;
}


void herding::print_data_to_file(FILE* fparticles, int jj){

    //Dumps sheep and dog position and orientations to a data file

    for(int i = 0; i <num_agents; i++){
        fprintf(fparticles, "%d %d %f %f %f", jj, i, x[i], y[i], theta[i]);
        for(int id = 0; id <num_dogs; id++) fprintf(fparticles, " %f %f",xdogsf[id], ydogsf[id]);
        fprintf(fparticles, "\n");
    }

}


void herding::init_arrs_and_vars(){

    //initializes arrays and variables
    
    //sheep
    x = new double[num_agents]; //temporary array to store x positions of sheep for a single timestep
    y = new double[num_agents]; //temporary array to store y positions of sheepfor a single timestep
    theta = new double[num_agents]; //temporary array to store angles for a single timestep

    x2 = new double[num_agents]; //temporary array to store x positions for next  timestep
    y2 = new double[num_agents]; //temporary array to store y positions for next timestep
    theta2 = new double[num_agents]; //temporary array to store angles for next timestep

    x_test = new double[num_agents]; //temporary array to store sampling positions for next  timestep
    y_test = new double[num_agents]; //temporary array to store sampling positions for next timestep


    //dog(s)
    xdogs = new double[num_dogs]; //array to store x positions of dogs
    ydogs = new double[num_dogs]; //array to store y positions of dogs
    xdogsf = new double[num_dogs]; //temporary array to store x positions of dogs
    ydogsf = new double[num_dogs]; //temporary array to store y positions of dogs


    //initialize other variables

    // //Additional temp arrays / variables

    //THIS SECTION NEEDS TO BE CLEANED UP (as of 02/08/2021)

    sheep_spread2 = 0;
    sheep_spread_final = 0;
    dist_weight_2 = dist_weight; //alpha value to play with
    v_dog_tmp = v_dog;
    max_spread = max_spread_X*ls;
    min_spread = min_spread_X*ls; 

    xcm_final = 0; 
    ycm_final = 0;
}


//initialize dog positions
void herding::initialize_dogs(){ 

    //Initializes the position and orientation of the dog at time t = 0

    for(int i = 0; i<num_dogs; i++){

        if(fence == 0){
            xdogs[i] = xd_start;
            ydogs[i] = yd_start;
        }


        else{
            //hardcoded example
            double tmp_theta = M_PI*(rand_float()-1)/4;
            double tmp_dist = (rand_float()+3)/2;
            xdogs[i] = ld*dog_dist_factor*1/3*cos(tmp_theta)*tmp_dist;
            ydogs[i] = ld*dog_dist_factor*1/3*sin(tmp_theta)*tmp_dist;
        }

    }

        xdogsf = xdogs;
        ydogsf = ydogs;


}

//initialize sheep positions
void herding::initialize_sheep(FILE* fparticles){

    //initializes positions and orientations of the sheep
    

    for(int i=0; i<num_agents;i++){
        x[i] = bound*rand_float();
        y[i] = bound*rand_float();
        theta[i] = 2*M_PI*rand_float();
    }

}

//function to generate random value -1 to 1
double herding::rand_float(){
        return (double) 2*rand()/(double) RAND_MAX-1; 
}


void herding::print_cost_to_file(FILE* fcost, int jj){

    //dumps some of the cost function data to a file

    fprintf(fcost, "%d %f %f %f %f %f %f %f \n", jj, dist_weight_2, v_dog_tmp, sheep_spread_final, 
    xcm_final, ycm_final ,xdogsf[0], ydogsf[0]);
}


void herding::print_params(){

    cout << "Nsheep: " << num_agents << endl;
    cout << "Ndogs: " << num_dogs << endl;
    cout << "v_dog: " << v_dog << endl;
    cout << "gamma: " << gamma << endl;
}


int herding::break_when_close(){

        //break if herd CM is very close to target 

        if((xcm_final-x_target)*(xcm_final-x_target)+(ycm_final-y_target)*(ycm_final-y_target)<(num_agents*ls)*(1)){
            
            printf("Close enough!!\n");

            return 1;
        }

        else return 0; 
}


//finds the average location of sheep at each timestep
void herding::avg_loc(double x_array[], double y_array[]){
  /*param x: array containing x position of all the sheep
  param y: array containing y position of all the sheep
  param num_agents: number of agents*/

  double tmp_x = 0;
  double tmp_y = 0;


  if(fence == 0){
    //find the average location of x & y
    for(int i =0; i <num_agents; i++){
      tmp_x += x_array[i];
      tmp_y += y_array[i];
    }


  pos_avg[0] = tmp_x/num_agents; //set pointer array to average x location
  pos_avg[1] = tmp_y/num_agents; //set pointer array to average y location
  }
  
  else{
    double counter = 0;
    for(int k = 0; k<num_agents; k++){
        if(x[k] > x_target){
          if(y[k] < y_target){
            tmp_x += x_array[k];
            tmp_y += y_array[k];
            counter +=1;
          }
        }
    }

  pos_avg[0] = tmp_x/counter; //set pointer array to average x location
  pos_avg[1] = tmp_y/counter; //set pointer array to average y location
  }

}















