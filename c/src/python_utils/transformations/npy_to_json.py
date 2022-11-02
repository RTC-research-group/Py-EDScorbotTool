import numpy as np
import json
from argparse import ArgumentParser

if __name__== '__main__':
    parser = ArgumentParser()
    parser.add_argument("file",type=str,action="store")
    args = parser.parse_args()
    arr = np.load(args.file,allow_pickle=True)
    f = open("./converted.json","w")
    js = json.dump(arr.tolist(),f)
    
