#! /usr/bin/env python
# coding: utf-8
#----------------------------------------------------------------------------
# Autor: Matthew Conde Oltra
# Fecha de creación: 22/04/2020
# Fecha actualización: 22/04/2020
#  client.py
#----------------------------------------------------------------------------
import rospy
from dream_team_msgs.srv import DreamTeamServiceMessage, DreamTeamServiceMessageResponse, DreamTeamServiceMessageRequest
from time import sleep
import smach_ros
import actionlib
import math
from nav_msgs.msg import Odometry
from OdomTopicReader import OdomTopicReader
from geometry_msgs.msg import Twist, Point, Pose

def my_callback(request): #Funcion que se ejecuta cuando se llama al servicio
    
    rospy.loginfo("The service navigation_stack has been called")
    print(request.direction)
    
    #Respuesta del servidor de mensajes
    response = DreamTeamServiceMessageResponse()
    response.success = True
    return response

if __name__=='__main__':

    rospy.init_node('client_dream_team', log_level=rospy.INFO) #Inicializamos el nodo
    #Llamada a la maquina de estados
    machine_state = rospy.ServiceProxy('/machine_state', DreamTeamServiceMessage)
    msg_request = DreamTeamServiceMessageRequest() #Creamos el objeto para la petición
    msg_request.on = 1
    msg_request.battery = 20
    rospy.loginfo("Llamando al servicio /machine_state")
    result = machine_state(msg_request) #Ejecuta la llamada al servidor
    rospy.loginfo("Resultado de la llamada: %s" % result) #Información para depuracion
    rospy.spin() #mantiene el service abierto