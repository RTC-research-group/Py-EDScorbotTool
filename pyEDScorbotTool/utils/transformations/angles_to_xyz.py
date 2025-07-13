import numpy as np
from argparse import ArgumentParser
import pandas as pd
import sys, os
#sys.path.append(os.path.abspath("../../"))
sys.path.append(os.path.abspath("/media/HDD/home/enrique/Proyectos/SMALL/dataset/"))
#from pyAER import pyEDScorbotTool
from visual_kinematics.RobotSerial import RobotSerial

def direcKin(q1,q2,q3,q4):
    a1 = 5.0
    a2 = 30
    a3 = 35
    a4 = 22
    d1 = 35.85
    d2 = -9.8
    d3 = 6.5
    
    x= a1*np.cos(q1) + a2*np.cos(q1)*np.cos(q2) - a3*np.sin(q2)*np.sin(q3)*np.cos(q1) + a3*np.cos(q1)*np.cos(q2)*np.cos(q3) + a4*(-np.sin(q2)*np.sin(q3)*np.cos(q1) + np.cos(q1)*np.cos(q2)*np.cos(q3))*np.cos(q4) + a4*(-np.sin(q2)*np.cos(q1)*np.cos(q3) - np.sin(q3)*np.cos(q1)*np.cos(q2))*np.sin(q4) - d2*np.sin(q1) - d3*np.sin(q1)


    y= a1*np.sin(q1) + a2*np.sin(q1)*np.cos(q2) - a3*np.sin(q1)*np.sin(q2)*np.sin(q3) + a3*np.sin(q1)*np.cos(q2)*np.cos(q3) + a4*(-np.sin(q1)*np.sin(q2)*np.sin(q3) + np.sin(q1)*np.cos(q2)*np.cos(q3))*np.cos(q4) + a4*(-np.sin(q1)*np.sin(q2)*np.cos(q3) - np.sin(q1)*np.sin(q3)*np.cos(q2))*np.sin(q4) + d2*np.cos(q1) + d3*np.cos(q1)


    z= -a2*np.sin(q2) - a3*np.sin(q2)*np.cos(q3) - a3*np.sin(q3)*np.cos(q2) + a4*(np.sin(q2)*np.sin(q3) - np.cos(q2)*np.cos(q3))*np.sin(q4) + a4*(-np.sin(q2)*np.cos(q3) - np.sin(q3)*np.cos(q2))*np.cos(q4) + d1

    return x,y,z

def angles_to_xyz(angles):
                           #d,         a,          alpha,        theta
    dh_params = np.array([[0.3585   , 0.05      , 0.5 * np.pi   , -23.6*(np.pi/180)],
                          [-0.098   , 0.3       , np.pi         , 22*(np.pi/180)],
                          [0.065    , 0.35      , 0.            , 22.4*(np.pi/180)],
                          [0.       ,  0.22     , 0.            , 0.]])
    
    # dh_params = np.array([[0.3585   , 0.05      , -0.5 * np.pi  , 23.6*(np.pi/180)],
    #                       [-0.098   , 0.3       , 0.            , -22*(np.pi/180)],
    #                       [0.065    , 0.35      , 0.            , 22.4*(np.pi/180)],
    #                       [0.       ,  0.22     , 0.            , 0.]])
    robot = RobotSerial(dh_params)
    
    if angles.shape[1] != 4:
        aux = np.zeros(shape=(angles.shape[0],4)) 
        try:
            aux [:,0] = angles[:,0]  
            aux [:,1] = angles[:,1]  
            aux [:,2] = angles[:,2]  
            aux [:,3] = angles[:,3]  
        except:
            pass
        angles = aux
    qs = []
    xyz = []
    
    for row in angles:

        q1 = row[0] 
        q2 = row[1]
        q3 = row[2]
        q4 = row[3]
        
        theta = np.array([q1,q2,q3,q4])
        f = robot.forward(theta)      
        
        x,y,z = direcKin(q1,q2,q3,q4)
        xyz.append([x/100,y/100,z/100])
       # xyz.append(f.t_3_1.reshape([3, ]))
        qs.append([q1,q2,q3,q4])
        
    return np.array(xyz),(np.array(qs)*(180/np.pi))

if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("input_file",type=str,action="store",help="Numpy file (.npy or pickled) with angles in format (q1,q2,q3,q4) to be converted to xyz points")
    parser.add_argument("--output_file","-o",type=str,action="store",help="Name of the output file",default="xyz_out.npy")
    
    args = parser.parse_args()
    input_file = args.input_file
    output_file = args.output_file
    arr = np.load(input_file,allow_pickle=True)
    xyz,qs = angles_to_xyz(arr)
  
    
    
    np.save(output_file,xyz)
    print("Saved output to file {}".format(output_file))

