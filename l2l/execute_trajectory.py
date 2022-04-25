from nis import match
import sys
  
# setting path
sys.path.append('../')

from pyAER import pyEDScorbotTool
import argparse
from transformations import w_to_angles
import numpy as np
from scorbot_direct_kinematics import direct_kinematics_position

if __name__== '__main__':

    parser = argparse.ArgumentParser(description="Trajectory execution tool to include ED-Scorbot in the L2L loop",allow_abbrev=True)
    parser.add_argument("trajectory",type=str,help="Trajectory file in NumPy format. By default, trajectories should be specified in angular velocities")
    parser.add_argument("--noconv","-n",help="Specify this flag to indicate that the input trajectory should not be converted to angles",action="store_const",const=True,default=False)
    parser.add_argument("--counters","-c",type=str,help="Name of the file in which we will store the time-stepped output in counter format",default=None)
    parser.add_argument("--position","-xyz",type=str,help="Name of the file in which we will store the time-stepped output in xyz format",default=None)

    args = parser.parse_args()

    traj = np.load(args.trajectory,allow_pickle=True)

    if not args.noconv:#Esto significa que hay que hacer la conversión
        traj = w_to_angles(traj)
        pass

    #Asumimos que el robot ha hecho el home previamente y que todo esta inicializado
    #Ejecucion de la trayectoria
    match_steps = []
    handler = pyEDScorbotTool(visible=False)
    handler.render_gui()
    handler.init_config()
    handler.checked.set(True)
    handler.checkUSB()
    sleep = 0.25
    handler.toggle_record()
    tj1 = handler.angle_to_ref(1,traj[:,0])
    tj2 = handler.angle_to_ref(2,traj[:,1])
    
    for j1,j2 in zip(tj1,tj2):
        match_steps.append([handler.Read_J1_pos(),handler.Read_J2_pos(),handler.Read_J3_pos(),handler.Read_J4_pos()])
        handler.d["Motor Config"]["ref_M1"].set(j1)
        handler.d["Motor Config"]["ref_M2"].set(j2)
        handler.SendCommandJoint1_lite()
        handler.SendCommandJoint2_lite()
       
        t1 = handler.millis_now()
        t2 = t1
        while not ((t2-t1)>=sleep*1000):
            handler.update()
            t2 = handler.millis_now()
        
        pass
    handler.update()
    handler.toggle_record()
    pass

    xyz_steps = []
    for j1,j2,j3,j4 in match_steps:
        a1 = handler.count_to_angle(1,j1)
        a2 = handler.count_to_angle(2,j2)
        xyz = direct_kinematics_position(a1*(np.pi/180),a2*(np.pi/180),0,0)
        xyz_steps.append(xyz)

    print(xyz_steps)
    print(match_steps)

    match_steps = np.array(match_steps)
    xyz_steps = np.array(xyz_steps)

    if args.counters == None:
        np.save("./counters_out.npy",match_steps,allow_pickle=True)
    else:
        np.save(args.counters,match_steps,allow_pickle=True)
    
    if args.position == None:
        np.save("./xyz_out.npy",xyz_steps,allow_pickle=True)
    else:
        np.save(args.position,xyz_steps,allow_pickle=True)

    
    