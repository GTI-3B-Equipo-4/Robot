#! /usr/bin/env python
# coding: utf-8
#----------------------------------------------------------------------------
# Autor: Matthew Conde Oltra
# Fecha de creación: 17/04/2020
# Fecha actualización: 17/04/2020
#   machine_state.py
#----------------------------------------------------------------------------

import rospy
from dream_team_msgs.srv import DreamTeamServiceMessage, DreamTeamServiceMessageResponse, DreamTeamServiceMessageRequest
from smach import State,StateMachine
from time import sleep
import smach_ros
import actionlib

class Connected(State):
    def __init__(self):
        State.__init__(self, outcomes=['1','0'], input_keys=['input'], output_keys=[''])

    def execute(self, userdata):
        print("On: {}".format(userdata.input))
        sleep(1)
        if userdata.input == 1:
             return '1'
        else:
             return '0'

class Disconnected(State):
    def __init__(self):
        State.__init__(self, outcomes=['1','0'], input_keys=['input'], output_keys=[''])

    def execute(self, userdata):
        print("Off: {}".format(userdata.input))
        sleep(1)
        if userdata.input == 1:
             return '1'
        else:
             return '0'

class Patrullando(State): #si la bateria es baja, enviar un valor de batería es baja y ordenar que vaya a la plataforma
    def __init__(self):
        State.__init__(self, outcomes=['1','0'], input_keys=['input'], output_keys=[''])

    def execute(self, userdata):
        sleep(1)
        if userdata.input > 20: #bateria llena

             return '0'
        elif userdata.input <= 20:#bateria baja

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
             return '0' #activamos reposo

class Reposo(State):
    def __init__(self):
        State.__init__(self, outcomes=['1','0'], input_keys=['input'], output_keys=[''])

    def execute(self, userdata):
        sleep(1)
        if userdata.input == 1:
             return '1'
        else:
             return '0'

def my_callback(request): #Funcion que se ejecuta cuando se llama al servicio
    
    #rospy.loginfo("The service machine_state has been called")
    #print(request.direction)
    sm = StateMachine(outcomes=['success'])
    #Recibir del servidor (ROSWEB)
    #sm.userdata.direction = request.direction
    sm.userdata.battery = request.battery
    #print("Porcentage batería:".format(request.battery))
    sm.userdata.on = request.on
    with sm:
        #StateMachine.add('Connected', Connected(), transitions={'1': 'Disconnected', '0': 'success'}, remapping={'input': 'on', 'output': ''})
        #StateMachine.add('Disconnected', Disconnected(), transitions={'1': 'success', '0': 'Connected'},remapping={'input': 'on', 'output': ''})
        StateMachine.add('Reposo', Reposo(), transitions={'1':'success','0':'Patrullando'}, remapping={'input':'on','output':''})
        StateMachine.add('Patrullando', Patrullando(), transitions={'1':'Cargando','0':'success'}, remapping={'input':'battery','output':''})
        StateMachine.add('Cargando', Cargando(), transitions={'1':'Patrullando','0':'success'}, remapping={'input':'battery','output':''})
        
    sm.execute()
    #Respuesta del servidor de mensajes
    response = DreamTeamServiceMessageResponse()
    response.success = True
    return response

if __name__=='__main__':

    rospy.init_node('service_machine', anonymous=True) #se inicializa el nodo
    rospy.Service('/machine_state', DreamTeamServiceMessage, my_callback) #se crea el servicio
    #rate = rospy.Rate(10)
    rospy.loginfo('Service /machine_state ready')
    rospy.spin() #mantiene el service abierto