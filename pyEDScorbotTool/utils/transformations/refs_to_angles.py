import numpy as np
from argparse import ArgumentParser
import pandas as pd
import sys, os
sys.path.append(os.path.abspath("../../"))
#from pyAER import pyEDScorbotTool
def ref_to_angle(motor,ref,strict=True):
        """
        Convert reference of motor to angle

        This function takes a motor and a reference and 
        returns the corresponding angle to said reference
        for that specific motor

        Args:
            motor (int): Number of the motor (1-4)
            ref (int): reference to be converted
            strict (boolean): Whether to restrict angle values to ther maximum bounds or not (default is True)

        
        Returns:
            float: Angle that corresponds to the reference given for the given motor or the joint's limit if the calculated reference is above (or below) it
        """
        f = lambda x:x

        bounds = [[155,-155,],[85,-85],[112.5,-112.5],[90,-90]]

        #############DEPRECATED################
        # if motor == 1:
        #     f = lambda x: (-1/3)*x
        # elif motor == 2:
        #     f = lambda x: ((-11/100)*x) + 53
        # elif motor == 3:
        #     #To be characterised
        #     if ((ref >=-400) and (ref <= 200)):
        #         f = lambda x: ((-67/200)*x) + 11
        #     else:
        #         self.alert("Joint 3 out of range. Ref must be between 200 and -400")
        #         return
        # elif motor == 4:
        #     f = lambda x:((9/50)*x) + 2
        ########################################

        if motor == 1: 
            f = lambda x:-(1/3)*x
        elif motor == 2:
            f = lambda x:-(1/9.4)*x
        elif motor == 3:
            f = lambda x:-(1/-3.0)*x
        elif motor == 4:
            f = lambda x: -0.056780795*x

        ret = f(ref)
        if not(ret < bounds[motor-1][0] and ret > bounds[motor-1][1]) and strict:
            ret = bounds[motor-1][0]*np.sign(ret)

        return ret

if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("input_file",type=str,action="store",help="Numpy file (.npy or pickled) with references in format (rj1,rj2,rj3,rj4) to be converted to angles")
    parser.add_argument("--output_file","-o",type=str,action="store",help="Name of the output file",default="angles_out.npy")
    
    args = parser.parse_args()

    input_file = args.input_file
    output_file = args.output_file

    arr = np.load(input_file,allow_pickle=True)
    df = pd.DataFrame(arr)
    i = 0
    for name, values in df.iteritems():
        #print(name,values)
        values = ref_to_angle(name+1,values)
        df[i] = values
        i+=1
    
    
    np.save(output_file,df.to_numpy())
    print("Saved output to file{}".format(output_file))
