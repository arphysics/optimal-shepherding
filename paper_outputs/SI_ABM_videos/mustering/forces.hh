#ifndef TEST_HEADER
#define TEST_HEADER

#include <cstdio>
#include <cmath>
#include <cstdlib>
#include <iostream>
#include <fstream>
#include <string>
using namespace std;

#include "herding.hh"

//Finds the orientation of a single person j, at a time t
double herding::viscek(int j){
  //param j: identifier of particle in question


  //temporary variables
  double delta; //used to calculate the square distance
  double tmp_sum = 0;
  double counter = 0;
  
  //add random uniform noise to each particle's position
  double noise = eta*2*(rand()/(double) RAND_MAX-0.5);
  
  //loop over the agents and find particles within radius of interaction
  for(int k =0; k<num_agents; k++){
      delta = (x[j]-x[k])*(x[j]-x[k])
            +(y[j]-y[k])*(y[j]-y[k]);

      //enforce Viscek radius
      if(delta<r*r){
          //find average orientation of nearest neighbors
          tmp_sum = tmp_sum + theta[k];
          counter +=1;
      }
  }
  return tmp_sum/counter + noise;
}



//Finds the direction for the dog to move towards the cm of the herd
double herding::dog_direction(int id){
  
  //average position of sheep herd
  double x_cm = pos_avg[0];
  double y_cm = pos_avg[1];

  double dx = x_cm - xdogs[id];
  double dy = y_cm - ydogs[id];

  double theta = atan2(dy,dx);

  return theta;
}


//Calculates the repulsion between sheep and dog
void herding::dog_repulsor(double sd_rf [], double angle, int j){
  //param j: identifier of particle in question
  //param angle: direction that the dog is moving in for implementing anisotropic repulsion (currently set to 0)
  //param sd_rf: 2D array to store force from the dog

  double B = 1; //arbitrary coefficient for the dog repulsion;


  //cout << "Value of xd2 in the dog_repulsor function: " << xd2 << endl;

  //currently we have hardcoded in 1 dog
  double dx = x[j]-xd2;
  double dy = y[j]-yd2;

  double rid_abs = sqrt(dx*dx + dy*dy);
  double theta_dr = atan2(dy,dx);

  //adding in an an-isotropic repulsion
  double lambda1 = 0; //parameter to control strength of anisotropy
  double f = B*exp(-rid_abs/ld)*exp(cos(theta_dr-angle)*lambda1);

  sd_rf[0] = f*cos(theta_dr);
  sd_rf[1] = f*sin(theta_dr);

}


//Calculates the long-range force of attraction between sheep
double herding::sheep_attractor(int j){

  //param j: identifier of particle in question


  double x_cm = pos_avg[0];
  double y_cm = pos_avg[1];

  double dx = x_cm - x[j];
  double dy = y_cm - y[j];

  double theta_lr = atan2(dy,dx);

  return theta_lr;
}

//Calculates the force due to hard-shell sheep-sheep interaction
void herding::sheep_repulsor(int j){
  
  //param j: identifier of particle in question

  double A = 1; //coefficient of repulsion
  double fx = 0; //x component of the force
  double fy = 0; //y component of the force
  double dx; //x distance between two particles
  double dy; //y distance between two particles
  double rid_abs; //total distance between two particles
  double theta_dr; //sets the direction of the force

  for(int k =0; k<num_agents; k++){
    if(j != k){
      dx = x[j]-x[k];
      dy = y[j]-y[k];
      rid_abs = sqrt(dx*dx + dy*dy);
      if(rid_abs <10*ls){
        theta_dr = atan2(dy,dx);
        fx += A*exp(-rid_abs/ls)*cos(theta_dr);
        fy += A*exp(-rid_abs/ls)*sin(theta_dr);
      }
    }
  }

  ssrf[0] = A*fx; //ssrf[0] is the x-component of the array containing the repulsion vector from all the other sheep to sheep j
  ssrf[1] = A*fy; //ssrf[1] is the y-component of the array containing the repulsion vector from all the other sheep to sheep j
}



//Calculates the repulsion between sheep and fence
void herding::fence_repulsor(double sf_rf[], int j, double r){
  /*param sf_rf: array containing x,y repulsion vector from the fence to the sheep
  param j: timestep (seems unnecessary)
  param r: also seems unnecessary*/


  //THIS FUNCTION NEEDS REVIEW--IT IS CURRENTLY NOT BEING USED IN THE CODE.

  double B = 20; //arbitrary coefficient for the dog repulsion;

  //currently we have hadcoded in 1 dog
  double dx = (x[j]-x_target);
  double dy = (y[j]-(y_target+0.5*ld));

  sf_rf[0] = 0;
  sf_rf[1] = 0;

  if(y[j]<y_target-0.5*ld){
    sf_rf[0] = dx/abs(dx)*B*exp(-abs(dx)/(r));
  }
  sf_rf[1] = dy/abs(dy)*B*exp(-abs(dy)/(r));

}



#endif






