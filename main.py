import tkinter as tk
from tkinter import ttk,messagebox
import usb.core
import usb.util
import json
import copy 
from tkinter import filedialog

class python_aer:

    def __init__(self):
        '''
        Constructor function

        Initializes GUI by creatin the root Tk object

        Sets icon of the app

        Initializes data structures to hold the value of all variables that are displayed

        Sets constants and handles needed for USB connection
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
    
    def alert(self,text):
        '''
        This function creates a messagebox with the text parameter as data

        Useful to alert the user that something has gone wrong

        To indicate successful procedures, please just print to console using print()
        '''
        messagebox.showinfo(message=text)

    def render_motor(self, motor_number, row, col):
        '''
        Function to create the inputs for all 6 motors

        Each variable created is stored in the "Motor Config" dictionary 
        and can be accessed directly using the name that appears on the graphical interface 

        Returns the labelframe in which the inputs are rendered
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
        Function to create joints text entries
        
        These entries are read-only, as they will contain the joints measures read from the encoders
        
        Each variable created is stored in the "Joints" dictionary 
        and can be accessed directly using the name that appears on the graphical interface

        Returns the LabelFrame in which the entries are rendered
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
        This function creates the Scan Parameters inputs

        Each variable created is stored in the "Scan Parameters" dictionary 
        and can be accessed directly using the name that appears on the graphical interface

        Returns the labelframe in which the inputs are rendered
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
        This function creates the buttons that will implement all different usable actions
        '''
        labels = ["ConfigureInit", "ConfigureLeds", "ConfigureSPID", "Draw8xy", "Example", "ScanAllMotor", "ScanMotor1", "ScanMotor2", "ScanMotor3", "ScanMotor4",
                  "ScanMotor5", "ScanMotor6", "Search_Home", "Send_Home", "SendFPGAReset", "SetAERIN_ref", "SetUSBSPI_ref", "SwitchOffLEDS"]
        labelframe = ttk.LabelFrame(self.root, text="Actions")
        labelframe.grid(column=col, row=row, sticky=(
            tk.N, tk.W), padx=5, pady=5)
        
        ttk.Button(labelframe,text="ConfigureInit",command=self.ConfigureInit).grid(column=1,row=1,sticky=(tk.W,tk.E))
        ttk.Button(labelframe,text="ConfigureLeds",command=self.ConfigureInit2).grid(column=2,row=1,sticky=(tk.W,tk.E))
        ttk.Button(labelframe,text="ConfigureSPID",command=self.ConfigureInit2).grid(column=3,row=1,sticky=(tk.W,tk.E))
        ttk.Button(labelframe,text="Draw8xy",command=self.ConfigureInit2).grid(column=1,row=2,sticky=(tk.W,tk.E))
        ttk.Button(labelframe,text="Example",command=self.ConfigureInit2).grid(column=2,row=2,sticky=(tk.W,tk.E))
        ttk.Button(labelframe,text="ScanAllMotor",command=self.ConfigureInit2).grid(column=3,row=2,sticky=(tk.W,tk.E))
        ttk.Button(labelframe,text="ScanMotor1",command=self.ConfigureInit2).grid(column=1,row=3,sticky=(tk.W,tk.E))
        ttk.Button(labelframe,text="ScanMotor2",command=self.ConfigureInit2).grid(column=2,row=3,sticky=(tk.W,tk.E))
        ttk.Button(labelframe,text="ScanMotor3",command=self.ConfigureInit2).grid(column=3,row=3,sticky=(tk.W,tk.E))
        ttk.Button(labelframe,text="ScanMotor4",command=self.ConfigureInit2).grid(column=1,row=4,sticky=(tk.W,tk.E))
        ttk.Button(labelframe,text="ScanMotor5",command=self.ConfigureInit2).grid(column=2,row=4,sticky=(tk.W,tk.E))
        ttk.Button(labelframe,text="ScanMotor6",command=self.ConfigureInit2).grid(column=3,row=4,sticky=(tk.W,tk.E))
        ttk.Button(labelframe,text="Search_Home",command=self.ConfigureInit2).grid(column=1,row=5,sticky=(tk.W,tk.E))
        ttk.Button(labelframe,text="Send_Home",command=self.ConfigureInit2).grid(column=2,row=5,sticky=(tk.W,tk.E))
        ttk.Button(labelframe,text="SendFPGAReset",command=self.ConfigureInit2).grid(column=3,row=5,sticky=(tk.W,tk.E))
        ttk.Button(labelframe,text="SetAERIN_ref",command=self.ConfigureInit2).grid(column=1,row=6,sticky=(tk.W,tk.E))
        ttk.Button(labelframe,text="SetUSBSPI_ref",command=self.ConfigureInit2).grid(column=2,row=6,sticky=(tk.W,tk.E))
        ttk.Button(labelframe,text="SwitchOffLEDS",command=self.ConfigureInit2).grid(column=3,row=6,sticky=(tk.W,tk.E))
        ttk.Button(labelframe,text="DumpConfig",command=self.dumpConfig).grid(column=1,row=7,sticky=(tk.W,tk.E))
        ttk.Button(labelframe,text="LoadConfig",command=self.loadConfig).grid(column=2,row=7,sticky=(tk.W,tk.E))
        ttk.Button(labelframe,text="ResetUSB",command=self.resetUSB).grid(column=3,row=7,sticky=(tk.W,tk.E))

    def render_usbEnable(self,row,col):
        '''
        This function creates the checkbox that enables opening USB devices

        The value of the box is stored in the checked variable available in the class
        '''
        labelframe = ttk.LabelFrame(self.root, text="USB")
        labelframe.grid(column=col, row=row, sticky=(
            tk.N, tk.W), padx=5, pady=5)

        checked = tk.BooleanVar()


        ttk.Checkbutton(labelframe,text="Open device",command=self.checkUSB,variable=checked,onvalue=True,offvalue=False).grid(column=1,row=3,sticky=(tk.W))
        self.checked = checked
    def openUSB(self):
        '''
        This function tries to open a connection with
        the AERNode USB board and claim its interface 
        to initiate communication and returns the connection
        to the device found
        '''
        dev = usb.core.find(idVendor=self.VID,idProduct=self.PID)
            
        #If the device can't be found, tell the user and end execution
        if dev is None:
            self.alert("Device not found, try again or check the connection")
            
        #If the device was found, set configuration to default, claim the 
        #default interface and attach the handler to dev
        else:
            
            dev.set_configuration()
            usb.util.claim_interface(dev,0)
            
            print("Device found and initialized successfully")

            return dev

    def closeUSB(self):
        '''
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
        This function checks wether USB usage has been enabled or not
        by reading the checked variable

        If it has, then tries to connect to AERNode board 
        
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
        
        for key in self.d["Joints"].keys():
            d["Joints"][key] = self.d["Joints"][key].get()
        
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
            
            for key in self.d["Joints"].keys():
                self.d["Joints"][key].set(j["Joints"][key])
            
            for key in self.d["Scan Parameters"].keys():
                self.d["Scan Parameters"][key].set(j["Scan Parameters"][key])
            
            return
        #If we cacth a KeyError, the config is invalid, so alert the user and end execution
        except KeyError:
            self.alert("Invalid config file")
            return
  
    def render_gui(self):
        '''
        This function serves as a top routine for rendering all 
        GUI widgets. It calls each function that renders a component,
        and assign them a place in the top window.

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

        #And call mainloop to display GUI
        self.root.mainloop()

    def ConfigureInit(self):
        
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
                    self.sendCommand16(0x0C, ((self.d["Motor Config"]["PD_FD_bank3_18bits_M1"].get() >> 8) & 0xFF),  ((512) & 0xFF), True) #FD I&G bank 3 M1
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
                    self.sendCommand16( 0x2C,  ((512 >> 8) & 0xFF),  ((512) & 0xFF), True); #FD I&G bank 3 M2
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
                    self.sendCommand16( 0x4C,  ((512 >> 8) & 0xFF),  ((512) & 0xFF), True); #FD I&G bank 3 M3
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
                    self.sendCommand16( 0x6C,  ((512 >> 8) & 0xFF),  ((512) & 0xFF), True); #FD I&G bank 3 M4
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
                    self.sendCommand16( 0x8C,  ((512 >> 8) & 0xFF),  ((512) & 0xFF), True); #FD I&G bank 3 M5
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
                    self.sendCommand16( 0xAC,  ((512 >> 8) & 0xFF),  ((512) & 0xFF), True); #FD I&G bank 3 M6
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
    
    def ConfigureInit2(self):
        
        for key in self.d["Motor Config"].keys():
            self.d["Motor Config"][key].set(45)
        
        for key in self.d["Joints"].keys():
            self.d["Joints"][key].set(45)
        
        for key in self.d["Scan Parameters"].keys():
            self.d["Scan Parameters"][key].set(45)

        return
    def SendCommandJoint1(self,ref):

        self.sendCommand16( 0,  (0x00), ((self.d["Motor Config"]["leds_M1"].get()) & 0xFF), True); #LEDs M1
        self.sendCommand16( 0x03,  (0x00),  ((3)&0xFF), True); #I banks disabled M1
        self.sendCommand16( 0x04,  ((512 >> 8) & 0xFF),  ((512) & 0xFF), True); #FD I&G bank 0 M1
        self.sendCommand16( 0x05,  ((512 >> 8) & 0xFF),  ((512) & 0xFF), True); #FD I&G bank 1 M1
        self.sendCommand16( 0x06,  ((512 >> 8) & 0xFF),  ((512) & 0xFF), True); #FD I&G bank 2 M1
        self.sendCommand16( 0x07,  ((PI_FD_bank3_18bits_M1 >> 8) & 0xFF),  ((PI_FD_bank3_18bits_M1) & 0xFF), True); #FD I&G bank 3 M1
        self.sendCommand16( 0x08,  (0x00),  ((512)&0xFF), True); #D banks disabled M1
        self.sendCommand16( 0x09,  ((512 >> 8) & 0xFF),  ((512) & 0xFF), True); #FD I&G bank 0 M1
        self.sendCommand16( 0x0A,  ((512 >> 8) & 0xFF),  ((512) & 0xFF), True); #FD I&G bank 1 M1
        self.sendCommand16( 0x0B,  ((512 >> 8) & 0xFF),  ((512) & 0xFF), True); #FD I&G bank 2 M1
        self.sendCommand16( 0x0C,  ((512 >> 8) & 0xFF),  ((512) & 0xFF), True); #FD I&G bank 3 M1
        self.sendCommand16( 0x12,  ((SpikeExpansor_M1 >> 8) & 0xFF),  ((SpikeExpansor_M1) & 0xFF), True); #spike expansor M1
        self.sendCommand16( 0x13,  (0x00),  ((EI_bank_select_M1)&0xFF), True); #EI bank enabled M1
        self.sendCommand16( 0x14,  ((EI_FD_bank0_12bits_M1 >> 8) & 0xFF),  ((EI_FD_bank0_12bits_M1) & 0xFF), True); #FD I&G bank 0 M1
        self.sendCommand16( 0x15,  ((EI_FD_bank1_14bits_M1 >> 8) & 0xFF),  ((EI_FD_bank1_14bits_M1) & 0xFF), True); #FD I&G bank 1 M1
        self.sendCommand16( 0x16,  ((EI_FD_bank2_16bits_M1 >> 8) & 0xFF),  ((EI_FD_bank2_16bits_M1) & 0xFF), True); #FD I&G bank 2 M1
        self.sendCommand16( 0x17,  ((EI_FD_bank3_18bits_M1 >> 8) & 0xFF),  ((EI_FD_bank3_18bits_M1) & 0xFF), True); #FD I&G bank 3 M1
        #self.sendCommand16( 0,  0,  0, false); #LEDs M1 off
        self.sendCommand16( 0x02,  ((Ref_M1 >> 8) & 0xFF),  ((Ref_M1) & 0xFF), True); #Ref M1 0
        self.sendCommand16( 0x02,  ((Ref_M1 >> 8) & 0xFF),  ((Ref_M1) & 0xFF), True); #Ref M1 0
        self.sendCommand16( 0x02,  ((Ref_M1 >> 8) & 0xFF),  ((Ref_M1) & 0xFF), True); #Ref M1 0
        pass

    def ConfigureSPID(self):
        if (((self.dev and self.checked.get()) == None) or (self.checked.get() == False)):
            self.alert("No device opened. Try checking USB option first")
            return
        else:
            if self.checked.get():
                for i in range(0,6):
                    self.SendCommandJoint(d["Motor Config"]["ref_M1"].get())

        pass

    def sendCommand16(self, cmd, data1, data2, spiEnable):
        '''
        This function allows to send 2 bytes of data to 
        the AERNode board via USB
        '''

        #Check if USB device is initialized
        if(self.dev == None):
            self.alert("There is no opened device. Try opening one first")
            return
        
        
        else:
            #Allocate data buffer as a byte array
            dataBuffer = bytearray(length=self.PACKET_LENGTH)
            
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


    def SendFPGAReset(self,spiEnable):

        if self.dev==None:
            self.alert("There is no opened device. Try opening one first")
            return
        else:
            dataBuffer = bytearray(length=self.PACKET_LENGTH)
            
    def resetUSB(self):
        '''
        This function resets USB connection by closing
        then reopening the device
        '''
        self.closeUSB()
        self.dev = self.openUSB()
        

if __name__ == "__main__":

    config = python_aer()
    config.render_gui()
    
    
    pass
