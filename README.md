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


