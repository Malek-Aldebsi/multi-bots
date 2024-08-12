import os

from ament_index_python.packages import get_package_share_directory
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration, TextSubstitution
from launch.actions import DeclareLaunchArgument
from launch.actions import IncludeLaunchDescription
from launch import LaunchDescription
from launch.actions import OpaqueFunction


def gen_robot_info():
    robot = [
        {
            'name': 'walle_v0', 
            'x_pose': 0.0,
            'y_pose': 0.0
            }, 
        {
            'name': 'walle_v1', 
            'x_pose': 2.0,
            'y_pose': 2.0
            },  
         ]
    return robot


def launch_setup(context, *args, **kwargs):
    launch_file_dir = os.path.join(get_package_share_directory(
        'multi_robot'), 'launch')

    robots = gen_robot_info()

    ld = LaunchDescription()

    for robot in robots:
        ld.add_action(IncludeLaunchDescription(
                PythonLaunchDescriptionSource(os.path.join(
                    launch_file_dir, 'spawn.launch.py')),
                launch_arguments={
                    'x_spawn': TextSubstitution(text=str(robot['x_pose'])),
                    'y_spawn': TextSubstitution(text=str(robot['y_pose'])),
                    'entity_name': robot['name']
                }.items()))

    return [ld]


def generate_launch_description():
    # Include the Gazebo launch file, provided by the gazebo_ros package
    gazebo = IncludeLaunchDescription(
            PythonLaunchDescriptionSource([os.path.join(
                get_package_share_directory('gazebo_ros'), 'launch', 'gazebo.launch.py')])
         )

    return LaunchDescription([
        gazebo,
        OpaqueFunction(function=launch_setup)
    ])
