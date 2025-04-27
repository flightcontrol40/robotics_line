import os
import sys

import launch
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare

name = 'beaker'
ip = '172.29.208.124'
os.environ['RCUTILS_CONSOLE_OUTPUT_FORMAT'] = '{time}: [{name}] [{severity}]\t{message}'

# It has to be passed like this, otherwise launch gets upset
for arg in sys.argv:
    if arg.startswith("robot_name:="):
        name = arg.split(":=")[1]
    elif arg.startswith("robot_ip:="):
        ip = arg.split(":=")[1]


def generate_launch_description():

    robot_name_launch_arg = DeclareLaunchArgument(
        'robot_name',
        default_value='beaker',
        description="Name of the robot these nodes will be attached to"
    )
    robot_ip_launch_arg = DeclareLaunchArgument(
        'robot_ip',
        default_value = '172.29.208.124',
        description="IP address of the robot these nodes will be attached to"
    )
    robot_name = LaunchConfiguration('robot_name')

    # Fanuc Drivers code
    fanuc_drivers = [
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
    ]

    # Camera Driver
    camera_driver = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([
            PathJoinSubstitution([
                FindPackageShare('camera_driver'),
                'launch',
                'launch.py'
            ])
        ])
    ),

    # Modbus Server
    modbus_server = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([
            PathJoinSubstitution([
                FindPackageShare('crx10_modbus'),
                'launch',
                'modbus_server.py'
            ])
        ]),
        launch_arguments={
                'robot_name': name,
                'robot_ip': ip,
            }.items()
    ),

    package_name = 'control_node'
    # Main Driver
    control_node = Node(
        package=package_name,
        executable='main',
        respawn=True,
        respawn_delay=4,
        parameters=[{"robot_name": robot_name}]
    )

    return launch.LaunchDescription([
        robot_name_launch_arg,
        robot_ip_launch_arg,
        camera_driver,
        modbus_server,
        control_node,
        *fanuc_drivers
    ])