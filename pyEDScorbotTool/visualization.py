import pandas
import numpy as np
import pickle as P
import matplotlib.pyplot as plt



def load_pickle(path):
    '''
    Función para cargar datos
    path: ruta a un pkl válido
    Devuelve un dataframe con los contenidos del pkl especificado
    '''
    f = pandas.read_pickle(path)
    df = pandas.DataFrame(f)

    return df

def load_numpy(path):
    '''
    Función para cargar datos
    path: ruta a un pkl válido
    Devuelve un dataframe con los contenidos del pkl especificado
    '''
    f = pandas.DataFrame(np.load(path))
    df = pandas.DataFrame(f)

    return df

def extract_joint_and_timestamp(df):
    '''
    Función para extraer los datos de las columnas del dataframe especificado
    La columna 0 es el j1, la 1 el j2, etc., y la columna 6 son los timestamps
    Se devuelven estos datos
    '''
    j1_data = df.loc[:,0]
    j2_data = df.loc[:,1]
    j3_data = df.loc[:,2]
    j4_data = df.loc[:,3]
    timestamps = df.loc[:,6]
    timestamps = timestamps - timestamps[0]

    return j1_data,j2_data,j3_data,j4_data,timestamps

def separate_ref_and_count(data):
    '''
    Función para separar la posición de un joint y su referencia
    Los datos tienen que venir en la forma:
    array([ref,pos],[ref,pos],...,[ref,pos])
    '''
    count = []
    ref = []
    for sample in data:
       count.append(sample[1])
       ref.append(sample[0])

    return np.array(count), np.array(ref)

def plot_joints_refs_separated(posj1,posj2,posj3,posj4,refj1,refj2,refj3,refj4,timestamps,savefig=None):
    fig = plt.figure(figsize=(20,10))
    plt.plot(timestamps/1000,posj1)
    plt.xlabel('Seconds')
    plt.ylabel('Position')
    plt.grid()
    if savefig != None and type(savefig) ==str:
        fname = savefig + "_j1.jpg"
        plt.savefig(fname)
    plt.show()

    plt.plot(refj1)
    plt.xlabel('Samples')
    plt.ylabel('Position')
    plt.show()

    #plt.plot(out1comm)
    #plt.xlabel('Samples')
    #plt.ylabel('Angles')
    ##plt.savefig('WTA_dynapSE2_scorbot.jpg')
    #plt.show()

    fig = plt.figure(figsize=(20,10))
    plt.plot(timestamps/1000,posj2)
    plt.xlabel('Seconds')
    plt.ylabel('Position')
    plt.grid()
    if savefig != None and type(savefig) ==str:
        fname = savefig + "_j2.jpg"
        plt.savefig(fname)
    plt.show()

    plt.plot(refj2)
    plt.xlabel('Samples')
    plt.ylabel('Reference')
    ##plt.savefig('WTA_dynapSE2_scorbot.jpg')
    plt.show()

    fig = plt.figure(figsize=(20,10))
    plt.plot(timestamps/1000,posj3)
    plt.xlabel('Seconds')
    plt.ylabel('Position')
    plt.grid()
    if savefig != None and type(savefig) ==str:
        fname = savefig + "_j3.jpg"
        plt.savefig(fname)
    plt.show()

    plt.plot(refj3)
    plt.xlabel('Samples')
    plt.ylabel('Reference')
    ##plt.savefig('WTA_dynapSE2_scorbot.jpg')
    plt.show()

    fig = plt.figure(figsize=(20,10))
    plt.plot(timestamps/1000,posj4)
    plt.xlabel('Seconds')
    plt.ylabel('Position')
    plt.grid()
    if savefig != None and type(savefig) ==str:
        fname = savefig + "_j4.jpg"
        plt.savefig(fname)
    plt.show()

    plt.plot(refj4)
    plt.xlabel('Samples')
    plt.ylabel('Reference')
    ##plt.savefig('WTA_dynapSE2_scorbot.jpg')
    plt.show()
def plot_joints_together_without_reference(posj1,posj2,posj3,posj4,timestamps,savefig=None):
    f = plt.figure(figsize=(20,10))
    plt.plot(timestamps/1000,posj1,label='Joint 1')
    plt.plot(timestamps/1000,posj2,label='Joint 2')
    plt.plot(timestamps/1000,posj3,label='Joint 3')
    plt.plot(timestamps/1000,posj4,label='Joint 4')
    plt.legend(loc='best')
    plt.ylabel('Position (angles)')
    plt.xlabel('Time (s)')
    plt.grid()
    if savefig != None and type(savefig) == str:
        fname = savefig + '_all_joints.jpg'
        plt.savefig(fname)
    plt.show()  
    
def plot3d(x,y,z):
    from mpl_toolkits import mplot3d

    # creating an empty canvas
    fig = plt.figure(figsize=(10,10))

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
    #or RGBA
    ax.plot3D(x, y, z,label="Corrected trajectory")
    #ax.plot3D(x2, y2, z2,label="Probe trajectory")
    plt.legend(loc="best")

    # Showing the above plot
    plt.show()
