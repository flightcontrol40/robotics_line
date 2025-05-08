
from launch.substitutions import PathJoinSubstitution, TextSubstitution
from launch_ros.substitutions import FindPackageShare

print("Hello world")
arg = PathJoinSubstitution([
    FindPackageShare('action_servers'),
    'launch',
    'action_servers.launch.py'
])

print(arg.describe())