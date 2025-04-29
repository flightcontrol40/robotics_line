"""


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
import numpy as np
import rclpy
from rclpy.client import Client as ServiceClient
import yaml
from action_msgs.msg import GoalStatus
from ament_index_python.packages import get_package_share_directory
from cv_bridge import CvBridge
import rclpy.task
from robot_3_interfaces.srv import QaDice

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

share_dir = get_package_share_directory("control_node")

ROBOT_NAME = 'beaker'
ROBOT_IP = '172.29.208.124'
R2_STATUS_TOPIC = "/dave/Status"
POSITIONS_FILE = share_dir +"/data/pos2.yaml"
CONV1_TOPIC = f"/{ROBOT_NAME}/prox_readings"
R4_CONV_TOPIC = "/bunsen/dice_sent"
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
    def __init__(self):
        super().__init__("robot")
        self.robot_name = ROBOT_NAME
        # Robot Control Types
        self.cart_ac = ActionClient(self, CartPose, f'/{self.robot_name}/cartesian_pose')
        self.convey_ac = ActionClient(self, Conveyor, f'/{self.robot_name}/conveyor')
        self.joints_ac = ActionClient(self, JointPose, f'/{self.robot_name}/joint_pose')
        self.schunk_ac = ActionClient(self, SchunkGripper, f'/{self.robot_name}/schunk_gripper')
        self.speed_sc = self.create_client(SetSpeed, f'{self.robot_name}/set_speed')

        # Robot State Vars
        self._current_step = CurrentState.WAITING_FOR_HANDOFF
        self._processing_command = False
        self.r2_status = RobotStatus(state=-1)
        self.prox_readings = ProxReadings(right=False, left=False)
        self.qa_image: cv2.typing.MatLike = BLANK_IMAGE

        # Control Structures
        self.order_queue: Queue[Order] = Queue()
        self._order_timer = self.create_timer(
            0.1,
            callback=self._process_commands,
        )
        self._qa_pass = False
        self._qa_image = BLANK_IMAGE
        self._qa_class = ""
        self.qa_complete = True
        self._error_state = ErrorState.OK
        self._state_timer = self.create_timer(
            0.5,
            callback=self._check_state,
        )
        self._img_timer = self.create_timer(
            0.5,
            callback=self._show_img,
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
        self._state_pub = self.create_publisher(
            FanucStatus,
            f"/{self.robot_name}/robot_state",
            10
        )
        self.bridge = CvBridge()
        self._dice_client = self.create_client(srv_type=QaDice, srv_name=f"/{self.robot_name}/qa_dice")
        order = Order(
            order_type=OrderType.MOVE_JOINT,
            args=get_pos_goal("Home")
        )
        self.order_queue.put(order)
        order  = Order(
            order_type=OrderType.MOVE_CONVEYOR,
            args=Conveyor.Goal(command="stop")
        )
        self.order_queue.put(order)
        cv2.namedWindow("QA Result", cv2.WINDOW_NORMAL)
        self.dice_qa_state = False
        self._doing_qa = False

    def _show_img(self):
        if not self._doing_qa:
            self._doing_qa = True
            self.get_logger().info("QA Request")
            self._dice_client.wait_for_service()
            future = self._dice_client.call_async(QaDice.Request())
            future.add_done_callback(self._qa_callback)
        cv2.imshow("QA Result", self.qa_image)
        cv2.waitKey(1)

    def _qa_callback(self, future: rclpy.task.Future):
        self.get_logger().info("QA Resp")
        resp: QaDice.Response = future.result()
        self._qa_class = resp.obj_cls
        self.qa_image = self.bridge.imgmsg_to_cv2(resp.qa_image)
        self.get_logger().info(f"QA Class: {self._qa_class}")
        self.qa_complete = True
        self._doing_qa = False
        if self.current_step == CurrentState.QA:
            if self._qa_class == "three":
                self.dice_qa_state = True
                self.current_step = CurrentState.QA_PASS
            else:
                self.dice_qa_state = False
                self.current_step = CurrentState.QA_FAIL


    @property
    def current_step(self) -> CurrentState:
        return self._current_step

    @current_step.setter
    def current_step(self, value: CurrentState):
        if not isinstance(value, CurrentState):
            raise ValueError(f"Invalid State {value}")
        self._current_step = value
        self._publish_robot_status()

    @property
    def dice_qa_state(self):
        return self._qa_pass

    @dice_qa_state.setter
    def dice_qa_state(self, state:bool):
        self._qa_pass = state
        self._publish_robot_status()

    @property
    def error_state(self):
        return self._error_state

    @error_state.setter
    def error_state(self, state: ErrorState):
        self._error_state = state
        self._publish_robot_status()

    def _publish_robot_status(self):
        state = FanucStatus(
            die_qa = bool(self.dice_qa_state),
            error_code= self.error_state.value,
            error_status= False if self.error_state == ErrorState.OK else True,
            process_state = self.current_step.value,
            r2_handoff = True if self._current_step == CurrentState.IN_HANDOFF else False
        )
        self._state_pub.publish(state)

    def _robot_status_callback(self, msg: RobotStatus):
        """Callback for robot 2 status"""
        self.r2_status = msg
        self.get_logger().info(f"R2 Status: {self.r2_status.state}")

    def _check_state(self):
        self._state_pub.publish(
            FanucStatus(
                die_qa = self.dice_qa_state,
                error_code= self.error_state.value,
                error_status= True if self.error_state == ErrorState.OK else False,
                process_state = self.current_step.value,
                r2_handoff = True if self._current_step == CurrentState.IN_HANDOFF else False
            )
        )
        if self.current_step == CurrentState.E_STOP:
            while self.order_queue.qsize():
                self.order_queue.get()
            self.get_logger().info("Stopping all orders")
            return

        elif self.current_step == CurrentState.WAITING_FOR_HANDOFF:
            if self.processing_command:
                return
            # Read r2 status
            if self.r2_status.state == 8:
                # R2 is ready to handoff
                self.get_logger().info("Initializing handoff")
                grab_order = Order(
                    order_type=OrderType.GRIPPER,
                    args=SchunkGripper.Goal(command="open")
                )
                self.order_queue.put(grab_order)
                order = Order(
                    order_type=OrderType.MOVE_JOINT,
                    args=get_pos_goal("handoff_offset")
                )
                self.order_queue.put(order)
                self.current_step = CurrentState.MOVING_TO_HANDOFF
                return
        elif self.current_step == CurrentState.MOVING_TO_HANDOFF:
            # Wait for orders to complete
            if self.processing_command:
                return

            # R2 is ready to handoff
            self.get_logger().info("Grabbing the dice from R2")
            order = Order(
                order_type=OrderType.MOVE_JOINT,
                args=get_pos_goal("handoff")
            )
            self.order_queue.put(order)
            grab_order = Order(
                order_type=OrderType.GRIPPER,
                args=SchunkGripper.Goal(command="close")
            )
            self.order_queue.put(grab_order)
            self.current_step = CurrentState.IN_HANDOFF
            return
        elif self.current_step == CurrentState.IN_HANDOFF:
            # Wait for orders to complete
            if self.processing_command:
                return
            # At this point We are gripping the dice and waiting for
            # R2 to send the signal that it has let go
            if self.r2_status.state != 8 and self.r2_status.state != 9: # 9 is error
                self.current_step = CurrentState.MOVE_TO_CONV1
                return
        elif self.current_step == CurrentState.MOVE_TO_CONV1:
            # Wait for moves to complete
            if self.processing_command:
                return
            self.get_logger().info("Sending dice to R4")
            order = Order(
                order_type=OrderType.MOVE_JOINT,
                args=get_pos_goal("handoff_offset")
            )
            self.order_queue.put(order)
            order = Order(
                order_type=OrderType.MOVE_JOINT,
                args=get_pos_goal("intermediate")
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
            # Move to conveyor 2
            order = Order(
                order_type=OrderType.MOVE_JOINT,
                args=get_pos_goal("Conv2Block")
            )
            self.order_queue.put(order)
            self.current_step = CurrentState.SEND_TO_R4
        elif self.current_step == CurrentState.SEND_TO_R4:
            # Wait for moves to complete
            if self.processing_command:
                return

            # Send the dice to R4
            self.get_logger().info("Sending dice to R4")
            order = Order(
                order_type=OrderType.MOVE_CONVEYOR,
                args=Conveyor.Goal(command="forward")
            )
            self.order_queue.put(order)

            self.current_step = CurrentState.WAIT_FOR_CONV1
            pass
        elif self.current_step == CurrentState.WAIT_FOR_CONV1:
            pass
        elif self.current_step == CurrentState.WAITING_FOR_R4_CONV:
            pass
        elif self.current_step == CurrentState.MOVE_TO_QA:
            if self.processing_command:
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
            self.order_queue.put(order)
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
            self.order_queue.put(order)
            self.current_step = CurrentState.QA
        elif self.current_step == CurrentState.QA:
            # Wait for orders to complete
            if self.processing_command:
                return
            if self.qa_complete:
                # Send QA Service
                self.qa_complete = False
                self._dice_client.wait_for_service()
                future = self._dice_client.call_async(QaDice.Request())
                future.add_done_callback(self._qa_callback)

        elif self.current_step == CurrentState.QA_PASS:
            if self.processing_command:
                return

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
            if self.processing_command:
                return

            # QA has failed,
            self.get_logger().info("QA Fail")
            pass
        elif self.current_step == CurrentState.RANDOM_PLACE:
            # Wait for orders to complete
            if self.processing_command:
                return

            self.current_step = CurrentState.WAITING_FOR_HANDOFF
            pass
        else:
            raise ValueError(f"Invalid State {self.current_step}")

    async def conveyer_sensor_callback(self, msg: ProxReadings):
        self.prox_readings = msg
        if msg.right:
            if self.current_step == CurrentState.WAIT_FOR_CONV1:
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

    @property
    def processing_command(self):
        if self.order_queue.empty() and not self._processing_command:
            return False
        return True

    def _process_commands(self):
        if self.order_queue.empty():
            return
        if self._processing_command:
            return
        try:
            self._processing_command = True
            new_order = self.order_queue.get()
        except Exception as e:
            self.get_logger().error(f"Error getting order: {e}")
            self._processing_command = False
            return
        # Check if the order is valid
        if not hasattr(self, new_order.order_type.value):
            raise KeyError("Invalid Order Name")
        self.get_logger().info("Processing command")
        self.get_logger().info(f"Order: {new_order.order_type.name}")
        self.get_logger().info(f"Args: {new_order.args}")
        caller: ActionClient|ServiceClient = getattr(self, new_order.order_type.value)
        if isinstance(caller, ActionClient):
            self.send_goal(caller, new_order.args)
        else:
            self.send_action(caller, new_order.args)

    def send_action(self, client: ServiceClient, srv):
        self.get_logger().info('Waiting for Service server...')
        client.wait_for_service()
        self.get_logger().info('Sending service request...')
        future = client.call_async(srv)
        future.add_done_callback(
            self.get_srv_callback
        )
        pass

    def get_srv_callback(self, future: rclpy.task.Future):
        result = future.result()
        if future.cancelled():
            self.get_logger().info('Service Canceled ')
        elif future.done():
            self.get_logger().info('Goal succeeded! Result: {0}'.format(result))
        self._processing_command = False

    def goal_response_callback(self, future):
        goal_handle = future.result()
        if not goal_handle.accepted:
            self.get_logger().info('Goal rejected :(')
            self._processing_command = False
            return
        self.get_logger().info('Goal accepted :)')
        get_result_future = goal_handle.get_result_async()
        get_result_future.add_done_callback(self.get_result_callback)

    def feedback_callback(self, feedback:JointPose.Feedback):
        self.get_logger().info('Received feedback: {0}'.format(feedback))

    def get_result_callback(self, future):
        result = future.result().result
        status = future.result().status
        if status == GoalStatus.STATUS_SUCCEEDED:
            self.get_logger().info('Goal succeeded! Result: {0}'.format(result))
        else:
            self.get_logger().info('Goal failed with status: {0}'.format(status))
        self._processing_command = False

    def send_goal(self, handler:ActionClient, goal, wait=True):
        self.get_logger().info('Waiting for action server...')
        handler.wait_for_server()
        self.get_logger().info('Sending goal request...')
        send_goal_future = handler.send_goal_async(
            goal,
            feedback_callback=self.feedback_callback
        )
        send_goal_future.add_done_callback(self.goal_response_callback)

def main():
    rclpy.init()
    node = ControlNode()

    while rclpy.ok():
        rclpy.spin_once(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()


#END
