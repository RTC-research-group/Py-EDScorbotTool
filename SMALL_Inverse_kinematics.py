# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %% [markdown]
# # Python code for the Scorbot robotic arm (project SMALL)
# 
# This python script includes the computation of the inverse kinematics for the Scorbot robot. 
# The working principle of this script is to select the wrist position that makes the robot reach the target from above. 
# 
# The notebook has been developped using Python 3
# 
# Most of the cells include markdown cells above to deeply explian its functionality.
# 
# #### Developed by Fernando Perez-Peña (UCA) (fernandoperez.pena@uca.es)
# %% [markdown]
# First, the packages needed are imported

# %%
import numpy as np 
import matplotlib.pyplot as plt
import sympy as sym

# %% [markdown]
# The following cell has to be executed only once since it contains the values of the links and several parameters of the robotic platform. 
# The links of the arm are needed to compute the inverse kinematics problem. 
# Suggestion: If you are going to use the notebook for an specific arm, you can introduce the links (cm) and remove the user input. 

# %%
print ("Introduce the lenghts of the links (cm)\n")
l1 = float(input("Lenght of the first link "))
l2 = float(input("Lenght of the second link "))
l3 = float(input("Lenght of the third link "))
l4 = float(input("Lenght of the fourth link "))
l5 = float(input("Lenght of the fifth link "))

#Include the parameters of the robotic arm. 

# %% [markdown]
# #### Target position 

# %%
px = float(input("Which is the target position (X-axis)? "))
py = float(input("Which is the target position (Y-axis)? "))
pz = float(input("Which is the target position (Z-axis)? "))

# %% [markdown]
# Since we have many possibilities for the position of the wirst, we are going to represent all of them and then, select the one that makes the last link to be as close as possible to 90 degrees. 
# 
# In the output plot of this cell, all the possibilities for the wrist are shown in red. The green line represents the projection of the target. 

# %%
circle1 = plt.Circle((0, 0), l1+l2, fc='None', color='r')
circle2 = plt.Circle((px, py), l3, fc='None', color='b')


fig_wirst_region = plt.figure(figsize=(15, 15), dpi=80)
ax = fig_wirst_region.add_subplot(111)
ax.set_xlim(0,l1+l2+l3)
ax.set_ylim(-2*l3,2*l3)
ax.add_artist(circle1)
ax.add_artist(circle2)
ax.set_yticks(np.arange(-2*l3,2*l3,0.5))
ax.tick_params(labelsize=8) 
ax.grid()


#Now we are going to set the criterion of fixing the wrist the closest to the target position. 

print ("In dotted green you find the line where wx=px and that line goes from (-l3,l3)")
ax.plot([px,px],[-l3,+l3],'g--')

from sympy import *

x,y= symbols('x,y')
#print "If we make wx=px (taking the most vertical solution)"
[y1,y2] = solve([(px-px)**2+(y-py)**2-l3**2],dict=True)
#print y1,y2

#print "If we make wy=py (pushing the last link to be completely horizontal)"
[x1,x2] = solve([(x-px)**2+(py-py)**2-l3**2], dict=True)
#print x1,x2

circle_1 = Eq((x-px)**2+(y-py)**2,l3**2)
circle_2= Eq(x**2+y**2,(l1+l2)**2)
(x,y)=solve([circle_1,circle_2],(x,y))

ax.plot(x[0],x[1],'o')
ax.plot(y[0],y[1],'o')

ax.plot(px,py,'*')

print ("The solution is:")
print (x[0],",",x[1])
print (y[0],",",y[1])

print ("All the points in that curve are valid solutions for (wx,wy)")

a=np.array([x[1]-py],dtype=np.float64)
b=np.array([x[0]-px],dtype=np.float64)

c1=np.arctan2(a,b)#* 180 / np.pi
print (c1* 180 / np.pi)

a=np.array([y[1]-py],dtype=np.float64)
b=np.array([y[0]-px],dtype=np.float64)

c2=np.arctan2(a,b)#* 180 / np.pi
print (c2* 180 / np.pi)


#We set the angle values to positive values so we can then create the incremental array 
if (c1<0): 
    c1=c1+2*np.pi
elif (c2<0):
    c2=c2+2*np.pi

print ("Angles updated according to the anti-clock wise direction")
print (c1* 180 / np.pi)
print (c2* 180 / np.pi)

#Now, c1 and c2 are positive angles (anti clock-wise reference) and we can build the incremental vector of angles. 
if (c1>c2): 
    print ("Since we are only interested in approaching the target from above, we limited the range of theta from %f to 180 degrees"%(c2*180/np.pi))
    theta=np.arange(c2,np.pi,0.0001)
    first_border=c2
    #theta=np.arange(c2,c1,0.001)
else:
    print ("Since we are only interested in approaching the target from above, we limited the range of theta from %f to 180 degrees"%(c1*180/np.pi))
    theta=np.arange(c1,np.pi,0.0001)
    first_border=c1
    #theta=np.arange(c1,c2,0.001)
    
#We give values to the the arch which are posible solutions for the wirst. 
x_=px+l3*np.cos(theta)
y_=py+l3*np.sin(theta)

#To plot, we use a reduced set of angles (for the shake of clarity)
ax.plot(x_,y_,'*')

# %% [markdown]
# Then, the wrist position is selected: 

# %%
print ("Now, we have to set wx=lambda*px and try to maximize the resulting function or minimize the function (1-lamda)")

#theta=np.arange(c1,c2+(2*np.pi),0.0001)
#x_=px+l3*np.cos(theta)
#wx=lm*px
#lm*px = px+l3*np.cos(theta)
#lm=1+(1/px)*(l3*np.cos(theta))
#the function 1-lm = -l3*np.cos(theta)/px
#derivative: l3*np.sin(theta)/px

print ("wx=px+l3cos(theta)")
print ("wx=lambda*px")
print ("lamddapx=px+l3cos(theta)")
print ("lambda=f(theta)=1+(1/px)(l3cos(theta))")
print ("(1-lambda)=g(theta)=-(1/px)(l3cos(theta))")
print ("g'(theta)=l3sin(theta)/px")

fun=(l3*np.sin(theta))/px

aux=abs(fun)
#aux=fun

#print aux
print ("Lambda=",aux.min())

print ("wx=",(1-aux.min())*px)
#This is the maximum value for lambda
lm=1-aux.min()

print "The cos(theta)=",px*(1-lm)/l3
          
theta_selected=np.arccos(px*(1-lm)/l3)
print "The theta is",theta_selected * 180 / np.pi

#We have to check if the theta is included within the range to set the sign of the angle
if ((theta_selected<first_border)):# and (theta_selected>np.pi)) : 
    print "The only solution, to have a right approach to the target is to do it from below"
    theta_selected=-np.arccos(px*(1-lm)/l3)
    
    print "Or using wx=lambdapx, wx=%fpx"%lm
    wx=float(x[0])
    wy=float(x[1])
    
    
else: 
    
    wx=lm*px
    wy=py+l3*np.sin(theta_selected)
    
    
plt.plot(theta,aux,'b--',label="Funct. to min.")
plt.plot(theta,abs(-l3*np.cos(theta)/px),'r--',label="Function to max.")
plt.grid()
plt.legend()

print "wx=",wx
print "wy=",wy

# %% [markdown]
# The constraints are checked

# %%
#The second restriction: 
#print "The second restriction:"
print "Is the following restriction met?"
print "(l1+l2)>=sqrt(wx^2+wy^2)"
print l1+l2,">=",np.sqrt(wx*wx+wy*wy),"\n"

#Check if the wirst position is in the work-space of the robot 
if (l1+l2)<(np.sqrt(wx*wx+wy*wy)):
    print "The wirst is out of the work-space"
    #print "To continue, we are going to change the value of wx by subtracting 1.0 to the original value"
    #wx=wx-1.0

#Computation of the cos(q2)(c3)
c2=(wy*wy+wx*wx-l1*l1-l2*l2)/(2*l1*l2)
print "cos(q2)=",c2
print "If cos has a positivesign, the angle should be on the first or fourth quadrant"
print "If cos has a negative sign, the angle should be on the second or third quadrant\n"

#Computation of the sin(q2)(s3)
#The sign choosen will determine the up or down elbow configuration
s2=-np.sqrt(1-c2*c2)
#Computation of q2    
q2=np.arctan2(s2,c2)

if (q2*180/np.pi)>0 : 
    print"q2[0]=",q2*180/np.pi,"First quadrant","or, which is equivalent:"
    print "q2[1]=",360-q2*180/np.pi, "fourth quadrant"
    
else: 
   
    print "q2[0]=",q2*180/np.pi+360,"fourth quadrant","or, which is equivalent:"
    print "q2[1]=",-q2*180/np.pi,"first quadrant "
    
q2_bis=-q2


# %%
print "We are going to consider q2=%f"%(q2*180/np.pi)
#Computation of the cos(q1)(c1)

c1=(l2*s2*wy+wx*(l1+l2*c2))/(l1*l1+2*l1*l2*c2+l2*l2)
    
print "cos(q1)=",c1
    
#Computation of the sin(q1)(s1)
print "The sign of the sin of q1 could be positive or negative:"
s1=np.sqrt(1-c1*c1)
s1_bis=-np.sqrt(1-c1*c1)
print s1,"or",s1_bis
#Computation of q1
q1=np.arctan2(s1,c1)
q1_bis=np.arctan2(s1_bis,c1)
#To print the angle, uncomment the following line: 
print "So we have two angles sets:"
print "q1=",q1*180/np.pi
print "q2=",q2*180/np.pi
print "---"
print "q1=",q1_bis*180/np.pi
print "q2=",q2*180/np.pi

print "******************************************"

print "We are going to consider q2=%f"%(q2_bis*180/np.pi)
#Computation of the cos(q1)(c1)

c1=(l2*(np.sin(q2_bis))*wy+wx*(l1+l2*c2))/(l1*l1+2*l1*l2*c2+l2*l2)
    
print "cos(q1)=",c1
    
#Computation of the sin(q1)(s1)
print "Here again, the sign of the sin of q1 could be positive or negative:"
s1_1=np.sqrt(1-c1*c1)
s1_1_bis=-np.sqrt(1-c1*c1)
#Computation of q1
q1_1=np.arctan2(s1_1,c1)
q1_1_bis=np.arctan2(s1_1_bis,c1)

print "So we have two angles sets:"
print "q1=",q1_1*180/np.pi
print "q2=",q2_bis*180/np.pi
print "---"
print "q1=",q1_1_bis*180/np.pi
print "q2=",q2_bis*180/np.pi


# %%
print "Now, we are plotting the angles we already have, q1 and q2." 
print "The partial end-effetor should be at the user-defined wrist position"

fig = plt.figure()
ax = fig.add_subplot(111)
ax.plot([0,l1*np.cos(q1),l1*np.cos(q1)+l2*np.cos(q1+q2)],[0,l1*np.sin(q1),l1*np.sin(q1)+l2*np.sin(q1+q2)],'r-o')
ax.plot([0,l1*np.cos(q1_bis),l1*np.cos(q1_bis)+l2*np.cos(q1_bis+q2_bis)],[0,l1*np.sin(q1_bis),l1*np.sin(q1_bis)+l2*np.sin(q1_bis+q2_bis)],'g--o')

ax.plot([0,l1*np.cos(q1_1),l1*np.cos(q1_1)+l2*np.cos(q1_1+q2_bis)],[0,l1*np.sin(q1_1),l1*np.sin(q1_1)+l2*np.sin(q1_1+q2_bis)],'b-o')
ax.plot([0,l1*np.cos(q1_1_bis),l1*np.cos(q1_1_bis)+l2*np.cos(q1_1_bis+q2_bis)],[0,l1*np.sin(q1_1_bis),l1*np.sin(q1_1_bis)+l2*np.sin(q1_1_bis+q2_bis)],'c--o')


ax.grid()


# %%
print "We are going to discard the sets that are not reaching the wrist position"
print "wrist=",(wx,wy)

print "So we have the following angles sets:"
print "q1=",q1*180/np.pi
print "q2=",q2*180/np.pi
print "---"
print "q1=",q1_bis*180/np.pi
print "q2=",q2*180/np.pi
print "---"
print "q1=",q1_1*180/np.pi
print "q2=",q2_bis*180/np.pi
print "---"
print "q1=",q1_1_bis*180/np.pi
print "q2=",q2_bis*180/np.pi

print "To see which of these are reaching the wirst position, we apply direct kinematics"
print "Direct kinematics for a two links arm:"
print "wx=l1*cos(q1)+l2*cos(q1+q2)"
print "wy=l1*sin(q1)+l2*sin(q1+q2)"

#Build arrays for each set 
q1_set=(q1,q1_bis,q1_1,q1_1_bis)
q2_set=(q2,q2,q2_bis,q2_bis)

#for loop to test the direct kinematics
k=0
#We allocate two positions since only two valid configurations are possible (elbow up/down)
q1=np.zeros(2)
q2=np.zeros(2)
for i in range (len(q1_set)):
    print "%d set of angles:"%i
    print (q1_set[i],q2_set[i])
    wx_reached=l1*np.cos(q1_set[i])+l2*np.cos(q1_set[i]+q2_set[i])
    wy_reached=l1*np.sin(q1_set[i])+l2*np.sin(q1_set[i]+q2_set[i])
    print "(wx,wy)=",(wx_reached,wy_reached)
    if ((np.abs(wx_reached-wx)<0.001) and (np.abs(wy_reached-wy)<0.001)):
        print "Selected set"
        q1[k]=q1_set[i]
        q2[k]=q2_set[i]
        k=k+1


# %%
#Calculate the angle phi     

phi=np.arctan2((py-wy),(px-wx))

q3=np.zeros(2)
#To print the angle, uncomment the following line: 
print "phi=",phi*180/np.pi

#Computation of q3
q3[0]=phi-(q2[0]+q1[0])
print "q3[0]=",q3[0]*180/np.pi

q3[1]=phi-(q2[1]+q1[1])
print "q3[1]=",q3[1]*180/np.pi


# %%
fig = plt.figure()
ax = fig.add_subplot(111)
#Using the first set of angles
ax.plot([0,l1*np.cos(q1[0]),l1*np.cos(q1[0])+l2*np.cos(q1[0]+q2[0]),l1*np.cos(q1[0])+l2*np.cos(q1[0]+q2[0])+l3*np.cos(phi)],[0,l1*np.sin(q1[0]),l1*np.sin(q1[0])+l2*np.sin(q1[0]+q2[0]),l1*np.sin(q1[0])+l2*np.sin(q1[0]+q2[0])+l3*np.sin(phi)],'r-o')
    
#Using the second set of angles
ax.plot([0,l1*np.cos(q1[1]),l1*np.cos(q1[1])+l2*np.cos(q1[1]+q2[1]),l1*np.cos(q1[1])+l2*np.cos(q1[1]+q2[1])+l3*np.cos(phi)],[0,l1*np.sin(q1[1]),l1*np.sin(q1[1])+l2*np.sin(q1[1]+q2[1]),l1*np.sin(q1[1])+l2*np.sin(q1[1]+q2[1])+l3*np.sin(phi)],'g--o')
    
ax.plot([0,wx,px],[0,wy,py],'go')
ax.annotate('Wrist', xy=(wx, wy), xytext=(wx-3, wy-3),arrowprops=dict(facecolor='black', shrink=0.05))
ax.annotate('Target', xy=(px, py), xytext=(px-3, py-3),arrowprops=dict(facecolor='black', shrink=0.05))
plt.grid()


# %%
print "First angle set"
print "q1",q1[0]*180/np.pi
print "q2",q2[0]*180/np.pi
print "q3",q3[0]*180/np.pi
print "******************"
print "Second angle set"
print "q1",q1[1]*180/np.pi
print "q2",q2[1]*180/np.pi
print "q3",q3[1]*180/np.pi
print "******************"
#double check of the positions calculated according to the direct kinematics

#Function needed to compute the direct kinematics according to the DH convention. 
def build_matrix(theta,alpha,d,a):
    """This function returns the DH matrix. Arguments are both, theta and alpha angles and both, d and a distances."""
    
    A = np.array([
        [sym.cos(theta), -sym.cos(alpha)*sym.sin(theta),  sym.sin(alpha)*sym.sin(theta), a*sym.cos(theta)],
        [sym.sin(theta),  sym.cos(alpha)*sym.cos(theta), -sym.sin(alpha)*sym.cos(theta), a*sym.sin(theta)],
        [0,              sym.sin(alpha),                sym.cos(alpha),               d              ],
        [0,              0,                            0,                           1              ]
    ])
    return A
    
    
print "We check the direct kinematics to see if the angles are correct (first set):"
l_base=30.0 #assuming 30 cm. 
#in cm
#d1=35.85 #I guess this is l0+d1
d1=5.85 #assuming 5 cm from q1 to q2.  
d2=0.0
d3=0.0
d4=0.0

#in cm
a1=5.0
a2=30.0 
a3=35.0
a4=21.2   # En el manual pone 25.1 pero en nuestro caso no es correcto.

#angles alphai (of DH algorithm -> they are fixed) (degrees)
alpha1=np.deg2rad(-90)
alpha2=np.deg2rad(0)
alpha3=np.deg2rad(0)
alpha4=np.deg2rad(0)

A_1=build_matrix(q1[0],alpha1,d1,a1)
A_2=build_matrix(q2[0],alpha2,d2,a2)
A_3=build_matrix(q3[0],alpha3,d3,a3)
A_4=build_matrix(0,alpha4,d4,a4)

T_1=np.dot(A_1,A_2)
T_2=np.dot(T_1,A_3)
T_3=np.dot(T_2,A_4)

T=T_3
x=T[0,3]
y=T[1,3]
z=T[2,3] #l_base is the distance from the base to the first actuator and must be added. 

print "x=",x
print "y=",y
print "z=",z+l_base

print "We check the direct kinematics to see if the angles are correct (second set):"
A_1=build_matrix(q1[1],alpha1,d1,a1)
A_2=build_matrix(q2[1],alpha2,d2,a2)
A_3=build_matrix(q3[1],alpha3,d3,a3)
A_4=build_matrix(0,alpha4,d4,a4)

T_1=np.dot(A_1,A_2)
T_2=np.dot(T_1,A_3)
T_3=np.dot(T_2,A_4)

T=T_3
x=T[0,3]
y=T[1,3]
z=T[2,3] #l_base is the distance from the base to the first actuator and must be added. 

print "x=",x
print "y=",y
print "z=",z+l_base


