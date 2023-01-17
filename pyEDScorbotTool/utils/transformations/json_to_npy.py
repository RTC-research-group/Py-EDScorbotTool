import numpy as np
import json
from argparse import ArgumentParser

if __name__== '__main__':
    parser = ArgumentParser()
    parser.add_argument("in_file",type=str,action="store")
    parser.add_argument("out_file",type=str,action="store")
    args = parser.parse_args()
    
    j = json.load(open(args.in_file))
    
    a = 1
    l = []
    for row in j:
        l.append([row[0],row[1],row[2],row[3],row[4],row[5],row[6]])
    arr = np.array(l)
    np.save(args.out_file,arr)
