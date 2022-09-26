#ifndef TIMESTEPPING
#define TIMESTEPPING

#include <cstdio>
#include <cmath>
#include <cstdlib>
#include <iostream>
#include <fstream>
#include <string>
using namespace std;

#include "herding.hh"
#include "forces.hh"
#include "cost_and_sampling.hh"

//run vicsek, cm attraction, hard repulsion force, and wall repulsion
void herding::sheep_step_no_dog(){

    double sf_rf[2]; //array to store results of sheep-fence repulsion force

    //calculate herd CM
    avg_loc(x, y);


    for(int i = 0; i<num_agents; i++){

        
        //Viscek interaction
        double theta_vsk = viscek(i); //alignment angle calculated from Vicsek
        double v_vsk[2] = {v*cos(theta_vsk), v*sin(theta_vsk)}; //take step according to Vicsek alignment angle
        double xnext = alpha*v_vsk[0]*dt; // viscek x step forward
        double ynext = alpha*v_vsk[1]*dt; // viscek y step forward

        //Hard sphere repulsion
        sheep_repulsor(i); //calculate hard sphere repulsion
        xnext += beta*ssrf[0]*dt; //sheep-sheep repulsion calculation x dir
        ynext += beta*ssrf[1]*dt; //sheep-sheep repulsion calculation y dir

        //CM attraction
        double theta_cm = sheep_attractor(i); //calculate orientation of CM attraction
        double v_cm[2] = {v*cos(theta_cm),v*sin(theta_cm)}; //take step towards center of mass
            
        //------------------temp code---------------------------
        //calculates distance between sheep and the CM of the herd...
        //TODO: put into a function and make dependent on a lambda parameter
        double lambda2 = 0;
        double temp_delta = pow((x[i]-pos_avg[0])*(x[i]-pos_avg[0])+(y[i]-pos_avg[1])*(y[i]-pos_avg[1]), lambda2);

        //------------------end temp code-------------------------
        
        xnext += gamma*v_cm[0]*dt*temp_delta; //CM attraction in the x direction
        ynext += gamma*v_cm[1]*dt*temp_delta; //CM attraction in the y direction


        //wall repulsion
        if(fence == 1){
            fence_repulsor(sf_rf, i, r); //calculate effects of a fence
            xnext += sf_rf[0]*dt; //fence effects in x direction
            ynext += sf_rf[1]*dt; //fence effects in y direction
        }

        x2[i] = xnext + x[i]; //take step
        y2[i] = ynext + y[i]; //take step

        xnext = 0; //reset step size
        ynext = 0; //reset step size

    } //end loop over agents

}




void herding::propogate_herd(int id, double v_dog_tmp, int time)
{
    

    //Propogate dog
    xd2 = xdogsf[id]; 
    yd2 = ydogsf[id];
    double xd = xdogs[id];
    double yd = ydogs[id];

    //temp variables 
    double xnext;
    double ynext;
    double sd_rf[2];

    double dog_vel_angle = atan2(yd2-yd, xd2-xd); //calculate the dogs heading

    //sanity check to make sure dog step size isn't too big
    if((yd2-yd)*(yd2-yd)+(xd2-xd)*(xd2-xd) > (v_dog_tmp*dt)*(v_dog_tmp*dt)){
        printf("Dog moving too FAST!!! %d \n", time);
        cout << "xd2, yd2" << xd2 <<", "<< yd2 << " xd, yd" << xd << ", "<< yd <<endl;
    } 


    double theta0 = 0; //temp variables to store the next timestep
  
    //loop over agents
    for(int i = 0; i<num_agents; i++){

        //bring back xnext from initial vicsek, CM, hard-shell run
        xnext = x2[i]-x[i];
        ynext = y2[i]-y[i]; 
        
        //Add in Dog repulsion
        dog_repulsor(sd_rf, dog_vel_angle, i);
        xnext += delta*sd_rf[0]*dt; //sheep-dog repulsion calculation x dir
        ynext += delta*sd_rf[1]*dt; //sheep-dog repulsion calculation y dir


        //update positions of each sheep
        x2[i] = xnext + x[i];
        y2[i] = ynext + y[i];

        //update directions of sheep
        theta0 = atan2(ynext,xnext);
        theta2[i] = theta0;
    }
}



void herding::test_propogate_sheep()
{

    double sd_rf[2];


    //loop over agents for dog movement
    for(int i = 0; i<num_agents; i++){
        double xnext_test;
        double ynext_test;

        //Dog repulsion
        dog_repulsor(sd_rf,dog_sample_angle, i);
        xnext_test = delta*sd_rf[0]*dt; //sheep-dog repulsion calculation x dir
        ynext_test = delta*sd_rf[1]*dt; //sheep-dog repulsion calculation y dir

        //cout << "Value of xnext_test within test_propogate_sheep: " <<xnext_test << endl;

        //update positions of each sheep
        x_test[i] = xnext_test + x2[i];
        y_test[i] = ynext_test + y2[i];

        //debug: check whether xnext is working
        //cout << "xnext, ynext: " << xnext_test << " , " <<ynext_test << endl; 
    }

}


void herding::first_round()
{


    //variables to implement reflective boundary conditions
    double dx = 0;
    double dy = 0;

    //set array to store results of cost function
    double min_cost = exp(100); //initial high value of cost function  
    double max_cost = 0; //initial high value of cost function
    double tmp_cost = 0; //initial value for temp cost function variable

    for(int id = 0; id <num_dogs; id++) //loop over dogs
        {


            //double rd_f[2];
            double xd_f = xdogs[id]; //initialize & set value for "best" dog x motion
            double yd_f = ydogs[id]; //initialize & set value for "best" dog y motion
            double xd = xdogs[id];   //initialize & set value for "current" dog x motion
            double yd = ydogs[id];   //initialize & set value for "current" dog x motion


            //begin sampling loop
            for(int k = 0; k<sample_number; k++){
                
                //printf("Is the location checker doing it's job? \n");
                avg_loc(x, y); //sets the average position of sheep herd

                //pick a random angle
                dog_sample_angle = dog_range*(rand()/(double) RAND_MAX-0.5);

                //pick a specific angle (dog speed dynamically set...v_dog_tmp)
                xd2 = xd + v_dog_tmp*cos(dog_sample_angle)*dt;
                yd2 = yd + v_dog_tmp*sin(dog_sample_angle)*dt;

                // cout << "v_dog_tmp: " << v_dog_tmp << endl;

                // cout << "Sample #: " << k << endl;
                // cout << "Value of dxd in the sampling loop: " << v_dog_tmp*cos(dog_sample_angle)*dt << endl;
                // cout << "Value of xd in the sampling loop: " << xd << endl;
                // cout << "Value of xd2 in the sampling loop: " << xd2 << endl;
                
                //dog reflective boundary conditions if a fence exists
                if(fence == 1){
                    dx = xd2 - x_target;
                    dy = yd2 - (y_target+0.5*ld);
                    if(dx<0) xd2 = x_target-dx;
                    if(dy>0) yd2 = y_target-dy;
                }



                //hardcoded maximum distance between dog and sheep
                if(sqrt((xd2-pos_avg[0])*(xd2-pos_avg[0])+(yd2-pos_avg[1])*(yd2-pos_avg[1]))<5*dog_dist_factor*ld) // begin dog_dist_factor if
                {

                    
                    // //debug 
                    // cout << "Sample Number: " << k << endl;


                    //loop over agents for dog movement
                    test_propogate_sheep();

                    //calculate the cost function:
                    cost_function(id);
                    
                    tmp_cost = cost_function_val[0]; //set tmp_cost to calculated cost_function value


                    //dump the optimization results to a file

                    //STILL NEED TO IMPLEMENT THIS!!!
                    //fprintf(foptimize, "%d %d %f %f \n", jj, k, dog_sample_angle, tmp_cost);

                
                    //Chooses sample with best value for cost function
                    if(tmp_cost<=min_cost){
                        xd_f = xd2; 
                        yd_f = yd2; 
                        min_cost = tmp_cost; //set new cost function
                        sheep_spread_final = cost_function_val[1];
                        xcm_final = cost_function_val[2];
                        ycm_final = cost_function_val[3];

                        //printf("%f %f \n", xcm_final, ycm_final);
                    }

                    //set maximum cost value if tmp_cost somehow exceeds maximum cost...
                    if(tmp_cost>=max_cost) max_cost = tmp_cost;

                } //end dog_dist_factor_if

                else //if further than the max allowed distance, dog just propogates towards herd CM
                { 
                    
                    double tmp_angle_dog_herd = atan2(pos_avg[1]-yd, pos_avg[0]-xd);

                    printf("Dog-herd-angle: %f \n", tmp_angle_dog_herd);

                    xd_f = xd + v_dog*cos(tmp_angle_dog_herd)*dt;
                    yd_f = yd + v_dog*sin(tmp_angle_dog_herd)*dt;

                    printf("crap \n");

                }

            } //end sampling loop


            xdogsf[id] = xd_f;
            ydogsf[id] = yd_f;

        } //end loop over dogs
}
    



//propogate herd with optimal parameters
void herding::final_round(int time)
{

        //propogate sheep using optimal dog parameters
         for(int id = 0; id<num_dogs; id++){
            
            propogate_herd(id, v_dog_tmp, time); 

            //switch pointers for next dog-step
            double* s_x = x2; x2 = x; x = s_x;
            double* s_y = y2; y2 = y; y = s_y;
            double* s_theta = theta2; theta2 = theta; theta = s_theta;
        }


        //switch pointers for dog
        double* s_xdogs = xdogsf; xdogsf = xdogs; xdogs = s_xdogs;
        double* s_ydogs = ydogsf; ydogsf = ydogs; ydogs = s_ydogs;

}





#endif