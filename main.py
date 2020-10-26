import tkinter as tk
from tkinter import ttk,messagebox
import usb.core
import usb.util
import json
import copy 
from tkinter import filedialog

class python_aer:

    def __init__(self):
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

        #Set vendor and product id for USB connection
        self.VID = 0x10c4
        self.PID = 0x0000

        #Handle for USB connection
        self.dev = None


        return
    def alert(self,text):
        messagebox.showinfo(message=text)

    
    def render_motor(self, motor_number, row, col):
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

        labelframe = ttk.LabelFrame(self.root, text="USB")
        labelframe.grid(column=col, row=row, sticky=(
            tk.N, tk.W), padx=5, pady=5)

        checked = tk.BooleanVar()


        ttk.Checkbutton(labelframe,text="Open device",command=self.openUSB,variable=checked,onvalue=True,offvalue=False).grid(column=1,row=3,sticky=(tk.W))
        self.checked = checked
    
    def openUSB(self):

        if self.checked.get() == False:
            usb.util.release_interface(self.dev,0)
            self.dev = None
            print("Device disconnected successfully")
            return
        
        else:
            dev = usb.core.find(idVendor=self.VID,idProduct=self.PID)
            if dev is None:
                self.alert("Device not found, try again or check the connection")
            else:
                
                dev.set_configuration()
                usb.util.claim_interface(dev,0)
                self.dev = dev
                print("Device found and initialized successfully")

                

    
    def dumpConfig(self):
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

        
        with open('config.json','w') as f:
            json.dump(d,f)
        
        print("Settings generated: "+str(d))

            
    def loadConfig(self):
       
        filename = filedialog.askopenfile(mode="r")
        obj = filename.read()
        j = json.loads(obj)
        for key in self.d["Motor Config"].keys():
            self.d["Motor Config"][key].set(j["Motor Config"][key])
        
        for key in self.d["Joints"].keys():
            self.d["Joints"][key].set(j["Joints"][key])
        
        for key in self.d["Scan Parameters"].keys():
            self.d["Scan Parameters"][key].set(j["Scan Parameters"][key])

        
        pass
        

    def render_gui(self):

        self.root.title("ATCEDScorbotConfig")
        self.frame_list = []
        i = 1
        for row in range(1, 3):
            for col in range(1, 4):
                frame = self.render_motor(i, row, col)

                i += 1
                self.frame_list.append(frame)
        self.frame_list.append(self.render_joints(3, 1))
        self.frame_list.append(self.render_scan_parameters(3, 2))
        self.render_buttons(3, 3)
        self.render_usbEnable(4,1)

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
        
        if(self.dev == None):
            self.alert("There is no opened device. Try opening one first")
        
        else:
            header = bytearray()
            header.append('A')
            header.append('T')
            header.append('C')
            header.append(0x01)
            header.append(0x02)
            header.append(0x00)
            header.append(0x00)
            header.append(0x00)
            header.append(cmd)
            header.append(0 if spiEnable else 1)

            cfg = self.dev.get_active_configuration()
            intf = cfg[(0,0)]

            ep = usb.util.find_descriptor(intf,custom_match=lambda e: usb.util.endpoint_address == 0x02)
            assert ep is not None
            ep.write(header)
            pass


        

if __name__ == "__main__":

    config = python_aer()
    config.render_gui()
    pass
