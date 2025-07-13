from pyAER import pyEDScorbotTool
import numpy as np

if __name__ == "__main__":
    
    config = pyEDScorbotTool(visible=False)
    bounds = np.array([[-155,155,],[-85,85],[-112.5,112.5],[-90,90]])
    
    for i in range(len(bounds)):
        bounds[i] = config.angle_to_ref(i+1,bounds[i])

    print(bounds)
        

    pass