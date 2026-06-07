Navegación Autónoma y Evasión de Obstáculos mediante Visión (ROS 2)
Este repositorio contiene el código fuente y la arquitectura modular para el proyecto de navegación de un vehículo autónomo simulado en Gazebo. El sistema utiliza exclusivamente una cámara a bordo para seguir una pista (líneas blancas) y realizar una maniobra de rebaso al detectar un obstáculo estático (vehículo verde).

Requisitos Previos (Entorno)
Para ejecutar este paquete, se requiere la siguiente infraestructura:

Sistema Operativo: Ubuntu 22.04 LTS

Framework: ROS 2 Humble

Simulador: Gazebo

Dependencias de Python: OpenCV, cv_bridge, numpy, rclpy

Estructura Modular del Proyecto
El código está dividido bajo el principio de separación de responsabilidades:

/vision_cv: Contiene los scripts de procesamiento de imágenes. Conversión BGR a HSV, aplicación de máscaras para la detección del carril blanco (canal V) y cálculo del centroide del obstáculo verde.

/control_pid: Contiene la lógica matemática. Implementa el controlador PID para calcular el error de trayectoria y la Máquina de Estados Finitos (FSM) para las transiciones (seguimiento -> evasión -> retorno).

/robot_integration: Paquete de ROS 2 que agrupa los nodos principales, suscribiéndose a /camera/image_raw y publicando comandos de movimiento en /cmd_vel.

/dataset: Evidencia de las capturas del entorno simulado utilizadas para calibrar la visión computacional.

Instrucciones de Despliegue (Ejecución)
Paso 1: Clonar el repositorio
Abre una terminal en tu entorno de Ubuntu y navega a tu espacio de trabajo (ros2_ws/src):

Bash
git clone [https://github.com/Angel24-11/Vehiculo-Autonomo-Guiado-por-Vision](https://github.com/Angel24-11/Vehiculo-Autonomo-Guiado-por-Vision)
Paso 2: Compilar el espacio de trabajo
Regresa a la raíz del workspace y compila los paquetes usando colcon:

Bash
cd ~/ros2_ws
colcon build --packages-select robot_integration
Paso 3: Cargar las variables de entorno

Bash
source install/setup.bash
Paso 4: Ejecutar la Simulación y el Nodo
Primero, lanza el entorno de Gazebo con la pista y los vehículos. En una nueva terminal, ejecuta:

Bash
# [PENDIENTE: AÑADIR COMANDO DE GAZEBO CUANDO EZEQUIEL LO PASE]
Finalmente, en la terminal donde compilaste el proyecto, ejecuta el nodo principal de navegación:

Bash
ros2 run robot_integration nodo_navegacion
Equipo de Desarrollo y Roles (Matriz ABET)
Zambrano Infante Angel: Arquitectura de Simulación y Adquisición de Datos (Dataset).

López Ortiz Karen: Procesamiento de Visión Computacional (OpenCV/HSV).

Jacome Chavez David: Lógica de Control y Sintonización del PID.

Paredes Ortega Ezequiel: Integración ROS 2 (Nodos y Tópicos) y Despliegue.
