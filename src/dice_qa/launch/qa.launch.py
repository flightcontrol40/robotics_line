import launch
from launch.actions import DeclareLaunchArgument, LogInfo
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def generate_launch_description():

    qa_node = Node(
        package='dice_qa',
        executable='qa_node',
        respawn=True,
        respawn_delay=4,
    )

    return launch.LaunchDescription([
        qa_node,
    ])