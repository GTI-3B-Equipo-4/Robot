#! /usr/bin/env python
#-*- coding: utf-8 -*-

import rospy
import math
from nav_msgs.msg import Odometry
from OdomTopicReader import OdomTopicReader
from my_custom_service_msg.srv import MyCustomServiceMessage, MyCustomServiceMessageResponse
from geometry_msgs.msg import Twist, Point, Pose

if __name__ == "__main__":
    rospy.init_node('move_to_coord', log_level=rospy.INFO)
    odom_reader_object = OdomTopicReader()
    rospy.loginfo(odom_reader_object.get_odomdata())
    rate = rospy.Rate(0.5)

    ctrl_c = False

    def shutdownhook():
        global ctrl_c
        print('Shutdown time!')
        ctrl_c = True

    def distancia(Ax, Ay):
        eX = math.pow(Ax, 2)
        eY = math.pow(Ay, 2)
        d = math.sqrt(eX+eY)
        #print(d)
        return d

    rospy.on_shutdown(shutdownhook)

    x=1.0 #coordenada X del tesoro
    y=1.0 #coordenada Y del tesoro

    dV =int(round(distancia(x, y))) # Distancia inicial al tesoro, suponiendo que la posición inicial
    #del robot es (0, 0)


    while not ctrl_c:
        data = odom_reader_object.get_odomdata()
        Ax = data.pose.pose.position.x - x
        Ay = data.pose.pose.position.y - y
        D = int(round(distancia(Ax, Ay)))
        rospy.loginfo("Distancia: {}".format(D))

        if dV < D:
            print('Te estas enfriando!!')
        elif D == 0:
            print('Te has quemado!!')

            shutdownhook()
        else:
            print('Frio!')

        #rospy.loginfo(data.pose.pose.position)#Sacamos solo la posición
        #rospy.loginfo(data.pose.pose.orientation)#Sacamos el quaternion para el giro

        rate.sleep()


