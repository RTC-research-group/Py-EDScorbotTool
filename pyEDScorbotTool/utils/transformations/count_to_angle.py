import sys
import os
sys.path.append(os.path.abspath("../../"))
sys.path.append(os.path.abspath("../"))
sys.path.append(os.path.abspath("/media/HDD/home/enrique/Proyectos/SMALL/dataset"))
from argparse import ArgumentParser
#from pyEDScorbotTool import pyAER
import numpy as np
from visual_kinematics.RobotSerial import RobotSerial
import json as j
def count_to_angle(motor,count):
        """
        Convert counter of motor to estimated angle

        This function takes a motor and its collected position and 
        returns the corresponding estimated angle to said position
        for that specific motor.

        Args:
            motor (int): Number of the motor (1-4)
            count (int): Position counter to be converted
        
        Returns:
            float: Estimated angle that corresponds to the position given for the given motor 
        """
        f = lambda x:x

        if motor == 1:
            f = lambda x:(1/125.5)*(x-32768)
        elif motor == 2:
            f = lambda x:(1/131)*(x-32768)
        elif motor == 3:
            f = lambda x:(1/132.5)*(x-32768)
        elif motor ==4:
            f = lambda x:0.012391573729863692*(x-32768)
        else:
            f = lambda x:x

        
        

        return f(count)
def cont_to_angle(conts):
    
    qs = []
    cs = []
    timestamps = []
    for row in conts:

        c1 = row[0] 
        c2 = row[1]
        c3 = row[2]
        c4 = row[3]
        ts = row[6]
        q1 = -(count_to_angle(1,c1) * np.pi/180)
        q2 = -(count_to_angle(2,c2) * np.pi/180)
        q3 = count_to_angle(3,c3) * np.pi/180
        q4 = count_to_angle(4,c4) * np.pi/180
        
        qs.append([q1,q2,q3,q4])
        cs.append([c1,c2,c3,c4])
        timestamps.append(ts)
    return np.array(qs),np.array(cs),np.array(timestamps)



if __name__== '__main__':
    
    parser = ArgumentParser()
    parser.add_argument("input_file",type=str,action="store",help="JSON file with counters output in EDScorbot format n tuples of (j1,j2,j3,j4,j5,j6,timestamp) elements")
    parser.add_argument("--output_file","-o",type=str,action="store",help="Name of the output file",default="angles_out.npy")
    parser.add_argument("--include_timestamps","-ts",action="store_true",help="Include timestamps in the output file. Output will be in (q1,q2,q3,q4,timestamp) format",default=False)
    args = parser.parse_args()

    cont_file = args.input_file
    output_file = args.output_file
    include_timestamps = args.include_timestamps
    conts = np.array(j.load(open(cont_file,'r')))
    qs,cs,timestamps= cont_to_angle(conts)
    

    if include_timestamps:
        import pandas
        df = pandas.DataFrame(qs)
        df[4] = timestamps
        np.save(output_file,df.to_numpy())
        
    else:
        np.save(output_file,qs)

    print("Saved output to file {}".format(output_file))
    print("Timestamp included: {}".format("Yes" if include_timestamps else "No"))




