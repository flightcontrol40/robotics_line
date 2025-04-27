"""
 This is a test of all the actions and (if added) their feedbacks
 https://github.com/UofI-CDACS/fanuc_ros2_drivers
"""
# ROS packages
import asyncio
import random
from copy import copy
from dataclasses import dataclass
from enum import Enum
from queue import Queue
from typing import Any

import cv2
import fanuc_interfaces  # noqa: F401
import numpy as np
import rclpy
import rclpy.service
import yaml
from action_msgs.msg import GoalStatus
from cv_bridge import CvBridge

# Fanuc packages
from fanuc_interfaces.action import (
    CartPose,
    Conveyor,
    JointPose,
    SchunkGripper,
)
from fanuc_interfaces.msg import ProxReadings
from fanuc_interfaces.srv import SetSpeed
from rclpy.action.client import ActionClient
from rclpy.node import Node
from sensor_msgs.msg import Image
from std_msgs.msg import Bool, String

from robot_3_interfaces.msg import RobotStatus as FanucStatus
from sbot_interfaces.msg import RobotStatus  # noqa: F401

R2_STATUS_TOPIC = "/Robot2/Status"
POSITIONS_FILE = "pos_2.yaml"
NAMESPACE = 'beaker'
CONV1_TOPIC = f"/{NAMESPACE}/prox_readings"
R4_CONV_TOPIC = "/bunsen/dice_sent"
CAMERA_IMAGE_TOPIC = "/camera_driver/vis/image_raw"
POSITIONS = {}

with open(POSITIONS_FILE, "r") as fd:
    POSITIONS = yaml.safe_load(fd)

JOINT_NAMES = [ "joint1", "joint2", "joint3", "joint4", "joint5", "joint6"]
CART_NAMES = [ "x", "y", "z", "w", "p", "r" ]
BLANK_IMAGE = np.zeros((1024,1000,3), np.uint8)


def get_pos_goal(name: str, joint:bool = True)-> JointPose.Goal|CartPose.Goal:
    """Returns a Goal for movement"""
    if not joint:
        name = name + "_cart"

    cords = POSITIONS.get(name, None)
    if cords is None:
        raise ValueError(f"Position {name} Does not exist!")
    if joint:
        kwargs = dict(zip(JOINT_NAMES,cords))
        return JointPose.Goal(**kwargs)
    else:
        kwargs = dict(zip(CART_NAMES,cords))
        return CartPose.Goal(**kwargs)


class ErrorState(Enum):
    OK = 0
    ERROR = 1

class CurrentState(Enum):
    """Robot States"""
    E_STOP              =-1
    WAITING_FOR_HANDOFF = 0
    MOVING_TO_HANDOFF   = 1
    IN_HANDOFF          = 2
    MOVE_TO_CONV1       = 3
    SEND_TO_R4          = 5
    WAIT_FOR_CONV1      = 6
    WAITING_FOR_R4_CONV = 7
    MOVE_TO_QA          = 8
    QA                  = 9
    QA_PASS             = 10
    QA_FAIL             = 11
    RANDOM_PLACE        = 12

class OrderType(Enum):
    """Order Types"""
    MOVE_JOINT = "joints_ac"
    MOVE_CART = "cart_ac"
    MOVE_CONVEYOR = "convey_ac"
    GRIPPER = "schunk_ac"
    SET_SPEED = "speed_sc"

@dataclass
class Order:
    """Order to be processed"""
    order_type: OrderType
    args: Any

class ControlNode(Node):
    def __init__(self, namespace):
        super().__init__("robot")
        # Robot Control Types
        self.cart_ac = ActionClient(self, CartPose, f'/{namespace}/cartesian_pose')
        self.convey_ac = ActionClient(self, Conveyor, f'/{namespace}/conveyor')
        self.joints_ac = ActionClient(self, JointPose, f'/{namespace}/joint_pose')
        self.schunk_ac = ActionClient(self, SchunkGripper, f'/{namespace}/schunk_gripper')
        self.speed_sc = self.create_client(SetSpeed, f'{namespace}/set_speed')
        
        # Robot State Vars
        self._current_step = CurrentState.WAITING_FOR_HANDOFF
        self.processing_command = False
        self.r2_status = RobotStatus(state=-1)
        self.prox_readings = ProxReadings(right=0, left=0)
        self.qa_image: cv2.typing.MatLike = BLANK_IMAGE

        # Control Structures
        self.order_queue: Queue[Order] = Queue()
        self._order_timer = self.create_timer(
            0.0001,
            callback=self._process_commands,
        )
        self._qa_pass = 0
        self._read_qa = False
        self._last_img_cls = ""
        self._qa_img = None
        self._error_state = ErrorState.OK
        self._state_timer = self.create_timer(
            0.0001,
            callback=self._check_state,
        )
        self.create_subscription(
            RobotStatus,
            R2_STATUS_TOPIC,
            self._robot_status_callback,
            10
        )
        self.create_subscription(
            ProxReadings,
            CONV1_TOPIC,
            self.conveyer_sensor_callback,
            10
        )
        self.create_subscription(
            Bool,
            R4_CONV_TOPIC,
            self._r4_conv_callback,
            10
        )
        self.create_subscription(
            String,
            f'/{self.get_parameter('robot_name').value}/qa/status',
            self._qa_status_callback,
            10
        )
        self.create_subscription(
            Image,
            f'/{self.get_parameter('robot_name').value}/qa/img',
            self._qa_image_callback,
            10
        )

        self._state_pub = self.create_publisher(
            FanucStatus,
            f"/{namespace}/robot_state",
            10
        )
        self.bridge = CvBridge()


    def _qa_status_callback(self, cls: String):
        self._last_img_cls = cls.data

    def _qa_image_callback(self, img: Image):
        self.qa_image = self.bridge.imgmsg_to_cv2(img)

    @property
    def current_step(self) -> CurrentState:
        return self._current_step

    @current_step.setter
    def current_step(self, value: CurrentState):
        if not isinstance(value, CurrentState):
            raise ValueError(f"Invalid State {value}")
        self._current_step = value
        self._publish_robot_status()

        # self._state_pub.publish(
        #     String(data=f"Current State: {self._current_step.name}")
        # )

    @property
    def dice_qa_state(self):
        return self._qa_pass

    @dice_qa_state.setter
    def _update_qa(self, state):
        self._qa_pass = state
        self._publish_robot_status()

    @property
    def error_state(self):
        return self._error_state

    @error_state.setter
    def _update_error(self, state: ErrorState):
        self._error_state = state
        self._publish_robot_status()

    def _publish_robot_status(self):
        state = FanucStatus(
            dice_qa = bool(self.dice_qa_state),
            error_code= self.error_state.value,
            error_status= 0 if self.error_state == ErrorState.OK else 1,
            process_state = self.current_step.value,
            r2_handoff = 1 if self._current_step == CurrentState.IN_HANDOFF else 0
        )
        self._state_pub.publish(state)

    def _robot_status_callback(self, msg: RobotStatus):
        self.r2_status = msg
        self.get_logger().debug(f"R2 Status: {self.r2_status.state}")

    def _check_state(self):
        self._state_pub.publish(
            String(data=f"Current State: {self._current_step.name}")
        )
        if self.current_step == CurrentState.E_STOP:
            self.order_queue.queue.clear()
            return
        elif self.current_step == CurrentState.WAITING_FOR_HANDOFF:
            # Read r2 status
            if self.r2_status == 8:
                # R2 is ready to handoff
                self.get_logger().info("Initializing handoff")

                order = Order(
                    order_type=OrderType.MOVE_JOINT,
                    args=get_pos_goal("handoff_off")
                )
                self.order_queue.put(order)
                self.current_step = CurrentState.MOVING_TO_HANDOFF
                return
        elif self.current_step == CurrentState.MOVING_TO_HANDOFF:
            # Wait for orders to complete
            if self.order_queue.empty():
                # R2 is ready to handoff
                self.get_logger().info("Grabbing the dice from R2")
                order = Order(
                    order_type=OrderType.MOVE_JOINT,
                    args=get_pos_goal("handoff")
                )
                self.order_queue.put(order)
                grab_order = Order(
                    name="schunk",
                    order_type=OrderType.GRIPPER,
                    args=SchunkGripper.Goal(command="close")
                )
                self.order_queue.put(grab_order)
                self.current_step = CurrentState.IN_HANDOFF
                return
        elif self.current_step == CurrentState.IN_HANDOFF:
            # Wait for orders to complete
            if not self.order_queue.empty():
                return
            # At this point We are gripping the dice and waiting for
            # R2 to send the signal that it has let go
            if self.r2_status != 8 and self.r2_status != 9: # 9 is error
                self.current_step = CurrentState.MOVE_TO_CONV1
                return
        elif self.current_step == CurrentState.MOVE_TO_CONV1:
            # Wait for moves to complete
            if not self.order_queue.empty():
                return
            self.get_logger().info("Sending dice to R4")
            order = Order(
                order_type=OrderType.MOVE_JOINT,
                args=get_pos_goal("handoff_off")
            )
            self.order_queue.put(order)
            order = Order(
                order_type=OrderType.MOVE_JOINT,
                args=get_pos_goal("AboveConv1")
            )
            self.order_queue.put(order)
            order = Order(
                order_type=OrderType.MOVE_JOINT,
                args=get_pos_goal("Conv1Place")
            )
            self.order_queue.put(order)
            order = Order(
                order_type=OrderType.GRIPPER,
                args=SchunkGripper.Goal(command="open")
            )
            self.order_queue.put(order)
            order = Order(
                order_type=OrderType.MOVE_CART,
                args=get_pos_goal("Conv1AfterPlace", joint=False)
            )
            self.order_queue.put(order)
            self.current_step = CurrentState.SEND_TO_R4
        elif self.current_step == CurrentState.SEND_TO_R4:
            # Wait for moves to complete
            if not self.order_queue.empty():
                return
            # Send the dice to R4
            self.get_logger().info("Sending dice to R4")
            order = Order(
                order_type=OrderType.MOVE_CONVEYOR,
                args=Conveyor.Goal(command="forward")
            )
            self.order_queue.put(order)
            # Move to conveyor 2
            order = Order(
                order_type=OrderType.MOVE_JOINT,
                args=get_pos_goal("Conv2Block")
            )
            self.order_queue.put(order)

            pass
        elif self.current_step == CurrentState.MOVE_TO_QA:
            if not self.order_queue.empty():
                return
            # Pick up the dice off the conveyor
            self.get_logger().info("Picking up the dice off the conveyor, Moving to QA")
            order = Order(
                order_type=OrderType.MOVE_JOINT,
                args=get_pos_goal("Conv2AfterBlock")
            )
            self.order_queue.put(order)
            order = Order(
                order_type=OrderType.MOVE_JOINT,
                args=get_pos_goal("Conv2BeforeGrab")
            )
            self.order_queue.put(order)
            order = Order(
                order_type=OrderType.MOVE_JOINT,
                args=get_pos_goal("Conv2Grab")
            )
            self.order_queue.put(order)
            order = Order(
                order_type=OrderType.GRIPPER,
                args=SchunkGripper.Goal(command="close")
            )
            order = Order(
                order_type=OrderType.MOVE_JOINT,
                args=get_pos_goal("Conv2BeforeGrab")
            )
            self.order_queue.put(order)
            # Move to QA Position
            order = Order(
                order_type=OrderType.MOVE_JOINT,
                args=get_pos_goal("scanPos")
            )
            pass
        elif self.current_step == CurrentState.QA:
            # Wait for orders to complete
            if not self.order_queue.empty():
                return
            # Check the image QA class
            if self._last_img_cls == "three":
                self._qa_pass = 1
                self.current_step = CurrentState.QA_PASS
            else: 
                self._qa_pass = 0
                self.current_step = CurrentState.QA_FAIL

        elif self.current_step == CurrentState.QA_PASS:
            # QA has passed, Place the dice
            self.get_logger().info("QA Pass, Moving to random place")
            order = Order(
                order_type=OrderType.MOVE_JOINT,
                args=get_pos_goal("RandomPlaceCenter")
            )
            self.order_queue.put(order)
            pos = copy(POSITIONS["RandomPlaceCenter_cart"])
            pos[0] += (random.random - 0.5) * 50
            pos[1] += (random.random - 0.5) * 50
            POSITIONS["RandomPlace_cart"] = pos
            order = Order(
                order_type=OrderType.MOVE_CART,
                args=get_pos_goal("RandomPlace_cart")
            )
            order = Order(
                order_type=OrderType.GRIPPER,
                args=SchunkGripper.Goal(command="open")
            )
            self.order_queue.put(order)
            pos[2] += 100
            POSITIONS["RandomPlaceAfter_cart"] = pos
            order = Order(
                order_type=OrderType.MOVE_CART,
                args=get_pos_goal("RandomPlaceAfter_cart")
            )
        elif self.current_step == CurrentState.QA_FAIL:
            # TODO: Add Rotate Dice Code
            # QA has failed,
            self.get_logger().info("QA Fail")
            pass
        elif self.current_step == CurrentState.RANDOM_PLACE:
            # Wait for orders to complete
            if not self.order_queue.empty():
                return
            self.current_step = CurrentState.WAITING_FOR_HANDOFF
            pass
        else:
            raise ValueError(f"Invalid State {self.current_step}")

    async def conveyer_sensor_callback(self, msg: ProxReadings):
        self.prox_readings = msg
        if msg.right == 1:
            if self.current_step == CurrentState.SEND_TO_R4:
                # wait for 1 second then stop the conveyor
                asyncio.sleep(1)
                self.get_logger().info("Stopping conveyor")
                order = Order(
                    order_type=OrderType.MOVE_CONVEYOR,
                    args=Conveyor.Goal(command="stop")
                )
                self.order_queue.put(order)
                self.current_step = CurrentState.WAITING_FOR_R4_CONV

    # TODO: Update this to get the actual interface from r4
    async def _r4_conv_callback(self, msg: Bool):
        if msg.data:
            self.get_logger().info("R4 has sent the dice back")
            if self.current_step == CurrentState.WAITING_FOR_R4_CONV:
                self.current_step = CurrentState.MOVE_TO_QA

    def _process_commands(self):
        if self.order_queue.empty():
            return
        if self.processing_command:
            return
        self.processing_command = True
        new_order = self.order_queue.get()
        if not hasattr(self, new_order.order_type.value):
            raise KeyError("Invalid Order Name")
        caller: ActionClient = getattr(self, new_order.order_type.value)
        self.send_goal(caller, new_order.args)

    def goal_response_callback(self, future):
        goal_handle = future.result()
        if not goal_handle.accepted:
            self.get_logger().info('Goal rejected :(')
            self.processing_command = False
            return
        self.get_logger().info('Goal accepted :)')
        get_result_future = goal_handle.get_result_async()
        get_result_future.add_done_callback(self.get_result_callback)

    def feedback_callback(self, feedback):
        self.get_logger().info('Received feedback: {0}'.format(feedback.feedback.sequence))

    def get_result_callback(self, future):
        result = future.result().result
        status = future.result().status
        if status == GoalStatus.STATUS_SUCCEEDED:
            self.get_logger().debug('Goal succeeded! Result: {0}'.format(result.success))
        else:
            self.get_logger().debug('Goal failed with status: {0}'.format(status))
        self.processing_command = False

    def send_goal(self, handler, goal, wait=True):
        self.get_logger().info('Waiting for action server...')
        handler.wait_for_server()
        self.get_logger().info('Sending goal request...')
        send_goal_future = handler.send_goal_async(
            goal,
            feedback_callback=self.feedback_callback
        )
        send_goal_future.add_done_callback(self.goal_response_callback)

async def ros_loop(node):
    while rclpy.ok():
        rclpy.spin_once(node, timeout_sec=0)
        await asyncio.sleep(1e-4)

def main():
    rclpy.init()
    node = ControlNode(NAMESPACE)

    future = asyncio.wait([ros_loop(node)])
    asyncio.get_event_loop().run_until_complete(future)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
    # fanuc = ControlNode(NAMESPACE)
    # fanuc.schunk_open()
    # # fanuc.home()
    # # fanuc.dice()
    # fanuc.schunk_close()
    # # fanuc.home()
    # # fanuc.new_pos()
    # fanuc.schunk_open()
    # # fanuc.home()