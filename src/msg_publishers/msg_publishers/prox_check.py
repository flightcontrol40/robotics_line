#!/usr/bin/env python3
import os
import sys

import dependencies.FANUCethernetipDriver as FANUCethernetipDriver
import rclpy
from dependencies.robot_controller import robot
from fanuc_interfaces.msg import ProxReadings
from rclpy.node import Node

FANUCethernetipDriver.DEBUG = False

sys.path.append('./pycomm3/pycomm3')

ROBOT_NAME = 'beaker'
ROBOT_IP = '172.29.208.124'

class check_prox(Node):
    def __init__(self):
        super().__init__('prox_pub')

        self.bot = robot(ROBOT_IP)
        self.publisher_ = self.create_publisher(ProxReadings, f"{ROBOT_NAME}/prox_readings", 10)
        timer_period = 0.1
        self.timer = self.create_timer(timer_period, self.timer_callback)

    def timer_callback(self):
        msg = ProxReadings()                                          
        msg.left = bool(self.bot.conveyor_proximity_sensor("left")) 
        msg.right = bool(self.bot.conveyor_proximity_sensor("right"))        
        self.publisher_.publish(msg)
        if FANUCethernetipDriver.DEBUG:
        	self.get_logger().info('Publishing: ' % msg.left,' ',msg.right)


def main(args=None):
    rclpy.init(args=args)

    publisher = check_prox()

    rclpy.spin(publisher)

    publisher.destroy_node()
    rclpy.shutdown()
    
if __name__ == '__main__':
    main()
    
