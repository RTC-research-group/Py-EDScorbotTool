import pyAER
import datetime
import time
import logging

if __name__ == "__main__":
    
    #Open logging file
    #Filename is current datetime in format YYYY:MM:DD-HH:MM:SS
    f = datetime.datetime.now().isoformat(sep='-')[0:-7]
    logging.basicConfig(level=logging.INFO,filename=f,format="%(message)s")
    logging.info("Fecha: {}".format(f))
    
    #Repeat initial steps of demo.py:

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
    robot_handler.ConfigureInit()

    #Search Home, this may not be required
    robot_handler.search_Home_J1()
    
    robot_handler.search_Home_J2()
    
    robot_handler.search_Home_J3()
    
    robot_handler.search_Home_J4()
    
    #Assign Read_JX_pos to more accesible variables
    read_j1 = robot_handler.Read_J1_pos()
    read_j2 = robot_handler.Read_J2_pos()
    read_j3 = robot_handler.Read_J3_pos()
    read_j4 = robot_handler.Read_J4_pos()

    #Finish initialization calling ConfigureInit and ConfigureSPID
    robot_handler.ConfigureSPID()



    #Begin sweep of joints

    #Define number of steps we want to perform
    nsteps = 20
    
    #Obtain deltas for each joint based on their reference range
    d1 = (51158-11771)/nsteps
    d2 = (44353-18478)/nsteps
    d3 = (47591-17583)/nsteps
    d4 = (39797-25477)/nsteps

    #Establish initial references 
    initial_ref1 = 11771
    initial_ref2 = 18478
    initial_ref3 = 17583
    initial_ref4 = 25477



    for i in range(nsteps):

        ref1 = initial_ref1 + i*d1
        ref2 = initial_ref2 + i*d2
        ref3 = initial_ref3 + i*d3
        ref4 = initial_ref4 + i*d4
    
        motors["ref_M1"].set(ref1)
        robot_handler.SendCommandJoint1_lite()

        motors["ref_M2"].set(ref2)
        robot_handler.SendCommandJoint2_lite()

        motors["ref_M3"].set(ref3)
        robot_handler.SendCommandJoint3_lite()

        motors["ref_M4"].set(ref4)
        robot_handler.SendCommandJoint4_lite()
        time.sleep(0.15)
        logging.info("Iteracion {}".format(i+1))
        logging.info("Referencias: \tJ1:{},\t J2:{},\t J3:{},\t J4:{}".format(ref1,ref2,ref3,ref4))
        logging.info("Posiciones: \tJ1:{},\t J2:{},\t J3:{},\t J4:{}".format(read_j1(),read_j2(),read_j3(),read_j4()))

    logging.info("Finalizando sesion")
    #Hacer lo mismo pero al reves? for i in range nsteps: ref1=final_ref1 - i*d1...

   
