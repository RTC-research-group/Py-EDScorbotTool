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
        labels = ["EI_FD_bank3_18bits", "PF_FD_bank3_22bits",
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
        ttk.Button(labelframe,text="ConfigureLeds",command=self.ConfigureInit).grid(column=2,row=1,sticky=(tk.W,tk.E))
        ttk.Button(labelframe,text="ConfigureSPID",command=self.ConfigureInit).grid(column=3,row=1,sticky=(tk.W,tk.E))
        ttk.Button(labelframe,text="Draw8xy",command=self.ConfigureInit).grid(column=1,row=2,sticky=(tk.W,tk.E))
        ttk.Button(labelframe,text="Example",command=self.ConfigureInit).grid(column=2,row=2,sticky=(tk.W,tk.E))
        ttk.Button(labelframe,text="ScanAllMotor",command=self.ConfigureInit).grid(column=3,row=2,sticky=(tk.W,tk.E))
        ttk.Button(labelframe,text="ScanMotor1",command=self.ConfigureInit).grid(column=1,row=3,sticky=(tk.W,tk.E))
        ttk.Button(labelframe,text="ScanMotor2",command=self.ConfigureInit).grid(column=2,row=3,sticky=(tk.W,tk.E))
        ttk.Button(labelframe,text="ScanMotor3",command=self.ConfigureInit).grid(column=3,row=3,sticky=(tk.W,tk.E))
        ttk.Button(labelframe,text="ScanMotor4",command=self.ConfigureInit).grid(column=1,row=4,sticky=(tk.W,tk.E))
        ttk.Button(labelframe,text="ScanMotor5",command=self.ConfigureInit).grid(column=2,row=4,sticky=(tk.W,tk.E))
        ttk.Button(labelframe,text="ScanMotor6",command=self.ConfigureInit).grid(column=3,row=4,sticky=(tk.W,tk.E))
        ttk.Button(labelframe,text="Search_Home",command=self.ConfigureInit).grid(column=1,row=5,sticky=(tk.W,tk.E))
        ttk.Button(labelframe,text="Send_Home",command=self.ConfigureInit).grid(column=2,row=5,sticky=(tk.W,tk.E))
        ttk.Button(labelframe,text="SendFPGAReset",command=self.ConfigureInit).grid(column=3,row=5,sticky=(tk.W,tk.E))
        ttk.Button(labelframe,text="SetAERIN_ref",command=self.ConfigureInit).grid(column=1,row=6,sticky=(tk.W,tk.E))
        ttk.Button(labelframe,text="SetUSBSPI_ref",command=self.ConfigureInit).grid(column=2,row=6,sticky=(tk.W,tk.E))
        ttk.Button(labelframe,text="SwitchOffLEDS",command=self.ConfigureInit).grid(column=3,row=6,sticky=(tk.W,tk.E))
        ttk.Button(labelframe,text="DumpConfig",command=self.dumpConfig).grid(column=1,row=7,sticky=(tk.W,tk.E))
        ttk.Button(labelframe,text="LoadConfig",command=self.loadConfig).grid(column=2,row=7,sticky=(tk.W,tk.E))

    def render_usbEnable(self,row,col):
        '''
        This function creates the checkbox that enables opening USB devices

        The value of the box is stored in the checked variable available in the class
        '''
        labelframe = ttk.LabelFrame(self.root, text="USB")
        labelframe.grid(column=col, row=row, sticky=(
            tk.N, tk.W), padx=5, pady=5)

        checked = tk.BooleanVar()


        ttk.Checkbutton(labelframe,text="Open device",command=self.openUSB,variable=checked,onvalue=True,offvalue=False).grid(column=1,row=3,sticky=(tk.W))
        self.checked = checked
    
    def openUSB(self):
        '''
        This function checks wether USB usage has been enabled or not
        by reading the checked variable

        If it has, then tries to connect to AERNode board 
        and claim its interface to initiate communication
        and sets the dev variable to the device found

        If it hasn't, releases the interface claimed and detaches
        the handle that was set previously
        '''
        #Check if USB is enabled
        if self.checked.get() == False:
            #If not, release the interface and detach the device handler
            usb.util.release_interface(self.dev,0)
            self.dev = None
            print("Device disconnected successfully")
            return
        
        else:
            #If USB is enabled, try to connect to AERNode board
            dev = usb.core.find(idVendor=self.VID,idProduct=self.PID)
            
            #If the device can't be found, tell the user and end execution
            if dev is None:
                self.alert("Device not found, try again or check the connection")
            
            #If the device was found, set configuration to default, claim the 
            #default interface and attach the handler to dev
            else:
                
                dev.set_configuration()
                usb.util.claim_interface(dev,0)
                self.dev = dev
                print("Device found and initialized successfully")

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
        
        for key in self.d["Motor Config"].keys():
            self.d["Motor Config"][key].set(45)
        
        for key in self.d["Joints"].keys():
            self.d["Joints"][key].set(45)
        
        for key in self.d["Scan Parameters"].keys():
            self.d["Scan Parameters"][key].set(45)

        return
    
    def ConfigureInit2(self):
        
        for key in self.motorvarlist.keys():
            self.motorvarlist[key].set(45)
        
        for key in self.jointvarlist.keys():
            self.jointvarlist[key].set(45)
        
        for key in self.scanparametervarlist.keys():
            self.scanparametervarlist[key].set(45)

        return
    
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


    def readSensor(self,sensor):

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


            read = self.dev.read(self.ENDPOINT_IN,readBuffer)
            if read==0:
                 print("Failed to receive whole packet")
            
            if readBuffer[34] == sensor:
                sensor_data = (0x0ff & readBuffer[35])*256 + readBuffer[36])
            else:
                sensor_data = -1

            return sensor_data

            
            
              

    def SendFPGAReset(self,spiEnable):

        if self.dev==None:
            self.alert("There is no opened device. Try opening one first")
            return
        else:
            dataBuffer = bytearray(length=self.PACKET_LENGTH)
            

        

if __name__ == "__main__":

    config = python_aer()
    config.render_gui()
    
    pass
