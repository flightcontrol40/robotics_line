#!/usr/bin/env python3
import sys
import os
import rclpy

import dependencies.FANUCethernetipDriver as FANUCethernetipDriver

from dependencies.robot_controller import robot
from fanuc_interfaces.msg import CurGripper
from rclpy.node import Node

FANUCethernetipDriver.DEBUG = False

sys.path.append('./pycomm3/pycomm3')

ROBOT_NAME = 'beaker'
ROBOT_IP = '172.29.208.124'

class check_grip(Node):
    def __init__(self):
        super().__init__('grip_pub')

        self.bot = robot(ROBOT_IP)
        self.publisher_ = self.create_publisher(CurGripper, f"{ROBOT_NAME}/grip_status", 10)
        timer_period = 0.5
        self.timer = self.create_timer(timer_period, self.timer_callback)

    def timer_callback(self):
        msg = CurGripper()                               
        msg.open = bool(self.bot.schunk_gripper_status())                      
        self.publisher_.publish(msg)
        # if FANUCethernetipDriver.DEBUG:
        # 	self.get_logger().info('Publishing: ' % msg.open)


def main(args=None):
    rclpy.init(args=args)

    publisher = check_grip()

    rclpy.spin(publisher)

    publisher.destroy_node()
    rclpy.shutdown()
    
if __name__ == '__main__':
    main()
    

