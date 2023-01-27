import numpy as np
from argparse import ArgumentParser
import pandas as pd
import sys, os
sys.path.append(os.path.abspath("../../../../python"))
from pyAER import pyEDScorbotTool
from visual_kinematics.RobotSerial import RobotSerial

def angles_to_xyz(angles):

    dh_params = np.array([[0.3585, 0.05, -0.5 * np.pi, 23.6*(np.pi/180)],
                      [-0.098, 0.3, 0., -22*(np.pi/180)],
                      [0.065, 0.35, 0., 22.4*(np.pi/180)],
                      [0., 0.22, 0., 0.]])
    robot = RobotSerial(dh_params)
    
    
    qs = []
    xyz = []
    
    for row in angles:

        q1 = row[0] 
        q2 = row[1]
        q3 = row[2]
        q4 = row[3]
        
        theta = np.array([q1,q2,q3,q4])
        f = robot.forward(theta)      
        #xyz.append(DirecKinScorbot(q1,q2,q3,q4))
        xyz.append(f.t_3_1.reshape([3, ]))
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

