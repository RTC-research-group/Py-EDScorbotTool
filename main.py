import tkinter as tk
from tkinter import ttk


class python_aer:

    def __init__(self):
        self.root = tk.Tk()
        # self.root.columnconfigure(0, weight=1)
        # self.root.rowconfigure(0, weight=1)
        self.motorvarlist = {}
        self.jointvarlist = {}
        self.scanparametervarlist = {}
        return

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
            self.motorvarlist[labeltext] = var
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
            self.jointvarlist[labeltext] = var

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
            self.scanparametervarlist[labeltext] = var

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
        ttk.Button(labelframe,text="GenerateConfig",command=self.ConfigureInit).grid(column=1,row=7,sticky=(tk.W,tk.E))
        ttk.Button(labelframe,text="LoadConfig",command=self.ConfigureInit).grid(column=2,row=7,sticky=(tk.W,tk.E))
        
        



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

        self.root.mainloop()

    def ConfigureInit(self):
        for key in self.motorvarlist.keys():
            self.motorvarlist[key].set(45)
        
        for key in self.jointvarlist.keys():
            self.jointvarlist[key].set(45)
        
        for key in self.scanparametervarlist.keys():
            self.scanparametervarlist[key].set(45)

        return

if __name__ == "__main__":

    config = python_aer()
    config.render_gui()

    pass
