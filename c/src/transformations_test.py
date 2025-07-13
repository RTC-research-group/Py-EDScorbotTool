import sys

import numpy as np
sys.path.append("/home/enrique/Trabajo/Py-EDScorbotTool/l2l")
import transformations
import numpy as np
np.set_printoptions(suppress=True)
arr = np.load("/home/enrique/Trabajo/Py-EDScorbotTool/c/src/target1.npy")
angs = transformations.w_to_angles(arr)
print(angs)


