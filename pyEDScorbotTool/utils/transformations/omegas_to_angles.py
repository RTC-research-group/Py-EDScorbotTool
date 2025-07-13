import numpy as np
from argparse import ArgumentParser
#codigo correcto
def w_to_angles(omegas):
    # angles = np.zeros((500,2),float)
    # #angles = np.cumsum(omegas*0.001,axis=1)* (180/np.pi)
    # angles[0][0]=(omegas[0][0]*0.001)*(180/np.pi)
    # angles[0][1]=(omegas[0][1]*0.001)*(180/np.pi)
    # for i in range(1,len(omegas)):
    #     angles[i][0] = ((omegas[i][0] * 0.001*180/np.pi) + angles[i-1][0])
    #     angles[i][1] = ((omegas[i][1] * 0.001*180/np.pi) + angles[i-1][1])
    # return  angles
    return np.cumsum(omegas * 0.001,axis=0)*( 180 / np.pi)


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("file",type=str,action="store")
    args = parser.parse_args()
    arr = np.load(args.file,allow_pickle=True)
    
    arr = w_to_angles(arr)
    fname = args.file[:-4] + "_angles"
    np.save(fname,arr)
