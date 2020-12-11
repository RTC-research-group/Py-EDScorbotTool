from datetime import time
from os import read
import tkinter as tk
from tkinter import ttk,messagebox
import usb.core
import usb.util
import usb.backend.libusb1
import json
from tkinter import filedialog
import datetime
import time
import logging

class pyAER:
    '''
    pyAER software, replacement of jAER

    This class is used for establishing a communication with ED-Scorbot 
    Robot in order to be able to control it via neuromorphic control, also called SPID
    '''
    def __init__(self):
        '''
        Constructor

        Initializes GUI by creating the root Tk object, sets icon of the app,
        initializes data structures to hold the value of all variables that 
        are displayed, creating a dictionary (self.d) to access their values
        and sets constants and handles needed for USB connection
        '''
        #Initialize GUI: create root Tk object
        self.root = tk.Tk()

        #Set the icon
        self.root.iconphoto(False,tk.PhotoImage(file="./atc.png"))

        #Create dictionaries where the interface data will be stored
        self.d = {}
        self.d["Motor Config"] = {}
        self.d["Joints"] = {}
        self.d["Scan Parameters"] = {}
        
        #Standalone variable to control if USB is enabled
        self.checked = False

        #Set USB constants needed
        self.VID = 0x10c4
        self.PID = 0x0000
        self.ENDPOINT_OUT = 0x02
        self.ENDPOINT_IN = 0x81
        self.PACKET_LENGTH = 64

        #Handle for USB connection
        self.dev = None


        return
  
    def millis_now(self):
        '''
        This function returns the time at the moment of the call in milliseconds
        
        '''
        return (time.time()*1000) #time.time() returns seconds, so mult. by 1000 to get ms

    def alert(self,text):
        '''
        This function creates a messagebox with the text parameter as data

        Useful to alert the user that something has gone wrong
        To indicate successful procedures, please just print to console using print()

        Args:
            text (str): Text to be displayed in the box

        '''
        messagebox.showinfo(message=text)

    def render_motor(self, motor_number, row, col):
        '''
        Create the inputs for 1 motor

        Each variable created is stored in the "Motor Config" dictionary 
        and can be accessed directly using the name that appears on the graphical interface 

        Args:
            motor_number (int): Number of the motor to be rendered
            row (int): Row of the grid in which the inputs will be displayed
            col (int): Column of the grid in which the inputs will be displayed
        
        Returns:
            Labelframe in which the inputs are rendered

        '''
        labels = ["EI_FD_bank3_18bits", "PD_FD_bank3_22bits",
                  "PI_FD_bank3_18bits", "leds", "ref", "spike_expansor"]
        labelframe = ttk.LabelFrame(
            self.root, text="Motor " + str(motor_number))
        labelframe.grid(
            column=col, row=row, sticky=(tk.N, tk.W), padx=5, pady=5)
        EI_FD_bank3_18bits = tk.IntVar()
        PF_FD_bank3_22bits = tk.IntVar()
        PI_FD_bank3_18bits = tk.IntVar()
        leds = tk.IntVar()
        ref = tk.IntVar()
        spike_expansor = tk.IntVar()
        variables = [EI_FD_bank3_18bits, PF_FD_bank3_22bits,
                     PI_FD_bank3_18bits, leds, ref, spike_expansor, labelframe]

        for var, row_, label in zip(variables, range(1, len(variables)), labels):
            ttk.Entry(labelframe, width=7, textvariable=var).grid(
                column=2, row=row_, sticky=(tk.W))
            labeltext = label + "_M" + str(motor_number)
            ttk.Label(labelframe, text=labeltext).grid(
                column=1, row=row_, sticky=(tk.W))
            self.d["Motor Config"][labeltext] = var

            # ttk.Scale(labelframe,from_=0,to=65535,orient=tk.HORIZONTAL,variable=var).grid(column=3,row=row,sticky=(tk.W))

        return labelframe

    def render_joints(self, row, col):
        '''
        Create joints text entries
        
        These entries are read-only, as they will contain the joints measures read from the encoders
        
        Each variable created is stored in the "Joints" dictionary 
        and can be accessed directly using the name that appears on the graphical interface

        Args:
            row (int): Row of the grid in which the inputs will be displayed
            col (int): Column of the grid in which the inputs will be displayed

        Returns:
            LabelFrame in which the entries are rendered
        '''

        labelframe = ttk.LabelFrame(self.root, text="Joint Sensors")
        labelframe.grid(column=col, row=row, sticky=(
            tk.N, tk.W), padx=5, pady=5)
        j1 = tk.IntVar()
        j2 = tk.IntVar()
        j3 = tk.IntVar()
        j4 = tk.IntVar()
        j5 = tk.IntVar()
        j6 = tk.IntVar()

        variables = [j1, j2, j3, j4, j5, j6]
        i = 1
        for var, row_ in zip(variables, range(1, len(variables)+1)):
            text = ttk.Entry(labelframe, width=7, textvariable=var)
            text.grid(column=2, row=row_, sticky=tk.W)
            text.config(state="readonly")
            labeltext = "J" + str(i) + "_sensor_value"
            ttk.Label(labelframe, text=labeltext).grid(
                column=1, row=row_, sticky=tk.W)
            i += 1
            self.d["Joints"][labeltext] = var

        return labelframe

    def render_scan_parameters(self, row, col):
        '''
        Create the Scan Parameters inputs

        Each variable created is stored in the "Scan Parameters" dictionary 
        and can be accessed directly using the name that appears on the graphical interface

        Args:
            row (int): Row of the grid in which the inputs will be displayed
            col (int): Column of the grid in which the inputs will be displayed

        Returns:
            Labelframe in which the inputs are rendered
        '''
        labels = ["Final_Value", "Init_Value", "Step_Value", "Wait_Time"]
        labelframe = ttk.LabelFrame(self.root, text="Scan Parameters")
        labelframe.grid(column=col, row=row, sticky=(
            tk.N, tk.W), padx=5, pady=5)
        final_value = tk.IntVar()
        init_value = tk.IntVar()
        step_value = tk.IntVar()
        wait_time = tk.IntVar()

        variables = [final_value, init_value, step_value, wait_time]
        for var, row_, label in zip(variables, range(1, len(variables)+1), labels):
            ttk.Entry(labelframe, width=7, textvariable=var).grid(
                column=2, row=row_, sticky=tk.W)
            labeltext = "scan_" + label
            ttk.Label(labelframe, text=labeltext).grid(
                column=1, row=row_, sticky=tk.W)
            self.d["Scan Parameters"][labeltext] = var

        return labelframe

    def render_buttons(self, row, col):
        '''
        Create the buttons that will be bounded to  all different usable actions
        
        Args:
            row (int): Row of the grid in which the buttons will be displayed
            col (int): Column of the grid in which the buttons will be displayed
        '''
        labels = ["ConfigureInit", "ConfigureLeds", "ConfigureSPID", "Draw8xy", "Example", "ScanAllMotor", "ScanMotor1", "ScanMotor2", "ScanMotor3", "ScanMotor4",
                  "ScanMotor5", "ScanMotor6", "Search_Home", "Send_Home", "SendFPGAReset", "SetAERIN_ref", "SetUSBSPI_ref", "SwitchOffLEDS"]
        labelframe = ttk.LabelFrame(self.root, text="Actions")
        labelframe.grid(column=col, row=row, sticky=(
            tk.N, tk.W), padx=5, pady=5)
        
        ttk.Button(labelframe,text="ConfigureInit",command=self.ConfigureInit).grid(column=1,row=1,sticky=(tk.W,tk.E))
        ttk.Button(labelframe,text="ConfigureLeds",command=self.ConfigureLeds).grid(column=2,row=1,sticky=(tk.W,tk.E))
        ttk.Button(labelframe,text="ConfigureSPID",command=self.ConfigureSPID).grid(column=3,row=1,sticky=(tk.W,tk.E))
        ttk.Button(labelframe,text="Draw8xy",command=self.Draw8xy).grid(column=1,row=2,sticky=(tk.W,tk.E))
        ttk.Button(labelframe,text="Example",command=lambda x: "").grid(column=2,row=2,sticky=(tk.W,tk.E))
        ttk.Button(labelframe,text="ScanAllMotor",command=self.ScanAllMotor).grid(column=3,row=2,sticky=(tk.W,tk.E))
        ttk.Button(labelframe,text="ScanMotor1",command=self.scanMotor1).grid(column=1,row=3,sticky=(tk.W,tk.E))
        ttk.Button(labelframe,text="ScanMotor2",command=self.scanMotor2).grid(column=2,row=3,sticky=(tk.W,tk.E))
        ttk.Button(labelframe,text="ScanMotor3",command=self.scanMotor3).grid(column=3,row=3,sticky=(tk.W,tk.E))
        ttk.Button(labelframe,text="ScanMotor4",command=self.scanMotor4).grid(column=1,row=4,sticky=(tk.W,tk.E))
        ttk.Button(labelframe,text="ScanMotor5",command=self.scanMotor5).grid(column=2,row=4,sticky=(tk.W,tk.E))
        ttk.Button(labelframe,text="ScanMotor6",command=self.scanMotor6).grid(column=3,row=4,sticky=(tk.W,tk.E))
        ttk.Button(labelframe,text="Search_Home",command=self.search_Home_all).grid(column=1,row=5,sticky=(tk.W,tk.E))
        ttk.Button(labelframe,text="Send_Home",command=self.send_Home_all).grid(column=2,row=5,sticky=(tk.W,tk.E))
        ttk.Button(labelframe,text="SendFPGAReset",command=self.SendFPGAReset).grid(column=3,row=5,sticky=(tk.W,tk.E))
        ttk.Button(labelframe,text="SetAERIN_ref",command=self.SetAERIN_ref).grid(column=1,row=6,sticky=(tk.W,tk.E))
        ttk.Button(labelframe,text="SetUSBSPI_ref",command=self.SetUSBSPI_ref).grid(column=2,row=6,sticky=(tk.W,tk.E))
        ttk.Button(labelframe,text="SwitchOffLEDS",command=self.SwitchOffLEDS).grid(column=3,row=6,sticky=(tk.W,tk.E))
        ttk.Button(labelframe,text="DumpConfig",command=self.dumpConfig).grid(column=1,row=7,sticky=(tk.W,tk.E))
        ttk.Button(labelframe,text="LoadConfig",command=self.loadConfig).grid(column=2,row=7,sticky=(tk.W,tk.E))
        ttk.Button(labelframe,text="ResetUSB",command=self.resetUSB).grid(column=3,row=7,sticky=(tk.W,tk.E))
        ttk.Button(labelframe,text="Send J1 Home",command=self.send_Home_J1).grid(column=1,row=8,sticky=(tk.W,tk.E))
        ttk.Button(labelframe,text="Send J2 Home",command=self.send_Home_J2).grid(column=2,row=8,sticky=(tk.W,tk.E))
        ttk.Button(labelframe,text="Send J3 Home",command=self.send_Home_J3).grid(column=3,row=8,sticky=(tk.W,tk.E))
        ttk.Button(labelframe,text="Send J4 Home",command=self.send_Home_J4).grid(column=1,row=9,sticky=(tk.W,tk.E))
        ttk.Button(labelframe,text="Send J5 Home",command=self.send_Home_J5).grid(column=2,row=9,sticky=(tk.W,tk.E))
        ttk.Button(labelframe,text="Send J6 Home",command=self.send_Home_J6).grid(column=3,row=9,sticky=(tk.W,tk.E))
        ttk.Button(labelframe,text="Search J1 Home",command=self.search_Home_J1).grid(column=1,row=10,sticky=(tk.W,tk.E))
        ttk.Button(labelframe,text="Search J2 Home",command=self.search_Home_J2).grid(column=2,row=10,sticky=(tk.W,tk.E))
        ttk.Button(labelframe,text="Search J3 Home",command=self.search_Home_J3).grid(column=3,row=10,sticky=(tk.W,tk.E))
        ttk.Button(labelframe,text="Search J4 Home",command=self.search_Home_J4).grid(column=1,row=11,sticky=(tk.W,tk.E))
        ttk.Button(labelframe,text="Search J5 Home",command=self.search_Home_J5).grid(column=2,row=11,sticky=(tk.W,tk.E))
        ttk.Button(labelframe,text="Search J6 Home",command=self.search_Home_J6).grid(column=3,row=11,sticky=(tk.W,tk.E))

    def render_usbEnable(self,row,col):
        '''
        Create the checkbox that enables opening USB devices

        The value of the box is stored in the checked
        variable available in the class (self.checked)

        Args:
            row (int): Row of the grid in which the checkbox will be displayed
            col (int): Column of the grid in which the checkbox will be displayed
        '''
        labelframe = ttk.LabelFrame(self.root, text="USB")
        labelframe.grid(column=col, row=row, sticky=(
            tk.N, tk.W), padx=5, pady=5)

        checked = tk.BooleanVar()


        ttk.Checkbutton(labelframe,text="Open device",command=self.checkUSB,variable=checked,onvalue=True,offvalue=False).grid(column=1,row=3,sticky=(tk.W))
        self.checked = checked
   
    def openUSB(self):
        '''
        Try to open USB connection with robot infrastructure

        This function tries to open a connection with
        the AERNode USB board and claim its interface 
        to initiate communication and returns the connection
        to the device found

        Returns:
            Device handler if connection was successful
            None if the connection couldn't be established
        '''

        try:
            dev = usb.core.find(idVendor=self.VID,idProduct=self.PID)
        except usb.core.NoBackendError:
            
            be = usb.backend.libusb1.get_backend(find_library = lambda x:"/lib/x86_64-linux-gnu/libusb-1.0.so.0")
            dev = usb.core.find(idVendor=self.VID,idProduct=self.PID,backend=be)
        finally:
            #If the device can't be found, tell the user and end execution
            if dev is None:
                self.alert("Device not found, try again or check the connection")
                self.checked.set(False)
                return None
                
            #If the device was found, set configuration to default, claim the 
            #default interface and attach the handler to dev
            else:
                
                dev.set_configuration()
                usb.util.claim_interface(dev,0)
                
                print("Device found and initialized successfully")

                return dev

    def closeUSB(self):
        '''
        Close USB connection

        This function releases the interface claimed
        and then detaches the handle to the device
        '''
        if(self.dev != None):
            usb.util.release_interface(self.dev,0)
            usb.util.dispose_resources(self.dev)
            self.dev = None

        print("Device disconnected successfully")
     
    def checkUSB(self):
        '''
        Check wether USB usage has been enabled or not

        This function reads the checked self variable to determine 
        whether USB connection has been enabled or not

        If it has, then tries to connect to AERNode board and sets
        self.dev to the device handler
        
        If it hasn't, it disconnects from the device
        '''
        #Check if USB is enabled
        if self.checked.get() == False:
            #If not, close the connection
            self.closeUSB()
        
        else:
            
            #If USB is enabled, try to connect to AERNode board
            self.dev = self.openUSB()
            
    def dumpConfig(self):
        '''
        Dump current configuration

        This function dumps current config (the one being
        displayed in the GUI) to a JSON file named "config.json"

        Generated config file is also printed in console
        '''

        # Create temporary dicts which will hold the values of each text entry
        # This is necessary because these entries can be modified using the 
        # set() method of the variables linked to them, but these variables
        # are not serializable directly because they are tkinter var objects,
        # so we need just their value to be able to serialize them properly
        d = {}
        d["Motor Config"] = {}
        d["Joints"] = {}
        d["Scan Parameters"] = {}

        for key in self.d["Motor Config"].keys():
            d["Motor Config"][key] =  self.d["Motor Config"][key].get()
        
        for key in self.d["Scan Parameters"].keys():
            d["Scan Parameters"][key] = self.d["Scan Parameters"][key].get()

        #Once we've collected all variables, dump dictionary d as json to config.json
        with open('config.json','w') as f:
            json.dump(d,f,indent=2)
            #And print generated config in the console
            jsondict = json.dumps(d,indent=2)
            print("Settings generated: \n"+jsondict)
                
    def loadConfig(self):
        '''
        Load configuration in an extern .json file

        This function allows users to load a json file containing
        a valid configuration file, just as the ones generated with 
        the dumpConfig function
        '''
        
        #Open file dialog to select config file
        filename = filedialog.askopenfile(mode="r")
        #Read file contents and parse as JSON
        obj = filename.read()
        j = json.loads(obj)

        #Then try to fit said JSON in the app variables
        try:
            for key in self.d["Motor Config"].keys():
                self.d["Motor Config"][key].set(j["Motor Config"][key])
            
            for key in self.d["Scan Parameters"].keys():
                self.d["Scan Parameters"][key].set(j["Scan Parameters"][key])
            
            return
        #If we catch a KeyError, the config is invalid, so alert the user and end execution
        except KeyError:
            self.alert("Invalid config file")
            return
  
    def render_gui(self,visible=True):
        '''
        Top level GUI routine 

        This function serves as a top routine for rendering all 
        GUI widgets. It calls each function that renders a component,
        and assigns them a place in the top window.

        Layout changes may be made here: just change the column and row
        of the component to render in its call to adjust it to your own needs
        '''

        #Set window title
        self.root.title("ATCEDScorbotConfig")
        
        #Set list of rendered frames
        self.frame_list = []
        i = 1
        #Render motors in a 2x3 (rowXcolumns) fashion
        for row in range(1, 3):
            for col in range(1, 4):
                frame = self.render_motor(i, row, col)

                i += 1
                self.frame_list.append(frame)
        #Render the rest of the components
        self.frame_list.append(self.render_joints(3, 1))
        self.frame_list.append(self.render_scan_parameters(3, 2))
        self.render_buttons(3, 3)
        self.render_usbEnable(4,1)

        self.init_config()
        if visible:
        #And call mainloop to display GUI
            self.root.mainloop()

    def ConfigureInit(self):
        
        '''
        Set current position as initial

        This function sets the current position of each joint
        as the initial position. This means that, after this
        function is called, the current position will match
        the position with a reference of 0
        '''

        if (((self.dev and self.checked.get()) == None) or (self.checked.get() == False)):
            self.alert("No device opened. Try checking USB option first")
            return
        else:
            
            if self.checked.get():
                for i in range(0,6):
                    #Motor 1
                    self.sendCommand16(0x00,0x00,0x03,True) #Leds M1
                    self.sendCommand16(0x02,0x00,0x00,True) #Ref M1 0
                    self.sendCommand16(0x03,0x00,0x0f,True) #I banks disabled M1
                    self.sendCommand16(0x04,((512>>8) & 0xFF),512 & 0xFF,True) #FD I&G bank 0 M1
                    self.sendCommand16(0x05,((512>>8) & 0xFF),512 & 0xFF,True) #FD I&G bank 1 M1
                    self.sendCommand16(0x06,((512>>8) & 0xFF),512 & 0xFF,True) #FD I&G bank 2 M1
                    self.sendCommand16(0x07,((self.d["Motor Config"]["PI_FD_bank3_18bits_M1"].get()>>8) & 0xFF),self.d["Motor Config"]["PI_FD_bank3_18bits_M1"].get() & 0xFF,True) #FD I&G bank 3 M1
                    self.sendCommand16(0x08,(0x00),(0x0f), True) #d banks disabled M1
                    self.sendCommand16(0x09, ((512 >> 8) & 0xFF),((512) & 0xFF), True) #FD I&G bank 0 M1
                    self.sendCommand16(0x0A, ((512 >> 8) & 0xFF), ((512) & 0xFF), True) #FD I&G bank 1 M1
                    self.sendCommand16(0x0B, ((512 >> 8) & 0xFF),  ((512) & 0xFF), True) #FD I&G bank 2 M1
                    self.sendCommand16(0x0C, ((self.d["Motor Config"]["PD_FD_bank3_22bits_M1"].get() >> 8) & 0xFF),  ((512) & 0xFF), True) #FD I&G bank 3 M1
                    self.sendCommand16(0x12, (0x00),  (0x0), True); #spike expansor M1
                    self.sendCommand16(0x13, (0x00),  (0x0f), True); #d banks disabled M1
                    self.sendCommand16(0x14, ((512 >> 8) & 0xFF),  ((512) & 0xFF), True); #FD I&G bank 0 M1
                    self.sendCommand16(0x15, ((512 >> 8) & 0xFF),  ((512) & 0xFF), True); #FD I&G bank 1 M1
                    self.sendCommand16(0x16, ((512 >> 8) & 0xFF),  ((512) & 0xFF), True); #FD I&G bank 2 M1
                    self.sendCommand16(0x17, ((self.d["Motor Config"]["EI_FD_bank3_18bits_M1"].get() >> 8) & 0xFF),  ((self.d["Motor Config"]["EI_FD_bank3_18bits_M1"].get()) & 0xFF), True); #FD I&G bank 3 M1
                    self.sendCommand16(0x00, 0x00,  0x00, False); #LEDs M1 off

                    print("PI_FD_bank0_12bits_M1={} \t PI_FD_bank1_14bits_M1={} \t PI_FD_bank2_16bits_M1={} \t PI_FD_bank3_18bits_M1={}\n"
                          .format(512,512,512,self.d["Motor Config"]["PI_FD_bank3_18bits_M1"].get()) +
                          "PD_FD_bank0_16bits_M1={} \t PD_FD_bank1_18bits_M1={} \t PD_FD_bank2_20bits_M1={} \t PD_FD_bank3_22bits_M1={}\n"
                          .format(512,512,512,512) +
                          "EI_FD_bank0_12bits_M1={} \t EI_FD_bank1_14bits_M1={} \t EI_FD_bank2_16bits_M1={} \t EI_FD_bank3_18bits_M1={}\n"
                          .format(512,512,512,self.d["Motor Config"]["EI_FD_bank3_18bits_M1"].get()))
                    
                    #Motor 2
                    self.sendCommand16( 0x20,  (0x00), (0x03), True); #LEDs M2
                    self.sendCommand16( 0x22,  (0x00),  (0x00), True); #Ref M2 0
                    self.sendCommand16( 0x23,  (0x00),  (0x0f), True); #I banks disabled M2
                    self.sendCommand16( 0x24,  ((512 >> 8) & 0xFF),  ((512) & 0xFF), True); #FD I&G bank 0 M2
                    self.sendCommand16( 0x25,  ((512 >> 8) & 0xFF),  ((512) & 0xFF), True); #FD I&G bank 1 M2
                    self.sendCommand16( 0x26,  ((512 >> 8) & 0xFF),  ((512) & 0xFF), True); #FD I&G bank 2 M2
                    self.sendCommand16( 0x27,  ((self.d["Motor Config"]["PI_FD_bank3_18bits_M2"].get() >> 8) & 0xFF),  ((self.d["Motor Config"]["PI_FD_bank3_18bits_M2"].get()) & 0xFF), True); #FD I&G bank 3 M2
                    self.sendCommand16( 0x28,  (0x00),  (0x0f), True); #I banks disabled M2
                    self.sendCommand16( 0x29,  ((512 >> 8) & 0xFF),  ((512) & 0xFF), True); #FD I&G bank 0 M2
                    self.sendCommand16( 0x2A,  ((512 >> 8) & 0xFF),  ((512) & 0xFF), True); #FD I&G bank 1 M2
                    self.sendCommand16( 0x2B,  ((512 >> 8) & 0xFF),  ((512) & 0xFF), True); #FD I&G bank 2 M2
                    self.sendCommand16( 0x2C,  ((self.d["Motor Config"]["PD_FD_bank3_22bits_M2"].get() >> 8) & 0xFF),  ((self.d["Motor Config"]["PD_FD_bank3_22bits_M2"].get()) & 0xFF), True); #FD I&G bank 3 M2
                    self.sendCommand16( 0x32,  (0x00),  (0x0), True); #spike expansor M2
                    self.sendCommand16( 0x33,  (0x00),  (0x0f), True); #d banks disabled M1
                    self.sendCommand16( 0x34,  ((512 >> 8) & 0xFF),  ((512) & 0xFF), True); #FD I&G bank 0 M1
                    self.sendCommand16( 0x35,  ((512 >> 8) & 0xFF),  ((512) & 0xFF), True); #FD I&G bank 1 M1
                    self.sendCommand16( 0x36,  ((512 >> 8) & 0xFF),  ((512) & 0xFF), True); #FD I&G bank 2 M1
                    self.sendCommand16( 0x37,  ((self.d["Motor Config"]["EI_FD_bank3_18bits_M2"].get() >> 8) & 0xFF),  ((self.d["Motor Config"]["EI_FD_bank3_18bits_M2"].get()) & 0xFF), True); #FD I&G bank 3 M1
                    self.sendCommand16( 0x20,  0,  0, False); #LEDs M2 off
                    print("PI_FD_bank0_12bits_M2={} \t PI_FD_bank1_14bits_M2={} \t PI_FD_bank2_16bits_M2={} \t PI_FD_bank3_18bits_M2={}\n"
                          .format(512,512,512,self.d["Motor Config"]["PI_FD_bank3_18bits_M2"].get()) +
                          "PD_FD_bank0_16bits_M2={} \t PD_FD_bank1_18bits_M2={} \t PD_FD_bank2_20bits_M2={} \t PD_FD_bank3_22bits_M2={}\n"
                          .format(512,512,512,512) +
                          "EI_FD_bank0_12bits_M2={} \t EI_FD_bank1_14bits_M2={} \t EI_FD_bank2_16bits_M2={} \t EI_FD_bank3_18bits_M2={}\n"
                          .format(512,512,512,self.d["Motor Config"]["EI_FD_bank3_18bits_M2"].get()))
                    #Motor 3

                    self.sendCommand16( 0x40,  (0x00), (0x03), True); #LEDs M3
                    self.sendCommand16( 0x42,  (0x00),  (0x00), True); #Ref M3 0
                    self.sendCommand16( 0x43,  (0x00),  (0x0f), True); #I banks disabled M3
                    self.sendCommand16( 0x44,  ((512 >> 8) & 0xFF),  ((512) & 0xFF), True); #FD I&G bank 0 M3
                    self.sendCommand16( 0x45,  ((512 >> 8) & 0xFF),  ((512) & 0xFF), True); #FD I&G bank 1 M3
                    self.sendCommand16( 0x46,  ((512 >> 8) & 0xFF),  ((512) & 0xFF), True); #FD I&G bank 2 M3
                    self.sendCommand16( 0x47,  ((self.d["Motor Config"]["PI_FD_bank3_18bits_M3"].get() >> 8) & 0xFF),  ((self.d["Motor Config"]["PI_FD_bank3_18bits_M3"].get()) & 0xFF), True); #FD I&G bank 3 M3
                    self.sendCommand16( 0x48,  (0x00),  (0x0f), True); #I banks disabled M3
                    self.sendCommand16( 0x49,  ((512 >> 8) & 0xFF),  ((512) & 0xFF), True); #FD I&G bank 0 M3
                    self.sendCommand16( 0x4A,  ((512 >> 8) & 0xFF),  ((512) & 0xFF), True); #FD I&G bank 1 M3
                    self.sendCommand16( 0x4B,  ((512 >> 8) & 0xFF),  ((512) & 0xFF), True); #FD I&G bank 2 M3
                    self.sendCommand16( 0x4C,  ((self.d["Motor Config"]["PD_FD_bank3_22bits_M3"].get() >> 8) & 0xFF),  ((self.d["Motor Config"]["PD_FD_bank3_22bits_M3"].get()) & 0xFF), True); #FD I&G bank 3 M3
                    self.sendCommand16( 0x52,  (0x00),  (0x0), True); #spike expansor M3
                    self.sendCommand16( 0x53,  (0x00),  (0x0f), True); #d banks disabled M1
                    self.sendCommand16( 0x54,  ((512 >> 8) & 0xFF),  ((512) & 0xFF), True); #FD I&G bank 0 M1
                    self.sendCommand16( 0x55,  ((512 >> 8) & 0xFF),  ((512) & 0xFF), True); #FD I&G bank 1 M1
                    self.sendCommand16( 0x56,  ((512 >> 8) & 0xFF),  ((512) & 0xFF), True); #FD I&G bank 2 M1
                    self.sendCommand16( 0x57,  ((self.d["Motor Config"]["EI_FD_bank3_18bits_M3"].get() >> 8) & 0xFF),  ((self.d["Motor Config"]["EI_FD_bank3_18bits_M3"].get()) & 0xFF), True); #FD I&G bank 3 M1
                    self.sendCommand16( 0x40,  0,  0, False); #LEDs M3 off
                    print("PI_FD_bank0_12bits_M3={} \t PI_FD_bank1_14bits_M3={} \t PI_FD_bank2_16bits_M3={} \t PI_FD_bank3_18bits_M3={}\n"
                          .format(512,512,512,self.d["Motor Config"]["PI_FD_bank3_18bits_M3"].get()) +
                          "PD_FD_bank0_16bits_M3={} \t PD_FD_bank1_18bits_M3={} \t PD_FD_bank2_20bits_M3={} \t PD_FD_bank3_22bits_M3={}\n"
                          .format(512,512,512,512) +
                          "EI_FD_bank0_12bits_M3={} \t EI_FD_bank1_14bits_M3={} \t EI_FD_bank2_16bits_M3={} \t EI_FD_bank3_18bits_M3={}\n"
                          .format(512,512,512,self.d["Motor Config"]["EI_FD_bank3_18bits_M3"].get()))
                    
                    #Motor 4

                    self.sendCommand16( 0x60,  (0x00), (0x03), True); #LEDs M4
                    self.sendCommand16( 0x62,  (0x00),  (0x00), True); #Ref M4 0
                    self.sendCommand16( 0x63,  (0x00),  (0x0f), True); #I banks disabled M4
                    self.sendCommand16( 0x64,  ((512 >> 8) & 0xFF),  ((512) & 0xFF), True); #FD I&G bank 0 M4
                    self.sendCommand16( 0x65,  ((512 >> 8) & 0xFF),  ((512) & 0xFF), True); #FD I&G bank 1 M4
                    self.sendCommand16( 0x66,  ((512 >> 8) & 0xFF),  ((512) & 0xFF), True); #FD I&G bank 2 M4
                    self.sendCommand16( 0x67,  ((self.d["Motor Config"]["PI_FD_bank3_18bits_M4"].get() >> 8) & 0xFF),  ((self.d["Motor Config"]["PI_FD_bank3_18bits_M4"].get()) & 0xFF), True); #FD I&G bank 3 M4
                    self.sendCommand16( 0x68,  (0x00),  (0x0f), True); #I banks disabled M4
                    self.sendCommand16( 0x69,  ((512 >> 8) & 0xFF),  ((512) & 0xFF), True); #FD I&G bank 0 M4
                    self.sendCommand16( 0x6A,  ((512 >> 8) & 0xFF),  ((512) & 0xFF), True); #FD I&G bank 1 M4
                    self.sendCommand16( 0x6B,  ((512 >> 8) & 0xFF),  ((512) & 0xFF), True); #FD I&G bank 2 M4
                    self.sendCommand16( 0x6C,  ((self.d["Motor Config"]["PD_FD_bank3_22bits_M4"].get() >> 8) & 0xFF),  ((self.d["Motor Config"]["PD_FD_bank3_22bits_M4"].get()) & 0xFF), True); #FD I&G bank 3 M4
                    self.sendCommand16( 0x72,  (0x00),  (0x0), True); #spike expansor M4
                    self.sendCommand16( 0x73,  (0x00),  (0x0f), True); #d banks disabled M1
                    self.sendCommand16( 0x74,  ((512 >> 8) & 0xFF),  ((512) & 0xFF), True); #FD I&G bank 0 M1
                    self.sendCommand16( 0x75,  ((512 >> 8) & 0xFF),  ((512) & 0xFF), True); #FD I&G bank 1 M1
                    self.sendCommand16( 0x76,  ((512 >> 8) & 0xFF),  ((512) & 0xFF), True); #FD I&G bank 2 M1
                    self.sendCommand16( 0x77,  ((self.d["Motor Config"]["EI_FD_bank3_18bits_M4"].get() >> 8) & 0xFF),  ((self.d["Motor Config"]["EI_FD_bank3_18bits_M4"].get()) & 0xFF), True); #FD I&G bank 3 M1
                    self.sendCommand16( 0x60,  0,  0, False); #LEDs M4 off
                    print("PI_FD_bank0_12bits_M4={} \t PI_FD_bank1_14bits_M4={} \t PI_FD_bank2_16bits_M4={} \t PI_FD_bank3_18bits_M4={}\n"
                          .format(512,512,512,self.d["Motor Config"]["PI_FD_bank3_18bits_M4"].get()) +
                          "PD_FD_bank0_16bits_M4={} \t PD_FD_bank1_18bits_M4={} \t PD_FD_bank2_20bits_M4={} \t PD_FD_bank3_22bits_M4={}\n"
                          .format(512,512,512,512) +
                          "EI_FD_bank0_12bits_M4={} \t EI_FD_bank1_14bits_M4={} \t EI_FD_bank2_16bits_M4={} \t EI_FD_bank3_18bits_M4={}\n"
                          .format(512,512,512,self.d["Motor Config"]["EI_FD_bank3_18bits_M4"].get()))

                    #Motor 5

                    self.sendCommand16( 0x80,  (0x00), (0x03), True); #LEDs M5
                    self.sendCommand16( 0x82,  (0x00),  (0x00), True); #Ref M5 0
                    self.sendCommand16( 0x83,  (0x00),  (0x0f), True); #I banks disabled M5
                    self.sendCommand16( 0x84,  ((512 >> 8) & 0xFF),  ((512) & 0xFF), True); #FD I&G bank 0 M5
                    self.sendCommand16( 0x85,  ((512 >> 8) & 0xFF),  ((512) & 0xFF), True); #FD I&G bank 1 M5
                    self.sendCommand16( 0x86,  ((512 >> 8) & 0xFF),  ((512) & 0xFF), True); #FD I&G bank 2 M5
                    self.sendCommand16( 0x87,  ((self.d["Motor Config"]["PI_FD_bank3_18bits_M5"].get() >> 8) & 0xFF),  ((self.d["Motor Config"]["PI_FD_bank3_18bits_M5"].get()) & 0xFF), True); #FD I&G bank 3 M5
                    self.sendCommand16( 0x88,  (0x00),  (0x0f), True); #I banks disabled M5
                    self.sendCommand16( 0x89,  ((512 >> 8) & 0xFF),  ((512) & 0xFF), True); #FD I&G bank 0 M5
                    self.sendCommand16( 0x8A,  ((512 >> 8) & 0xFF),  ((512) & 0xFF), True); #FD I&G bank 1 M5
                    self.sendCommand16( 0x8B,  ((512 >> 8) & 0xFF),  ((512) & 0xFF), True); #FD I&G bank 2 M5
                    self.sendCommand16( 0x8C,  ((self.d["Motor Config"]["PD_FD_bank3_22bits_M5"].get() >> 8) & 0xFF),  ((self.d["Motor Config"]["PD_FD_bank3_22bits_M5"].get()) & 0xFF), True); #FD I&G bank 3 M5
                    self.sendCommand16( 0x92,  (0x00),  (0x0), True); #spike expansor M5
                    self.sendCommand16( 0x93,  (0x00),  (0x0f), True); #d banks disabled M1
                    self.sendCommand16( 0x94,  ((512 >> 8) & 0xFF),  ((512) & 0xFF), True); #FD I&G bank 0 M1
                    self.sendCommand16( 0x95,  ((512 >> 8) & 0xFF),  ((512) & 0xFF), True); #FD I&G bank 1 M1
                    self.sendCommand16( 0x96,  ((512 >> 8) & 0xFF),  ((512) & 0xFF), True); #FD I&G bank 2 M1
                    self.sendCommand16( 0x97,  ((self.d["Motor Config"]["EI_FD_bank3_18bits_M5"].get() >> 8) & 0xFF),  ((self.d["Motor Config"]["EI_FD_bank3_18bits_M5"].get()) & 0xFF), True); #FD I&G bank 3 M1
                    self.sendCommand16( 0x80,  0,  0, False); #LEDs M5 off
                    print("PI_FD_bank0_12bits_M5={} \t PI_FD_bank1_14bits_M5={} \t PI_FD_bank2_16bits_M5={} \t PI_FD_bank3_18bits_M5={}\n"
                          .format(512,512,512,self.d["Motor Config"]["PI_FD_bank3_18bits_M5"].get()) +
                          "PD_FD_bank0_16bits_M5={} \t PD_FD_bank1_18bits_M5={} \t PD_FD_bank2_20bits_M5={} \t PD_FD_bank3_22bits_M5={}\n"
                          .format(512,512,512,512) +
                          "EI_FD_bank0_12bits_M5={} \t EI_FD_bank1_14bits_M5={} \t EI_FD_bank2_16bits_M5={} \t EI_FD_bank3_18bits_M5={}\n"
                          .format(512,512,512,self.d["Motor Config"]["EI_FD_bank3_18bits_M5"].get()))

                    #Motor 6

                    self.sendCommand16( 0xA0,  (0x00), (0x03), True); #LEDs M6
                    self.sendCommand16( 0xA2,  (0x00),  (0x00), True); #Ref M6 0
                    self.sendCommand16( 0xA3,  (0x00),  (0x0f), True); #I banks disabled M6
                    self.sendCommand16( 0xA4,  ((512 >> 8) & 0xFF),  ((512) & 0xFF), True); #FD I&G bank 0 M6
                    self.sendCommand16( 0xA5,  ((512 >> 8) & 0xFF),  ((512) & 0xFF), True); #FD I&G bank 1 M6
                    self.sendCommand16( 0xA6,  ((512 >> 8) & 0xFF),  ((512) & 0xFF), True); #FD I&G bank 2 M6
                    self.sendCommand16( 0xA7,  ((self.d["Motor Config"]["PI_FD_bank3_18bits_M6"].get() >> 8) & 0xFF),  ((self.d["Motor Config"]["PI_FD_bank3_18bits_M6"].get()) & 0xFF), True); #FD I&G bank 3 M6
                    self.sendCommand16( 0xA8,  (0x00),  (0x0f), True); #I banks disabled M6
                    self.sendCommand16( 0xA9,  ((512 >> 8) & 0xFF),  ((512) & 0xFF), True); #FD I&G bank 0 M6
                    self.sendCommand16( 0xAA,  ((512 >> 8) & 0xFF),  ((512) & 0xFF), True); #FD I&G bank 1 M6
                    self.sendCommand16( 0xAB,  ((512 >> 8) & 0xFF),  ((512) & 0xFF), True); #FD I&G bank 2 M6
                    self.sendCommand16( 0xAC,  ((self.d["Motor Config"]["PD_FD_bank3_22bits_M5"].get() >> 8) & 0xFF),  ((self.d["Motor Config"]["PD_FD_bank3_22bits_M5"].get()) & 0xFF), True); #FD I&G bank 3 M6
                    self.sendCommand16( 0xB2,  (0x00),  (0x0), True); #spike expansor M6
                    self.sendCommand16( 0xB3,  (0x00),  (0x0f), True); #d banks disabled M1
                    self.sendCommand16( 0xB4,  ((512 >> 8) & 0xFF),  ((512) & 0xFF), True); #FD I&G bank 0 M1
                    self.sendCommand16( 0xB5,  ((512 >> 8) & 0xFF),  ((512) & 0xFF), True); #FD I&G bank 1 M1
                    self.sendCommand16( 0xB6,  ((512 >> 8) & 0xFF),  ((512) & 0xFF), True); #FD I&G bank 2 M1
                    self.sendCommand16( 0xB7,  ((self.d["Motor Config"]["EI_FD_bank3_18bits_M6"].get() >> 8) & 0xFF),  ((self.d["Motor Config"]["EI_FD_bank3_18bits_M6"].get()) & 0xFF), True); #FD I&G bank 3 M1
                    self.sendCommand16( 0xA0,  0,  0, False); #LEDs M6 off
                    print("PI_FD_bank0_12bits_M6={} \t PI_FD_bank1_14bits_M6={} \t PI_FD_bank2_16bits_M6={} \t PI_FD_bank3_18bits_M6={}\n"
                          .format(512,512,512,self.d["Motor Config"]["PI_FD_bank3_18bits_M6"].get()) +
                          "PD_FD_bank0_16bits_M6={} \t PD_FD_bank1_18bits_M6={} \t PD_FD_bank2_20bits_M6={} \t PD_FD_bank3_22bits_M6={}\n"
                          .format(512,512,512,512) +
                          "EI_FD_bank0_12bits_M6={} \t EI_FD_bank1_14bits_M6={} \t EI_FD_bank2_16bits_M6={} \t EI_FD_bank3_18bits_M6={}\n"
                          .format(512,512,512,self.d["Motor Config"]["EI_FD_bank3_18bits_M6"].get()))

                    
                    print("Sending USB SPI")
                    print(i)

        return

    def SendCommandJoint1(self,ref):
        '''
        Send reference to 1st joint

        This function allows to send a reference
        to the 1st joint in order to move it
        Reference to angle are mapped in this link: INSERT LINK
        '''
        #EI_FD_bank0_12bits_M1 = 512
        #EI_FD_bank0_14bits_M1 = 512
        #EI_FD_bank0_16bits_M1 = 512
        #PI_FD_bank0_12bits_M1 = 512
        #PI_FD_bank0_14bits_M1 = 512
        #PI_FD_bank0_16bits_M1 = 512
        self.sendCommand16( 0,  (0x00), ((self.d["Motor Config"]["leds_M1"].get()) & 0xFF), True) #LEDs M1
        self.sendCommand16( 0x03,  (0x00),  ((3)&0xFF), True) #I banks disabled M1
        self.sendCommand16( 0x04,  ((512 >> 8) & 0xFF),  ((512) & 0xFF), True) #FD I&G bank 0 M1
        self.sendCommand16( 0x05,  ((512 >> 8) & 0xFF),  ((512) & 0xFF), True) #FD I&G bank 1 M1
        self.sendCommand16( 0x06,  ((512 >> 8) & 0xFF),  ((512) & 0xFF), True) #FD I&G bank 2 M1
        self.sendCommand16( 0x07,  ((self.d["Motor Config"]["PI_FD_bank3_18bits_M1"].get() >> 8) & 0xFF),  ((self.d["Motor Config"]["PI_FD_bank3_18bits_M1"].get()) & 0xFF), True) #FD I&G bank 3 M1
        self.sendCommand16( 0x08,  (0x00),  ((512)&0xFF), True) #D banks disabled M1
        self.sendCommand16( 0x09,  ((512 >> 8) & 0xFF),  ((512) & 0xFF), True) #FD I&G bank 0 M1
        self.sendCommand16( 0x0A,  ((512 >> 8) & 0xFF),  ((512) & 0xFF), True) #FD I&G bank 1 M1
        self.sendCommand16( 0x0B,  ((512 >> 8) & 0xFF),  ((512) & 0xFF), True) #FD I&G bank 2 M1
        self.sendCommand16( 0x0C,  ((self.d["Motor Config"]["PD_FD_bank3_22bits_M1"].get() >> 8) & 0xFF),  ((self.d["Motor Config"]["PD_FD_bank3_22bits_M1"].get()) & 0xFF), True) #FD I&G bank 3 M1
        self.sendCommand16( 0x12,  ((self.d["Motor Config"]["spike_expansor_M1"].get() >> 8) & 0xFF),  ((self.d["Motor Config"]["spike_expansor_M1"].get()) & 0xFF), True) #spike expansor M1
        self.sendCommand16( 0x13,  (0x00),  ((3)&0xFF), True) #EI bank enabled M1 EI_bank_select_M1 = 3
        self.sendCommand16( 0x14,  ((512 >> 8) & 0xFF),  ((512) & 0xFF), True) #FD I&G bank 0 M1
        self.sendCommand16( 0x15,  ((512 >> 8) & 0xFF),  ((512) & 0xFF), True) #FD I&G bank 1 M1
        self.sendCommand16( 0x16,  ((512 >> 8) & 0xFF),  ((512) & 0xFF), True) #FD I&G bank 2 M1
        self.sendCommand16( 0x17,  ((self.d["Motor Config"]["EI_FD_bank3_18bits_M1"].get() >> 8) & 0xFF),  ((self.d["Motor Config"]["EI_FD_bank3_18bits_M1"].get()) & 0xFF), True) #FD I&G bank 3 M1
        #self.sendCommand16( 0,  0,  0, false) #LEDs M1 off
        self.sendCommand16( 0x02,  ((ref >> 8) & 0xFF),  ((ref) & 0xFF), True) #Ref M1 0
        self.sendCommand16( 0x02,  ((ref >> 8) & 0xFF),  ((ref) & 0xFF), True) #Ref M1 0
        self.sendCommand16( 0x02,  ((ref >> 8) & 0xFF),  ((ref) & 0xFF), True) #Ref M1 0
        pass

    def SendCommandJoint2(self,ref):
        '''
        Send reference to 2nd joint

        This function allows to send a reference
        to the 2nd joint in order to move it
        Reference to angle are mapped in this link: INSERT LINK
        '''
        #EI_FD_bank0_12bits_M2 = 512
        #EI_FD_bank0_14bits_M2 = 512
        #EI_FD_bank0_16bits_M2 = 512
        #PI_FD_bank0_12bits_M2 = 512
        #PI_FD_bank0_14bits_M2 = 512
        #PI_FD_bank0_16bits_M2 = 512
        self.sendCommand16( 0x20,  (0x00), ((self.d["Motor Config"]["leds_M2"].get()) & 0xFF), True) #LEDs M2
        self.sendCommand16( 0x23,  (0x00),  ((3)&0xFF), True) #I banks disabled M2
        self.sendCommand16( 0x24,  ((512 >> 8) & 0xFF),  ((512) & 0xFF), True) #FD I&G bank 0 M2
        self.sendCommand16( 0x25,  ((512 >> 8) & 0xFF),  ((512) & 0xFF), True) #FD I&G bank 1 M2
        self.sendCommand16( 0x26,  ((512 >> 8) & 0xFF),  ((512) & 0xFF), True) #FD I&G bank 2 M2
        self.sendCommand16( 0x27,  ((self.d["Motor Config"]["PI_FD_bank3_18bits_M2"].get() >> 8) & 0xFF),  ((self.d["Motor Config"]["PI_FD_bank3_18bits_M2"].get()) & 0xFF), True) #FD I&G bank 3 M2
        self.sendCommand16( 0x28,  (0x00),  ((512)&0xFF), True) #D banks disabled M2
        self.sendCommand16( 0x29,  ((512 >> 8) & 0xFF),  ((512) & 0xFF), True) #FD I&G bank 0 M2
        self.sendCommand16( 0x2A,  ((512 >> 8) & 0xFF),  ((512) & 0xFF), True) #FD I&G bank 1 M2
        self.sendCommand16( 0x2B,  ((512 >> 8) & 0xFF),  ((512) & 0xFF), True) #FD I&G bank 2 M2
        self.sendCommand16( 0x2C,  ((self.d["Motor Config"]["PD_FD_bank3_22bits_M2"].get() >> 8) & 0xFF),  ((self.d["Motor Config"]["PD_FD_bank3_22bits_M2"].get()) & 0xFF), True) #FD I&G bank 3 M2
        self.sendCommand16( 0x32,  ((self.d["Motor Config"]["spike_expansor_M2"].get() >> 8) & 0xFF),  ((self.d["Motor Config"]["spike_expansor_M2"].get()) & 0xFF), True) #spike expansor M2
        self.sendCommand16( 0x33,  (0x00),  ((3)&0xFF), True) #EI bank enabled M2 EI_bank_select_M2 = 3
        self.sendCommand16( 0x34,  ((512 >> 8) & 0xFF),  ((512) & 0xFF), True) #FD I&G bank 0 M2
        self.sendCommand16( 0x35,  ((512 >> 8) & 0xFF),  ((512) & 0xFF), True) #FD I&G bank 1 M2
        self.sendCommand16( 0x36,  ((512 >> 8) & 0xFF),  ((512) & 0xFF), True) #FD I&G bank 2 M2
        self.sendCommand16( 0x37,  ((self.d["Motor Config"]["EI_FD_bank3_18bits_M2"].get() >> 8) & 0xFF),  ((self.d["Motor Config"]["EI_FD_bank3_18bits_M2"].get()) & 0xFF), True) #FD I&G bank 3 M2
        #self.sendCommand16( 0,  0,  0, false) #LEDs M2 off
        self.sendCommand16( 0x22,  ((ref >> 8) & 0xFF),  ((ref) & 0xFF), True) #Ref M2 0
        self.sendCommand16( 0x22,  ((ref >> 8) & 0xFF),  ((ref) & 0xFF), True) #Ref M2 0
        self.sendCommand16( 0x22,  ((ref >> 8) & 0xFF),  ((ref) & 0xFF), True) #Ref M2 0
        pass

    def SendCommandJoint3(self,ref):
        '''
        Send reference to 3rd joint

        This function allows to send a reference
        to the 3rd joint in order to move it
        Reference to angle are mapped in this link: INSERT LINK
        '''
        #EI_FD_bank0_12bits_M3 = 512
        #EI_FD_bank0_14bits_M3 = 512
        #EI_FD_bank0_16bits_M3 = 512
        #PI_FD_bank0_12bits_M3 = 512
        #PI_FD_bank0_14bits_M3 = 512
        #PI_FD_bank0_16bits_M3 = 512
        self.sendCommand16( 0x40,  (0x00), ((self.d["Motor Config"]["leds_M3"].get()) & 0xFF), True) #LEDs M3
        self.sendCommand16( 0x43,  (0x00),  ((3)&0xFF), True) #I banks disabled M3
        self.sendCommand16( 0x44,  ((512 >> 8) & 0xFF),  ((512) & 0xFF), True) #FD I&G bank 0 M3
        self.sendCommand16( 0x45,  ((512 >> 8) & 0xFF),  ((512) & 0xFF), True) #FD I&G bank 1 M3
        self.sendCommand16( 0x46,  ((512 >> 8) & 0xFF),  ((512) & 0xFF), True) #FD I&G bank 2 M3
        self.sendCommand16( 0x47,  ((self.d["Motor Config"]["PI_FD_bank3_18bits_M3"].get() >> 8) & 0xFF),  ((self.d["Motor Config"]["PI_FD_bank3_18bits_M3"].get()) & 0xFF), True) #FD I&G bank 3 M3
        self.sendCommand16( 0x48,  (0x00),  ((512)&0xFF), True) #D banks disabled M3
        self.sendCommand16( 0x49,  ((512 >> 8) & 0xFF),  ((512) & 0xFF), True) #FD I&G bank 0 M3
        self.sendCommand16( 0x4A,  ((512 >> 8) & 0xFF),  ((512) & 0xFF), True) #FD I&G bank 1 M3
        self.sendCommand16( 0x4B,  ((512 >> 8) & 0xFF),  ((512) & 0xFF), True) #FD I&G bank 2 M3
        self.sendCommand16( 0x4C,  ((self.d["Motor Config"]["PD_FD_bank3_22bits_M3"].get() >> 8) & 0xFF),  ((self.d["Motor Config"]["PD_FD_bank3_22bits_M3"].get()) & 0xFF), True) #FD I&G bank 3 M3
        self.sendCommand16( 0x52,  ((self.d["Motor Config"]["spike_expansor_M3"].get() >> 8) & 0xFF),  ((self.d["Motor Config"]["spike_expansor_M3"].get()) & 0xFF), True) #spike expansor M3
        self.sendCommand16( 0x53,  (0x00),  ((3)&0xFF), True) #EI bank enabled M3 EI_bank_select_M3 = 3
        self.sendCommand16( 0x54,  ((512 >> 8) & 0xFF),  ((512) & 0xFF), True) #FD I&G bank 0 M3
        self.sendCommand16( 0x55,  ((512 >> 8) & 0xFF),  ((512) & 0xFF), True) #FD I&G bank 1 M3
        self.sendCommand16( 0x56,  ((512 >> 8) & 0xFF),  ((512) & 0xFF), True) #FD I&G bank 2 M3
        self.sendCommand16( 0x57,  ((self.d["Motor Config"]["EI_FD_bank3_18bits_M3"].get() >> 8) & 0xFF),  ((self.d["Motor Config"]["EI_FD_bank3_18bits_M3"].get()) & 0xFF), True) #FD I&G bank 3 M3
        #self.sendCommand16( 0,  0,  0, false) #LEDs M3 off
        self.sendCommand16( 0x42,  ((ref >> 8) & 0xFF),  ((ref) & 0xFF), True) #Ref M3 0
        self.sendCommand16( 0x42,  ((ref >> 8) & 0xFF),  ((ref) & 0xFF), True) #Ref M3 0
        self.sendCommand16( 0x42,  ((ref >> 8) & 0xFF),  ((ref) & 0xFF), True) #Ref M3 0
        pass
        
    def SendCommandJoint4(self,ref):
        '''
        Send reference to 4th joint

        This function allows to send a reference
        to the 4th joint in order to move it
        Reference to angle are mapped in this link: INSERT LINK
        '''
        #EI_FD_bank0_12bits_M4 = 512
        #EI_FD_bank0_14bits_M4 = 512
        #EI_FD_bank0_16bits_M4 = 512
        #PI_FD_bank0_12bits_M4 = 512
        #PI_FD_bank0_14bits_M4 = 512
        #PI_FD_bank0_16bits_M4 = 512
        self.sendCommand16( 0x60,  (0x00), ((self.d["Motor Config"]["leds_M4"].get()) & 0xFF), True) #LEDs M4
        self.sendCommand16( 0x63,  (0x00),  ((3)&0xFF), True) #I banks disabled M4
        self.sendCommand16( 0x64,  ((512 >> 8) & 0xFF),  ((512) & 0xFF), True) #FD I&G bank 0 M4
        self.sendCommand16( 0x65,  ((512 >> 8) & 0xFF),  ((512) & 0xFF), True) #FD I&G bank 1 M4
        self.sendCommand16( 0x66,  ((512 >> 8) & 0xFF),  ((512) & 0xFF), True) #FD I&G bank 2 M4
        self.sendCommand16( 0x67,  ((self.d["Motor Config"]["PI_FD_bank3_18bits_M4"].get() >> 8) & 0xFF),  ((self.d["Motor Config"]["PI_FD_bank3_18bits_M4"].get()) & 0xFF), True) #FD I&G bank 3 M4
        self.sendCommand16( 0x68,  (0x00),  ((512)&0xFF), True) #D banks disabled M4
        self.sendCommand16( 0x69,  ((512 >> 8) & 0xFF),  ((512) & 0xFF), True) #FD I&G bank 0 M4
        self.sendCommand16( 0x6A,  ((512 >> 8) & 0xFF),  ((512) & 0xFF), True) #FD I&G bank 1 M4
        self.sendCommand16( 0x6B,  ((512 >> 8) & 0xFF),  ((512) & 0xFF), True) #FD I&G bank 2 M4
        self.sendCommand16( 0x6C,  ((512 >> 8) & 0xFF),  ((512) & 0xFF), True) #FD I&G bank 3 M4
        self.sendCommand16( 0x72,  ((self.d["Motor Config"]["spike_expansor_M4"].get() >> 8) & 0xFF),  ((self.d["Motor Config"]["spike_expansor_M4"].get()) & 0xFF), True) #spike expansor M4
        self.sendCommand16( 0x73,  (0x00),  ((3)&0xFF), True) #EI bank enabled M4 EI_bank_select_M4 = 3
        self.sendCommand16( 0x74,  ((512 >> 8) & 0xFF),  ((512) & 0xFF), True) #FD I&G bank 0 M4
        self.sendCommand16( 0x75,  ((512 >> 8) & 0xFF),  ((512) & 0xFF), True) #FD I&G bank 1 M4
        self.sendCommand16( 0x76,  ((512 >> 8) & 0xFF),  ((512) & 0xFF), True) #FD I&G bank 2 M4
        self.sendCommand16( 0x77,  ((self.d["Motor Config"]["EI_FD_bank3_18bits_M4"].get() >> 8) & 0xFF),  ((self.d["Motor Config"]["EI_FD_bank3_18bits_M4"].get()) & 0xFF), True) #FD I&G bank 3 M4
        #self.sendCommand16( 0,  0,  0, false) #LEDs M4 off
        self.sendCommand16( 0x62,  ((ref >> 8) & 0xFF),  ((ref) & 0xFF), True) #Ref M4 0
        self.sendCommand16( 0x62,  ((ref >> 8) & 0xFF),  ((ref) & 0xFF), True) #Ref M4 0
        self.sendCommand16( 0x62,  ((ref >> 8) & 0xFF),  ((ref) & 0xFF), True) #Ref M4 0
        pass

    def SendCommandJoint5(self,ref):
        '''
        Send reference to 5th joint

        This function allows to send a reference
        to the 5th joint in order to move it
        Reference to angle are mapped in this link: INSERT LINK
        '''
        #EI_FD_bank0_12bits_M5 = 512
        #EI_FD_bank0_14bits_M5 = 512
        #EI_FD_bank0_16bits_M5 = 512
        #PI_FD_bank0_12bits_M5 = 512
        #PI_FD_bank0_14bits_M5 = 512
        #PI_FD_bank0_16bits_M5 = 512
        self.sendCommand16( 0x80,  (0x00), ((self.d["Motor Config"]["leds_M5"].get()) & 0xFF), True) #LEDs M5
        self.sendCommand16( 0x83,  (0x00),  ((3)&0xFF), True) #I banks disabled M5
        self.sendCommand16( 0x84,  ((512 >> 8) & 0xFF),  ((512) & 0xFF), True) #FD I&G bank 0 M5
        self.sendCommand16( 0x85,  ((512 >> 8) & 0xFF),  ((512) & 0xFF), True) #FD I&G bank 1 M5
        self.sendCommand16( 0x86,  ((512 >> 8) & 0xFF),  ((512) & 0xFF), True) #FD I&G bank 2 M5
        self.sendCommand16( 0x87,  ((self.d["Motor Config"]["PI_FD_bank3_18bits_M5"].get() >> 8) & 0xFF),  ((self.d["Motor Config"]["PI_FD_bank3_18bits_M5"].get()) & 0xFF), True) #FD I&G bank 3 M5
        self.sendCommand16( 0x88,  (0x00),  ((512)&0xFF), True) #D banks disabled M5
        self.sendCommand16( 0x89,  ((512 >> 8) & 0xFF),  ((512) & 0xFF), True) #FD I&G bank 0 M5
        self.sendCommand16( 0x8A,  ((512 >> 8) & 0xFF),  ((512) & 0xFF), True) #FD I&G bank 1 M5
        self.sendCommand16( 0x8B,  ((512 >> 8) & 0xFF),  ((512) & 0xFF), True) #FD I&G bank 2 M5
        self.sendCommand16( 0x8C,  ((self.d["Motor Config"]["PD_FD_bank3_22bits_M5"].get() >> 8) & 0xFF),  ((self.d["Motor Config"]["PD_FD_bank3_22bits_M5"].get()) & 0xFF), True) #FD I&G bank 3 M5
        self.sendCommand16( 0x92,  ((self.d["Motor Config"]["spike_expansor_M5"].get() >> 8) & 0xFF),  ((self.d["Motor Config"]["spike_expansor_M5"].get()) & 0xFF), True) #spike expansor M5
        self.sendCommand16( 0x93,  (0x00),  ((3)&0xFF), True) #EI bank enabled M5 EI_bank_select_M5 = 3
        self.sendCommand16( 0x94,  ((512 >> 8) & 0xFF),  ((512) & 0xFF), True) #FD I&G bank 0 M5
        self.sendCommand16( 0x95,  ((512 >> 8) & 0xFF),  ((512) & 0xFF), True) #FD I&G bank 1 M5
        self.sendCommand16( 0x96,  ((512 >> 8) & 0xFF),  ((512) & 0xFF), True) #FD I&G bank 2 M5
        self.sendCommand16( 0x97,  ((self.d["Motor Config"]["EI_FD_bank3_18bits_M5"].get() >> 8) & 0xFF),  ((self.d["Motor Config"]["EI_FD_bank3_18bits_M5"].get()) & 0xFF), True) #FD I&G bank 3 M5
        #self.sendCommand16( 0,  0,  0, false) #LEDs M5 off
        self.sendCommand16( 0x82,  ((ref >> 8) & 0xFF),  ((ref) & 0xFF), True) #Ref M5 0
        self.sendCommand16( 0x82,  ((ref >> 8) & 0xFF),  ((ref) & 0xFF), True) #Ref M5 0
        self.sendCommand16( 0x82,  ((ref >> 8) & 0xFF),  ((ref) & 0xFF), True) #Ref M5 0
        pass

    def SendCommandJoint6(self,ref):
        '''
        Send reference to 6th joint

        This function allows to send a reference
        to the 6th joint in order to move it
        Reference to angle are mapped in this link: INSERT LINK
        '''
        #EI_FD_bank0_12bits_M6 = 512
        #EI_FD_bank0_14bits_M6 = 512
        #EI_FD_bank0_16bits_M6 = 512
        #PI_FD_bank0_12bits_M6 = 512
        #PI_FD_bank0_14bits_M6 = 512
        #PI_FD_bank0_16bits_M6 = 512
        self.sendCommand16( 0xA0,  (0x00), ((self.d["Motor Config"]["leds_M6"].get()) & 0xFF), True) #LEDs M6
        self.sendCommand16( 0xA3,  (0x00),  ((3)&0xFF), True) #I banks disabled M6
        self.sendCommand16( 0xA4,  ((512 >> 8) & 0xFF),  ((512) & 0xFF), True) #FD I&G bank 0 M6
        self.sendCommand16( 0xA5,  ((512 >> 8) & 0xFF),  ((512) & 0xFF), True) #FD I&G bank 1 M6
        self.sendCommand16( 0xA6,  ((512 >> 8) & 0xFF),  ((512) & 0xFF), True) #FD I&G bank 2 M6
        self.sendCommand16( 0xA7,  ((self.d["Motor Config"]["PI_FD_bank3_18bits_M6"].get() >> 8) & 0xFF),  ((self.d["Motor Config"]["PI_FD_bank3_18bits_M6"].get()) & 0xFF), True) #FD I&G bank 3 M6
        self.sendCommand16( 0xA8,  (0x00),  ((512)&0xFF), True) #D banks disabled M6
        self.sendCommand16( 0xA9,  ((512 >> 8) & 0xFF),  ((512) & 0xFF), True) #FD I&G bank 0 M6
        self.sendCommand16( 0xAA,  ((512 >> 8) & 0xFF),  ((512) & 0xFF), True) #FD I&G bank 1 M6
        self.sendCommand16( 0xAB,  ((512 >> 8) & 0xFF),  ((512) & 0xFF), True) #FD I&G bank 2 M6
        self.sendCommand16( 0xAC,  ((self.d["Motor Config"]["PD_FD_bank3_22bits_M6"].get() >> 8) & 0xFF),  ((self.d["Motor Config"]["PD_FD_bank3_22bits_M6"].get()) & 0xFF), True) #FD I&G bank 3 M6
        self.sendCommand16( 0xB2,  ((self.d["Motor Config"]["spike_expansor_M6"].get() >> 8) & 0xFF),  ((self.d["Motor Config"]["spike_expansor_M6"].get()) & 0xFF), True) #spike expansor M6
        self.sendCommand16( 0xB3,  (0x00),  ((3)&0xFF), True) #EI bank enabled M6 EI_bank_select_M6 = 3
        self.sendCommand16( 0xB4,  ((512 >> 8) & 0xFF),  ((512) & 0xFF), True) #FD I&G bank 0 M6
        self.sendCommand16( 0xB5,  ((512 >> 8) & 0xFF),  ((512) & 0xFF), True) #FD I&G bank 1 M6
        self.sendCommand16( 0xB6,  ((512 >> 8) & 0xFF),  ((512) & 0xFF), True) #FD I&G bank 2 M6
        self.sendCommand16( 0xB7,  ((self.d["Motor Config"]["EI_FD_bank3_18bits_M6"].get() >> 8) & 0xFF),  ((self.d["Motor Config"]["EI_FD_bank3_18bits_M6"].get()) & 0xFF), True) #FD I&G bank 3 M6
        #self.sendCommand16( 0,  0,  0, false) #LEDs M6 off
        self.sendCommand16( 0xA2,  ((ref >> 8) & 0xFF),  ((ref) & 0xFF), True) #Ref M6 0
        self.sendCommand16( 0xA2,  ((ref >> 8) & 0xFF),  ((ref) & 0xFF), True) #Ref M6 0
        self.sendCommand16( 0xA2,  ((ref >> 8) & 0xFF),  ((ref) & 0xFF), True) #Ref M6 0
        pass

    def ConfigureSPID(self):
        
        '''
        Command a movement to all the joints
        
        It calls sendCommandJoint1-6 and sends the 
        reference that is specified in the
        input boxes that the GUI offers.
        
        '''

        if (((self.dev and self.checked.get()) == None) or (self.checked.get() == False)):
            self.alert("No device opened. Try checking USB option first")
            return
        else:
            if self.checked.get():
                for i in range(0,6):

                    self.SendCommandJoint1(self.d["Motor Config"]["ref_M1"].get())
                    print("ref_M1:",self.d["Motor Config"]["ref_M1"].get())
                    print("PI_FD_bank0_12bits_M1={} \t PI_FD_bank1_14bits_M1={} \t PI_FD_bank2_16bits_M1={} \t PI_FD_bank3_18bits_M1={}\n"
                          .format(512,512,512,self.d["Motor Config"]["PI_FD_bank3_18bits_M1"].get()) +
                          "PD_FD_bank0_16bits_M1={} \t PD_FD_bank1_18bits_M1={} \t PD_FD_bank2_20bits_M1={} \t PD_FD_bank3_22bits_M1={}\n"
                          .format(512,512,512,512) +
                          "EI_FD_bank0_12bits_M1={} \t EI_FD_bank1_14bits_M1={} \t EI_FD_bank2_16bits_M1={} \t EI_FD_bank3_18bits_M1={}\n"
                          .format(512,512,512,self.d["Motor Config"]["EI_FD_bank3_18bits_M1"].get()))
                    
                    self.SendCommandJoint2(self.d["Motor Config"]["ref_M2"].get())
                    print("ref_M2:",self.d["Motor Config"]["ref_M2"].get())
                    print("PI_FD_bank0_12bits_M2={} \t PI_FD_bank1_14bits_M2={} \t PI_FD_bank2_16bits_M2={} \t PI_FD_bank3_18bits_M2={}\n"
                          .format(512,512,512,self.d["Motor Config"]["PI_FD_bank3_18bits_M2"].get()) +
                          "PD_FD_bank0_16bits_M2={} \t PD_FD_bank1_18bits_M2={} \t PD_FD_bank2_20bits_M2={} \t PD_FD_bank3_22bits_M2={}\n"
                          .format(512,512,512,512) +
                          "EI_FD_bank0_12bits_M2={} \t EI_FD_bank1_14bits_M2={} \t EI_FD_bank2_16bits_M2={} \t EI_FD_bank3_18bits_M2={}\n"
                          .format(512,512,512,self.d["Motor Config"]["EI_FD_bank3_18bits_M2"].get()))

                    self.SendCommandJoint3(self.d["Motor Config"]["ref_M3"].get())
                    print("ref_M3:",self.d["Motor Config"]["ref_M3"].get())
                    print("PI_FD_bank0_12bits_M3={} \t PI_FD_bank1_14bits_M3={} \t PI_FD_bank2_16bits_M3={} \t PI_FD_bank3_18bits_M3={}\n"
                          .format(512,512,512,self.d["Motor Config"]["PI_FD_bank3_18bits_M3"].get()) +
                          "PD_FD_bank0_16bits_M3={} \t PD_FD_bank1_18bits_M3={} \t PD_FD_bank2_20bits_M3={} \t PD_FD_bank3_22bits_M3={}\n"
                          .format(512,512,512,512) +
                          "EI_FD_bank0_12bits_M3={} \t EI_FD_bank1_14bits_M3={} \t EI_FD_bank2_16bits_M3={} \t EI_FD_bank3_18bits_M3={}\n"
                          .format(512,512,512,self.d["Motor Config"]["EI_FD_bank3_18bits_M3"].get()))
                    
                    self.SendCommandJoint4(self.d["Motor Config"]["ref_M4"].get())
                    print("ref_M4:",self.d["Motor Config"]["ref_M4"].get())
                    print("PI_FD_bank0_12bits_M4={} \t PI_FD_bank1_14bits_M4={} \t PI_FD_bank2_16bits_M4={} \t PI_FD_bank3_18bits_M4={}\n"
                          .format(512,512,512,self.d["Motor Config"]["PI_FD_bank3_18bits_M4"].get()) +
                          "PD_FD_bank0_16bits_M4={} \t PD_FD_bank1_18bits_M4={} \t PD_FD_bank2_20bits_M4={} \t PD_FD_bank3_22bits_M4={}\n"
                          .format(512,512,512,512) +
                          "EI_FD_bank0_12bits_M4={} \t EI_FD_bank1_14bits_M4={} \t EI_FD_bank2_16bits_M4={} \t EI_FD_bank3_18bits_M4={}\n"
                          .format(512,512,512,self.d["Motor Config"]["EI_FD_bank3_18bits_M4"].get()))

                    self.SendCommandJoint5(self.d["Motor Config"]["ref_M5"].get())
                    print("ref_M5:",self.d["Motor Config"]["ref_M5"].get())
                    print("PI_FD_bank0_12bits_M5={} \t PI_FD_bank1_14bits_M5={} \t PI_FD_bank2_16bits_M5={} \t PI_FD_bank3_18bits_M5={}\n"
                          .format(512,512,512,self.d["Motor Config"]["PI_FD_bank3_18bits_M5"].get()) +
                          "PD_FD_bank0_16bits_M5={} \t PD_FD_bank1_18bits_M5={} \t PD_FD_bank2_20bits_M5={} \t PD_FD_bank3_22bits_M5={}\n"
                          .format(512,512,512,512) +
                          "EI_FD_bank0_12bits_M5={} \t EI_FD_bank1_14bits_M5={} \t EI_FD_bank2_16bits_M5={} \t EI_FD_bank3_18bits_M5={}\n"
                          .format(512,512,512,self.d["Motor Config"]["EI_FD_bank3_18bits_M5"].get()))
                    
                    self.SendCommandJoint6(self.d["Motor Config"]["ref_M6"].get())
                    print("ref_M6:",self.d["Motor Config"]["ref_M6"].get())
                    print("PI_FD_bank0_12bits_M6={} \t PI_FD_bank1_14bits_M6={} \t PI_FD_bank2_16bits_M6={} \t PI_FD_bank3_18bits_M6={}\n"
                          .format(512,512,512,self.d["Motor Config"]["PI_FD_bank3_18bits_M6"].get()) +
                          "PD_FD_bank0_16bits_M6={} \t PD_FD_bank1_18bits_M6={} \t PD_FD_bank2_20bits_M6={} \t PD_FD_bank3_22bits_M6={}\n"
                          .format(512,512,512,512) +
                          "EI_FD_bank0_12bits_M6={} \t EI_FD_bank1_14bits_M6={} \t EI_FD_bank2_16bits_M6={} \t EI_FD_bank3_18bits_M6={}\n"
                          .format(512,512,512,self.d["Motor Config"]["EI_FD_bank3_18bits_M6"].get()))

                    print("Sending USB SPI")
                    print(i)
    
    def ConfigureSPID_allJoints(self):

        '''
        Same as ConfigureSPID but it doesn't print the information in the console
        '''

        #Check if USB device is initialized
        if(self.dev == None):
            self.alert("There is no opened device. Try opening one first")
            return
        
        if self.checked.get():
            for i in range (0,2):
                self.SendCommandJoint1(self.d["Motor Config"]["ref_M1"].get())
                self.SendCommandJoint2(self.d["Motor Config"]["ref_M2"].get())
                self.SendCommandJoint3(self.d["Motor Config"]["ref_M3"].get())
                self.SendCommandJoint4(self.d["Motor Config"]["ref_M4"].get())
                self.SendCommandJoint5(self.d["Motor Config"]["ref_M5"].get())
                self.SendCommandJoint6(self.d["Motor Config"]["ref_M6"].get())
                print("Sending USB SPI")
                print(i)

    def sendCommand16(self, cmd, data1, data2, spiEnable):
        '''
        Send 2 bytes of data and an address via USB to robot's infrastructure

        This function allows to send 2 bytes of data to 
        a specific address to the AERNode board via USB

        Args:
            cmd (int): Address to which data will be sent
            data1 (byte): Byte 1 of data
            data2 (byte): Byte 2 of data
            spiEnable (bool): Legacy option not to break anything, always True in this program
        '''

        #Check if USB device is initialized
        if(self.dev == None):
            self.alert("There is no opened device. Try opening one first")
            return
        
        
        else:
            #Allocate data buffer as a byte array
            dataBuffer = bytearray(self.PACKET_LENGTH)
            
            #Then fill it for the first transfer
            dataBuffer[0] = ord('A')
            dataBuffer[1] = ord('T')
            dataBuffer[2] = ord('C')
            dataBuffer[3] = 0x01 # Command always 1 for SPI upload.
            dataBuffer[4] = 0x02 # Data length always 2 for 2 bytes.
            dataBuffer[5] = 0x00
            dataBuffer[6] = 0x00
            dataBuffer[7] = 0x00
            dataBuffer[8] = cmd
            dataBuffer[9] = 0 if spiEnable else 1

            #Library determines automatically transfer type via endpoint addresses
            #so no need to specify bulk or interrupt
            written = self.dev.write(self.ENDPOINT_OUT,dataBuffer)

            #If the amount of bytes written is not the expected, raise a warning
            if(written != self.PACKET_LENGTH): 
                print("Failed to transfer whole packet")
            
            #Fill buffer for the second transfer,
            #which contains the actual data
            dataBuffer[0] = cmd
            dataBuffer[1] = data1
            dataBuffer[2] = data2
            
            written = self.dev.write(self.ENDPOINT_OUT,dataBuffer)
            
            #And check again for a correct transfer
            if(written != self.PACKET_LENGTH):
                print("Failed to transfer whole packet")

    def readSensor(self,sensor):
        '''
        Read a joint's position sensor

        This function allows for a joint sensor
        to be read, so that you are able to
        know a joint's position in any given moment

        Args:
            sensor (int): The number of the sensor to be read, ranging from 1 to 6
        
        Returns:
            int: Sensor position if everything went well
            int: -1 if something went wrong
        '''

        if(self.dev == None):
            self.alert("There is no opened device. Try opening one first")
            return   

        else:
            #Allocate data buffer as a byte array
            dataBuffer = bytearray(self.PACKET_LENGTH)
            
            #Then fill it for the first transfer
            dataBuffer[0] = ord('A')
            dataBuffer[1] = ord('T')
            dataBuffer[2] = ord('C')
            dataBuffer[3] = 0x02 # Command always 2 for reading operation
            dataBuffer[4] = 64 # Data length always 3 for 3 bytes.

            readBuffer = bytearray(self.PACKET_LENGTH)

            written = self.dev.write(self.ENDPOINT_OUT,dataBuffer)

            #Check for a correct transfer
            if(written != self.PACKET_LENGTH):
                print("Failed to transfer whole packet")


            readBuffer = self.dev.read(self.ENDPOINT_IN,self.PACKET_LENGTH,10000)
            if read==0:
                 print("Failed to receive whole packet")
            
            if readBuffer[34] == sensor:
                sensor_data = (0x0ff & readBuffer[35])*256 + readBuffer[36]
            else:
                sensor_data = -1

            return sensor_data
  
    def scanMotor1(self):
        '''
        Scan Motor 1

        This function commands the robot to perform 
        the scan procedure defined by the 4 Scan Parameters
        (available in the dictionary as "Scan Parameters")

        These functions (scanMotor1-6) can be used to obtain data
        that can be later be displayed in different graphs
        '''
        if self.dev==None:
            self.alert("There is no opened device. Try opening one first")
            return
        # Convert ms time into clock cycles.
        scan_Init_Value = self.d["Scan Parameters"]["scan_Init_Value"].get()
        scan_Final_Value = self.d["Scan Parameters"]["scan_Final_Value"].get()
        scan_Step_Value = self.d["Scan Parameters"]["scan_Step_Value"].get()
        scan_Wait_Time = self.d["Scan Parameters"]["scan_Wait_Time"].get()

        if self.checked.get():
            
            #Fecha en str, formato: yyyy_MM_dd_HH_mm_ss

            date = datetime.datetime.now()
            timeStamp = date.strftime("%Y_%b_%d_%H_%M_%S")
            #Abrir archivo de log con el nombre de la fecha
            logging.basicConfig(filename='./logs/Scan1_' + timeStamp + '.log',filemode='w')
            logging.info("SMALL ED-Scorbot Joint1 Scan Log file")

            #
            self.sendCommand16( 0x03,  (0x00),  ((3)&0xFF), True) #I banks disabled M1 PI_bank_select_M1 = 3
            self.sendCommand16( 0x07,  ((self.d["Motor Config"]["PI_FD_bank3_18bits_M1"].get() >> 8) & 0xFF),  ((self.d["Motor Config"]["PI_FD_bank3_18bits_M1"].get()) & 0xFF), True) #FD I&G bank 3 M1
            self.sendCommand16( 0x08,  (0x00),  ((3)&0xFF), True) #D banks disabled M1 PD_bank_select_M1 = 3
            self.sendCommand16( 0x0C,  ((self.d["Motor Config"]["PD_FD_bank3_22bits_M1"].get() >> 8) & 0xFF),  ((self.d["Motor Config"]["PD_FD_bank3_22bits_M1"].get()) & 0xFF), True) #FD I&G bank 3 M1
            self.sendCommand16( 0x12,  ((self.d["Motor Config"]["spike_expansor_M1"].get() >> 8) & 0xFF),  ((self.d["Motor Config"]["spike_expansor_M1"].get()) & 0xFF), True) #spike expansor M1
            self.sendCommand16( 0x13,  (0x00),  ((3)&0xFF), True) #EI bank enabled M1 EI_bank_select_M1 = 3
            self.sendCommand16( 0x17,  ((self.d["Motor Config"]["EI_FD_bank3_18bits_M1"].get() >> 8) & 0xFF),  ((self.d["Motor Config"]["EI_FD_bank3_18bits_M1"].get()) & 0xFF), True) #FD I&G bank 3 M1
            self.sendCommand16( 0x02,  ((scan_Init_Value >> 8) & 0xFF),  ((scan_Init_Value) & 0xFF), True) #Ref M1 0


            logging.info("Time\tM1 Ref\tJ1 Pos\tM2 Ref\tJ2 Pos\tM3 Ref\tJ3 Pos\tM4 Ref\tJ4 Pos\tM5 Ref\tJ5 Pos\tM6 Ref\tJ6 Pos\t")

            start = self.millis_now()
            now = self.millis_now()
            while (abs(now-start) < 1500):
                lap = self.millis_now()
                while(abs(now-lap) < 100):
                    now = self.millis_now()
                logging.info("{}\t,{}\t,{}\t,{}\t,{}\t,{}\t,{}\t,{}\t,{}\t,{}\t,{}\t,{}\t,{}\t".format((self.millis_now()-start),scan_Init_Value,self.Read_J1_pos(),0,self.Read_J2_pos(),0,self.Read_J3_pos(),0,self.Read_J4_pos(),0,self.Read_J5_pos(),0,self.Read_J6_pos()))
                now = self.millis_now()


            for j in range(0,5):
                i = scan_Init_Value
                while(i <= scan_Final_Value):
                    self.sendCommand16( 0x02,  ((i >> 8) & 0xFF),  ((i) & 0xFF), True); #Ref M1 0

                    start2 = self.millis_now()
                    now = self.millis_now()

                    while (abs(now-start2) < scan_Wait_Time):
                        lap = self.millis_now()
                        while((now-lap) < 100):
                            now = self.millis_now()
                        logging.info("{}\t,{}\t,{}\t,{}\t,{}\t,{}\t,{}\t,{}\t,{}\t,{}\t,{}\t,{}\t,{}\t".format((now-start),i,self.Read_J1_pos(),0,self.Read_J2_pos(),0,self.Read_J3_pos(),0,self.Read_J4_pos(),0,self.Read_J5_pos(),0,self.Read_J6_pos()))
                        now = self.millis_now()
                    i = i + scan_Step_Value
                
                i = scan_Final_Value
                while(i>=scan_Init_Value):
                    self.sendCommand16( 0x02,  ((i >> 8) & 0xFF),  ((i) & 0xFF), True); #Ref M1 0


                    start2 = self.millis_now()
                    now = self.millis_now()
                    while (abs(now-start2) < scan_Wait_Time):
                        lap = self.millis_now()
                        while((now-lap) < 100):
                            now = self.millis_now()
                        logging.info("{}\t,{}\t,{}\t,{}\t,{}\t,{}\t,{}\t,{}\t,{}\t,{}\t,{}\t,{}\t,{}\t".format((now-start),i,self.Read_J1_pos(),0,self.Read_J2_pos(),0,self.Read_J3_pos(),0,self.Read_J4_pos(),0,self.Read_J5_pos(),0,self.Read_J6_pos()))
                        now = self.millis_now()
                    
                    i = i - scan_Step_Value
                    
        pass
                      
    def scanMotor2(self):
        '''
        Scan Motor 2

        This function commands the robot to perform 
        the scan procedure defined by the 4 Scan Parameters
        (available in the dictionary as "Scan Parameters")

        These functions (scanMotor1-6) can be used to obtain data
        that can be later be displayed in different graphs
        '''
        if self.dev==None:
            self.alert("There is no opened device. Try opening one first")
            return
        # Convert ms time into clock cycles.
        scan_Init_Value = self.d["Scan Parameters"]["scan_Init_Value"].get()
        scan_Final_Value = self.d["Scan Parameters"]["scan_Final_Value"].get()
        scan_Step_Value = self.d["Scan Parameters"]["scan_Step_Value"].get()
        scan_Wait_Time = self.d["Scan Parameters"]["scan_Wait_Time"].get()

        if self.checked.get():
            
            #Fecha en str, formato: yyyy_MM_dd_HH_mm_ss

            date = datetime.datetime.now()
            timeStamp = date.strftime("%Y_%b_%d_%H_%M_%S")
            #Abrir archivo de log con el nombre de la fecha
            logging.basicConfig(filename='./logs/Scan2_' + timeStamp + '.log',filemode='w')
            logging.info("SMALL ED-Scorbot Joint2 Scan Log file")

            #
            self.sendCommand16( 0x23,  (0x00),  ((3)&0xFF), True) #I banks disabled M2 PI_bank_select_M2 = 3
            self.sendCommand16( 0x27,  ((self.d["Motor Config"]["PI_FD_bank3_18bits_M2"].get() >> 8) & 0xFF),  ((self.d["Motor Config"]["PI_FD_bank3_18bits_M2"].get()) & 0xFF), True) #FD I&G bank 3 M2
            self.sendCommand16( 0x28,  (0x00),  ((3)&0xFF), True) #D banks disabled M2 PD_bank_select_M2 = 3
            self.sendCommand16( 0x2C,  ((self.d["Motor Config"]["PD_FD_bank3_22bits_M2"].get() >> 8) & 0xFF),  ((self.d["Motor Config"]["PD_FD_bank3_22bits_M2"].get()) & 0xFF), True) #FD I&G bank 3 M2
            self.sendCommand16( 0x32,  ((self.d["Motor Config"]["spike_expansor_M2"].get() >> 8) & 0xFF),  ((self.d["Motor Config"]["spike_expansor_M2"].get()) & 0xFF), True) #spike expansor M2
            self.sendCommand16( 0x33,  (0x00),  ((3)&0xFF), True) #EI bank enabled M2 EI_bank_select_M2 = 3
            self.sendCommand16( 0x37,  ((self.d["Motor Config"]["EI_FD_bank3_18bits_M2"].get() >> 8) & 0xFF),  ((self.d["Motor Config"]["EI_FD_bank3_18bits_M2"].get()) & 0xFF), True) #FD I&G bank 3 M2
            self.sendCommand16( 0x22,  ((scan_Init_Value >> 8) & 0xFF),  ((scan_Init_Value) & 0xFF), True) #Ref M2 0


            logging.info("Time\tM2 Ref\tJ1 Pos\tM2 Ref\tJ2 Pos\tM3 Ref\tJ3 Pos\tM4 Ref\tJ4 Pos\tM5 Ref\tJ5 Pos\tM6 Ref\tJ6 Pos\t")

            start = self.millis_now()
            now = self.millis_now()
            while (abs(now-start) < 1500):
                lap = self.millis_now()
                while(abs(now-lap) < 100):
                    now = self.millis_now()
                logging.info("{}\t,{}\t,{}\t,{}\t,{}\t,{}\t,{}\t,{}\t,{}\t,{}\t,{}\t,{}\t,{}\t".format((self.millis_now()-start),scan_Init_Value,self.Read_J1_pos(),0,self.Read_J2_pos(),0,self.Read_J3_pos(),0,self.Read_J4_pos(),0,self.Read_J5_pos(),0,self.Read_J6_pos()))
                now = self.millis_now()


            for j in range(0,5):
                i = scan_Init_Value
                while(i <= scan_Final_Value):
                    self.sendCommand16( 0x22,  ((i >> 8) & 0xFF),  ((i) & 0xFF), True); #Ref M2 0

                    start2 = self.millis_now()
                    now = self.millis_now()

                    while (abs(now-start2) < scan_Wait_Time):
                        lap = self.millis_now()
                        while((now-lap) < 100):
                            now = self.millis_now()
                        logging.info("{}\t,{}\t,{}\t,{}\t,{}\t,{}\t,{}\t,{}\t,{}\t,{}\t,{}\t,{}\t,{}\t".format((now-start),i,self.Read_J1_pos(),0,self.Read_J2_pos(),0,self.Read_J3_pos(),0,self.Read_J4_pos(),0,self.Read_J5_pos(),0,self.Read_J6_pos()))
                        now = self.millis_now()
                    i = i + scan_Step_Value
                
                i = scan_Final_Value
                while(i>=scan_Init_Value):
                    self.sendCommand16( 0x22,  ((i >> 8) & 0xFF),  ((i) & 0xFF), True); #Ref M2 0


                    start2 = self.millis_now()
                    now = self.millis_now()
                    while (abs(now-start2) < scan_Wait_Time):
                        lap = self.millis_now()
                        while((now-lap) < 100):
                            now = self.millis_now()
                        logging.info("{}\t,{}\t,{}\t,{}\t,{}\t,{}\t,{}\t,{}\t,{}\t,{}\t,{}\t,{}\t,{}\t".format((now-start),i,self.Read_J1_pos(),0,self.Read_J2_pos(),0,self.Read_J3_pos(),0,self.Read_J4_pos(),0,self.Read_J5_pos(),0,self.Read_J6_pos()))
                        now = self.millis_now()
                    
                    i = i - scan_Step_Value
                    
        pass
              
    def scanMotor3(self):
        '''
        Scan Motor 3

        This function commands the robot to perform 
        the scan procedure defined by the 4 Scan Parameters
        (available in the dictionary as "Scan Parameters")

        These functions (scanMotor1-6) can be used to obtain data
        that can be later be displayed in different graphs
        '''
        if self.dev==None:
            self.alert("There is no opened device. Try opening one first")
            return
        # Convert ms time into clock cycles.
        scan_Init_Value = self.d["Scan Parameters"]["scan_Init_Value"].get()
        scan_Final_Value = self.d["Scan Parameters"]["scan_Final_Value"].get()
        scan_Step_Value = self.d["Scan Parameters"]["scan_Step_Value"].get()
        scan_Wait_Time = self.d["Scan Parameters"]["scan_Wait_Time"].get()

        if self.checked.get():
            
            #Fecha en str, formato: yyyy_MM_dd_HH_mm_ss

            date = datetime.datetime.now()
            timeStamp = date.strftime("%Y_%b_%d_%H_%M_%S")
            #Abrir archivo de log con el nombre de la fecha
            logging.basicConfig(filename='./logs/Scan3_' + timeStamp + '.log',filemode='w')
            logging.info("SMALL ED-Scorbot Joint3 Scan Log file")

            #
            self.sendCommand16( 0x43,  (0x00),  ((3)&0xFF), True) #I banks disabled M3 PI_bank_select_M3 = 3
            self.sendCommand16( 0x47,  ((self.d["Motor Config"]["PI_FD_bank3_18bits_M3"].get() >> 8) & 0xFF),  ((self.d["Motor Config"]["PI_FD_bank3_18bits_M3"].get()) & 0xFF), True) #FD I&G bank 3 M3
            self.sendCommand16( 0x48,  (0x00),  ((3)&0xFF), True) #D banks disabled M3 PD_bank_select_M3 = 3
            self.sendCommand16( 0x4C,  ((self.d["Motor Config"]["PD_FD_bank3_22bits_M3"].get() >> 8) & 0xFF),  ((self.d["Motor Config"]["PD_FD_bank3_22bits_M3"].get()) & 0xFF), True) #FD I&G bank 3 M3
            self.sendCommand16( 0x52,  ((self.d["Motor Config"]["spike_expansor_M3"].get() >> 8) & 0xFF),  ((self.d["Motor Config"]["spike_expansor_M3"].get()) & 0xFF), True) #spike expansor M3
            self.sendCommand16( 0x53,  (0x00),  ((3)&0xFF), True) #EI bank enabled M3 EI_bank_select_M3 = 3
            self.sendCommand16( 0x57,  ((self.d["Motor Config"]["EI_FD_bank3_18bits_M3"].get() >> 8) & 0xFF),  ((self.d["Motor Config"]["EI_FD_bank3_18bits_M3"].get()) & 0xFF), True) #FD I&G bank 3 M3
            self.sendCommand16( 0x42,  ((scan_Init_Value >> 8) & 0xFF),  ((scan_Init_Value) & 0xFF), True) #Ref M3 0


            logging.info("Time\tM3 Ref\tJ1 Pos\tM3 Ref\tJ2 Pos\tM3 Ref\tJ3 Pos\tM4 Ref\tJ4 Pos\tM5 Ref\tJ5 Pos\tM6 Ref\tJ6 Pos\t")

            start = self.millis_now()
            now = self.millis_now()
            while (abs(now-start) < 1500):
                lap = self.millis_now()
                while(abs(now-lap) < 100):
                    now = self.millis_now()
                logging.info("{}\t,{}\t,{}\t,{}\t,{}\t,{}\t,{}\t,{}\t,{}\t,{}\t,{}\t,{}\t,{}\t".format((self.millis_now()-start),scan_Init_Value,self.Read_J1_pos(),0,self.Read_J2_pos(),0,self.Read_J3_pos(),0,self.Read_J4_pos(),0,self.Read_J5_pos(),0,self.Read_J6_pos()))
                now = self.millis_now()


            for j in range(0,5):
                i = scan_Init_Value
                while(i <= scan_Final_Value):
                    self.sendCommand16( 0x42,  ((i >> 8) & 0xFF),  ((i) & 0xFF), True); #Ref M3 0

                    start2 = self.millis_now()
                    now = self.millis_now()

                    while (abs(now-start2) < scan_Wait_Time):
                        lap = self.millis_now()
                        while((now-lap) < 100):
                            now = self.millis_now()
                        logging.info("{}\t,{}\t,{}\t,{}\t,{}\t,{}\t,{}\t,{}\t,{}\t,{}\t,{}\t,{}\t,{}\t".format((now-start),i,self.Read_J1_pos(),0,self.Read_J2_pos(),0,self.Read_J3_pos(),0,self.Read_J4_pos(),0,self.Read_J5_pos(),0,self.Read_J6_pos()))
                        now = self.millis_now()
                    i = i + scan_Step_Value
                
                i = scan_Final_Value
                while(i>=scan_Init_Value):
                    self.sendCommand16( 0x42,  ((i >> 8) & 0xFF),  ((i) & 0xFF), True); #Ref M3 0


                    start2 = self.millis_now()
                    now = self.millis_now()
                    while (abs(now-start2) < scan_Wait_Time):
                        lap = self.millis_now()
                        while((now-lap) < 100):
                            now = self.millis_now()
                        logging.info("{}\t,{}\t,{}\t,{}\t,{}\t,{}\t,{}\t,{}\t,{}\t,{}\t,{}\t,{}\t,{}\t".format((now-start),i,self.Read_J1_pos(),0,self.Read_J2_pos(),0,self.Read_J3_pos(),0,self.Read_J4_pos(),0,self.Read_J5_pos(),0,self.Read_J6_pos()))
                        now = self.millis_now()
                    
                    i = i - scan_Step_Value
                    
        pass
        
    def scanMotor4(self):
        '''
        Scan Motor 4

        This function commands the robot to perform 
        the scan procedure defined by the 4 Scan Parameters
        (available in the dictionary as "Scan Parameters")

        These functions (scanMotor1-6) can be used to obtain data
        that can be later be displayed in different graphs
        '''
        if self.dev==None:
            self.alert("There is no opened device. Try opening one first")
            return
        # Convert ms time into clock cycles.
        scan_Init_Value = self.d["Scan Parameters"]["scan_Init_Value"].get()
        scan_Final_Value = self.d["Scan Parameters"]["scan_Final_Value"].get()
        scan_Step_Value = self.d["Scan Parameters"]["scan_Step_Value"].get()
        scan_Wait_Time = self.d["Scan Parameters"]["scan_Wait_Time"].get()

        if self.checked.get():
            
            #Fecha en str, formato: yyyy_MM_dd_HH_mm_ss

            date = datetime.datetime.now()
            timeStamp = date.strftime("%Y_%b_%d_%H_%M_%S")
            #Abrir archivo de log con el nombre de la fecha
            logging.basicConfig(filename='./logs/Scan4_' + timeStamp + '.log',filemode='w')
            logging.info("SMALL ED-Scorbot Joint4 Scan Log file")

            #
            self.sendCommand16( 0x63,  (0x00),  ((3)&0xFF), True) #I banks disabled M4 PI_bank_select_M4 = 3
            self.sendCommand16( 0x67,  ((self.d["Motor Config"]["PI_FD_bank3_18bits_M4"].get() >> 8) & 0xFF),  ((self.d["Motor Config"]["PI_FD_bank3_18bits_M4"].get()) & 0xFF), True) #FD I&G bank 3 M4
            self.sendCommand16( 0x68,  (0x00),  ((3)&0xFF), True) #D banks disabled M4 PD_bank_select_M4 = 3
            self.sendCommand16( 0x6C,  ((self.d["Motor Config"]["PD_FD_bank3_22bits_M4"].get() >> 8) & 0xFF),  ((self.d["Motor Config"]["PD_FD_bank3_22bits_M4"].get()) & 0xFF), True) #FD I&G bank 3 M4
            self.sendCommand16( 0x72,  ((self.d["Motor Config"]["spike_expansor_M4"].get() >> 8) & 0xFF),  ((self.d["Motor Config"]["spike_expansor_M4"].get()) & 0xFF), True) #spike expansor M4
            self.sendCommand16( 0x73,  (0x00),  ((3)&0xFF), True) #EI bank enabled M4 EI_bank_select_M4 = 3
            self.sendCommand16( 0x77,  ((self.d["Motor Config"]["EI_FD_bank3_18bits_M4"].get() >> 8) & 0xFF),  ((self.d["Motor Config"]["EI_FD_bank3_18bits_M4"].get()) & 0xFF), True) #FD I&G bank 3 M4
            self.sendCommand16( 0x62,  ((scan_Init_Value >> 8) & 0xFF),  ((scan_Init_Value) & 0xFF), True) #Ref M4 0


            logging.info("Time\tM4 Ref\tJ1 Pos\tM4 Ref\tJ2 Pos\tM4 Ref\tJ3 Pos\tM4 Ref\tJ4 Pos\tM5 Ref\tJ5 Pos\tM6 Ref\tJ6 Pos\t")

            start = self.millis_now()
            now = self.millis_now()
            while (abs(now-start) < 1500):
                lap = self.millis_now()
                while(abs(now-lap) < 100):
                    now = self.millis_now()
                logging.info("{}\t,{}\t,{}\t,{}\t,{}\t,{}\t,{}\t,{}\t,{}\t,{}\t,{}\t,{}\t,{}\t".format((self.millis_now()-start),scan_Init_Value,self.Read_J1_pos(),0,self.Read_J2_pos(),0,self.Read_J3_pos(),0,self.Read_J4_pos(),0,self.Read_J5_pos(),0,self.Read_J6_pos()))
                now = self.millis_now()


            for j in range(0,5):
                i = scan_Init_Value
                while(i <= scan_Final_Value):
                    self.sendCommand16( 0x62,  ((i >> 8) & 0xFF),  ((i) & 0xFF), True); #Ref M4 0

                    start2 = self.millis_now()
                    now = self.millis_now()

                    while (abs(now-start2) < scan_Wait_Time):
                        lap = self.millis_now()
                        while((now-lap) < 100):
                            now = self.millis_now()
                        logging.info("{}\t,{}\t,{}\t,{}\t,{}\t,{}\t,{}\t,{}\t,{}\t,{}\t,{}\t,{}\t,{}\t".format((now-start),i,self.Read_J1_pos(),0,self.Read_J2_pos(),0,self.Read_J3_pos(),0,self.Read_J4_pos(),0,self.Read_J5_pos(),0,self.Read_J6_pos()))
                        now = self.millis_now()
                    i = i + scan_Step_Value
                
                i = scan_Final_Value
                while(i>=scan_Init_Value):
                    self.sendCommand16( 0x62,  ((i >> 8) & 0xFF),  ((i) & 0xFF), True); #Ref M4 0


                    start2 = self.millis_now()
                    now = self.millis_now()
                    while (abs(now-start2) < scan_Wait_Time):
                        lap = self.millis_now()
                        while((now-lap) < 100):
                            now = self.millis_now()
                        logging.info("{}\t,{}\t,{}\t,{}\t,{}\t,{}\t,{}\t,{}\t,{}\t,{}\t,{}\t,{}\t,{}\t".format((now-start),i,self.Read_J1_pos(),0,self.Read_J2_pos(),0,self.Read_J3_pos(),0,self.Read_J4_pos(),0,self.Read_J5_pos(),0,self.Read_J6_pos()))
                        now = self.millis_now()
                    
                    i = i - scan_Step_Value
                    
        pass
      
    def scanMotor5(self):
        '''
        Scan Motor 5

        This function commands the robot to perform 
        the scan procedure defined by the 4 Scan Parameters
        (available in the dictionary as "Scan Parameters")

        These functions (scanMotor1-6) can be used to obtain data
        that can be later be displayed in different graphs
        '''
        if self.dev==None:
            self.alert("There is no opened device. Try opening one first")
            return
        # Convert ms time into clock cycles.
        scan_Init_Value = self.d["Scan Parameters"]["scan_Init_Value"].get()
        scan_Final_Value = self.d["Scan Parameters"]["scan_Final_Value"].get()
        scan_Step_Value = self.d["Scan Parameters"]["scan_Step_Value"].get()
        scan_Wait_Time = self.d["Scan Parameters"]["scan_Wait_Time"].get()

        if self.checked.get():
            
            #Fecha en str, formato: yyyy_MM_dd_HH_mm_ss

            date = datetime.datetime.now()
            timeStamp = date.strftime("%Y_%b_%d_%H_%M_%S")
            #Abrir archivo de log con el nombre de la fecha
            logging.basicConfig(filename='./logs/Scan5_' + timeStamp + '.log',filemode='w')
            logging.info("SMALL ED-Scorbot Joint5 Scan Log file")

            #
            self.sendCommand16( 0x83,  (0x00),  ((3)&0xFF), True) #I banks disabled M5 PI_bank_select_M5 = 3
            self.sendCommand16( 0x87,  ((self.d["Motor Config"]["PI_FD_bank3_18bits_M5"].get() >> 8) & 0xFF),  ((self.d["Motor Config"]["PI_FD_bank3_18bits_M5"].get()) & 0xFF), True) #FD I&G bank 3 M5
            self.sendCommand16( 0x88,  (0x00),  ((3)&0xFF), True) #D banks disabled M5 PD_bank_select_M5 = 3
            self.sendCommand16( 0x8C,  ((self.d["Motor Config"]["PD_FD_bank3_22bits_M5"].get() >> 8) & 0xFF),  ((self.d["Motor Config"]["PD_FD_bank3_22bits_M5"].get()) & 0xFF), True) #FD I&G bank 3 M5
            self.sendCommand16( 0x92,  ((self.d["Motor Config"]["spike_expansor_M5"].get() >> 8) & 0xFF),  ((self.d["Motor Config"]["spike_expansor_M5"].get()) & 0xFF), True) #spike expansor M5
            self.sendCommand16( 0x93,  (0x00),  ((3)&0xFF), True) #EI bank enabled M5 EI_bank_select_M5 = 3
            self.sendCommand16( 0x97,  ((self.d["Motor Config"]["EI_FD_bank3_18bits_M5"].get() >> 8) & 0xFF),  ((self.d["Motor Config"]["EI_FD_bank3_18bits_M5"].get()) & 0xFF), True) #FD I&G bank 3 M5
            self.sendCommand16( 0x82,  ((scan_Init_Value >> 8) & 0xFF),  ((scan_Init_Value) & 0xFF), True) #Ref M5 0


            logging.info("Time\tM5 Ref\tJ1 Pos\tM5 Ref\tJ2 Pos\tM5 Ref\tJ3 Pos\tM5 Ref\tJ4 Pos\tM5 Ref\tJ5 Pos\tM6 Ref\tJ6 Pos\t")

            start = self.millis_now()
            now = self.millis_now()
            while (abs(now-start) < 1500):
                lap = self.millis_now()
                while(abs(now-lap) < 100):
                    now = self.millis_now()
                logging.info("{}\t,{}\t,{}\t,{}\t,{}\t,{}\t,{}\t,{}\t,{}\t,{}\t,{}\t,{}\t,{}\t".format((self.millis_now()-start),scan_Init_Value,self.Read_J1_pos(),0,self.Read_J2_pos(),0,self.Read_J3_pos(),0,self.Read_J4_pos(),0,self.Read_J5_pos(),0,self.Read_J6_pos()))
                now = self.millis_now()


            for j in range(0,5):
                i = scan_Init_Value
                while(i <= scan_Final_Value):
                    self.sendCommand16( 0x82,  ((i >> 8) & 0xFF),  ((i) & 0xFF), True); #Ref M5 0

                    start2 = self.millis_now()
                    now = self.millis_now()

                    while (abs(now-start2) < scan_Wait_Time):
                        lap = self.millis_now()
                        while((now-lap) < 100):
                            now = self.millis_now()
                        logging.info("{}\t,{}\t,{}\t,{}\t,{}\t,{}\t,{}\t,{}\t,{}\t,{}\t,{}\t,{}\t,{}\t".format((now-start),i,self.Read_J1_pos(),0,self.Read_J2_pos(),0,self.Read_J3_pos(),0,self.Read_J4_pos(),0,self.Read_J5_pos(),0,self.Read_J6_pos()))
                        now = self.millis_now()
                    i = i + scan_Step_Value
                
                i = scan_Final_Value
                while(i>=scan_Init_Value):
                    self.sendCommand16( 0x82,  ((i >> 8) & 0xFF),  ((i) & 0xFF), True); #Ref M5 0


                    start2 = self.millis_now()
                    now = self.millis_now()
                    while (abs(now-start2) < scan_Wait_Time):
                        lap = self.millis_now()
                        while((now-lap) < 100):
                            now = self.millis_now()
                        logging.info("{}\t,{}\t,{}\t,{}\t,{}\t,{}\t,{}\t,{}\t,{}\t,{}\t,{}\t,{}\t,{}\t".format((now-start),i,self.Read_J1_pos(),0,self.Read_J2_pos(),0,self.Read_J3_pos(),0,self.Read_J4_pos(),0,self.Read_J5_pos(),0,self.Read_J6_pos()))
                        now = self.millis_now()
                    
                    i = i - scan_Step_Value
                    
        pass
   
    def scanMotor6(self):
        '''
        Scan Motor 2

        This function commands the robot to perform 
        the scan procedure defined by the 4 Scan Parameters
        (available in the dictionary as "Scan Parameters")

        These functions (scanMotor1-6) can be used to obtain data
        that can be later be displayed in different graphs
        '''
        if self.dev==None:
            self.alert("There is no opened device. Try opening one first")
            return
        # Convert ms time into clock cycles.
        scan_Init_Value = self.d["Scan Parameters"]["scan_Init_Value"].get()
        scan_Final_Value = self.d["Scan Parameters"]["scan_Final_Value"].get()
        scan_Step_Value = self.d["Scan Parameters"]["scan_Step_Value"].get()
        scan_Wait_Time = self.d["Scan Parameters"]["scan_Wait_Time"].get()

        if self.checked.get():
            
            #Fecha en str, formato: yyyy_MM_dd_HH_mm_ss

            date = datetime.datetime.now()
            timeStamp = date.strftime("%Y_%b_%d_%H_%M_%S")
            #Abrir archivo de log con el nombre de la fecha
            logging.basicConfig(filename='./logs/Scan6_' + timeStamp + '.log',filemode='w')
            logging.info("SMALL ED-Scorbot Joint6 Scan Log file")

            #
            self.sendCommand16( 0xA3,  (0x00),  ((3)&0xFF), True) #I banks disabled M6 PI_bank_select_M6 = 3
            self.sendCommand16( 0xA7,  ((self.d["Motor Config"]["PI_FD_bank3_18bits_M6"].get() >> 8) & 0xFF),  ((self.d["Motor Config"]["PI_FD_bank3_18bits_M6"].get()) & 0xFF), True) #FD I&G bank 3 M6
            self.sendCommand16( 0xA8,  (0x00),  ((3)&0xFF), True) #D banks disabled M6 PD_bank_select_M6 = 3
            self.sendCommand16( 0xAC,  ((self.d["Motor Config"]["PD_FD_bank3_22bits_M6"].get() >> 8) & 0xFF),  ((self.d["Motor Config"]["PD_FD_bank3_22bits_M6"].get()) & 0xFF), True) #FD I&G bank 3 M6
            self.sendCommand16( 0xB2,  ((self.d["Motor Config"]["spike_expansor_M6"].get() >> 8) & 0xFF),  ((self.d["Motor Config"]["spike_expansor_M6"].get()) & 0xFF), True) #spike expansor M6
            self.sendCommand16( 0xB3,  (0x00),  ((3)&0xFF), True) #EI bank enabled M6 EI_bank_select_M6 = 3
            self.sendCommand16( 0xB7,  ((self.d["Motor Config"]["EI_FD_bank3_18bits_M6"].get() >> 8) & 0xFF),  ((self.d["Motor Config"]["EI_FD_bank3_18bits_M6"].get()) & 0xFF), True) #FD I&G bank 3 M6
            self.sendCommand16( 0xA2,  ((scan_Init_Value >> 8) & 0xFF),  ((scan_Init_Value) & 0xFF), True) #Ref M6 0


            logging.info("Time\tM6 Ref\tJ1 Pos\tM6 Ref\tJ2 Pos\tM6 Ref\tJ3 Pos\tM6 Ref\tJ4 Pos\tM6 Ref\tJ5 Pos\tM6 Ref\tJ6 Pos\t")

            start = self.millis_now()
            now = self.millis_now()
            while (abs(now-start) < 1500):
                lap = self.millis_now()
                while(abs(now-lap) < 100):
                    now = self.millis_now()
                logging.info("{}\t,{}\t,{}\t,{}\t,{}\t,{}\t,{}\t,{}\t,{}\t,{}\t,{}\t,{}\t,{}\t".format((self.millis_now()-start),scan_Init_Value,self.Read_J1_pos(),0,self.Read_J2_pos(),0,self.Read_J3_pos(),0,self.Read_J4_pos(),0,self.Read_J5_pos(),0,self.Read_J6_pos()))
                now = self.millis_now()


            for j in range(0,5):
                i = scan_Init_Value
                while(i <= scan_Final_Value):
                    self.sendCommand16( 0xA2,  ((i >> 8) & 0xFF),  ((i) & 0xFF), True); #Ref M6 0

                    start2 = self.millis_now()
                    now = self.millis_now()

                    while (abs(now-start2) < scan_Wait_Time):
                        lap = self.millis_now()
                        while((now-lap) < 100):
                            now = self.millis_now()
                        logging.info("{}\t,{}\t,{}\t,{}\t,{}\t,{}\t,{}\t,{}\t,{}\t,{}\t,{}\t,{}\t,{}\t".format((now-start),i,self.Read_J1_pos(),0,self.Read_J2_pos(),0,self.Read_J3_pos(),0,self.Read_J4_pos(),0,self.Read_J5_pos(),0,self.Read_J6_pos()))
                        now = self.millis_now()
                    i = i + scan_Step_Value
                
                i = scan_Final_Value
                while(i>=scan_Init_Value):
                    self.sendCommand16( 0xA2,  ((i >> 8) & 0xFF),  ((i) & 0xFF), True); #Ref M6 0


                    start2 = self.millis_now()
                    now = self.millis_now()
                    while (abs(now-start2) < scan_Wait_Time):
                        lap = self.millis_now()
                        while((now-lap) < 100):
                            now = self.millis_now()
                        logging.info("{}\t,{}\t,{}\t,{}\t,{}\t,{}\t,{}\t,{}\t,{}\t,{}\t,{}\t,{}\t,{}\t".format((now-start),i,self.Read_J1_pos(),0,self.Read_J2_pos(),0,self.Read_J3_pos(),0,self.Read_J4_pos(),0,self.Read_J5_pos(),0,self.Read_J6_pos()))
                        now = self.millis_now()
                    
                    i = i - scan_Step_Value
                    
        pass
 
    def Read_J1_pos(self):
        '''
        Read position of the first joint

        This function makes combined use of sendCommand16 and
        readSensor functions to retrieve J1 position

        Returns:
            int: Position of J1
            int: -1 if something went wrong
        '''
        j1_pos = -1
        if self.dev==None:
            self.alert("There is no opened device. Try opening one first")
            return
        
        if self.checked.get():
            sensor_j1 = -1
            for i in range(0,10):
                self.sendCommand16( 0xF1,  (0x00), (0x00), True); 
                self.sendCommand16( 0xF1,  (0x00), (0x00), True); 
                sensor_j1 = self.readSensor(0x01)

                if sensor_j1 > 0:
                    break
            
            j1_pos = sensor_j1

            return j1_pos

    def Read_J2_pos(self):
        '''
        Read position of the second joint

        This function makes combined use of sendCommand16 and
        readSensor functions to retrieve J2 position

        Returns:
            int: Position of J2
            int: -1 if something went wrong
        '''
        j2_pos = -1
        if self.dev==None:
            self.alert("There is no opened device. Try opening one first")
            return
        
        if self.checked.get():
            sensor_j2 = -1
            for i in range(0,10):
                self.sendCommand16( 0xF2,  (0x00), (0x00), True); 
                self.sendCommand16( 0xF2,  (0x00), (0x00), True); 
                sensor_j2 = self.readSensor(0x02)

                if sensor_j2 > 0:
                    break
            
            j2_pos = sensor_j2

            return j2_pos
        
    def Read_J3_pos(self):
        '''
        Read position of the third joint

        This function makes combined use of sendCommand16 and
        readSensor functions to retrieve J3 position

        Returns:
            int: Position of J3
            int: -1 if something went wrong
        '''
        j3_pos = -1
        if self.dev==None:
            self.alert("There is no opened device. Try opening one first")
            return
        
        if self.checked.get():
            sensor_j3 = -1
            for i in range(0,10):
                self.sendCommand16( 0xF3,  (0x00), (0x00), True); 
                self.sendCommand16( 0xF3,  (0x00), (0x00), True); 
                sensor_j3 = self.readSensor(0x03)

                if sensor_j3 > 0:
                    break
            
            j3_pos = sensor_j3

            return j3_pos

    def Read_J4_pos(self):
        '''
        Read position of the fourth joint

        This function makes combined use of sendCommand16 and
        readSensor functions to retrieve J4 position

        Returns:
            int: Position of J4
            int: -1 if something went wrong
        '''
        j4_pos = -1
        if self.dev==None:
            self.alert("There is no opened device. Try opening one first")
            return
        
        if self.checked.get():
            sensor_j4 = -1
            for i in range(0,10):
                self.sendCommand16( 0xF4,  (0x00), (0x00), True); 
                self.sendCommand16( 0xF4,  (0x00), (0x00), True); 
                sensor_j4 = self.readSensor(0x04)

                if sensor_j4 > 0:
                    break
            
            j4_pos = sensor_j4

            return j4_pos

    def Read_J5_pos(self):
        '''
        Read position of the fifth joint

        This function makes combined use of sendCommand16 and
        readSensor functions to retrieve J5 position

        Returns:
            int: Position of J5 or -1 if something went wrong
        '''
        j5_pos = -1
        if self.dev==None:
            self.alert("There is no opened device. Try opening one first")
            return
        
        if self.checked.get():
            sensor_j5 = -1
            for i in range(0,10):
                self.sendCommand16( 0xF5,  (0x00), (0x00), True); 
                self.sendCommand16( 0xF5,  (0x00), (0x00), True); 
                sensor_j5 = self.readSensor(0x05)

                if sensor_j5 > 0:
                    break
            
            j5_pos = sensor_j5

            return j5_pos
    
    def Read_J6_pos(self):
        '''
        Read position of the sixth joint

        This function makes combined use of sendCommand16 and
        readSensor functions to retrieve J6 position

        Returns:
            int: Position of J6
            int: -1 if something went wrong
        '''
        j6_pos = -1
        if self.dev==None:
            self.alert("There is no opened device. Try opening one first")
            return
        
        if self.checked.get():
            sensor_j6 = -1
            for i in range(0,10):
                self.sendCommand16( 0xF6,  (0x00), (0x00), True); 
                self.sendCommand16( 0xF6,  (0x00), (0x00), True); 
                sensor_j6 = self.readSensor(0x06)

                if sensor_j6 > 0:
                    break
            
            j6_pos = sensor_j6

            return j6_pos

    def Reset_J1_pos(self):
        self.sendCommand16( 0xF1,  (0x00),  (0xF1), True)
    
    def Reset_J2_pos(self):
        self.sendCommand16( 0xF2,  (0x00),  (0xF2), True)
    
    def Reset_J3_pos(self):
        self.sendCommand16( 0xF3,  (0x00),  (0xF3), True)
    
    def Reset_J4_pos(self):
        self.sendCommand16( 0xF4,  (0x00),  (0xF4), True)

    def Reset_J5_pos(self):
        self.sendCommand16( 0xF5,  (0x00),  (0xF5), True)
    
    def Reset_J6_pos(self):
        self.sendCommand16( 0xF6,  (0x00),  (0xF6), True)

    def SendFPGAReset(self):
        '''
        Command the FPGA to force an internal reset

        This function tells the FPGA to reset, in order 
        to restore its initial configuration in case
        something is not working properly and we don't 
        know what's going on

        '''
        if self.dev==None:
            self.alert("There is no opened device. Try opening one first")
            return
        else:
            if self.checked.get():
                for i in range(0,2):
                    self.sendCommand16( 0,  (0x00), (0x00), True) #LEDs M1
                    self.sendCommand16( 0x03,  (0x00),  (0x0f), True) #I banks disabled M1
                    self.sendCommand16( 0x08,  (0x00),  (0x0f), True) #d banks disabled M1
                    self.sendCommand16( 0x12,  (0x00),  (0x0), True) #spike expansor M1
                    self.sendCommand16( 0x13,  (0x00),  (0x0f), True) #d banks disabled M1

                    self.sendCommand16( 0x20,  (0x00), (0x00), True) #LEDs M2
                    self.sendCommand16( 0x23,  (0x00),  (0x0f), True) #I banks disabled M1
                    self.sendCommand16( 0x28,  (0x00),  (0x0f), True) #d banks disabled M1
                    self.sendCommand16( 0x32,  (0x00),  (0x0), True) #spike expansor M1
                    self.sendCommand16( 0x33,  (0x00),  (0x0f), True) #d banks disabled M1

                    self.sendCommand16( 0x40,  (0x00), (0x00), True) #LEDs M3
                    self.sendCommand16( 0x43,  (0x00),  (0x0f), True) #I banks disabled M1
                    self.sendCommand16( 0x48,  (0x00),  (0x0f), True) #d banks disabled M1
                    self.sendCommand16( 0x52,  (0x00),  (0x0), True) #spike expansor M1
                    self.sendCommand16( 0x53,  (0x00),  (0x0f), True) #d banks disabled M1

                    self.sendCommand16( 0x60,  (0x00), (0x00), True) #LEDs M4
                    self.sendCommand16( 0x63,  (0x00),  (0x0f), True) #I banks disabled M1
                    self.sendCommand16( 0x68,  (0x00),  (0x0f), True) #d banks disabled M1
                    self.sendCommand16( 0x72,  (0x00),  (0x0), True) #spike expansor M1
                    self.sendCommand16( 0x73,  (0x00),  (0x0f), True) #d banks disabled M1

                    self.sendCommand16( 0x80,  (0x00), (0x00), True) #LEDs M5
                    self.sendCommand16( 0x83,  (0x00),  (0x0f), True) #I banks disabled M1
                    self.sendCommand16( 0x88,  (0x00),  (0x0f), True) #d banks disabled M1
                    self.sendCommand16( 0x92,  (0x00),  (0x0), True) #spike expansor M1
                    self.sendCommand16( 0x93,  (0x00),  (0x0f), True) #d banks disabled M1

                    self.sendCommand16( 0xA0,  (0x00), (0x00), True) #LEDs M6
                    self.sendCommand16( 0xA3,  (0x00),  (0x0f), True) #I banks disabled M1
                    self.sendCommand16( 0xA8,  (0x00),  (0x0f), True) #d banks disabled M1
                    self.sendCommand16( 0xB2,  (0x00),  (0x0), True) #spike expansor M1
                    self.sendCommand16( 0xB3,  (0x00),  (0x0f), True) #d banks disabled M1

                    for i in range(0,2):
                        self.sendCommand16( 0,  (0x00), (0xFF), True) #LEDs M1
                        self.sendCommand16( 0xff,  (0xFF),  (0xFF), True) #FPGA reset
                        self.sendCommand16( 0xfe,  (0xFF),  (0xFF), True) #FPGA reset
                        self.sendCommand16( 0xff,  (0x00),  (0x00), True) #FPGA reset
                        self.sendCommand16( 0xfe,  (0x00),  (0x00), True) #FPGA reset
                    
                    for i in range(0,2):
                        self.SendCommandJoint1(0)
                        self.SendCommandJoint2(0)
                        self.SendCommandJoint3(0)
                        self.SendCommandJoint4(0)
                        self.SendCommandJoint5(0)
                        self.SendCommandJoint6(0)

    def ScanAllMotor(self):
        '''
        Perform scan procedure on all 6 joints

        This function commands the robot to find 
        its base position on all 6 joints at 
        the same time
        '''
        if self.dev==None:
            self.alert("There is no opened device. Try opening one first")
            return
        else:
            scan_Init_Value = self.d["Scan Parameters"]["scan_Init_Value"].get()
            scan_Final_Value = self.d["Scan Parameters"]["scan_Final_Value"].get()
            scan_Step_Value = self.d["Scan Parameters"]["scan_Step_Value"].get()
            scan_Wait_Time = self.d["Scan Parameters"]["scan_Wait_Time"].get()

        if self.checked.get():
            
            #Fecha en str, formato: yyyy_MM_dd_HH_mm_ss

            date = datetime.datetime.now()
            timeStamp = date.strftime("%Y_%b_%d_%H_%M_%S")
            #Abrir archivo de log con el nombre de la fecha
            logging.basicConfig(filename='./logs/ScanAllMotor_' + timeStamp + '.log',filemode='w')
            logging.info("SMALL ED-Scorbot Scan All Motors Log file")

            iSIV = scan_Init_Value
            iSFV = scan_Final_Value
            iSSV = scan_Step_Value

            if scan_Init_Value > 200:
                iSIV = 200
            elif scan_Init_Value < -200:
                iSIV = -200
            
            if scan_Final_Value > 200:
                iSFV = 200
            elif scan_Final_Value < -200:
                iSFV = -200

            if scan_Step_Value > 200:
                iSSV = 200
            elif scan_Step_Value < -200:
                iSSV = -200

            self.sendCommand16( 0x03,  (0x00),  ((3)&0xFF), True) #I banks disabled M1 PI_bank_select_M1 = 3
            self.sendCommand16( 0x07,  ((self.d["Motor Config"]["PI_FD_bank3_18bits_M1"].get() >> 8) & 0xFF),  ((self.d["Motor Config"]["PI_FD_bank3_18bits_M1"].get()) & 0xFF), True) #FD I&G bank 3 M1
            self.sendCommand16( 0x08,  (0x00),  ((3)&0xFF), True) #D banks disabled M1 PD_bank_select_M1 = 3
            self.sendCommand16( 0x0C,  ((self.d["Motor Config"]["PD_FD_bank3_22bits_M1"].get() >> 8) & 0xFF),  ((self.d["Motor Config"]["PD_FD_bank3_22bits_M1"].get()) & 0xFF), True) #FD I&G bank 3 M1
            self.sendCommand16( 0x12,  ((self.d["Motor Config"]["spike_expansor_M1"].get() >> 8) & 0xFF),  ((self.d["Motor Config"]["spike_expansor_M1"].get()) & 0xFF), True) #spike expansor M1
            self.sendCommand16( 0x13,  (0x00),  ((3)&0xFF), True) #EI bank enabled M1 EI_bank_select_M1 = 3
            self.sendCommand16( 0x17,  ((self.d["Motor Config"]["EI_FD_bank3_18bits_M1"].get() >> 8) & 0xFF),  ((self.d["Motor Config"]["EI_FD_bank3_18bits_M1"].get()) & 0xFF), True) #FD I&G bank 3 M1
            self.sendCommand16( 0x02,  ((iSIV >> 8) & 0xFF),  ((iSIV) & 0xFF), True) #Ref M1 0
            
            self.sendCommand16( 0x23,  (0x00),  ((3)&0xFF), True) #I banks disabled M1 PI_bank_select_M2 = 3
            self.sendCommand16( 0x27,  ((self.d["Motor Config"]["PI_FD_bank3_18bits_M2"].get() >> 8) & 0xFF),  ((self.d["Motor Config"]["PI_FD_bank3_18bits_M2"].get()) & 0xFF), True) #FD I&G bank 3 M1
            self.sendCommand16( 0x28,  (0x00),  ((3)&0xFF), True) #D banks disabled M1 PD_bank_select_M2 = 3
            self.sendCommand16( 0x2C,  ((self.d["Motor Config"]["PD_FD_bank3_22bits_M2"].get() >> 8) & 0xFF),  ((self.d["Motor Config"]["PD_FD_bank3_22bits_M2"].get()) & 0xFF), True) #FD I&G bank 3 M1
            self.sendCommand16( 0x32,  ((self.d["Motor Config"]["spike_expansor_M2"].get() >> 8) & 0xFF),  ((self.d["Motor Config"]["spike_expansor_M2"].get()) & 0xFF), True) #spike expansor M1
            self.sendCommand16( 0x33,  (0x00),  ((3)&0xFF), True) #EI bank enabled M1 EI_bank_select_M2 = 3
            self.sendCommand16( 0x37,  ((self.d["Motor Config"]["EI_FD_bank3_18bits_M2"].get() >> 8) & 0xFF),  ((self.d["Motor Config"]["EI_FD_bank3_18bits_M2"].get()) & 0xFF), True) #FD I&G bank 3 M1
            self.sendCommand16( 0x22,  ((iSIV >> 8) & 0xFF),  ((iSIV) & 0xFF), True) #Ref M1 0
            
            self.sendCommand16( 0x43,  (0x00),  ((3)&0xFF), True) #I banks disabled M1 PI_bank_select_M3 = 3
            self.sendCommand16( 0x47,  ((self.d["Motor Config"]["PI_FD_bank3_18bits_M3"].get() >> 8) & 0xFF),  ((self.d["Motor Config"]["PI_FD_bank3_18bits_M3"].get()) & 0xFF), True) #FD I&G bank 3 M1
            self.sendCommand16( 0x48,  (0x00),  ((3)&0xFF), True) #D banks disabled M1 PD_bank_select_M3 = 3
            self.sendCommand16( 0x4C,  ((self.d["Motor Config"]["PD_FD_bank3_22bits_M3"].get() >> 8) & 0xFF),  ((self.d["Motor Config"]["PD_FD_bank3_22bits_M3"].get()) & 0xFF), True) #FD I&G bank 3 M1
            self.sendCommand16( 0x52,  ((self.d["Motor Config"]["spike_expansor_M3"].get() >> 8) & 0xFF),  ((self.d["Motor Config"]["spike_expansor_M3"].get()) & 0xFF), True) #spike expansor M1
            self.sendCommand16( 0x53,  (0x00),  ((3)&0xFF), True) #EI bank enabled M1 EI_bank_select_M2 = 3
            self.sendCommand16( 0x57,  ((self.d["Motor Config"]["EI_FD_bank3_18bits_M3"].get() >> 8) & 0xFF),  ((self.d["Motor Config"]["EI_FD_bank3_18bits_M3"].get()) & 0xFF), True) #FD I&G bank 3 M1
            self.sendCommand16( 0x42,  ((iSIV >> 8) & 0xFF),  ((iSIV) & 0xFF), True) #Ref M1 0
            
            self.sendCommand16( 0x63,  (0x00),  ((3)&0xFF), True) #I banks disabled M4 PI_bank_select_M4 = 3
            self.sendCommand16( 0x67,  ((self.d["Motor Config"]["PI_FD_bank3_18bits_M4"].get() >> 8) & 0xFF),  ((self.d["Motor Config"]["PI_FD_bank3_18bits_M4"].get()) & 0xFF), True) #FD I&G bank 3 M4
            self.sendCommand16( 0x68,  (0x00),  ((3)&0xFF), True) #D banks disabled M4 PD_bank_select_M4 = 3
            self.sendCommand16( 0x6C,  ((self.d["Motor Config"]["PD_FD_bank3_22bits_M4"].get() >> 8) & 0xFF),  ((self.d["Motor Config"]["PD_FD_bank3_22bits_M4"].get()) & 0xFF), True) #FD I&G bank 3 M4
            self.sendCommand16( 0x72,  ((self.d["Motor Config"]["spike_expansor_M4"].get() >> 8) & 0xFF),  ((self.d["Motor Config"]["spike_expansor_M4"].get()) & 0xFF), True) #spike expansor M4
            self.sendCommand16( 0x73,  (0x00),  ((3)&0xFF), True) #EI bank enabled M4 EI_bank_select_M4 = 3
            self.sendCommand16( 0x77,  ((self.d["Motor Config"]["EI_FD_bank3_18bits_M4"].get() >> 8) & 0xFF),  ((self.d["Motor Config"]["EI_FD_bank3_18bits_M4"].get()) & 0xFF), True) #FD I&G bank 3 M4
            self.sendCommand16( 0x62,  ((iSIV >> 8) & 0xFF),  ((iSIV) & 0xFF), True)
            '''
            self.sendCommand16( 0x83,  (0x00),  ((3)&0xFF), True) #I banks disabled M5 PI_bank_select_M5 = 3
            self.sendCommand16( 0x87,  ((self.d["Motor Config"]["PI_FD_bank3_18bits_M5"].get() >> 8) & 0xFF),  ((self.d["Motor Config"]["PI_FD_bank3_18bits_M5"].get()) & 0xFF), True) #FD I&G bank 3 M5
            self.sendCommand16( 0x88,  (0x00),  ((3)&0xFF), True) #D banks disabled M5 PD_bank_select_M5 = 3
            self.sendCommand16( 0x8C,  ((self.d["Motor Config"]["PD_FD_bank3_22bits_M5"].get() >> 8) & 0xFF),  ((self.d["Motor Config"]["PD_FD_bank3_22bits_M5"].get()) & 0xFF), True) #FD I&G bank 3 M5
            self.sendCommand16( 0x92,  ((self.d["Motor Config"]["spike_expansor_M5"].get() >> 8) & 0xFF),  ((self.d["Motor Config"]["spike_expansor_M5"].get()) & 0xFF), True) #spike expansor M5
            self.sendCommand16( 0x93,  (0x00),  ((3)&0xFF), True) #EI bank enabled M5 EI_bank_select_M5 = 3
            self.sendCommand16( 0x97,  ((self.d["Motor Config"]["EI_FD_bank3_18bits_M5"].get() >> 8) & 0xFF),  ((self.d["Motor Config"]["EI_FD_bank3_18bits_M5"].get()) & 0xFF), True) #FD I&G bank 3 M5
            self.sendCommand16( 0x82,  ((iSIV >> 8) & 0xFF),  ((iSIV) & 0xFF), True) #Ref M5 0
            
            self.sendCommand16( 0xA3,  (0x00),  ((3)&0xFF), True) #I banks disabled M6 PI_bank_select_M6 = 3
            self.sendCommand16( 0xA7,  ((self.d["Motor Config"]["PI_FD_bank3_18bits_M6"].get() >> 8) & 0xFF),  ((self.d["Motor Config"]["PI_FD_bank3_18bits_M6"].get()) & 0xFF), True) #FD I&G bank 3 M6
            self.sendCommand16( 0xA8,  (0x00),  ((3)&0xFF), True) #D banks disabled M6 PD_bank_select_M6 = 3
            self.sendCommand16( 0xAC,  ((self.d["Motor Config"]["PD_FD_bank3_22bits_M6"].get() >> 8) & 0xFF),  ((self.d["Motor Config"]["PD_FD_bank3_22bits_M6"].get()) & 0xFF), True) #FD I&G bank 3 M6
            self.sendCommand16( 0xB2,  ((self.d["Motor Config"]["spike_expansor_M6"].get() >> 8) & 0xFF),  ((self.d["Motor Config"]["spike_expansor_M6"].get()) & 0xFF), True) #spike expansor M6
            self.sendCommand16( 0xB3,  (0x00),  ((3)&0xFF), True) #EI bank enabled M6 EI_bank_select_M6 = 3
            self.sendCommand16( 0xB7,  ((self.d["Motor Config"]["EI_FD_bank3_18bits_M6"].get() >> 8) & 0xFF),  ((self.d["Motor Config"]["EI_FD_bank3_18bits_M6"].get()) & 0xFF), True) #FD I&G bank 3 M6
            self.sendCommand16( 0xA2,  ((iSIV >> 8) & 0xFF),  ((iSIV) & 0xFF), True) #Ref M6 0
            '''

            logging.info("Time\tM1 Ref\tJ1 Pos\tM2 Ref\tJ2 Pos\tM3 Ref\tJ3 Pos\tM4 Ref\tJ4 Pos\tM5 Ref\tJ5 Pos\tM6 Ref\tJ6 Pos\t")

            start = self.millis_now()
            now = self.millis_now()

            while(abs(now-start) < 1500):
                lap = self.millis_now()
                while(abs(now-lap) < 100):
                    now = self.millis_now()
                logging.info("{}\t,{}\t,{}\t,{}\t,{}\t,{}\t,{}\t,{}\t,{}\t,{}\t,{}\t,{}\t,{}\t".format((self.millis_now() - start),scan_Init_Value,self.Read_J1_pos(),scan_Init_Value,self.Read_J2_pos(),scan_Init_Value,self.Read_J3_pos(),scan_Init_Value,self.Read_J4_pos(),scan_Init_Value,self.Read_J5_pos(),scan_Init_Value,self.Read_J6_pos()))
                now = self.millis_now()

            for j in range(0,5):
                i = iSIV
                while( i <= iSFV):
                    
                    #self.sendCommand16( 0xA2,  ((i >> 8) & 0xFF),  ((i) & 0xFF), True) #Ref M6 I
                    #self.sendCommand16( 0x82,  ((i >> 8) & 0xFF),  ((i) & 0xFF), True) #Ref M5 I
                    self.sendCommand16( 0x62,  ((i >> 8) & 0xFF),  ((i) & 0xFF), True) #Ref M4 I
                    self.sendCommand16( 0x42,  ((i >> 8) & 0xFF),  ((i) & 0xFF), True) #Ref M3 I
                    self.sendCommand16( 0x22,  ((i >> 8) & 0xFF),  ((i) & 0xFF), True) #Ref M2 I
                    self.sendCommand16( 0x02,  ((i >> 8) & 0xFF),  ((i) & 0xFF), True) #Ref M1 I

                    start2 = self.millis_now()
                    now = self.millis_now()

                    while(abs(now-start2) < scan_Wait_Time):
                        lap = self.millis_now()
                        while(abs(now-lap) < 100):
                            now = self.millis_now()
                        logging.info("{}\t,{}\t,{}\t,{}\t,{}\t,{}\t,{}\t,{}\t,{}\t,{}\t,{}\t,{}\t,{}\t".format((now-start),i,self.Read_J1_pos(),i,self.Read_J2_pos(),i,self.Read_J3_pos(),i,self.Read_J4_pos(),i,self.Read_J5_pos(),i,self.Read_J6_pos()))

                    i = i + iSSV

                i = iSFV
                while(i >= iSIV):
                    
                    #self.sendCommand16( 0xA2,  ((i >> 8) & 0xFF),  ((i) & 0xFF), True) #Ref M6 I
                    #self.sendCommand16( 0x82,  ((i >> 8) & 0xFF),  ((i) & 0xFF), True) #Ref M5 I
                    self.sendCommand16( 0x62,  ((i >> 8) & 0xFF),  ((i) & 0xFF), True) #Ref M4 I
                    self.sendCommand16( 0x42,  ((i >> 8) & 0xFF),  ((i) & 0xFF), True) #Ref M3 I
                    self.sendCommand16( 0x22,  ((i >> 8) & 0xFF),  ((i) & 0xFF), True) #Ref M2 I
                    self.sendCommand16( 0x02,  ((i >> 8) & 0xFF),  ((i) & 0xFF), True) #Ref M1 I

                    start2 = self.millis_now()
                    now = self.millis_now()

                    while(abs(now-start2) < scan_Wait_Time):
                        lap = self.millis_now()
                        while(abs(now-lap) < 100):
                            now = self.millis_now()
                        logging.info("{}\t,{}\t,{}\t,{}\t,{}\t,{}\t,{}\t,{}\t,{}\t,{}\t,{}\t,{}\t,{}\t".format((now-start),i,self.Read_J1_pos(),i,self.Read_J2_pos(),i,self.Read_J3_pos(),i,self.Read_J4_pos(),i,self.Read_J5_pos(),i,self.Read_J6_pos()))
                        now = self.millis_now()
                    
                    i = i - iSSV

    def SetAERIN_ref(self):
        '''
        Not used
        '''
        if self.dev==None:
            self.alert("There is no opened device. Try opening one first")
            return
        else:
            if self.checked.get():
                self.sendCommand16(0xF0,(0xFF),(0xFF), True)
                self.sendCommand16(0xF0,(0xFF),(0xFF), True)
    
    def SetUSBSPI_ref(self):
        '''
        Not used
        '''
        if self.dev==None:
            self.alert("There is no opened device. Try opening one first")
            return
        else:
            if self.checked.get():
                self.sendCommand16(0xF0,(0x00),(0x00), True);
                self.sendCommand16(0xF0,(0x00),(0x00), True)

    def resetUSB(self):
        '''
        Reset USB connection

        This function resets USB connection by closing
        and then reopening the device
        '''
        self.closeUSB()
        self.dev = self.openUSB()
        self.checked.set(True)
        
    def ConfigureLeds(self):
        '''
        Not used
        '''
        if self.dev==None:
            self.alert("There is no opened device. Try opening one first")
            return
        else:
            if self.checked.get():
                self.sendCommand16( 0,  (0x00), ((self.d["Motor Config"]["leds_M1"].get()) & 0xFF), True) #LEDs M1
                self.sendCommand16( 0x20,  (0x00), ((self.d["Motor Config"]["leds_M2"].get()) & 0xFF), True) #LEDs M2
                self.sendCommand16( 0x40,  (0x00), ((self.d["Motor Config"]["leds_M3"].get()) & 0xFF), True) #LEDs M3
                self.sendCommand16( 0x60,  (0x00), ((self.d["Motor Config"]["leds_M4"].get()) & 0xFF), True) #LEDs M4
                self.sendCommand16( 0x80,  (0x00), ((self.d["Motor Config"]["leds_M5"].get()) & 0xFF), True) #LEDs M5
                self.sendCommand16( 0xA0,  (0x00), ((self.d["Motor Config"]["leds_M6"].get()) & 0xFF), True) #LEDs M6

    def SwitchOffLEDS(self):
        '''
        Not used
        '''
        if self.dev==None:
            self.alert("There is no opened device. Try opening one first")
            return
        else:
            if self.checked.get():
                self.sendCommand16( 0,  0,  0, False) #LEDs M1 off
                self.sendCommand16( 0x20,  0,  0, False) #LEDs M2 off
                self.sendCommand16( 0x40,  0,  0, False) #LEDs M3 off
                self.sendCommand16( 0x60,  0,  0, False) #LEDs M4 off
                self.sendCommand16( 0x80,  0,  0, False) #LEDs M5 off
                self.sendCommand16( 0xA0,  0,  0, False) #LEDs M6 off

    def Draw8xy(self):
        '''
        Not used
        '''
        if self.dev==None:
            self.alert("There is no opened device. Try opening one first")
            return
        else:
            if self.checked.get():
                scan_Wait_Time = self.d["Scan Parameters"]["scan_Wait_Time"]
                refsM1 = [0,-200,0,200,0]
                refsM2 = [0,-50,0,-50,0]
                refsM3 = [0, -200,    0, -200,    0]
                refsM4 = [0, -200,    0, -200,    0]

                date = datetime.datetime.now()
                timeStamp = date.strftime("%Y_%b_%d_%H_%M_%S")
                #Abrir archivo de log con el nombre de la fecha
                logging.basicConfig(filename='./logs/Print8xy_' + timeStamp + '.log',filemode='w')
                logging.info("CITEC ED-BioRob Print 8 x,y Log file") #Se usa esta funcion??

                self.sendCommand16( 0x03,  (0x00),  ((3)&0xFF), True) #I banks disabled M1
                self.sendCommand16( 0x07,  ((self.d["Motor Config"]["PI_FD_bank3_18bits_M1"].get() >> 8) & 0xFF),  ((self.d["Motor Config"]["PI_FD_bank3_18bits_M1"].get()) & 0xFF), True) #FD I&G bank 3 M1
                self.sendCommand16( 0x08,  (0x00),  ((3)&0xFF), True) #D banks disabled M1
                self.sendCommand16( 0x0C,  ((self.d["Motor Config"]["PD_FD_bank3_22bits_M1"].get() >> 8) & 0xFF),  ((self.d["Motor Config"]["PD_FD_bank3_22bits_M1"].get()) & 0xFF), True) #FD I&G bank 3 M1
                self.sendCommand16( 0x12,  ((self.d["Motor Config"]["spike_expansor_M1"].get() >> 8) & 0xFF),  ((self.d["Motor Config"]["spike_expansor_M1"].get()) & 0xFF), True) #spike expansor M1
                self.sendCommand16( 0x13,  (0x00),  ((3)&0xFF), True) #EI bank enabled M1
                self.sendCommand16( 0x17,  ((self.d["Motor Config"]["EI_FD_bank3_18bits_M1"].get() >> 8) & 0xFF),  ((self.d["Motor Config"]["EI_FD_bank3_18bits_M1"].get()) & 0xFF), True) #FD I&G bank 3 M1
                self.sendCommand16( 0x02,  ((refsM1[0] >> 8) & 0xFF),  ((refsM1[0]) & 0xFF), True) #Ref M1 0
                
                self.sendCommand16( 0x23,  (0x00),  ((3)&0xFF), True) #I banks disabled M1
                self.sendCommand16( 0x27,  ((self.d["Motor Config"]["PI_FD_bank3_18bits_M2"].get() >> 8) & 0xFF),  ((self.d["Motor Config"]["PI_FD_bank3_18bits_M2"].get()) & 0xFF), True) #FD I&G bank 3 M1
                self.sendCommand16( 0x28,  (0x00),  ((3)&0xFF), True) #D banks disabled M1
                self.sendCommand16( 0x2C,  ((self.d["Motor Config"]["PD_FD_bank3_22bits_M2"].get() >> 8) & 0xFF),  ((self.d["Motor Config"]["PD_FD_bank3_22bits_M2"].get()) & 0xFF), True) #FD I&G bank 3 M1
                self.sendCommand16( 0x32,  ((self.d["Motor Config"]["spike_expansor_M2"].get() >> 8) & 0xFF),  ((self.d["Motor Config"]["spike_expansor_M2"].get()) & 0xFF), True) #spike expansor M1
                self.sendCommand16( 0x33,  (0x00),  ((3)&0xFF), True) #EI bank enabled M1
                self.sendCommand16( 0x37,  ((self.d["Motor Config"]["EI_FD_bank3_18bits_M2"].get() >> 8) & 0xFF),  ((self.d["Motor Config"]["EI_FD_bank3_18bits_M2"].get()) & 0xFF), True) #FD I&G bank 3 M1
                self.sendCommand16( 0x22,  ((refsM2[0] >> 8) & 0xFF),  ((refsM2[0]) & 0xFF), True) #Ref M1 0
                
                self.sendCommand16( 0x43,  (0x00),  ((3)&0xFF), True) #I banks disabled M1
                self.sendCommand16( 0x47,  ((self.d["Motor Config"]["PI_FD_bank3_18bits_M3"].get() >> 8) & 0xFF),  ((self.d["Motor Config"]["PI_FD_bank3_18bits_M3"].get()) & 0xFF), True) #FD I&G bank 3 M1
                self.sendCommand16( 0x48,  (0x00),  ((3)&0xFF), True) #D banks disabled M1
                self.sendCommand16( 0x4C,  ((self.d["Motor Config"]["PD_FD_bank3_22bits_M3"].get() >> 8) & 0xFF),  ((self.d["Motor Config"]["PD_FD_bank3_22bits_M3"].get()) & 0xFF), True) #FD I&G bank 3 M1
                self.sendCommand16( 0x52,  ((self.d["Motor Config"]["spike_expansor_M3"].get() >> 8) & 0xFF),  ((self.d["Motor Config"]["spike_expansor_M3"].get()) & 0xFF), True) #spike expansor M1
                self.sendCommand16( 0x53,  (0x00),  ((3)&0xFF), True) #EI bank enabled M1
                self.sendCommand16( 0x57,  ((self.d["Motor Config"]["EI_FD_bank3_18bits_M3"].get() >> 8) & 0xFF),  ((self.d["Motor Config"]["EI_FD_bank3_18bits_M3"].get()) & 0xFF), True) #FD I&G bank 3 M1
                self.sendCommand16( 0x42,  ((refsM3[0] >> 8) & 0xFF),  ((refsM3[0]) & 0xFF), True) #Ref M1 0
                
                self.sendCommand16( 0x63,  (0x00),  ((3)&0xFF), True) #I banks disabled M4
                self.sendCommand16( 0x67,  ((self.d["Motor Config"]["PI_FD_bank3_18bits_M4"].get() >> 8) & 0xFF),  ((self.d["Motor Config"]["PI_FD_bank3_18bits_M4"].get()) & 0xFF), True) #FD I&G bank 3 M4
                self.sendCommand16( 0x68,  (0x00),  ((3)&0xFF), True) #D banks disabled M4
                self.sendCommand16( 0x6C,  ((self.d["Motor Config"]["PD_FD_bank3_22bits_M4"].get() >> 8) & 0xFF),  ((self.d["Motor Config"]["PD_FD_bank3_22bits_M4"].get()) & 0xFF), True) #FD I&G bank 3 M4
                self.sendCommand16( 0x72,  ((self.d["Motor Config"]["spike_expansor_M4"].get() >> 8) & 0xFF),  ((self.d["Motor Config"]["spike_expansor_M4"].get()) & 0xFF), True) #spike expansor M4
                self.sendCommand16( 0x73,  (0x00),  ((3)&0xFF), True) #EI bank enabled M4
                self.sendCommand16( 0x77,  ((self.d["Motor Config"]["EI_FD_bank3_18bits_M4"].get() >> 8) & 0xFF),  ((self.d["Motor Config"]["EI_FD_bank3_18bits_M4"].get()) & 0xFF), True) #FD I&G bank 3 M4
                self.sendCommand16( 0x62,  ((refsM4[0] >> 8) & 0xFF),  ((refsM4[0]) & 0xFF), True) #Ref M4 0

                logging.info("Time\tM1 Ref\tJ1 Pos\tM2 Ref\tJ2 Pos\tM3 Ref\tJ3 Pos\tM4 Ref\tJ4 Pos\t")
                start = self.millis_now()
                now = self.millis_now()
                
                while(abs(now-start)< 3000):
                    lap = self.millis_now()
                    while(abs(now-lap)<100):
                        now = self.millis_now()
                    logging.info("{}\t,{}\t,{}\t,{}\t,{}\t,{}\t,{}\t,{}\t,{}\t".format((self.millis_now()-start),refsM1[0],self.Read_J1_pos(),refsM2[0],self.Read_J2_pos(),refsM3[0],self.Read_J3_pos(),refsM4[0],self.Read_J4_pos()))
                    now = self.millis_now()
                
                for j in range(0,2):
                    for i in range(0,5):
                        self.sendCommand16( 0x62,  ((refsM4[i] >> 8) & 0xFF),  ((refsM4[i]) & 0xFF), True) #Ref M4 0
                        self.sendCommand16( 0x42,  ((refsM3[i] >> 8) & 0xFF),  ((refsM3[i]) & 0xFF), True) #Ref M4 0
                        self.sendCommand16( 0x22,  ((refsM2[i] >> 8) & 0xFF),  ((refsM2[i]) & 0xFF), True) #Ref M4 0
                        self.sendCommand16( 0x02,  ((refsM1[i] >> 8) & 0xFF),  ((refsM1[i]) & 0xFF), True) #Ref M4 0

                        start2 = self.millis_now()
                        now = self.millis_now()
                        while(abs(now-start2) < scan_Wait_Time):
                            lap = self.millis_now()
                            while(abs(now-lap) < 100):
                                now = self.millis_now()
                            logging.info("{}\t,{}\t,{}\t,{}\t,{}\t,{}\t,{}\t,{}\t,{}\t".format((now-start),refsM1[i],self.Read_J1_pos(),refsM2[i],self.Read_J2_pos(),refsM3[i],self.Read_J3_pos(),refsM4[i],self.Read_J4_pos()))
                            now = self.millis_now()
    
    def search_Joint_home(self,JOINTNUM,pol):
        '''
        Implement the method of searching a joint's home. 
        
        First it moves the joint until it hits one
        of its limits, then progressively moves the 
        joint in the opposite direction until
        the controller receives the home signal
        from the joint

        Args:
            JOINTNUM (int): Number of the joint we want to find home position for
            pol (int): 1 or -1, depending on the joint 
        '''
        if self.dev==None:
            self.alert("There is no opened device. Try opening one first")
            return 
        
        old_sj = 0x20000/4
        sj = 0x20000/4
        addr_j = 0x02
        inc_j = -50*pol

        if JOINTNUM == 1:
            self.SendCommandJoint1(inc_j)
        
        elif JOINTNUM == 2:
            self.SendCommandJoint2(inc_j)
        
        elif JOINTNUM == 3:
            self.SendCommandJoint3(inc_j)

        elif JOINTNUM == 4:
            self.SendCommandJoint4(inc_j)

        elif JOINTNUM == 5:
            self.SendCommandJoint5(inc_j)
        
        elif JOINTNUM == 6:
            self.SendCommandJoint6(inc_j)

        time.sleep(2)

        if JOINTNUM == 1:
            sj = self.Read_J1_pos()
        
        elif JOINTNUM == 2:
            sj = self.Read_J2_pos()
        
        elif JOINTNUM == 3:
            sj = self.Read_J3_pos()

        elif JOINTNUM == 4:
            sj = self.Read_J4_pos()

        elif JOINTNUM == 5:
            sj = self.Read_J5_pos()
        
        elif JOINTNUM == 6:
            sj = self.Read_J6_pos()

        while( abs(sj - old_sj) != 0 ):
            inc_j = inc_j - 50*pol

            if JOINTNUM == 1:
                self.SendCommandJoint1(inc_j)
        
            elif JOINTNUM == 2:
                self.SendCommandJoint2(inc_j)
            
            elif JOINTNUM == 3:
                self.SendCommandJoint3(inc_j)

            elif JOINTNUM == 4:
                self.SendCommandJoint4(inc_j)

            elif JOINTNUM == 5:
                self.SendCommandJoint5(inc_j)
            
            elif JOINTNUM == 6:
                self.SendCommandJoint6(inc_j)

            time.sleep(2)

            old_sj = sj

            if JOINTNUM == 1:
                sj = self.Read_J1_pos()
        
            elif JOINTNUM == 2:
                sj = self.Read_J2_pos()
            
            elif JOINTNUM == 3:
                sj = self.Read_J3_pos()

            elif JOINTNUM == 4:
                sj = self.Read_J4_pos()

            elif JOINTNUM == 5:
                sj = self.Read_J5_pos()
            
            elif JOINTNUM == 6:
                sj = self.Read_J6_pos()
            
            if( abs(sj - old_sj) < 0x5):
                break
            
        self.SendFPGAReset()

        if JOINTNUM == 1:
            self.Reset_J1_pos()
        
        elif JOINTNUM == 2:
            self.Reset_J2_pos()
        
        elif JOINTNUM == 3:
            self.Reset_J3_pos()

        elif JOINTNUM == 4:
            self.Reset_J4_pos()

        elif JOINTNUM == 5:
            self.Reset_J5_pos()
        
        elif JOINTNUM == 6:
            self.Reset_J6_pos()
        
        if JOINTNUM == 1:
            inc_j = 350*pol
            self.SendCommandJoint1(inc_j)
        
        elif JOINTNUM == 2:
            inc_j = 400*pol
            self.SendCommandJoint2(inc_j)
        
        elif JOINTNUM == 3:
            inc_j = 200*pol
            self.SendCommandJoint3(inc_j)

        elif JOINTNUM == 4:
            inc_j = 10*pol
            self.SendCommandJoint4(inc_j)

        elif JOINTNUM == 5:
            self.SendCommandJoint5(inc_j)
        
        elif JOINTNUM == 6:
            self.SendCommandJoint6(inc_j)

        time.sleep(2)

        if JOINTNUM == 1:
            sj = self.Read_J1_pos()
        
        elif JOINTNUM == 2:
            sj = self.Read_J2_pos()
        
        elif JOINTNUM == 3:
            sj = self.Read_J3_pos()

        elif JOINTNUM == 4:
            sj = self.Read_J4_pos()

        elif JOINTNUM == 5:
            sj = self.Read_J5_pos()
        
        elif JOINTNUM == 6:
            sj = self.Read_J6_pos()

        old_sj = sj + 1000

        while( abs(old_sj - sj) > 200):
            old_sj = sj
            if JOINTNUM == 1:
                sj = self.Read_J1_pos()
        
            elif JOINTNUM == 2:
                sj = self.Read_J2_pos()
            
            elif JOINTNUM == 3:
                sj = self.Read_J3_pos()

            elif JOINTNUM == 4:
                sj = self.Read_J4_pos()

            elif JOINTNUM == 5:
                sj = self.Read_J5_pos()
            
            elif JOINTNUM == 6:
                sj = self.Read_J6_pos()

        while(abs(sj - (0x20000/4)) > 0x400):
            inc_j = inc_j + (10*pol)

            if JOINTNUM == 1:
                self.SendCommandJoint1(inc_j)
            
            elif JOINTNUM == 2:
                self.SendCommandJoint2(inc_j)
            
            elif JOINTNUM == 3:
                self.SendCommandJoint3(inc_j)

            elif JOINTNUM == 4:
                self.SendCommandJoint4(inc_j)

            elif JOINTNUM == 5:
                self.SendCommandJoint5(inc_j)
            
            elif JOINTNUM == 6:
                self.SendCommandJoint6(inc_j)

            time.sleep(1.5)

            old_sj = sj

            if JOINTNUM == 1:
                sj = self.Read_J1_pos()
            
            elif JOINTNUM == 2:
                sj = self.Read_J2_pos()
            
            elif JOINTNUM == 3:
                sj = self.Read_J3_pos()

            elif JOINTNUM == 4:
                sj = self.Read_J4_pos()

            elif JOINTNUM == 5:
                sj = self.Read_J5_pos()
            
            elif JOINTNUM == 6:
                sj = self.Read_J6_pos()

            if (abs(sj - (0x20000/4)) < 0x400 and abs(old_sj - sj) > 0x300):
                self.SendFPGAReset()
                self.ConfigureSPID_allJoints()

    def search_Home_J1(self):
        '''
        Search Home position for joint 1

        This function uses search_Joint_home function to 
        search the home position of joint 1
        '''
        
        if self.dev==None:
            self.alert("There is no opened device. Try opening one first")
            return 
    
        self.search_Joint_home(1,1)
    
    def search_Home_J2(self):
        '''
        Search Home position for joint 2

        This function uses search_Joint_home function to 
        search the home position of joint 2
        '''
        if self.dev==None:
            self.alert("There is no opened device. Try opening one first")
            return 
    
        self.search_Joint_home(2,-1)

    def search_Home_J3(self):
        '''
        Search Home position for joint 3

        This function uses search_Joint_home function to 
        search the home position of joint 3
        '''
        if self.dev==None:
            self.alert("There is no opened device. Try opening one first")
            return
    
        self.search_Joint_home(3,-1)

    def search_Home_J4(self):
        '''
        Search Home position for joint 4

        This function uses search_Joint_home function to 
        search the home position of joint 4
        '''
        if self.dev==None:
            self.alert("There is no opened device. Try opening one first")
            return
    
        self.search_Joint_home(4,-1)

    def search_Home_J5(self):
        '''
        Search Home position for joint 5

        This function uses search_Joint_home function to 
        search the home position of joint 5
        '''
        if self.dev==None:
            self.alert("There is no opened device. Try opening one first")
            return 
    
        self.search_Joint_home(5,-1)

    def search_Home_J6(self):
        '''
        Search Home position for joint 6

        This function uses search_Joint_home function to 
        search the home position of joint 6
        '''
        if self.dev==None:
            self.alert("There is no opened device. Try opening one first")
            return 
    
        self.search_Joint_home(6,-1)
    
    def search_Home_all(self):
        '''
        Search Home position for all joints

        This function uses search_Joint_home function to 
        search the home position of all joints

        Be careful: this function won't stop execution until 
        it has completely finished rendering the graphical 
        interface stuck in the process, so bear that in mind when using it
        '''
        if self.dev==None:
            self.alert("There is no opened device. Try opening one first")
            return 
        self.search_Joint_home(1,1)
        self.search_Joint_home(2,-1)
        self.search_Joint_home(3,-1)
        self.search_Joint_home(4,-1)
        self.search_Joint_home(5,-1)
        self.search_Joint_home(6,-1)

    #doGo_Home separado en 6
    def send_Home_J1(self):
        '''
        Send Joint 1 to current home position

        This function uses sendCommand16 to send 
        the first joint to its current home position,
        which is specified by passing '0' as reference
        '''
        if self.dev==None:
            self.alert("There is no opened device. Try opening one first")
            return
        
        self.sendCommand16( 0x03,  (0x00),  ((3)&0xFF), True) #I banks disabled M1 PI_bank_select_M1 = 3
        self.sendCommand16( 0x07,  ((self.d["Motor Config"]["PI_FD_bank3_18bits_M1"].get() >> 8) & 0xFF),  ((self.d["Motor Config"]["PI_FD_bank3_18bits_M1"].get()) & 0xFF), True) #FD I&G bank 3 M1
        self.sendCommand16( 0x08,  (0x00),  ((3)&0xFF), True) #D banks disabled M1 PD_bank_select_M1 = 3
        self.sendCommand16( 0x0C,  ((self.d["Motor Config"]["PD_FD_bank3_22bits_M1"].get() >> 8) & 0xFF),  ((self.d["Motor Config"]["PD_FD_bank3_22bits_M1"].get()) & 0xFF), True) #FD I&G bank 3 M1
        self.sendCommand16( 0x12,  ((self.d["Motor Config"]["spike_expansor_M1"].get() >> 8) & 0xFF),  ((self.d["Motor Config"]["spike_expansor_M1"].get()) & 0xFF), True) #spike expansor M1
        self.sendCommand16( 0x13,  (0x00),  ((3)&0xFF), True) #EI bank enabled M1 EI_bank_select_M1 = 3
        self.sendCommand16( 0x17,  ((self.d["Motor Config"]["EI_FD_bank3_18bits_M1"].get() >> 8) & 0xFF),  ((self.d["Motor Config"]["EI_FD_bank3_18bits_M1"].get()) & 0xFF), True) #FD I&G bank 3 M1
        self.sendCommand16( 0x02,  (0),  (0), True) #Ref M1 0

        #Go to home position
        self.sendCommand16( 0x02, (( 0 >> 8) & 0xFF),((0) & 0xFF), True) # Ref M1 0


        pass

    def send_Home_J2(self):
        '''
        Send Joint 2 to current home position

        This function uses sendCommand16 to send 
        the second joint to its current home position,
        which is specified by passing '0' as reference
        '''
        if self.dev==None:
            self.alert("There is no opened device. Try opening one first")
            return
        
        self.sendCommand16( 0x23,  (0x00),  ((3)&0xFF), True) #I banks disabled M2 PI_bank_select_M2 = 3
        self.sendCommand16( 0x27,  ((self.d["Motor Config"]["PI_FD_bank3_18bits_M2"].get() >> 8) & 0xFF),  ((self.d["Motor Config"]["PI_FD_bank3_18bits_M2"].get()) & 0xFF), True) #FD I&G bank 3 M2
        self.sendCommand16( 0x28,  (0x00),  ((3)&0xFF), True) #D banks disabled M2 PD_bank_select_M2 = 3
        self.sendCommand16( 0x2C,  ((self.d["Motor Config"]["PD_FD_bank3_22bits_M2"].get() >> 8) & 0xFF),  ((self.d["Motor Config"]["PD_FD_bank3_22bits_M2"].get()) & 0xFF), True) #FD I&G bank 3 M2
        self.sendCommand16( 0x32,  ((self.d["Motor Config"]["spike_expansor_M2"].get() >> 8) & 0xFF),  ((self.d["Motor Config"]["spike_expansor_M2"].get()) & 0xFF), True) #spike expansor M2
        self.sendCommand16( 0x33,  (0x00),  ((3)&0xFF), True) #EI bank enabled M2 EI_bank_select_M2 = 3
        self.sendCommand16( 0x37,  ((self.d["Motor Config"]["EI_FD_bank3_18bits_M2"].get() >> 8) & 0xFF),  ((self.d["Motor Config"]["EI_FD_bank3_18bits_M2"].get()) & 0xFF), True) #FD I&G bank 3 M2
        self.sendCommand16( 0x22,  (0),  (0), True) #Ref M2 0

        #Go to home position
        self.sendCommand16( 0x22, (( 0 >> 8) & 0xFF),((0) & 0xFF), True) # Ref M2 0

        pass

    def send_Home_J3(self):
        '''
        Send Joint 3 to current home position

        This function uses sendCommand16 to send 
        the third joint to its current home position,
        which is specified by passing '0' as reference
        '''
        if self.dev==None:
            self.alert("There is no opened device. Try opening one first")
            return
        
        self.sendCommand16( 0x43,  (0x00),  ((3)&0xFF), True) #I banks disabled M3 PI_bank_select_M3 = 3
        self.sendCommand16( 0x47,  ((self.d["Motor Config"]["PI_FD_bank3_18bits_M3"].get() >> 8) & 0xFF),  ((self.d["Motor Config"]["PI_FD_bank3_18bits_M3"].get()) & 0xFF), True) #FD I&G bank 3 M3
        self.sendCommand16( 0x48,  (0x00),  ((3)&0xFF), True) #D banks disabled M3 PD_bank_select_M3 = 3
        self.sendCommand16( 0x4C,  ((self.d["Motor Config"]["PD_FD_bank3_22bits_M3"].get() >> 8) & 0xFF),  ((self.d["Motor Config"]["PD_FD_bank3_22bits_M3"].get()) & 0xFF), True) #FD I&G bank 3 M3
        self.sendCommand16( 0x52,  ((self.d["Motor Config"]["spike_expansor_M3"].get() >> 8) & 0xFF),  ((self.d["Motor Config"]["spike_expansor_M3"].get()) & 0xFF), True) #spike expansor M3
        self.sendCommand16( 0x53,  (0x00),  ((3)&0xFF), True) #EI bank enabled M3 EI_bank_select_M3 = 3
        self.sendCommand16( 0x57,  ((self.d["Motor Config"]["EI_FD_bank3_18bits_M3"].get() >> 8) & 0xFF),  ((self.d["Motor Config"]["EI_FD_bank3_18bits_M3"].get()) & 0xFF), True) #FD I&G bank 3 M3
        self.sendCommand16( 0x42,  (0),  (0), True) #Ref M3 0

        #Go to home position
        self.sendCommand16( 0x42, (( 0 >> 8) & 0xFF),((0) & 0xFF), True) # Ref M3 0

        pass

    def send_Home_J4(self):
        '''
        Send Joint 4 to current home position

        This function uses sendCommand16 to send 
        the fourth joint to its current home position,
        which is specified by passing '0' as reference
        '''
        if self.dev==None:
            self.alert("There is no opened device. Try opening one first")
            return
        
        self.sendCommand16( 0x63,  (0x00),  ((3)&0xFF), True) #I banks disabled M4 PI_bank_select_M4 = 3
        self.sendCommand16( 0x67,  ((self.d["Motor Config"]["PI_FD_bank3_18bits_M4"].get() >> 8) & 0xFF),  ((self.d["Motor Config"]["PI_FD_bank3_18bits_M4"].get()) & 0xFF), True) #FD I&G bank 3 M4
        self.sendCommand16( 0x68,  (0x00),  ((3)&0xFF), True) #D banks disabled M4 PD_bank_select_M4 = 3
        self.sendCommand16( 0x6C,  ((self.d["Motor Config"]["PD_FD_bank3_22bits_M4"].get() >> 8) & 0xFF),  ((self.d["Motor Config"]["PD_FD_bank3_22bits_M4"].get()) & 0xFF), True) #FD I&G bank 3 M4
        self.sendCommand16( 0x72,  ((self.d["Motor Config"]["spike_expansor_M4"].get() >> 8) & 0xFF),  ((self.d["Motor Config"]["spike_expansor_M4"].get()) & 0xFF), True) #spike expansor M4
        self.sendCommand16( 0x73,  (0x00),  ((3)&0xFF), True) #EI bank enabled M4 EI_bank_select_M4 = 3
        self.sendCommand16( 0x77,  ((self.d["Motor Config"]["EI_FD_bank3_18bits_M4"].get() >> 8) & 0xFF),  ((self.d["Motor Config"]["EI_FD_bank3_18bits_M4"].get()) & 0xFF), True) #FD I&G bank 3 M4
        self.sendCommand16( 0x62,  (0),  (0), True) #Ref M4 0

        #Go to home position
        self.sendCommand16( 0x62, (( 0 >> 8) & 0xFF),((0) & 0xFF), True) # Ref M4 0
        
        pass
        
    def send_Home_J5(self):
        '''
        Send Joint 5 to current home position

        This function uses sendCommand16 to send 
        the fifth joint to its current home position,
        which is specified by passing '0' as reference
        '''
        if self.dev==None:
            self.alert("There is no opened device. Try opening one first")
            return
        
        self.sendCommand16( 0x83,  (0x00),  ((3)&0xFF), True) #I banks disabled M5 PI_bank_select_M5 = 3
        self.sendCommand16( 0x87,  ((self.d["Motor Config"]["PI_FD_bank3_18bits_M5"].get() >> 8) & 0xFF),  ((self.d["Motor Config"]["PI_FD_bank3_18bits_M5"].get()) & 0xFF), True) #FD I&G bank 3 M5
        self.sendCommand16( 0x88,  (0x00),  ((3)&0xFF), True) #D banks disabled M5 PD_bank_select_M5 = 3
        self.sendCommand16( 0x8C,  ((self.d["Motor Config"]["PD_FD_bank3_22bits_M5"].get() >> 8) & 0xFF),  ((self.d["Motor Config"]["PD_FD_bank3_22bits_M5"].get()) & 0xFF), True) #FD I&G bank 3 M5
        self.sendCommand16( 0x92,  ((self.d["Motor Config"]["spike_expansor_M5"].get() >> 8) & 0xFF),  ((self.d["Motor Config"]["spike_expansor_M5"].get()) & 0xFF), True) #spike expansor M5
        self.sendCommand16( 0x93,  (0x00),  ((3)&0xFF), True) #EI bank enabled M5 EI_bank_select_M5 = 3
        self.sendCommand16( 0x97,  ((self.d["Motor Config"]["EI_FD_bank3_18bits_M5"].get() >> 8) & 0xFF),  ((self.d["Motor Config"]["EI_FD_bank3_18bits_M5"].get()) & 0xFF), True) #FD I&G bank 3 M5
        self.sendCommand16( 0x82,  (0),  (0), True) #Ref M5 0

        #Go to home position
        self.sendCommand16( 0x82, (( 0 >> 8) & 0xFF),((0) & 0xFF), True) # Ref M5 0

        pass

    def send_Home_J6(self):
        '''
        Send Joint 6 to current home position

        This function uses sendCommand16 to send 
        the sixth joint to its current home position,
        which is specified by passing '0' as reference
        '''
        if self.dev==None:
            self.alert("There is no opened device. Try opening one first")
            return
        
        self.sendCommand16( 0xA3,  (0x00),  ((3)&0xFF), True) #I banks disabled M6 PI_bank_select_M6 = 3
        self.sendCommand16( 0xA7,  ((self.d["Motor Config"]["PI_FD_bank3_18bits_M6"].get() >> 8) & 0xFF),  ((self.d["Motor Config"]["PI_FD_bank3_18bits_M6"].get()) & 0xFF), True) #FD I&G bank 3 M6
        self.sendCommand16( 0xA8,  (0x00),  ((3)&0xFF), True) #D banks disabled M6 PD_bank_select_M6 = 3
        self.sendCommand16( 0xAC,  ((self.d["Motor Config"]["PD_FD_bank3_22bits_M6"].get() >> 8) & 0xFF),  ((self.d["Motor Config"]["PD_FD_bank3_22bits_M6"].get()) & 0xFF), True) #FD I&G bank 3 M6
        self.sendCommand16( 0xB2,  ((self.d["Motor Config"]["spike_expansor_M6"].get() >> 8) & 0xFF),  ((self.d["Motor Config"]["spike_expansor_M6"].get()) & 0xFF), True) #spike expansor M6
        self.sendCommand16( 0xB3,  (0x00),  ((3)&0xFF), True) #EI bank enabled M6 EI_bank_select_M6 = 3
        self.sendCommand16( 0xB7,  ((self.d["Motor Config"]["EI_FD_bank3_18bits_M6"].get() >> 8) & 0xFF),  ((self.d["Motor Config"]["EI_FD_bank3_18bits_M6"].get()) & 0xFF), True) #FD I&G bank 3 M6
        self.sendCommand16( 0xA2,  (0),  (0), True) #Ref M6 0

        #Go to home position
        self.sendCommand16( 0xA2, (( 0 >> 8) & 0xFF),((0) & 0xFF), True) # Ref M6 0

        pass
    
    #doGo_Home y con todo junto
    def send_Home_all(self):
        '''
        Send Joint 1-6 to current home position

        This function uses sendCommand16 to send 
        all joints to its current home position,
        using send_Home_JX functions, with X 
        being the joint's number
        '''
        if self.dev==None:
            self.alert("There is no opened device. Try opening one first")
            return
        
        self.send_Home_J1()
        self.send_Home_J2()
        self.send_Home_J3()
        self.send_Home_J4()
        self.send_Home_J5()
        self.send_Home_J6()

    def init_config(self):
        '''
        Load initial config

        This function tries to load the initial configuration
        for the program containing all the necessary values
        that make the SPID control work properly. There must be
        an "initial_config.json" file for this to work properly
        and, in case you are missing it, you can download the file
        directly from the latest master branch of the repository 
        '''
        try:
            f = open('./initial_config.json')
            j = json.loads(f.read())

        except FileNotFoundError:
            self.alert("Initial config file missing. Please download initial_config.json from the repository if you want the default configuration")
        try:
            for key in self.d["Motor Config"].keys():
                self.d["Motor Config"][key].set(j["Motor Config"][key])
            
            for key in self.d["Scan Parameters"].keys():
                self.d["Scan Parameters"][key].set(j["Scan Parameters"][key])
            
            return
        #If we cacth a KeyError, the config is invalid, so alert the user and end execution
        except KeyError:
            self.alert("Invalid config file")
            return
    
    def ref_to_angle(self,motor,ref):
        """
        Convert reference of motor to angle

        This function takes a motor and a reference and 
        returns the corresponding angle to said reference
        for that specific motor

        Args:
            motor (int): Number of the motor (1-4)
            ref (int): reference to be converted
        
        Returns:
            int: Angle that corresponds to the reference given for the given motor
        """
        f = lambda x:x

        if motor == 1:
            f = lambda x: (-1/3)*x
        elif motor == 2:
            f = lambda x: (-3/8)*x
        elif motor == 3:
            #To be characterised
            f = lambda x: x
        elif motor == 4:
            f = lambda x:(7/40)*x
        
        return f(ref)
            
    def angle_to_ref(self,motor,angle):
        """
        Convert angle of motor to reference

        This function takes a motor and an angle and 
        returns the corresponding reference to said angle
        for that specific motor

        Args:
            motor (int): Number of the motor (1-4)
            angle (int): angle to be converted
        
        Returns:
            int: Reference that corresponds to the angle given for the given motor
        """
        f = lambda x:x

        if motor == 1:
            f = lambda x: (-3)*x
        elif motor == 2:
            f = lambda x: (-8/3)*x
        elif motor == 3:
            #To be characterised
            f = lambda x: x
        elif motor == 4:
            f = lambda x:(40/7)*x
        
        return f(angle)    
    
# if __name__ == "__main__":

#     config = pyAER()
#     config.render_gui()
    
    
#     pass
