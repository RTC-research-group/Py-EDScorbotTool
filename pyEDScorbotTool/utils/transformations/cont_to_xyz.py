import sys
sys.path.append('.')
from .count_to_angle import cont_to_angle
from .angles_to_xyz import angles_to_xyz
#from ...pyAER import pyEDScorbotTool
from argparse import ArgumentParser
import numpy as np
import json as j

def cont_to_xyz(cont):
    qs,cs,timestamps= cont_to_angle(cont)

    xyz,_ = angles_to_xyz(qs)
    return xyz

def cont_to_xyz_cli(args):
    #print(args)
    input_file = args.input_file
    output_file = args.output_file
    include_timestamps = args.include_timestamps
    numpy =  args.numpy

    if numpy:
        conts = np.load(input_file,allow_pickle=True)
    else:
        conts = np.array(j.load(open(input_file,'r')))    
    qs,cs,timestamps= cont_to_angle(conts)

    xyz,_ = angles_to_xyz(qs)
    
    if include_timestamps:
        import pandas
        df = pandas.DataFrame(xyz)
        df[3] = timestamps
        np.save(output_file,df.to_numpy())
        
    else:
        np.save(output_file,xyz)
    
    print("Saved output to file {}".format(output_file))
    print("Timestamp included: {}".format("Yes" if include_timestamps else "No"))

    pass

if __name__== '__main__':

    parser = ArgumentParser()
    parser.add_argument("input_file",type=str,action="store",help="JSON file with counters output in EDScorbot format n tuples of (j1,j2,j3,j4,j5,j6,timestamp) elements")
    parser.add_argument("--output_file","-o",type=str,action="store",help="Name of the output file",default="xyz_out.npy")
    parser.add_argument("--include_timestamps","-ts",action="store_true",help="Include timestamps in the output file. Output will be in (q1,q2,q3,q4,timestamp) format",default=False)
    parser.add_argument("--numpy","-np",action="store_true",help="Convert file from Numpy array instead of JSON",default=False)
    args = parser.parse_args()
    cont_to_xyz_cli(args)
    