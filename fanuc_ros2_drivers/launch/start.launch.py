from launch_ros.substitutions import FindPackageShare

from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import PathJoinSubstitution, TextSubstitution
import sys

name = ''
ip = ''

# It has to be passed like this, otherwise launch gets upset
for arg in sys.argv:
    if arg.startswith("robot_name:="):
        name = arg.split(":=")[1]
    elif arg.startswith("robot_ip:="):
    	ip = arg.split(":=")[1]

def generate_launch_description():
    return LaunchDescription([
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource([
                PathJoinSubstitution([
                    FindPackageShare('action_servers'),
                    'launch',
                    'action_servers.launch.py'
                ])
            ]),
            launch_arguments={
                'robot_name': name,
                'robot_ip': ip,
            }.items()
        ),
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource([
                PathJoinSubstitution([
                    FindPackageShare('msg_publishers'),
                    'launch',
                    'message_publishers.launch.py'
                ])
            ]),
            launch_arguments={
                'robot_name': name,
                'robot_ip': ip,
            }.items()
        ),
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource([
                PathJoinSubstitution([
                    FindPackageShare('srv_services'),
                    'launch',
                    'srv_services.launch.py'
                ])
            ]),
            launch_arguments={
                'robot_name': name,
                'robot_ip': ip,
            }.items()
        ),
    ])