#! /usr/bin/env python
#-*- coding: utf-8 -*-
import rospy
from nav_msgs.msg import Odometry

class OdomTopicReader(object):
    def __init__(self, topic_name = '/odom'):
        self._topic_name = topic_name
        self._sub = rospy.Subscriber(self._topic_name, Odometry, self.topic_callback)
        self._odomdata = Odometry()
    def topic_callback(self, msg):
        self._odomdata = msg
        rospy.logdebug(self._odomdata)
    def get_odomdata(self):
        return self._odomdata

