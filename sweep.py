from pyAER import pyEDScorbotTool
if __name__ == "__main__":
    
    config = pyEDScorbotTool(visible=False)
    config.render_gui()

    config.checked.set(True)
    # Then open the USB
    config.checkUSB()
    # We store the dictionary that contains the motors' variables
    # to access them easily
    motors = config.d["Motor Config"]

    #Initialize the robot in order to work with it
    config.ConfigureInit()

    # You may have to execute this part depending on whether 
    # home algorithm has been performed or not
    # #config.search_Home_J1()
    # time.sleep(2)
    # config.search_Home_J2()
    # time.sleep(2)
    # config.search_Home_J3()
    # time.sleep(2)
    # config.search_Home_J4()
    # time.sleep(2)
    
    
    #Finish initialization calling ConfigureSPID
    config.ConfigureSPID()

    #Then move the robot's joints
    '''
    Para hacer un barrido hace falta:
    1.- Saber los rangos de cada articulacion
    2.- Definir cuantos pasos se van a dar (bien por intervalo de tiempo bien por numero de pasos)
    3.- Comandar al robot a que se mueva desde su referencia inicial hasta la final con incrementos que dependen del numero de pasos
    
    ranges = [a,b,c,d] <- asi sería si los rangos fuera de [0,a], [0,b], etc.add()
    nsteps = ... <- establecer a mano o calcular con el intervalo de tiempo

    #Calcular deltas(incrementos)
    da = a/nsteps
    db = b/nsteps
    dc = c/nsteps
    dd = d/nsteps

    r1 = 0
    r2 = 0
    r3 = 0
    r4 = 0

    for step in range(nsteps): 
        r1 += da
        r2 += db
        r3 += dc
        r4 += dd

        motors["ref_M1"].set(r1)
        motors["ref_M2"].set(r2)
        motors["ref_M3"].set(r3)
        motors["ref_M4"].set(r4)

        config.SendCommandJoint1_lite()
        config.SendCommandJoint2_lite()
        config.SendCommandJoint3_lite()
        config.SendCommandJoint4_lite()

        log_position()
        time.sleep(x)

    
    '''
    
    

    motors["ref_M1"].set(50)
    config.SendCommandJoint1_lite()
    

    pass