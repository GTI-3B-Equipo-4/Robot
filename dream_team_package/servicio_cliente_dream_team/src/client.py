#! /usr/bin/env python
# coding: utf-8

"""

:FILE_NAME:client.py
:AUTHOR:Matthew Conde Oltra
:DATE:22/04/2020

"""

import rospy
from dream_team_msgs.srv import DreamTeamServiceMessage, DreamTeamServiceMessageResponse, DreamTeamServiceMessageRequest
from time import sleep
import smach_ros
import actionlib
import math
from nav_msgs.msg import Odometry
from OdomTopicReader import OdomTopicReader
from geometry_msgs.msg import Twist, Point, Pose


"""

:function_name:my_callback
:input:request
:descripcion:se ejecuta cuando se llama al servicio

"""
def my_callback(request):
    
    rospy.loginfo("The service navigation_stack has been called")
   
    response = DreamTeamServiceMessageResponse()
    response.success = True
    return response



"""

:function_name:main
:descripcion: inicializa el nodo, llama a la maquina de estados,crea la peticion y ejecuta la llamada al servidor

"""
def main():

    rospy.init_node('client_dream_team', log_level=rospy.INFO) 

   
    machine_state = rospy.ServiceProxy('/machine_state', DreamTeamServiceMessage)
    msg_request = DreamTeamServiceMessageRequest() 
    rospy.loginfo("Llamando al servicio /machine_state")
    result = machine_state(msg_request) 

    ctrl_c = False

    def shutdownhook():
        
        rospy.loginfo("Robot apagado!")
        ctrl_c=True
        
    rospy.on_shutdown(shutdownhook)

    while not ctrl_c:
        rate.sleep()


if __name__ == '__main__':
    main()

    