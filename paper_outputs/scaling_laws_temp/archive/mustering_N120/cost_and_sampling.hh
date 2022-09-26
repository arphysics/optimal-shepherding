#ifndef COST_AND_SAMPLING
#define COST_AND_SAMPLING

#include <cstdio>
#include <cmath>
#include <cstdlib>
#include <iostream>
#include <fstream>
#include <string>
using namespace std;

#include "herding.hh"
#include "forces.hh"


//calculate the cost function
void herding::cost_function(int id) 
{

    if(fence ==0){ //currently (02/08/2021) this code only works in the case of open boundary conditions, no fence capability yet

      //metrics for evaluating the cost function
      //printf("BEFORE: pos_avg[0]: %f \n", pos_avg[0]);
      avg_loc(x_test, y_test); //calculates the average position of sheep herd
      //printf("AFTER: pos_avg[0]: %f \n", pos_avg[0]);


      //find the distance to the target
      double dx; double dy; 
      double dr; //set variables to use within functions
      double xcm = pos_avg[0]; double ycm = pos_avg[1]; //set xcm, ycm positions
      double dist;
      

      //calculate distance term
      dx = x_target-xcm;
      dy = y_target-ycm;
      dr = sqrt(dx*dx + dy*dy);



      //standard deviation
      double sheep_spread = 0;
      for(int k = 0; k<num_agents; k++){
        dx = x_test[k] - xcm;
        dy = y_test[k] - ycm;
        dist = dx*dx*dx*dx + dy*dy*dy*dy; //to calculate the L4 nrom
        sheep_spread += dist;
      }


      sheep_spread = sqrt(sqrt(sheep_spread/num_agents)); //sqrt and normalize to calculate the L4 Norm

      //ONLY FOR REFERENCE...this version is wrong
      //sheep_spread = sqrt(sheep_spread)/num_agents; //OLD VERSION!!! sqrt and normalize to calculate the standard deviation

      
      cost_function_val[1] = sheep_spread;


      double tmp_angle_herd_target = atan2(y_target-pos_avg[1], x_target-pos_avg[0]); // herd-cm to target angle

      //define this as the "dog target"
      double tmp_x_dog_target = pos_avg[0]-ld*cos(tmp_angle_herd_target);
      double tmp_y_dog_target = pos_avg[1]-ld*sin(tmp_angle_herd_target);
      
      double tmp_driving_cost = (xd2-tmp_x_dog_target)*(xd2-tmp_x_dog_target)+(yd2-tmp_y_dog_target)*(yd2-tmp_y_dog_target);


      //the value of the cost-function
      cost_function_val[0] =  dist_weight*dr+spread_weight*sheep_spread+coll_weight_factor*tmp_driving_cost;
     
      //spit out cm to be used elsewhere
      cost_function_val[2] = xcm;
      cost_function_val[3] = ycm; 
    }
}

#endif