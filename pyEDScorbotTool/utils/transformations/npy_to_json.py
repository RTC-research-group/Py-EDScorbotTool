import numpy as np
import json
from argparse import ArgumentParser

if __name__== '__main__':
    parser = ArgumentParser()
    parser.add_argument("file",type=str,action="store")
    args = parser.parse_args()
    arr = np.load(args.file,allow_pickle=True)
    f = open("./converted.json","w")
    #js = json.dump(arr.tolist(),f)
    try:
        d_js = {
            "J1":arr[:,0].tolist(),
            "J2":arr[:,1].tolist(),
            "J3":arr[:,2].tolist(),
            "J4":arr[:,3].tolist(),
            "J5":arr[:,4].tolist(),
            "J6":arr[:,5].tolist()
        }
    except Exception as e:
        d_js = {
            "J1":arr[:,0].tolist(),
            "J2":arr[:,1].tolist(),
            "J3":arr[:,2].tolist(),
            "J4":arr[:,3].tolist(),
        }

    js = json.dump(d_js,f,indent=4)
    f.close()
    
