"""
 This is a test of all the actions and (if added) their feedbacks
 https://github.com/UofI-CDACS/fanuc_ros2_drivers
"""
# ROS packages
from time import sleep

import rclpy
from action_msgs.msg import GoalStatus

# Fanuc packages
from fanuc_interfaces.action import (
    CartPose,
    Conveyor,
    JointPose,
    SchunkGripper,
    SJointPose,
)
from fanuc_interfaces.srv import SetSpeed
from rclpy.action.client import ActionClient
from rclpy.node import Node

namespace = 'beaker'


class FanucActions(Node):
    def __init__(self, namespace):
        super().__init__("robot")
        # Actions
        self.cart_ac = ActionClient(self, CartPose, f'/{namespace}/cartesian_pose')
        self.convey_ac = ActionClient(self, Conveyor, f'/{namespace}/conveyor')
        self.joints_ac = ActionClient(self, JointPose, f'/{namespace}/joint_pose')
        self.schunk_ac = ActionClient(self, SchunkGripper, f'/{namespace}/schunk_gripper')
        self.sin_joint_ac = ActionClient(self, SJointPose, f'/{namespace}/single_joint_pose')
        self.speed_sc = self.create_client(SetSpeed, f'{namespace}/set_speed')
        request = SetSpeed.Request()
        request.speed = 250
        while not self.speed_sc.wait_for_service(timeout_sec=1.0):
            pass # Wait for service to be ready
        print("Service ready, sending request")
        future = self.speed_sc.call_async(request)
        while rclpy.ok():
            rclpy.spin_once(self)
            if future.done():
                self.get_logger().info('Set Speed to %d mm/s' % 250)
                break

    # def home(self):
    #     print("Moving to home position")
    #     self.send_goal(self.joints_ac, HOME_POS, True)
    #     sleep(5)

    # def dice(self):
    #     print("Moving to Dice position")
    #     self.send_goal(self.joints_ac, DICE_POS,True)
    #     sleep(5)

    # def new_pos(self):
    #     print("Moving to new position")
    #     self.send_goal(self.joints_ac, NEW_POS,True)
    #     sleep(5)

    def schunk_open(self):
        print("opening Schunk ")
        schunk_goal = SchunkGripper.Goal()
        schunk_goal.command = 'open'
        self.get_logger().info('Sending goal request...')
        self.send_goal(self.schunk_ac, schunk_goal)
        sleep(2)

    def schunk_close(self):
        print("closeing Schunk ")
        schunk_goal = SchunkGripper.Goal()
        schunk_goal.command = "close"
        self.get_logger().info('Sending goal request...')
        self.send_goal(self.schunk_ac, schunk_goal)
        sleep(2)

    def goal_response_callback(self, future):
        goal_handle = future.result()
        if not goal_handle.accepted:
            self.get_logger().info('Goal rejected :(')
            return
        self.get_logger().info('Goal accepted :)')
        self._get_result_future = goal_handle.get_result_async()
        self._get_result_future.add_done_callback(self.get_result_callback)

    def feedback_callback(self, feedback):
        self.get_logger().info('Received feedback: {0}'.format(feedback.feedback.sequence))

    def get_result_callback(self, future):
        result = future.result().result
        status = future.result().status
        print(result)
        print(dir(result))
        if status == GoalStatus.STATUS_SUCCEEDED:
            self.get_logger().info('Goal succeeded! Result: {0}'.format(result.success))
        else:
            self.get_logger().info('Goal failed with status: {0}'.format(status))
        # Shutdown after receiving a result
        rclpy.shutdown()



    def send_goal(self, handler, goal, wait=True):
        self.get_logger().info('Waiting for action server...')
        handler.wait_for_server()
        self.get_logger().info('Sending goal request...')
        send_goal_future = handler.send_goal_async(
            goal,
            feedback_callback=self.feedback_callback)
        send_goal_future.add_done_callback(self.goal_response_callback)
        if wait:
            while not send_goal_future.done:
                pass

if __name__ == '__main__':
    rclpy.init()
    fanuc = FanucActions(namespace)
    fanuc.schunk_open()
    # fanuc.home()
    # fanuc.dice()
    fanuc.schunk_close()
    # fanuc.home()
    # fanuc.new_pos()
    fanuc.schunk_open()
    # fanuc.home()