import pyAER
import datetime
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
        with open(logfile) as f:
            dt = datetime.datetime.now().isoformat()
            f.write(dt,"Position of joint",j,":",read)

    return read

if __name__ == "__main__":
    #Instance the class
    robot_handler = pyAER.pyAER(visible=False)

    #Init configuration, although we called render_gui it won't render anything because
    #we passed the "visible" parameter as False to constructor
    robot_handler.render_gui()
    robot_handler.checked.set(True)
    robot_handler.checkUSB()
    motors = robot_handler.d["Motor Config"]

    #Initialize the robot in order to work with it
    robot_handler.search_Home_all()
    #This is the same as calling robot_handler.search_Home_J1-J6() sequentially 
    
    #Finish initialization calling ConfigureInit and ConfigureSPID
    robot_handler.ConfigureInit()
    robot_handler.ConfigureSPID()

    #Then move one of the robot's joints
    motors["ref_M1"].set(50)
    robot_handler.SendCommandJoint1_lite()
    log_position(1,robot_handler,"./log.txt")
    # motors["ref_M2"].set(50)
    # robot_handler.SendCommandJoint2_lite()
    # motors["ref_M3"].set(50)
    # robot_handler.SendCommandJoint3_lite()
    # motors["ref_M4"].set(50)
    # robot_handler.SendCommandJoint4_lite()
    #Access and change
    pass
            
    #print(robot_handler.d)

