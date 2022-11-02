import sys
import os
sys.path.append(os.path.abspath("../../../python"))
from argparse import ArgumentParser
from pyAER import pyEDScorbotTool
import numpy as np

def cont_to_xyz(fname):
    parser = ArgumentParser()
    parser.add_argument("file",type=str,action="store")
    args = parser.parse_args()

    conts = np.array(j.load(open(fname)))
    qs = []
    xyz = []
    cs = []
    timestamps = []
    for row in conts:

        c1 = row[0] 
        c2 = row[1]
        c3 = row[2]
        c4 = row[3]
        ts = row[6]
        q1 = -(pyEDScorbotTool.count_to_angle(1,c1) * np.pi/180)
        q2 = -(pyEDScorbotTool.count_to_angle(2,c2) * np.pi/180)
        q3 = pyEDScorbotTool.count_to_angle(3,c3) * np.pi/180
        q4 = pyEDScorbotTool.count_to_angle(4,c4) * np.pi/180
        theta = np.array([q1,q2,q3,q4])
        f = robot.forward(theta)      
        #xyz.append(DirecKinScorbot(q1,q2,q3,q4))
        xyz.append(f.t_3_1.reshape([3, ]))
        qs.append([q1,q2,q3,q4])
        cs.append([c1,c2,c3,c4])
        timestamps.append(ts)
    return np.array(xyz),np.array(qs),np.array(cs),np.array(timestamps)
dh_params = np.array([[0.3585, 0.05, -0.5 * np.pi, 23.6*(np.pi/180)],
                      [-0.098, 0.3, 0., -22*(np.pi/180)],
                      [0.065, 0.35, 0., 22.4*(np.pi/180)],
                      [0., 0.22, 0., 0.]])
robot = RobotSerial(dh_params)



xyz,qs,cs,timestamps= cont_to_xyz('ejez_0.3-0.6_10sleep_nohome_out.json')
timestamps = timestamps - timestamps[0]