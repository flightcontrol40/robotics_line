#!/usr/bin/env python3
import sys
import os
import rclpy

import dependencies.FANUCethernetipDriver as FANUCethernetipDriver

from dependencies.robot_controller import robot
from fanuc_interfaces.action import OnRobotGripper
from rclpy.node import Node
from rclpy.action import ActionServer, GoalResponse, CancelResponse

FANUCethernetipDriver.DEBUG = False

sys.path.append('./pycomm3/pycomm3')


class onrobot_gripper_server(Node):
    def __init__(self):
        super().__init__('onrobot_gripper_server')

        self.declare_parameters(
            namespace='',
            parameters=[('robot_ip','172.29.208.0'),
                        ('robot_name','noNAME')] # custom, default
        )

        self.goal = OnRobotGripper.Goal()
        self.bot = robot(self.get_parameter('robot_ip').value)

        self._action_server = ActionServer(self, OnRobotGripper, f"{self.get_parameter('robot_name').value}/onrobot_gripper", 
                                        execute_callback = self.execute_callback, 
                                        goal_callback = self.goal_callback,
                                        cancel_callback = self.cancel_callback)

    def goal_callback(self, goal_request):
        """ Accepts or Rejects client request to begin Action """
        self.goal = goal_request 
        
        # Check that it recieved a valid goal
        if self.goal.width > 160 | self.goal.width < 0:
            self.get_logger().info(f'Width should be between [0,160], got: {self.goal.width}')
            return GoalResponse.REJECT
        if self.goal.force > 120 | self.goal.force < 0:
            self.get_logger().info(f'Force should be between [0,120], got: {self.goal.force}')
            return GoalResponse.REJECT
        else:
            self.get_logger().info('OnRobot goal recieved: '+ str(self.goal))
            return GoalResponse.ACCEPT
                
    def cancel_callback(self, goal_handle):
        """Accept or reject a client request to cancel an action."""
        if self.goal == None:
            self.get_logger().info('No goal to cancel...')
            return CancelResponse.REJECT
        else:
            self.get_logger().info('Received cancel request')
            goal_handle.canceled()
            return CancelResponse.ACCEPT

    async def execute_callback(self, goal_handle):
        # WIP: Add Try/Except to catch possible error
        self.bot.onRobot_gripper(self.goal.width, self.goal.force)
        
        goal_handle.succeed()
        result = OnRobotGripper.Result()
        result.success = True
        self.goal = OnRobotGripper.Goal() # Reset
        return result

    def destroy(self):
        self._action_server.destroy()
        super().destroy_node()


def main(args=None):
    rclpy.init()

    onrobot_gripper_action_server = onrobot_gripper_server()

    rclpy.spin(onrobot_gripper_action_server)

    onrobot_gripper_action_server.destroy()
    rclpy.shutdown()

if __name__ == '__main__':
    main()

