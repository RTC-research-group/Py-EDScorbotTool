import pyAER
import datetime
import time

def log_position(j,handler,logfile=None):
    read = -1234567
    if j ==1:
        read = handler.Read_J1_pos()
    elif j ==2:
        read = handler.Read_J2_pos()
    elif j ==3:
        read = handler.Read_J3_pos()
    elif j ==4:
        read = handler.Read_J4_pos()
    elif j ==5:
        read = handler.Read_J5_pos()
    elif j ==6:
        read = handler.Read_J6_pos()
    else:
        handler.alert("Invalid number of joint")
    
    if(logfile is not None):
        with open(logfile,'a') as f:
            dt = datetime.datetime.now().isoformat()
            s = str(dt) + " Position of joint " + str(j) + ": " + str(read)
            f.write(s)

    return read

if __name__ == "__main__":
    #Instance the class
    robot_handler = pyAER.pyAER(visible=False)

    # Init configuration, although we called render_gui it won't render anything because
    # we passed the "visible" parameter as False to constructor
    robot_handler.render_gui()

    # Check the open USB connection checkbox as we would do in GUI
    robot_handler.checked.set(True)
    # Then open the USB
    robot_handler.checkUSB()
    # We store the dictionary that contains the motors' variables
    # to access them easily
    motors = robot_handler.d["Motor Config"]

    #Initialize the robot in order to work with it
    robot_handler.search_Home_J1()
    time.sleep(2)
    robot_handler.search_Home_J2()
    time.sleep(2)
    robot_handler.search_Home_J3()
    time.sleep(2)
    robot_handler.search_Home_J4()
    time.sleep(2)
    
    
    #Finish initialization calling ConfigureInit and ConfigureSPID
    robot_handler.ConfigureInit()
    robot_handler.ConfigureSPID()

    #Then move the robot's joints
    motors["ref_M1"].set(50)
    robot_handler.SendCommandJoint1_lite()
    log_position(1,robot_handler,"./log.txt")
    time.sleep(2)
    
    motors["ref_M2"].set(100)
    robot_handler.SendCommandJoint2_lite()
    time.sleep(2)
    
    motors["ref_M3"].set(100)
    robot_handler.SendCommandJoint3_lite()
    time.sleep(2)

    motors["ref_M4"].set(-100)
    robot_handler.SendCommandJoint4_lite()
    time.sleep(2)
    #Access and change
    pass
            
    #print(robot_handler.d)

