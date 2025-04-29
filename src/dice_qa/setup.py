import os
from glob import glob

from setuptools import find_packages, setup

package_name = 'dice_qa'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        ('share/' + package_name + '/model', glob('model/*.pt')),
        (os.path.join('share', package_name, 'launch'), glob(os.path.join('launch', '*.py')))
    ],
    install_requires=['setuptools'],
    package_dir={
        "dice_qa": "dice_qa"
    },

    zip_safe=True,
    maintainer='nathan',
    maintainer_email='nathanhampton40000@gmail.com',
    description='TODO: Package description',
    license='Apache-2.0',

    entry_points={
        'console_scripts': [
            'qa_node = dice_qa.qa:main' 
        ],
    },
)
