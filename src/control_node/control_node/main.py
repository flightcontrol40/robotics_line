import asyncio

import rclpy
from fanuc_interfaces.action import CartPose

from control_node.x_client import ActionClientX

rclpy.init()
node = rclpy.create_node('async_action_client')

async def control_loop():
    print('Node started.')
    action_client = ActionClientX(node, CartPose, '/beaker/cartesian_pose')
    goal_msg = CartPose.Goal()
    goal_msg.x = 525.809
    goal_msg.y =  -361.400
    goal_msg.z =  90.387
    goal_msg.w =  -93.223
    goal_msg.p =  -28.668
    goal_msg.r =  179.427
    async for (feedback, result) in action_client.send_goal_async(goal_msg):
        if feedback:
            print(f'Feedback: {feedback}')
        else:
            print(f'Result: {result}')
    print('Finished.')

async def ros_loop():
    while rclpy.ok():
        rclpy.spin_once(node, timeout_sec=0)
        await asyncio.sleep(1e-4)

def main():
    future = asyncio.wait([ros_loop(), control_loop()])
    asyncio.get_event_loop().run_until_complete(future)

# if __name__ == "__main__":
#     future = asyncio.wait([ros_loop(), main()])
#     asyncio.get_event_loop().run_until_complete(future)