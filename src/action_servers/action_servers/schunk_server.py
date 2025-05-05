#!/usr/bin/env python3
import asyncio
import os
import sys
import time

import dependencies.FANUCethernetipDriver as FANUCethernetipDriver
import rclpy
from dependencies.robot_controller import robot
from fanuc_interfaces.action import SchunkGripper
from rclpy.action import ActionServer, CancelResponse, GoalResponse
from rclpy.node import Node

FANUCethernetipDriver.DEBUG = False

sys.path.append("./pycomm3/pycomm3")

ROBOT_NAME = 'beaker'
ROBOT_IP = '172.29.208.124'

class schunk_gripper_server(Node):
    def __init__(self):
        super().__init__("schunk_gripper_server")


        self.goal = SchunkGripper.Goal()
        self.bot = robot(ROBOT_IP)

        self._action_server = ActionServer(
            self,
            SchunkGripper,
            f"{ROBOT_NAME}/schunk_gripper",
            execute_callback=self.execute_callback,
            goal_callback=self.goal_callback,
            cancel_callback=self.cancel_callback,
        )

    def goal_callback(self, goal_request):
        """Accepts or Rejects client request to begin Action"""
        self.goal = goal_request

        # Check that it received a valid goal
        if self.goal.command == "open" or self.goal.command == "close":
            self.get_logger().info("Schunk goal recieved: " + str(self.goal))
            return GoalResponse.ACCEPT
        else:
            self.get_logger().info(
                f"Invalid request, got: {self.goal.command} type: {type(self.goal.command)}"
            )
            return GoalResponse.REJECT

    def cancel_callback(self, goal_handle):
        """Accept or reject a client request to cancel an action."""
        if self.goal == None:
            self.get_logger().info("No goal to cancel...")
            return CancelResponse.REJECT
        else:
            self.get_logger().info("Received cancel request")
            goal_handle.canceled()
            return CancelResponse.ACCEPT

    async def execute_callback(self, goal_handle):
        # WIP: Add Try/Except to catch possible error
        self.bot.schunk_gripper(self.goal.command)
        goal_handle.succeed()
        result = SchunkGripper.Result()
        result.success = True
        self.goal = SchunkGripper.Goal()  # Reset
        asyncio.run(wait())

        return result

    def destroy(self):
        self._action_server.destroy()
        super().destroy_node()


async def wait():
    await asyncio.sleep(0.5)

def main(args=None):
    rclpy.init()

    schunk_gripper_action_server = schunk_gripper_server()

    rclpy.spin(schunk_gripper_action_server)

    schunk_gripper_action_server.destroy()
    rclpy.shutdown()


if __name__ == "__main__":
    main()
