from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        Node(
            package='cmp3103_tidy_bot',
            executable='tidy_bot',
            name='tidy_bot_node',
            output='screen',
            parameters=[{
                'use_sim_time': True,
                'linear_speed': 0.3,
                'angular_speed': 0.8,
            }],
        )
    ])
