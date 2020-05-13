#! /usr/bin/env python
# coding: utf-8
#----------------------------------------------------------------------------
# Autor: Matthew Conde Oltra
# Fecha de creación: 17/04/2020
# Fecha actualización: 12/05/2020
#   machine_state.py
#----------------------------------------------------------------------------

import rospy
from dream_team_msgs.srv import DreamTeamServiceMessage, DreamTeamServiceMessageResponse, DreamTeamServiceMessageRequest
from smach import State,StateMachine
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal, MoveBaseActionFeedback
from time import sleep
import smach_ros
import actionlib
import smach
import time
from smach_ros import IntrospectionServer
from tf.transformations import quaternion_from_euler
from collections import OrderedDict
#Importamos librerias para la clase DetectarPersonas
import cv2
import numpy as np 
from cv_bridge import CvBridge, CvBridgeError
from sensor_msgs.msg import Image


## Puntos de la vital
lugares = [
    ['Garita', (-10.42, -10.66, 0.001186), (0.0, 0.0, 1.0, 0.0)],
    ['Almacen', (-14.68, -8.4280, -0.000987), (0.0, 0.0, 1.0, 0.0)],
    ['Tienda', (-19.046, -11.028, -0.000987), (0.0, 0.0, 1.0, 0.0)],
    ['Oficina', (-25.2595, -13.3887, -0.000987), (0.0, 0.0, 1.0, 0.0)],
]

def shutdownhook():
    detectorPersonas_obj.clean_up()
    rospy.loginfo("Robot apagado!")
    ctrl_c=True

class Connected(State):
    def __init__(self):
        State.__init__(self, outcomes=['1','0'], input_keys=['input'], output_keys=[''])

    def execute(self, userdata):
        print("On: {}".format(userdata.input))
        sleep(1)
        if userdata.input == 1:
            ctrl_c = False
            return '1'
        else:
            ctrl_c = True #apagar será ON
            rospy.on_shutdown(shutdownhook)
            while not ctrl_c:
                rate.sleep()              
            
            return '0'

class Disconnected(State):
    def __init__(self):
        State.__init__(self, outcomes=['1','0'], input_keys=['input'], output_keys=[''])

    def execute(self, userdata):
        print("Off: {}".format(userdata.input))
        sleep(1)
        if userdata.input == 1:
            ctrl_c = False 
            return '1'
        else:
            ctrl_c = True #apagar será ON
            rospy.on_shutdown(shutdownhook)
            while not ctrl_c:
                rate.sleep()              
            
            return '0'


class Patrullando(State): #si la bateria es baja, enviar un valor de batería es baja y ordenar que vaya a la plataforma

    def __init__(self, lugar):
        State.__init__(self, outcomes=['1', '0'], input_keys=['input'], output_keys=[''])
        
        lugarAlQueIr = []
        for l in lugares:
            if l[0] == lugar:
                #cogemos el nuevo lugar
                lugarAlQueIr = l 
        
        self._position =lugarAlQueIr[1]
        self._orientation =lugarAlQueIr[2]
        self._place = lugarAlQueIr[0]
        self._move_base = actionlib.SimpleActionClient("/move_base", MoveBaseAction)
        rospy.loginfo("Activando el cliente de navegacion..")
        self._move_base.wait_for_server(rospy.Duration(15))

    def execute(self, userdata):
        sleep(1)
        time.sleep(2)
        goal = MoveBaseGoal()
        goal.target_pose.header.frame_id = 'map'
        rospy.loginfo(self._position)
        goal.target_pose.pose.position.x = self._position[0]
        goal.target_pose.pose.position.y = self._position[1]
        goal.target_pose.pose.position.z = self._position[2]
        goal.target_pose.pose.orientation.x = self._orientation[0]
        goal.target_pose.pose.orientation.y = self._orientation[1]
        goal.target_pose.pose.orientation.z = self._orientation[2]
        goal.target_pose.pose.orientation.w = self._orientation[3]

        rospy.loginfo("ROBOT %s" %(self._place))
        # sends the goal
        self._move_base.send_goal(goal)
        self._move_base.wait_for_result()
        # Comprobamos el estado de la navegacion
        nav_state = self._move_base.get_state()
        rospy.loginfo("[Result] State: %d" % (nav_state))
        nav_state = 3


        if nav_state == 3:
            #Robot se pone en reposo
            return '1'
        else:
            return '0'


class Cargando(State): #mientras no llegue a la carga completa
    def __init__(self):
        State.__init__(self, outcomes=['1','0'], input_keys=['input'], output_keys=[''])

    def execute(self, userdata):
        sleep(1)
        if userdata.input == 100: #si llega a la carga completa, activamos patrullando
             return '1'
        else:
             return '0' #se queda cargando

class Reposo(State):
    def __init__(self):
        State.__init__(self, outcomes=['1','0'], input_keys=['input'], output_keys=[''])

    def execute(self, userdata):
        sleep(1)

        if userdata.input == 1: 
             return '1'
        else:
             return '0'

class DetectarPersonas(object):
    
    def __init__(self):
        State.__init__(self, outcomes=['1','0'], input_keys=['input'], output_keys=[''])
        self.bridge_object = CvBridge()
        self.image_sub = rospy.Subscriber("/turtlebot3/camera/image_raw", Image, self.camera_callback)

    def camera_callback(self, data):

        try:
            cv_image =  self.bridge_object.imgmsg_to_cv2(data, desired_encoding="bgr8")
        except CvBridgeError as e:
            print(e)

        #detener_robot = False
        #Calculamos la dimension de la imagen capturada
        height, width, channels = cv_image.shape

        #Definimos el clasificador
        #ruta = "/home/mawco/catkin_ws/src/deteccion_personas/src/clasificadores/haarcascade_upperbody.xml"
        ruta = "/home/mawco/catkin_ws/src/deteccion_personas/src/clasificadores/haarcascade_fullbody.xml"
        #ruta = "/home/mawco/catkin_ws/src/deteccion_personas/src/clasificadores/haarcascade_frontalface_alt2.xml"
        cascada = cv2.CascadeClassifier(ruta)

        #Convertimos la imagen a escala de grises
        #img_gray = cv2.cvtColor(cv_image, cv2.COLOR_BGR2HSV)
        
        cascada = cascada.detectMultiScale(cv_image, 1.1, 5)
        intruso = 0
        #Recoremos cada uno de los objetos que ha encontrado
        for x,y,w,h in cascada:
            
            cv2.rectangle(cv_image, (x,y), (x+w, y+h),(255,0,0),3)

        cv2.imshow("Original", cv_image)
        cv2.waitKey(1)

        
        

    def clean_up(self):
        cv2.destroyAllWindows()
        

def my_callback(request): #Funcion que se ejecuta cuando se llama al servicio
    
    #rospy.loginfo("The service machine_state has been called")
    #print(request.direction)
    sm = StateMachine(outcomes=['success','abort'])
    #Recibir del servidor (ROSWEB)
    # si está on/off
    # batería
    # lugar al que nos dirigimos
    sm.userdata.on = request.on

    sm.userdata.battery = request.battery
    
    sm.userdata.lugar = request.lugar

    with sm:
        #StateMachine.add('Connected', Connected(), transitions={'1': 'Disconnected', '0': 'success'}, remapping={'input': 'on', 'output': ''})
        #StateMachine.add('Disconnected', Disconnected(), transitions={'1': 'success', '0': 'Connected'},remapping={'input': 'on', 'output': ''})
        StateMachine.add('Reposo', Reposo(), transitions={'1':'success','0':'Patrullando'}, remapping={'input':'on','output':''})
        StateMachine.add('Patrullando', Patrullando(request.lugar), transitions={'1':'success','0':'Reposo'}, remapping={'input':['battery','lugar'],'output':''})
        StateMachine.add('Cargando', Cargando(), transitions={'1':'Patrullando','0':'success'}, remapping={'input':'battery','output':''})
        
    sm.execute()
    #Respuesta del servidor de mensajes
    response = DreamTeamServiceMessageResponse()
    response.success = True
    return response

if __name__=='__main__':

    rospy.init_node('service_machine', anonymous=True) #se inicializa el nodo
    rospy.Service('/machine_state', DreamTeamServiceMessage, my_callback) #se crea el servicio
    rospy.loginfo('Service /machine_state ready')
    rospy.spin() #mantiene el service abierto