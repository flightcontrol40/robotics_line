import os
import sys

from ament_index_python import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import PathJoinSubstitution, TextSubstitution
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare

name = 'beaker'
ip = '172.29.208.124'

def generate_launch_description():
    return LaunchDescription([
        # Faunc driver options
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
        # Camera driver options
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource([
                PathJoinSubstitution([
                    FindPackageShare('camera_driver'),
                    'launch',
                    'launch.py'
                ])
            ]),
        ),
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource([
                PathJoinSubstitution([
                    FindPackageShare('control_node'),
                    'launch',
                    'runner.py'
                ])
            ]),
        ),

    ])

# END
