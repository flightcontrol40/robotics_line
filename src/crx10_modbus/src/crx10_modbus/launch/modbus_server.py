import os
import sys

import launch
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node

name = 'beaker'
ip = '172.29.208.124'
os.environ['RCUTILS_CONSOLE_OUTPUT_FORMAT'] = '{time}: [{name}] [{severity}]\t{message}'


def generate_launch_description():

    modbus_server = Node(
        package='crx10_modbus',
        executable='modbus',
        respawn=True,
        respawn_delay=4,
    )

    return launch.LaunchDescription([
        modbus_server,
    ])