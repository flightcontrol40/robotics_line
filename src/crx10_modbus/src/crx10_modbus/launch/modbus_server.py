import os
import sys

import launch
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node

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
        default_value='noName',
        description="Name of the robot these nodes will be attached to"
    )
    robot_name = LaunchConfiguration('robot_name')

    modbus_server = Node(
        package='crx10_modbus',
        executable='modbus',
        respawn=True,
        respawn_delay=4,
        parameters=[{"robot_name": robot_name}],
    )

    return launch.LaunchDescription([
        robot_name_launch_arg,
        modbus_server,
    ])