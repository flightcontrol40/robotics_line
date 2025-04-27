import launch
from launch.actions import DeclareLaunchArgument, LogInfo
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def generate_launch_description():

    robot_name_launch_arg = DeclareLaunchArgument(
        'robot_name',
        default_value='noName',
        description="Name of the robot these nodes will be attached to"
    )
    robot_name = LaunchConfiguration('robot_name')

    qa_node = Node(
        package='dice_qa',
        executable='qa_node',
        parameters=[{"robot_name": robot_name}],
        respawn=True,
        respawn_delay=4,
    )

    return launch.LaunchDescription([
        robot_name_launch_arg,
        qa_node,
        LogInfo(msg=LaunchConfiguration('robot_name')),
    ])