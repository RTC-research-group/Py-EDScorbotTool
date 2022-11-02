import numpy as np
from argparse import ArgumentParser
import pandas as pd
import math

def angle_to_ref(motor,angle,strict=False):
        """
        Convert angle of motor to reference

        This function takes a motor and an angle and 
        returns the corresponding reference to said angle
        for that specific motor.

        Args:
            motor (int): Number of the motor (1-4)
            angle (int): angle to be converted
            strict (boolean): Whether to restrict reference values to ther maximum bounds or not (default is True)
        
        Returns:
            float: Reference that corresponds to the angle given for the given motor or the joint's limit if the calculated reference is above (or below) it
        """
        f = lambda x:x

        bounds = [[400,-400],[700,-900],[300,-400],[1583,-1583]]
        ##############DEPRECATED#############
        #These are the inverse of the functions that appear in ref_to_angle function
        
        # if motor == 1:
        #     f = lambda x: (-3)*x #https://www.symbolab.com/solver/function-inverse-calculator/inverse%20f%5Cleft(x%5Cright)%3D-%5Cfrac%7B1%7D%7B3%7Dx
        # elif motor == 2:
        #     f = lambda x: -(((100*x) - 5300)/11) #https://www.symbolab.com/solver/function-inverse-calculator/inverse%20f%5Cleft(x%5Cright)%3D%20-%5Cfrac%7B11%7D%7B100%7Dx%2B53
        # elif motor == 3:
        #     if ((angle >=-66.5) and (angle <= 143.5)):
        #         f = lambda x: -(((200*x)-2200)/67) #https://www.symbolab.com/solver/function-inverse-calculator/inverse%20f%5Cleft(x%5Cright)%3D-%5Cfrac%7B67%7D%7B200%7Dx%2B11
        #     else:
        #         self.alert("Joint 3 out of range. Angle must be between 143.5 and -66.5")
        #         return
        # elif motor == 4:
        #     f = lambda x:-(((50*x)-100)/9) #https://www.symbolab.com/solver/function-inverse-calculator/inverse%20f%5Cleft(x%5Cright)%3D%5Cfrac%7B9%7D%7B50%7Dx%20%2B2
        #####################################

        if motor == 1:
            #f = lambda x:-3.1428474*x
            f = lambda x:-3*x
        elif motor == 2:
            #f = lambda x:-8.824695*x
            f = lambda x:-9.4*x
        elif motor == 3:
            #f = lambda x:-3.4044209*x
            f = lambda x:-3.1*x
        elif motor ==4:
            f = lambda x:-17.61158871*x
        else:
            return 0

        ret = round(f(angle))
        # if not(ret < bounds[motor-1][0] and ret > bounds[motor-1][1]) and strict:
        #     ret = bounds[motor-1][0]*np.sign(ret)

        return ret

if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("file",type=str,action="store")
    args = parser.parse_args()
    arr = np.load(args.file,allow_pickle=True)
    df = pd.DataFrame(arr)
    l = []
    i = 0
    for name, values in df.iteritems():
        #print(name,values)
        values = angle_to_ref(name+1,values)
        df[i] = values
        i+=1
    
    fname = args.file[:-4] + "_refs"
    np.save(fname,df.to_numpy())
