# -*- coding: utf-8 -*-
def DirecKinScorbot(q1,q2,q3,q4):
    import numpy as np 
    
    d1=35.8
    a2=30.0
    a3=25.0
    a4=21.2 
    d2=7.5
    a1=5.0
    
    x= np.cos(q1)*(a4*np.cos(q2+q3+q4)+a3*np.cos(q2+q3)+a2*np.cos(q2)+a1)+d2*np.sin(q1)
    y= np.sin(q1)*(a4*np.cos(q2+q3+q4)+a3*np.cos(q2+q3)+a2*np.cos(q2)+a1)+d2*np.cos(q1)
    z= d1-a3*np.sin(q2+q3)-a2*np.sin(q2)-a4*np.sin(q2+q3+q4)
    
    return (x,y,z)