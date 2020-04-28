#! /usr/bin/env python
# coding: utf-8
#----------------------------------------------------------------------------
# Autor: Matthew Conde Oltra
# Fecha de creación: 17/04/2020
# Fecha actualización: 22/04/2020
#   move_to_coord.py
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

lugar = []
## Puntos de la vital
lugares = [
    ['SALA1', (1.0, 3.0, 0.0), (0.0, 0.0, 1.0, 0.0)],
    ['ALMACEN', (3.0, 3.0, 0.0), (0.0, 0.0, 1.0, 0.0)],
    ['SALA2',(-6.0, 0.0, 0.0), (0.0, 0.0, 1.0, 0.0)],
    ['PASILLO', (-3.0, 1.0, 0.0), (0.0, 0.0, 1.0, 0.0)],
]


ctrl_c = False
#Función que termina el programa cuando llega al tesoro
def shutdownhook():
    global ctrl_c
    print('Shutdown time!')
    ctrl_c = True

#Función que calcula la distanci con la diferencia de posiciones
def distancia(x, y):
    eX = math.pow(x,2)
    eY = math.pow(y, 2)
    d = math.sqrt(eX+eY)
    #print(d)
    return d

def my_callback(request): #Funcion que se ejecuta cuando se llama al servicio
    
    rospy.loginfo("The service navigation_stack has been called")
    print("Lugar: {}".format(request.lugar))
    #Cogemos el lugar que se ha elegido
    for l in lugares:
        if l[0] == request.lugar:
            lugar = l

    #Bucle que mueve al robot hasta el destino
    while not ctrl_c:

        data = odom_reader_object.get_odomdata()

        print("Posición actual del robot: ({},{},{})".format(data.pose.pose.position.x,data.pose.pose.position.y, data.pose.pose.position.z))#cogemos la posición x e y del robot en todo momento
        print("Data: ({},{},{},{})".format(data.pose.pose.orientation.x,data.pose.pose.orientation.y,data.pose.pose.orientation.z,data.pose.pose.orientation.w))

        x = round(data.pose.pose.position.x) - lugar[1][0]
        y = round(data.pose.pose.position.y) - lugar[1][1]


        #Redondeamos la distancia que le queda por recorrer porque cuesta que la distancia sea exactamente 0 mientras nosotros lo estemos controlando
        # pero en el caso de que le demos unas coordenadas exactas, a las que moverse, no haría falta redondear.
        D = float(distancia(x, y)) #con la diferencia de posiciones, calculamos la distancia
        print(" Estas a esta distancia del tesoro: {} m".format(D))

        
        if round(D) == float(0): #cuando te estas acercando mucho
           
            print(' (/·3·)/ ¡¡TE ESTAS QUEMANDO!! (/·3·)/')
            #Paramos el robot
            move.linear.x = 0 
            move.angular.z = 0
            pub.publish(move)
            rate.sleep()

        #este elif solo nos serve si le indicamos las coordenadas al robot y va a tener si ho sí las coordenadas exactas
        #elif data.pose.pose.position.x == x and data.pose.pose.position.y == y : #cuando estas exactamente encima del tesoro

            print(' (/^-^)/ ¡¡LO HAS ENCONTRADO!! (/^-^)/')

        else: #cuando te estas alejando
            
            print(' _/(>w<_/) ¡¡FRIO!! _/(>w<_/)')
            z = round(data.pose.pose.orientation.z)
            #Debemos de ver si tenemos la orientación que corresponde 
            print("Orientación Z: {}".format(z))
            print("Orientación Z de la SALA1: {}".format(lugar[2][2]))
            if z == lugar[2][2]:
                #Le añadimos velocidad en x para ir a las coordenadas
                move.angular.z = 0
                move.linear.x = 0.2
                pub.publish(move)

                x = round(data.pose.pose.position.x)
                #Si la posición de X es igual a la posición de la X del lugar entonces dejamos de mover en X
                if x == lugar[1][1]:
                    move.linear.x == 0
                    pub.publish(move)

                rate.sleep()
            else:
                move.linear.x = 0
                move.angular.z = 0.1
                pub.publish(move)
                rate.sleep()
        #rospy.loginfo(data.pose.pose.position)#Sacamos solo la posición
        #rospy.loginfo(data.pose.pose.orientation)#Sacamos el quaternion para el giro

        rate.sleep()



    #Respuesta del servidor de mensajes
    response = DreamTeamServiceMessageResponse()
    response.success = True
    return response

if __name__=='__main__':

    #Inicializamos el nodo
    rospy.init_node('move_to_coord', log_level=rospy.INFO) 
    #Hacemos referencia a la función de apagado del robot
    rospy.on_shutdown(shutdownhook)
    #Creamos el objeto para la posición del robot
    odom_reader_object = OdomTopicReader()
    #Creamos el servicio
    rospy.Service('/move_to_coord', DreamTeamServiceMessage, my_callback)
    #Se crea la comunicación con el topic
    pub = rospy.Publisher('/cmd_vel', Twist, queue_size=1)
    move = Twist()

    rate = rospy.Rate(10)
    rospy.loginfo('Service /move_to_coord ready')
    rospy.spin() #mantiene el service abierto