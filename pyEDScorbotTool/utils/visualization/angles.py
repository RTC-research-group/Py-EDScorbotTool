from argparse import ArgumentParser
import numpy as np
import matplotlib.pyplot as plt


def plotangles(x,label,title,timestamps=None):

    fig = plt.figure(figsize=(10,10))

    
    plt.title(title)
    if type(timestamps) is not type(None):
        plt.plot(timestamps/1000000,x,marker=".",label=label)
        plt.xlabel('Seconds', linespacing=4)
    else:
        plt.plot(x,marker=".",label=label)
        plt.xlabel('Samples', linespacing=4)
    
    plt.ylabel('Angles(º)', linespacing=4)
    plt.legend(loc='best')

    plt.show()
        

if __name__== '__main__':
    parser = ArgumentParser()
    parser.add_argument("input_file",type=str,action="store",help="Numpy file (.npy or pickled) with angles in format (q1,q2,q3,q4) to be visualized")
    parser.add_argument("--output_file","-o",type=str,action="store",help="Name of the output figure",default="angles_out.jpg")
    parser.add_argument("--show","-sh",action="store_true",help="Display figure or not",default=False)
    parser.add_argument("--save","-sv",action="store_true",help="Save figure or not",default=False)
    parser.add_argument("--include_timestamps","-ts",action="store_true",help="Include timestamps in the figure",default=False)
    parser.add_argument("--label","-l",action="store",type=str,help="Label of the data for the plot",default="Angle data")
    parser.add_argument("--title","-t",action="store",type=str,help="Title of the plot",default="Angle Plot")
    args = parser.parse_args()

    input_file = args.input_file
    output_file = args.output_file
    show = args.show
    save = args.save
    include_timestamps = args.include_timestamps
    label = args.label
    title = args.title
    angles = np.load(input_file,allow_pickle=True)

    if include_timestamps:

        plotangles(angles[:,:-1],label=label,title=title,timestamp=angles[:,-1])       
    else:
        plotangles(angles*(180/np.pi),label=label,title=title)       

