import numpy as np
from argparse import ArgumentParser
import pandas as pd
import sys, os
sys.path.append(os.path.abspath("../../../python"))
from pyAER import pyEDScorbotTool


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("input_file",type=str,action="store",help="Numpy file (.npy or pickled) with angles in format (q1,q2,q3,q4) to be converted to references")
    parser.add_argument("--output_file","-o",type=str,action="store",help="Name of the output file",default="refs_out.npy")
    
    args = parser.parse_args()
    input_file = args.input_file
    output_file = args.output_file
    arr = np.load(input_file,allow_pickle=True)
    df = pd.DataFrame(arr)
    l = []
    i = 0
    for name, values in df.iteritems():
        #print(name,values)
        values = pyEDScorbotTool.angle_to_ref(name+1,values)
        df[i] = values
        i+=1
    
    
    np.save(output_file,df.to_numpy())
    print("Saved output to file{}".format(output_file))
