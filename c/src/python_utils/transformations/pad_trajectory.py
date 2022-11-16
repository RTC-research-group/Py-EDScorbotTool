import numpy as np
import json
from argparse import ArgumentParser

'''
This script receives a trajectory file as input (format can be .npy or pickled files (.p)) and outputs a padded, json version of it. 
The input file is expected to be a numpy array of shape (m,n), where m can be any number of points and n <= 6, indicating how many joints should the trajectory affect
The output file is a json version of the numpy array that was inputted, however this json version is of fixed shape (m,6), because the software that executes 
trajectories in the robot will always expect an array of shape (m,6).
Usage of this script is not necessary if the trajectory is already in the shape (m,6). Conversion to json format is still needed, though.
'''


if __name__== '__main__':
    parser = ArgumentParser()
    parser.add_argument("file",type=str,action="store",help="Name of input file")
    parser.add_argument("--out_file","-o",type=str,action="store",help="Name of desired output file",default="6_dims_converted.json")
    args = parser.parse_args()
    arr = np.load(args.file,allow_pickle=True)
    n_to_fill = None
    shape = arr.shape
    new_arr = np.zeros((shape[0],6))
    if shape[1] < 6:
        n_to_fill = 6 -shape[1]
    
    if n_to_fill != None:
        #Hay que rellenar la trayectoria con 0s
        for i in range(arr.shape[0]):
            for j in range(6-n_to_fill):
                new_arr[i][j] = arr[i][j]
                
    pass


    f = open(args.out_file,"w")
    
    d_js = {
        "J1":new_arr[:,0].tolist(),
        "J2":new_arr[:,1].tolist(),
        "J3":new_arr[:,2].tolist(),
        "J4":new_arr[:,3].tolist(),
        "J5":new_arr[:,4].tolist(),
        "J6":new_arr[:,5].tolist()
    }
    
    js = json.dump(d_js,f,indent=4)
    f.close()
    
