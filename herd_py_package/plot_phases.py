#python3

import numpy as np
import matplotlib.pyplot as plt
from sklearn import svm
import os


def colorator(phase):
    if phase == 0:
      return 1,0,0
    if phase == 1:
      return 0,1,0
    if phase == 2:
      return 0,0.2,1
    if phase == 3:
      return 0,0,0
    if phase ==4:
      return 1,0.7,0


def labels(phase):
  if phase == 0:
    return 'Droving'
  if phase == 1:
    return 'Driving'
  if phase == 2:
    return 'Mustering 1'
  if phase == 3:
    return 'Uncontrolled'
  if phase ==4: 
    return "Mustering 2"


def phase_plotter_func(Nfixed = 0, logscale = 1):

  print(os.getcwd())

  #download the data

  # if path.exists("comb_phase_data.txt"):
  #   p_dat = np.loadtxt('comb_phase_data.txt', skiprows=0)
  # else: 
  #   p_dat = np.loadtxt('average_phases.txt', skiprows=0)

  try: 
    p_dat = np.loadtxt('comb_phase_data.txt', skiprows=0)
  # except Warning:
  #   "User warning triggered!"
  #   p_dat = np.loadtxt('average_phases.txt', skiprows=0)
  except:
    p_dat = np.loadtxt('average_phases.txt', skiprows=0) 

  N = p_dat[:,0]
  ls = p_dat[:,1]
  ld = p_dat[:,2]
  vs = p_dat[:,3]
  vd = p_dat[:,4]
  phases = p_dat[:,5]
  #conf = p_dat[:,6]

  tmp_colors = [colorator(phases[k]) for k in range(len(phases))]
  #tmp_labels = [labels(phases[k]) for k in range(len(phases))]


# run with only 4 phases, not 5
  for kk in range(len(phases)):
    if phases[kk] == 2:
      phases[kk] = 0

  for phase in phases:
    if phase == 2:
      print("Error! Mustering phase not yet eliminated")


  

  #-------BEGIN------plotting parameters------------------


  if Nfixed == True:

    plt_title = str(int(N[0]))+"_agents.pdf"


    #set log_scale for data plotting
    if logscale == True: 
      x1 = np.log(ls/ld)
      x2 = np.log(vs/vd)
      y = phases

      x_label_1 = str(r'$\sqrt{N}\frac{l_a}{l_s}$') # x label for log-scale
      y_label_1 = str(r'$log(\frac{v_a}{v_d})$') # y label for log-scale
    


    if logscale == False:
      x1 = ls/ld
      x2 = vs/vd
      y = phases

    main_title = "Phase Diagram for " +str(int(N[0])) +" Agents:"

    

  else: 
    plt_title = ".pdf"

    if logscale == True:
      x1 = np.log(np.sqrt(N)*ls/ld)
      x2 = np.log(vs/vd)
      y = phases

      x_label_1 = str(r'$log(\sqrt{N}\frac{l_a}{l_s})$') # x label for log-scale
      y_label_1 = str(r'$log(\frac{v_a}{v_s})$') # y label for log-scale


      plt_title = "_logscale.pdf"


    if logscale == False:
      x1 = np.sqrt(N)*ls/ld
      x2 = vs/vd
      y = phases


      x_label_1 = str(r'$\sqrt{N}\frac{l_a}{l_s}$') # x label for lin-scale
      y_label_1 = str(r'$\frac{v_a}{v_s}$') # y label for lin-scale

      plt_title = "_linscale.pdf"

    main_title = "Phase Diagram "


  figres = (10,8) #figure resolution and size

  title_on = 0 #decide whether plots should have titles



  

  #---------BEGIN SVM boundary drawing------------------

  mat = np.stack((x1,x2,y), axis = -1)
  X = mat[:, :2]

  if logscale == True:
    #clf = svm.SVC(kernel='rbf', gamma=.5)
    clf = svm.SVC(kernel='rbf', gamma=0.7)
  
  if logscale == False:
    clf = svm.SVC(kernel='linear', gamma=.5)
  
  clf.fit(X,y),y

  plt_extra_x_dist = 0.1*np.abs(np.max(x1)-np.min(x1))
  #print("np.min(x2): ", np.min(x1))
  plt_extra_y_dist = 0.1*np.abs(np.max(x2)-np.min(x2))

  #meshsize 
  h = 0.005
  # create a mesh to plot in
  x_min, x_max = np.min(x1)-plt_extra_x_dist, np.max(x1)+plt_extra_x_dist
  y_min, y_max = np.min(x2)-plt_extra_y_dist, np.max(x2)+plt_extra_y_dist
  xx, yy = np.meshgrid(np.arange(x_min, x_max, h),
                       np.arange(y_min, y_max, h))


  Z = clf.predict(np.c_[xx.ravel(), yy.ravel()])
  #print("Made it here!!")

  #color map
  color_map = {0: (1,0,0), 1: (0, 1, 0), 2: (0, 0.2, 1), 3: (0, 0, 0), 4: (1, 0.7, 0)}

  #---------END SVM boundary drawing--------------------




  #-----SET plot titles------------
  title_1 = " Data Only"
  title_2 = " SVM Only"
  title_3 = " Data with SVM Color Overlay."
  #-------------------------------------

  #-------END------plotting parameters------------------


  #data only figure
  plt.figure(figsize = figres)
  plt.scatter(x1, x2, c = tmp_colors, marker = '.')
  if title_on ==1: 
    plt.title(main_title+title_1)
  plt.xlabel(x_label_1)
  plt.ylabel(y_label_1)
  plt.legend()
  plt.savefig("Phase_data_"+plt_title)



  #SVM only figure
  plt.figure(figsize = figres)
  if title_on ==1:
    plt.title(main_title+title_2)
  Z = Z.reshape(xx.shape)
  #plt.contourf(xx, yy, Z, levels = [-1,0,1,2,3,4], alpha = 1, colors =['red','green', 'blue', 'black', 'orange'], extend = 'both') #cmap=plt.cm.Paired)
  plt.contourf(xx, yy, Z, levels = [-1,0,1,2,3,4], alpha = .3, colors =['red','green', 'blue', 'black', 'orange'], extend = 'both') #cmap=plt.cm.Paired)
  colors = [color_map[i] for i in y]
  #plt.legend()
  plt.savefig("Phase_SVM_"+plt_title)

  
  #main figure with data and SVM overlay
  plt.figure(figsize = figres)
  if title_on ==1:
    plt.title(main_title+title_3)
  Z = Z.reshape(xx.shape)
  plt.contourf(xx, yy, Z, levels = [-1,0,1,2,3,4], alpha = .3, colors =['red','green', 'blue', 'black', 'orange'], extend = 'both') #cmap=plt.cm.Paired)
  colors = [color_map[i] for i in y]
  plt.scatter(X[:, 0], X[:, 1], c=colors, marker = ".", alpha = 0.8)
  plt.xlabel(x_label_1, fontsize=20)
  plt.ylabel(y_label_1, fontsize = 20)
  #plt.ylim(0,10)
  plt.savefig("Phase_SVM_and_data_"+plt_title)
  #plt.legend()


def pull_data_Phase_v1(pull_type):


  if pull_type == "phase_1":

    #extract current folder name
    f_name = os.getcwd().split('/')[-1]

    #get data from base:

    #base_extract = "aditya@10.243.53.250:/home3/aditya/new_phase_test/"

    #base_extract = "aditya@10.243.53.250:/home3/aditya/phases_class_based_code/"

    #base_extract = "aditya@10.243.53.250:/home3/aditya/smaller_weight/SI/fixed_N/"

    base_extract = "aditya@10.243.53.250:/home3/aditya/smaller_weight/SI"

    
    #end naming convention
    #end_extract = "/main_phase/Final_phase_data.txt"

    end_extract = '/Final_phase_data.txt'

    #save data to location
    save_to = "./main_phase" 
    #save_to = "."

    #construct pull command
    pull_command_1 = "rsync -avze ssh " +base_extract + f_name + end_extract + " " + save_to

    print(pull_command_1)

    return pull_command_1

  else:
    print("No pull-type specified!")


def pull_data_from_server(override=0):

   #setting this up for an eventual override

  if override==0:
    pull_or_not = input("Pull data from server? Please type 'y' or 'n'.  ")
  else:
    pull_or_not=1


  if pull_or_not == "Y" or pull_or_not == "y" or pull_or_not == "yes" or pull_or_not == "Yes":

    pull_command = pull_data_Phase_v1('phase_1')

    #pull latest main-phase
    os.system(pull_command)


    #automate this process next
    os.system("cat ./main_phase/Final_phase_data.txt >comb_phase_data.txt")


