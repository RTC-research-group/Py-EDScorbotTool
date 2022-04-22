import sys
  
# setting path
sys.path.append('../')

from pyAER import pyEDScorbotTool
import argparse
from transformations import w_to_angles
import numpy as np

if __name__== '__main__':

    parser = argparse.ArgumentParser(description="Trajectory execution tool to include ED-Scorbot in the L2L loop",allow_abbrev=True)
    parser.add_argument("trajectory",type=str,help="Trajectory file in NumPy format. By default, trajectories should be specified in angular velocities")
    parser.add_argument("--noconv","-n",help="Specify this flag to indicate that the input trajectory should not be converted to angles",action="store_const",const=False)
    
    args = parser.parse_args()

    traj = np.load(args.trajectory,allow_pickle=True)

    if args.noconv == None:#Esto significa que hay que hacer la conversión
        traj = w_to_angles(traj)
        pass

    #Asumimos que el robot ha hecho el home previamente y que todo esta inicializado
    #Ejecucion de la trayectoria
    handler = pyEDScorbotTool(visible=False)
    for j1,j2 in traj:
        handler.SendCommandJoint1_lite(j1)
        handler.SendCommandJoint2_lite(j2)
        t = handler.millis_now()
        while()
        pass

    pass