import launch
from launch_ros.actions import Node, PushRosNamespace
from launch.actions import DeclareLaunchArgument, LogInfo
from launch.substitutions import LaunchConfiguration

ROBOT_NAME = 'beaker'
ROBOT_IP = '172.29.208.124'

def generate_launch_description():

    package_name = 'srv_services'


    mount_node = Node(
        package=package_name,
        executable='mount_position',
        #namespace=robot_name,
        respawn=True,
        respawn_delay=4,
    )
    speed_node = Node(
        package=package_name,
        executable='set_speed',
        #namespace=robot_name,
        respawn=True,
        respawn_delay=4,
    )
 

    return launch.LaunchDescription([
        
       mount_node,
       speed_node,
       #LogInfo(msg=LaunchConfiguration('robot_ip')),
       #LogInfo(msg=LaunchConfiguration('robot_name')),
    ])