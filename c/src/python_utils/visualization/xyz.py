from argparse import ArgumentParser
import numpy as np
import matplotlib.pyplot as plt


def plot3d(x,y,z,label,title,timestamps=None):

    fig = plt.figure(figsize=(10,10))

    ax = plt.axes(projection='3d')
    ax.set_title(title)
    if type(timestamps) is not type(None):
        ax.plot(x,y,z,timestamps,marker=".",label=label)
    else:
        ax.plot(x,y,z,marker=".",label=label)
    ax.set_xlabel('X', linespacing=4)
    ax.set_ylabel('Y', linespacing=4)
    ax.set_zlabel('Z', linespacing=4)

    ax.set_xlim(-1,1)
    ax.set_ylim(-1,1)
    ax.set_zlim(0,1)

    ax.legend(loc='best')

    plt.show()
        

if __name__== '__main__':
    parser = ArgumentParser()
    parser.add_argument("input_file",type=str,action="store",help="Numpy file with xyz output transformed from EDScorbot execution. Data file can include timestamps")
    parser.add_argument("--output_file","-o",type=str,action="store",help="Name of the output figure",default="3d_out.jpg")
    parser.add_argument("--show","-sh",action="store_true",help="Display figure or not",default=False)
    parser.add_argument("--save","-sv",action="store_true",help="Save figure or not",default=False)
    parser.add_argument("--include_timestamps","-ts",action="store_true",help="Include timestamps in the figure",default=False)
    parser.add_argument("--label","-l",action="store",type=str,help="Label of the data for the plot",default="XYZ data")
    parser.add_argument("--title","-t",action="store",type=str,help="Title of the plot",default="3D Plot")
    args = parser.parse_args()

    input_file = args.input_file
    output_file = args.output_file
    show = args.show
    save = args.save
    include_timestamps = args.include_timestamps
    label = args.label
    title = args.title
    xyz = np.load(input_file,allow_pickle=True)

    if include_timestamps:

        plot3d(xyz[:,0],xyz[:,1],xyz[:,2],label=label,title=title)
        
    else:
        plot3d(xyz[:,0],xyz[:,1],xyz[:,2],label=label,title=title)
        pass
