import os

import launch
from launch_ros.actions import Node

os.environ['RCUTILS_CONSOLE_OUTPUT_FORMAT'] = '{time}: [{name}] [{severity}]\t{message}'

def generate_launch_description():

    package_name = 'camera_driver'

    driver = Node(
        package=package_name,
        executable='driver',
        respawn=True,
        respawn_delay=4,
    )

    return launch.LaunchDescription([
       driver,
    ])