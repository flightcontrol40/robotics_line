#!/usr/bin/env python3
import sys
import os
import rclpy

import dependencies.FANUCethernetipDriver as FANUCethernetipDriver

from dependencies.robot_controller import robot
from fanuc_interfaces.msg import CurJoints
from rclpy.node import Node

FANUCethernetipDriver.DEBUG = False

sys.path.append('./pycomm3/pycomm3')

ROBOT_NAME = 'beaker'
ROBOT_IP = '172.29.208.124'

class current_joint(Node):
    def __init__(self):
        super().__init__('curr_joint')

        self.bot = robot(ROBOT_IP)
        self.publisher_ = self.create_publisher(CurJoints, f"{ROBOT_NAME}/cur_joints", 10)
        timer_period = 0.5
        self.timer = self.create_timer(timer_period, self.timer_callback)

    def timer_callback(self):
        msg = CurJoints()                                  
        msg.joints = self.bot.read_current_joint_position()
        self.publisher_.publish(msg)
        if FANUCethernetipDriver.DEBUG:
        	self.get_logger().info('Publishing: ' % msg.joints)


def main(args=None):
    rclpy.init(args=args)

    publisher = current_joint()

    rclpy.spin(publisher)

    publisher.destroy_node()
    rclpy.shutdown()
    
if __name__ == '__main__':
    main()
    
