import os
from collections import OrderedDict
import numpy as np
import matplotlib.pyplot as plt


def load_params_auto(file_pointer = 'params.in'):


  '''function to load parameters automatically, independent of the order of the parameters in the param file. 
  This function should search for the regular expressions within the parameter file
  '''

  #----------------------------------------
  # param params.in file with parameters for the python code
  #----------------------------------------


  #conditions-------------------------

  tmp_conditions = OrderedDict() #dictionary of conditions

  tmp_conditions['N_Timesteps'] = 'timesteps'
  tmp_conditions['Step_size'] = 'dt'
  tmp_conditions['Distance_Sensitivity'] = 'lR'
  tmp_conditions['Angular_Sensitivity'] = 'lT'
  tmp_conditions['Area_Sensitivity'] = 'lA'
  tmp_conditions['ARatio_Sensitivity'] = 'lQ'
  tmp_conditions['Force_Strength'] = 'f0'
  tmp_conditions['Repulsion_lengthscale'] = 'ls'
  tmp_conditions['Force_Area_Sensitivity'] = 'gamma'
  tmp_conditions['omega'] = 'omega'
  tmp_conditions['uT_Area_Sensitivity'] = 'zeta'
  tmp_conditions['Theta Weight'] = 'alpha'
  tmp_conditions['Area Weight'] = 'beta'
  tmp_conditions['Distance Weight'] = 'delta'
  tmp_conditions['Natural_Area'] = 'A0'
  tmp_conditions['Natural Aspect Ratio'] = 'Q0'
  tmp_conditions['Goal_Angle'] = 'ThetaGoal'
  tmp_conditions['Modder'] = 'modder'
  tmp_conditions['Initial array'] = 'init_H'
  tmp_conditions['Dog R velocity'] = 'uR_mag'
  tmp_conditions['Dog theta velocity'] = 'uT_mag'
  tmp_conditions['Sample number'] = 'sample_number'

  '''output should be:
  timesteps, dt, lR, lT, lA, lQ, f0, ls, gamma, omega, delta, alpha, beta, delta, A0, Q0, ThetaGoal, modder, Hinit, uR_mag, 
  uT_mag, sample_number= load_params_auto()
  '''


  
  #variables that need to be integers
  ints = ['N_Timesteps', 'Sample number']
  arrays = ['Initial array']


  tmp_variables = OrderedDict()

  for key, value in tmp_conditions.items():
    fp = open('params.in')
    for line in fp:
      #print(line)
      broken_line = line.split(' #')
      if value in broken_line[1]: 
        if key in ints:
          tmp_variables[key] = int(broken_line[0])
        elif key in arrays:
          blah = broken_line[0].split(',')
          blah2 = [np.float(item) for item in blah]

          tmp_variables[key] = np.array(blah2)
        else:
          tmp_variables[key] = float(broken_line[0])
        #print("The ", key, ' is ', broken_line[0])
    fp.close()

  #print(tmp_variables.values)

  return tmp_variables.values()




