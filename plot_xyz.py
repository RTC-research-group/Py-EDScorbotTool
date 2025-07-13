from mpl_toolkits import mplot3d
#from ast import main
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import argparse
from l2l.DirecKinScorbot import DirecKinScorbot
from pyAER import pyEDScorbotTool


def load_numpy(path):
    '''
    Función para cargar datos
    path: ruta a un pkl válido
    Devuelve un dataframe con los contenidos del pkl especificado
    '''
    f = pd.DataFrame(np.load(path))
    df = pd.DataFrame(f)

    return df


def plot3d(x, y, z):


    # creating an empty canvas
    fig = plt.figure(figsize=(10, 10))

    # defining the axes with the projection
    # as 3D so as to plot 3D graphs
    ax = plt.axes(projection="3d")

    # creating a wide range of points x,y,z
    # x1=xyz.loc[:,0]
    # y1=xyz.loc[:,1]
    # z1=xyz.loc[:,2]

    # x2=probe_xyz.loc[:,0]
    # y2=probe_xyz.loc[:,1]
    # z2=probe_xyz.loc[:,2]


    # plotting a 3D line graph with X-coordinate,
    # Y-coordinate and Z-coordinate respectively
    #ax.plot3D(x, y, z, 'red')

    # plotting a scatter plot with X-coordinate,
    # Y-coordinate and Z-coordinate respectively
    # and defining the points color as cividis
    # and defining c as z which basically is a
    # definition of 2D array in which rows are RGB
    # or RGBA
    ax.plot3D(x, y, z, label="Corrected trajectory")
    #ax.plot3D(x2, y2, z2,label="Probe trajectory")
    plt.legend(loc="best")

    # Showing the above plot
    plt.show()


def plot3d_timestamp(x, y, z,ts):


    # creating an empty canvas
    fig = plt.figure(figsize=(10, 10))

    # defining the axes with the projection
    # as 3D so as to plot 3D graphs
    ax = plt.axes(projection="3d")

    # creating a wide range of points x,y,z
    # x1=xyz.loc[:,0]
    # y1=xyz.loc[:,1]
    # z1=xyz.loc[:,2]

    # x2=probe_xyz.loc[:,0]
    # y2=probe_xyz.loc[:,1]
    # z2=probe_xyz.loc[:,2]


    # plotting a 3D line graph with X-coordinate,
    # Y-coordinate and Z-coordinate respectively
    #ax.plot3D(x, y, z, 'red')

    # plotting a scatter plot with X-coordinate,
    # Y-coordinate and Z-coordinate respectively
    # and defining the points color as cividis
    # and defining c as z which basically is a
    # definition of 2D array in which rows are RGB
    # or RGBA
    ax.plot3D(x, y, z, label="Corrected trajectory")
    #ax.plot3D(x2, y2, z2,label="Probe trajectory")
    plt.legend(loc="best")

    # Showing the above plot
    plt.show()


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "file", type=str, help="Trajectory record file in NumPy format")
    args = parser.parse_args()

    cont_data = load_numpy(args.file)

    j1 = pyEDScorbotTool.count_to_angle(1,cont_data[0])
    j2 = pyEDScorbotTool.count_to_angle(2,cont_data[1])
    j3 = pyEDScorbotTool.count_to_angle(3,cont_data[2])
    j4 = pyEDScorbotTool.count_to_angle(4,cont_data[3])
    ts = cont_data[6]

    x, y, z = DirecKinScorbot(j1, j2, j3, j4)
    plot3d(x,y,z)
    pass
