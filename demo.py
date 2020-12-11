import pyAER
import time
if __name__ == "__main__":
    #Instance the class
    robot_handler = pyAER.pyAER(visible=False)

    #Init configuration but not make gui visible
    robot_handler.render_gui()
    #All parameters are in a dictionary called "d" within the pyAER object
    
    #Access and change
    pass
            
    #print(robot_handler.d)

