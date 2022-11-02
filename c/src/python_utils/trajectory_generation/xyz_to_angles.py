import numpy as np
from argparse import ArgumentParser
import pandas as pd
import sys, os
sys.path.append(os.path.abspath("../../../python"))
from visual_kinematics import RobotSerial, RobotTrajectory, Frame

dh_params = np.array([[0.3585, 0.05, -0.5 * np.pi, 23.6*(np.pi/180)],
                      [-0.098, 0.3, 0., -22*(np.pi/180)],
                      [0.065, 0.35, 0., 22.4*(np.pi/180)],
                      [0., 0.22, 0., 0.]])    
    


def Line3d(x_0=0, y_0=0, z_0=0, x_1=0, y_1=0, z_1=0, points=250):
	
    # Parameter array
    t = np.linspace(0,1,points)
            
        # Parametric Lemniscata Formulae
    x = x_0 + (x_1-x_0) * t
    y = y_0 + (y_1-y_0) * t
    z = z_0 + (z_1-z_0) * t

    return [x,y,z]

if __name__== '__main__':
    pass
    
    robot = RobotSerial(dh_params)
    robot.ws_lim = np.array([[-125*np.pi/180, 125*np.pi/180], [-135*np.pi/180, 30*np.pi/180], [-112.5*np.pi/180, 112.5*np.pi/180], [-np.pi/2, np.pi/2]])
    robot.ws_division = 10
    robot.plot_xlim = [-1, 1]
    robot.plot_ylim = [-1, 1]
    robot.plot_zlim = [0, 1]
    
    x,y,z = Line3d(15,8,20,15,8,40,100);
    #x,y,z = Lemniscate_rot3D(90,0,90,10,100,15,8,20,0,45);
    x=x/30
    y=y/60
    z=z/60

    print (x)
    frames = []

    for i in range(100):
        #print (x[0][i])
        #print(y[0][i])
        #print(z[0][i])
        frames.append(Frame.from_euler_3(np.array([np.pi, np.pi, 0.0]), np.array([[x[i]], [y[i]], [z[i]]])))
        print(frames[i].t_4_4)
    time_points = np.arange(100)*1.0;    
    trajectory = RobotTrajectory(robot, frames, time_points);

    values, timeslots = trajectory.show(motion="p2p",num_segs=10);