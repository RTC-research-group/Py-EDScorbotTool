#!/usr/bin/env python

import math
import numpy as np
import rospy
from std_msgs.msg import Float64
from sensor_msgs.msg import JointState
import sys
import roslib #; roslib.load_manifest('scorbot_joint')

def joint_states_callback(data):
    global current_position 
    global printJointStates
    current_position = data
    #if printJointStates:
    print (current_position.position)

def bern_lamniscata(alpha,num=200,plot=False):
    

    t = np.linspace(0, 2*np.pi, num)

    x = alpha * np.sqrt(2) * np.cos(t) / (np.sin(t)**2 + 1)
    y = alpha * np.sqrt(2) * np.cos(t) * np.sin(t) / (np.sin(t)**2 + 1)

    if plot:
        import matplotlib.pyplot as plt
        plt.plot(x, y)
        plt.show()
    return x,y

def trajectory(x,y):
    
    nsteps = x.shape[0]
    # pub = rospy.Publisher('/scorbot/trajectory_controller/command', JointTrajectory, queue_size=10)
    joints = {}
    joints["J1"] = rospy.Publisher('/scorbot/base_position_controller/command', Float64, queue_size=10)         #J1
    joints["J2"] = rospy.Publisher('/scorbot/shoulder_position_controller/command', Float64, queue_size=10)     #J2
    joints["J3"] = rospy.Publisher('/scorbot/elbow_position_controller/command', Float64, queue_size=10)        #J3
    joints["J4"] = rospy.Publisher('/scorbot/pitch_position_controller/command', Float64, queue_size=10)        #J4
    joints["J5"] = rospy.Publisher('/scorbot/roll_position_controller/command', Float64, queue_size=10)         #J5
    rospy.init_node('simple_mover_scorbot')
    rate = rospy.Rate(1)
    start_time = 0

    while not start_time:
        start_time = rospy.Time.now().to_sec()

    while not rospy.is_shutdown():
        elapsed = rospy.Time.now().to_sec() - start_time

        for i in range(nsteps):
            a1,a2,a3,a4,a5 = 0
            # Convertimos de posicion (x,y,z) a angulos:
            #a1,a2,a3,a4,a5 = inverse_kinematics(x,y,z)

            joints["J1"].publish(a1)
            joints["J1"].publish(a2)
            joints["J1"].publish(a3)
            joints["J1"].publish(a4)
            joints["J1"].publish(a5)

            rate.sleep()

        # pub_base.publish (math.sin(2*math.pi*0.1*elapsed)*(math.pi/2))
        # pub_shoulder.publish (math.sin(2*math.pi*0.1*elapsed)*(math.pi/2))
        # pub_elbow.publish (math.sin(2*math.pi*0.1*elapsed)*(math.pi/2))
        # pub_pitch.publish (math.sin(2*math.pi*0.1*elapsed)*(math.pi/2))
        # pub_roll.publish (math.sin(2*math.pi*0.1*elapsed)*(math.pi/2))
        
        # pub_shoulder.publish (0)
        
        # pub_shoulder.publish (-90)
        

if __name__ == '__main__':

    
    #Define a subscriber to check robot's positioning
    rospy.Subscriber('/scorbot/joint_states', JointState, joint_states_callback)
    
    #Define publishers for each joint
    

    x,y = bern_lamniscata(50)



    try:
        trajectory(x,y)
    except rospy.ROSInterruptException:
        pass
