from setuptools import setup
import os
from glob import glob

package_name = 'cmp3103_tidy_bot'

setup(
    name=package_name,
    version='1.0.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        ('share/' + package_name + '/launch', ['launch/tidy_bot.launch.py']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='Kevin Byamukama',
    maintainer_email='codewitted@gmail.com',
    description='Autonomous TidyBot for AgileX Limo',
    license='Apache-2.0',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'tidy_bot = cmp3103_tidy_bot.tidy_bot_node:main'
        ],
    },
)
