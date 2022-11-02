import sys
import os
sys.path.append(os.path.abspath("../../../python"))
sys.path.append(os.path.abspath("../"))
sys.path.append(os.path.abspath(r"D:\Universidad\Master\Ondrive Cloud\OneDrive - UNIVERSIDAD DE SEVILLA\Trabajo\SMALL\dataset"))
from argparse import ArgumentParser
from pyAER import pyEDScorbotTool
import numpy as np
from visual_kinematics import RobotSerial

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
        q1 = -(pyEDScorbotTool.count_to_angle(1,c1) * np.pi/180)
        q2 = -(pyEDScorbotTool.count_to_angle(2,c2) * np.pi/180)
        q3 = pyEDScorbotTool.count_to_angle(3,c3) * np.pi/180
        q4 = pyEDScorbotTool.count_to_angle(4,c4) * np.pi/180
        
        qs.append([q1,q2,q3,q4])
        cs.append([c1,c2,c3,c4])
        timestamps.append(ts)
    return np.array(qs),np.array(cs),np.array(timestamps)



if __name__== '__main__':
    
    parser = ArgumentParser()
    parser.add_argument("input_file",type=str,action="store",help="JSON file with counters output in EDScorbot format n tuples of (j1,j2,j3,j4,j5,j6,timestamp) elements")
    parser.add_argument("--output_file","-o",type=str,action="store",help="Name of the output file",default="angles_out.npy")
    parser.add_argument("--include_timestamps","-ts",type=bool,action="store_true",help="Include timestamps in the output file. Output will be in (q1,q2,q3,q4,timestamp) format",default=False)
    args = parser.parse_args()

    cont_file = args.input_file
    output_file = args.output_file
    include_timestamps = args.include_timestamps
    conts = np.load(cont_file,allow_pickle=True)
    qs,cs,timestamps= cont_to_angle(cont_file)
    

    if include_timestamps:
        import pandas
        df = pandas.DataFrame(qs)
        df[4] = cs
        np.save(output_file,df.to_numpy())
        
    else:
        np.save(output_file,qs)

    print("Saved output to file{}".format(output_file))
    print("Timestamp included: {}".format("Yes" if include_timestamps else "No"))




