#! usr/bin/env python
#-*- coding:utf-8 -*-

# Autor: Emilio Esteve Peiró
# Fecha: 10 03 2020
# Descripción: Clase para obtener el porcentaje de batería que le queda al robot

import rospy
from sensor_msgs.msg import BatteryState


class LectorDeBateria(object):

    # ------------------------------------------------------------------------------
    # topic_name: Texto -->
    # constructor() -->
    # _topic_name:Texto, _sub:rospy.Suscriber(), _batterydata:BatteryState()
    # ------------------------------------------------------------------------------
    def __init__(self, topic_name='/battery_state'):
        self._topic_name = topic_name
        self._sub = rospy.Subscriber(self._topic_name, BatteryState, self.topic_callback)
        self._batterydata = BatteryState()

    def topic_callback(self, msg):
        self._batterydata = msg
        rospy.logdebug(self._batterydata)

    # ------------------------------------------------------------------------------
    # getPorcentajeDeBateriaRestante()
    # --> R
    # ------------------------------------------------------------------------------
    def getPorcentajeDeBateriaRestante(self):
        return self._batterydata.percentage
