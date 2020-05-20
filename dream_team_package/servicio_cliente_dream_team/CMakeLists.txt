cmake_minimum_required(VERSION 2.8.3)
project(servicio_cliente_dream_team)

find_package(catkin REQUIRED COMPONENTS
  rospy
  actionlib
  dream_team_msgs
  smach
  smach_ros
)

include_directories(

  ${catkin_INCLUDE_DIRS}
)
