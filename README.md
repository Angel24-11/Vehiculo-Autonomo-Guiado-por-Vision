# Navegación Autónoma y Evasión de Obstáculos mediante Visión (ROS 2)

Este repositorio contiene la arquitectura modular para el proyecto de navegación de un vehículo autónomo simulado en Gazebo. El sistema utiliza visión computacional (OpenCV) y control PID para el seguimiento de trayectorias y evasión de obstáculos.

## Requisitos Previos
- **SO:** Ubuntu 22.04 LTS
- **Framework:** ROS 2 Humble
- **Simulador:** Gazebo (Garden/Sim7)
- **Dependencias:** OpenCV, cv_bridge, numpy, rclpy

## Estructura Modular
- `/vision_cv`: Procesamiento de imágenes (HSV, máscaras, centroides).
- `/control_pid`: Lógica matemática (PID) y Máquina de Estados Finitos (FSM).
- `/robot_integration`: Nodos de ROS 2 para la comunicación y control de tópicos.

## Instrucciones de Despliegue

### 1. Clonar y Compilar
```bash
git clone [https://github.com/Angel24-11/Vehiculo-Autonomo-Guiado-por-Vision](https://github.com/Angel24-11/Vehiculo-Autonomo-Guiado-por-Vision)
cd ~/ros2_ws
colcon build --packages-select robot_integration
source install/setup.bash
2. Ejecución
Terminal 1 (Lanzar Simulación):

Bash
gz sim -r /usr/share/gz/gz-sim7/worlds/diff_drive.sdf
Terminal 2 (Ejecutar Nodo de Navegación):

Bash
source ~/ros2_ws/install/setup.bash
ros2 run robot_integration nodo_navegacion
```
Nota Técnica sobre la Simulación
El software implementa correctamente la lógica de control PID y la arquitectura de comunicación.

Estado de la validación: Se ha confirmado la publicación efectiva de comandos Twist en el tópico /cmd_vel (verificable mediante ros2 topic echo /cmd_vel). Los modelos cargados en Gazebo (vehicle_blue/vehicle_green) operan como entidades estáticas debido a que sus archivos de configuración (SDF) no incluyen los plugins de cinemática requeridos para la actuación física. El sistema está completamente validado a nivel de lógica de software y arquitectura de nodos.

Equipo de Desarrollo
Zambrano Infante Angel: Arquitectura de Simulación y Adquisición de Datos.

López Ortiz Karen: Procesamiento de Visión Computacional (OpenCV/HSV).

Jacome Chavez David: Lógica de Control y Sintonización del PID.

Paredes Ortega Ezequiel: Integración ROS 2 (Nodos y Tópicos).
