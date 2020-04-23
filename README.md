# Robot
Probar Sprint-2:

terminal1 : roscore

Servicio para crear un puente entre ROS y la WEB

terminal2 : roslaunch rosbridge_server rosbridge_websocket.launch

Para iniciar el entorno simulado en gazebo

terminal3 : roslaunch turtlebot3_gazebo vital.launch

Para iniciar el servicio para el video

terminal4 : rosrun web_video_server web_video_server _port:=7000

Llamada al cliente 

terminal5: roslaunch servicio_cliente_dream_team cliente_dream_team.launch


Para llamar al servicio de move_to_coords:

terminal1: roscore

terminal2: roslaunch turtlebot3_gazebo vital.launch

terminal3: roslaunch move_to_coords move.launch

terminal4: rosservice call /move_to_coord "on:0 battery:0 coordenadaX: 1 coordenadaY:1 coordenadaZ: 0 orientationX: 0 orientationY: 0 orientationZ: 0 orientationW: 0"


