from tkinter import EW
from pyAER import pyEDScorbotTool
import argparse

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Launch pyEDScorbotTool")
    parser.add_argument("-c",'--config',type=str,help="Configuration File in json format",default=None)
    parser.add_argument("-s",'--scripting',help="Run in scripting mode (no GUI)",default=False,action="store_true")

    args = parser.parse_args()

    config = pyEDScorbotTool(visible=(not args.scripting))
    config.render_gui()

    pass