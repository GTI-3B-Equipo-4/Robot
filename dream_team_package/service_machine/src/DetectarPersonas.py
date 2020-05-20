#! /usr/bin/env python
# coding: utf-8

#----------------------------------------------------------------------------
# Autor: Matthew Conde Oltra
# Fecha de creación: 7/05/2020
# Fecha actualización: 20/05/2020
#   DetectarPersonas.py
#----------------------------------------------------------------------------

import rospy
import cv2
import numpy as np 
from cv_bridge import CvBridge, CvBridgeError
from sensor_msgs.msg import Image

class DetectarPersonas(object):

    def __init__(self):
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
       
        ruta = "/home/mawco/catkin_ws/src/deteccion_personas/src/clasificadores/haarcascade_fullbody.xml"

        cascada = cv2.CascadeClassifier(ruta)

        #Convertimos la imagen a escala de grises
        #img_gray = cv2.cvtColor(cv_image, cv2.COLOR_BGR2HSV)
        
        cascada = cascada.detectMultiScale(cv_image, 1.1, 5)

        #Recoremos cada uno de los ojetos que ha encontrado
        for x,y,w,h in cascada:
            cv2.rectangle(cv_image, (x,y), (x+w, y+h),(255,0,0),3)

        cv2.imshow("Original", cv_image)

        cv2.waitKey(1)

    def clean_up(self):
        cv2.destroyAllWindows()


