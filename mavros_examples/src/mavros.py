#!/usr/bin/env python3

import rospy
from std_msgs.msg import String
from sensor_msgs.msg import NavSatFix
from mavros_msgs.srv import *
from geometry_msgs.msg import TwistStamped
import mavros

#global variable
latitude =0.0
longitude=0.0


def setGuidedMode():
    rospy.wait_for_service('/mavros/set_mode')
    try:
        set_mode_client = rospy.ServiceProxy('/mavros/set_mode', mavros_msgs.srv.SetMode)
        #http://wiki.ros.org/mavros/CustomModes for custom modes
        #sModeChanged = flightModeService(custom_mode='OFFBOARD') #return true or false
        offb_set_mode = SetModeRequest()
        print('OFFBOARD')
        offb_set_mode.custom_mode = 'OFFBOARD'
        if(set_mode_client.call(offb_set_mode).mode_sent == True):
            rospy.loginfo("OFFBOARD enabled")
    
    except rospy.ServiceException as e:
        print ("service set_mode call failed GUIDED Mode could not be set. Check that GPS is enabled")
        
def setStabilizeMode():
    rospy.wait_for_service('/mavros/set_mode')
    try:
        flightModeService = rospy.ServiceProxy('/mavros/set_mode', mavros_msgs.srv.SetMode)
        #http://wiki.ros.org/mavros/CustomModes for custom modes
        isModeChanged = flightModeService(custom_mode='STABILIZE') #return true or false
    except rospy.ServiceException as e:
        print ("service set_mode call failed GUIDED Mode could not be set. Check that GPS is enabled")

def setLandMode():
    rospy.wait_for_service('/mavros/cmd/land')
    try:
        landService = rospy.ServiceProxy('/mavros/cmd/land', mavros_msgs.srv.CommandTOL)
        #http://wiki.ros.org/mavros/CustomModes for custom modes
        isLanding = landService(altitude = 0, latitude = 0, longitude = 0, min_pitch = 0, yaw = 0)
    except rospy.ServiceException as e:
        print ("service land call failed The vehicle cannot land ")          
def setArm():
    rospy.wait_for_service('/mavros/cmd/arming')
    try:
        arming_client = rospy.ServiceProxy('/mavros/cmd/arming', mavros_msgs.srv.CommandBool)
        arm_cmd = CommandBoolRequest()
        arm_cmd.value = True
        if(arming_client.call(arm_cmd).success == True):
                rospy.loginfo("Vehicle armed")
        else:
            print ("not armed")

            

    except rospy.ServiceException as e:
        print ("Service arm call failed")
        
def setDisarm():
    rospy.wait_for_service('/mavros/cmd/arming')
    try:
        armService = rospy.ServiceProxy('/mavros/cmd/arming', mavros_msgs.srv.CommandBool)
        armService(False)
    except rospy.ServiceException as e:
        print ("Service arm call failed")


def setTakeoffMode():
    rospy.wait_for_service('/mavros/cmd/takeoff')
    try:
        takeoffService = rospy.ServiceProxy('/mavros/cmd/takeoff', mavros_msgs.srv.CommandTOL) 
        takeoffService(altitude = 2, latitude = 0, longitude = 0, min_pitch = 0, yaw = 0)
    except rospy.ServiceException as e:
        print ("Service takeoff call failed: %s")%e
    
    

def globalPositionCallback(globalPositionCallback):
    global latitude
    global longitude
    latitude = globalPositionCallback.latitude
    longitude = globalPositionCallback.longitude
    #print ("longitude: %.7f" %longitude)
    #print ("latitude: %.7f" %latitude)

def menu():
    print ("Press")
    print ("1: to set mode to GUIDED")
    print ("2: to set mode to STABILIZE")
    print ("3: to set mode to ARM the drone")
    print ("4: to set mode to DISARM the drone")
    print ("5: to set mode to TAKEOFF")
    print ("6: to set mode to LAND")
    print ("7: print GPS coordinates")
    
def myLoop():
    x='1'
    while ((not rospy.is_shutdown())and (x in ['1','2','3','4','5','6','7'])):
        menu()
        x = input("Enter your input: ");
        if (x=='1'):
            setGuidedMode()
        elif(x=='2'):
            setStabilizeMode()
        elif(x=='3'):
            setArm()
        elif(x=='4'):
            setDisarm()
        elif(x=='5'):
            setTakeoffMode()
        elif(x=='6'):
            setLandMode()
        elif(x=='7'):
            global latitude
            global longitude
            print ("longitude: %.7f" %longitude)
            print ("latitude: %.7f" %latitude)
        else: 
            print ("Exit")
        
        
    

if __name__ == '__main__':
    rospy.init_node('gapter_pilot_node', anonymous=True)
    rospy.Subscriber("/mavros/global_position/raw/fix", NavSatFix, globalPositionCallback)
    velocity_pub = rospy.Publisher('/mavros/setpoint_velocity/cmd_vel', TwistStamped, queue_size=10)
    # spin() simply keeps python from exiting until this node is stopped
    
    #listener()
    myLoop()
    #rospy.spin()