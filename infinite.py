import numpy as np
import matplotlib.pyplot as plt

#Alpha cambia los valores absolutos de los puntos (x,y)
#Alpha mayor -> puntos con coordenadas mayores, la forma se queda igual
def bern_lamniscata(alpha):
    
    t = np.linspace(0, 2*np.pi, num=200)

    x = alpha * np.sqrt(2) * np.cos(t) / (np.sin(t)**2 + 1)
    y = alpha * np.sqrt(2) * np.cos(t) * np.sin(t) / (np.sin(t)**2 + 1)


    plt.plot(x, y)
    plt.show()
    pass

if __name__== '__main__':
    bern_lamniscata(1)
    bern_lamniscata(0.5)
    bern_lamniscata(2)
    bern_lamniscata(5)
    pass