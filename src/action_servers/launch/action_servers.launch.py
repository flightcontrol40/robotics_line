import sys

import launch
from launch.actions import DeclareLaunchArgument, LogInfo
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node

name = 'beaker'
ip = '172.29.208.124'

def generate_launch_description():


    cart_node = Node(
        package='action_servers',
        executable='cart_pose_server',
        #namespace=robot_name,
        respawn=True,
        respawn_delay=4,
    )
    convey_node = Node(
        package='action_servers',
        executable='convey_server',
        #namespace=robot_name,
        respawn=True,
        respawn_delay=4,
    )
    joint_node = Node(
        package='action_servers',
        executable='joint_pose_server',
        #namespace=robot_name,
        respawn=True,
        respawn_delay=4,
    )
    onrobot_node = Node(
        package='action_servers',
        executable='onrobot_server',
        #namespace=robot_name,
        respawn=True,
        respawn_delay=4,
    )
    schunk_node = Node(
        package='action_servers',
        executable='schunk_server',
        #namespace=robot_name,
        respawn=True,
        respawn_delay=4,
    )
    sjoint_node = Node(
        package='action_servers',
        executable='single_joint_server',
        #namespace=robot_name,
        respawn=True,
        respawn_delay=4,
    )

    return launch.LaunchDescription([
       cart_node,
       convey_node,
       joint_node,
       onrobot_node,
       schunk_node,
       sjoint_node,
    ])