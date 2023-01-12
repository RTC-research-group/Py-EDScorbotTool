import numpy as np
from argparse import ArgumentParser
import pandas as pd
import sys, os
sys.path.append(os.path.abspath("../../../../python"))
#from pyAER import pyEDScorbotTool
from copy import deepcopy
from .angles_to_refs import angles_to_refs
from .pad_trajectory import pad
import json

def angles_to_json(df):
    df[0] = -df[0]
    df[1] = -df[1]
    
    df = angles_to_refs(df) #angles to refs
    new_arr = pad(df.to_numpy()) #pad reference trajectory
    return new_arr

if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("input_file",type=str,action="store",help="Numpy file (.npy or pickled) with angles in format (q1,q2,q3,q4) to be converted to references")
    parser.add_argument("--output_file","-o",type=str,action="store",help="Name of the output file",default="6dims_converted_out.npy")
    
    args = parser.parse_args()
    input_file = args.input_file
    output_file = args.output_file
    arr = np.load(input_file,allow_pickle=True)
    df = pd.DataFrame(arr)
    #Cambiamos la direccion del movimiento (no coincide entre visual kinematics y la realidad)
    df[0] = -df[0]
    df[1] = -df[1]
    
    df = transform(df) #angles to refs
    new_arr = pad(df.to_numpy()) #pad reference trajectory
    
   
    f = open(output_file,"w")
    
    js = json.dump(new_arr.tolist(),f,indent=4)
    
    f.close()
    print("Saved output to file {}".format(output_file))
