#! /usr/bin/env python

import rospy
from Bateria import LectorDeBateria

if __name__ == "__main__":
    rospy.init_node('battery_topic_suscriber')
    laBateria = LectorDeBateria()
    rospy.loginfo(laBateria.getPorcentajeDeBateriaRestante())
    rate = rospy.Rate(0.5)

    ctrl_c = False

    def shutdown_hook():
        global ctrl_c
        print("Shutdown time")
        ctrl_c = True

    rospy.on_shutdown(shutdown_hook)

    while not ctrl_c:
        data = laBateria.getPorcentajeDeBateriaRestante()
        rospy.loginfo(data)
        rate.sleep()