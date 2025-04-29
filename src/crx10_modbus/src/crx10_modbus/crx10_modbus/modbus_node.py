import asyncio

import rclpy
from fanuc_interfaces.msg import CurCartesian, CurGripper
from rclpy.node import Node

from crx10_modbus.modbus import CRX10ModbusServer, PosData
from robot_3_interfaces.msg import RobotStatus

name = 'beaker'
ip = '172.29.208.124'

class ModbusServer(Node):

    def __init__(self):
        super().__init__('ModbusServer')
        self.server = CRX10ModbusServer()
        robot_name = name
        self._pos_sub = self.create_subscription(
            CurCartesian,
            f'/{robot_name}/cur_cartesian',
            callback=self._update_pos,
        )
        self._gripper_sub = self.create_subscription(
            CurCartesian,
            f'/{robot_name}/grip_status',
            callback=self._update_gripper,
        )
        self._robot_status_sub = self.create_subscription(
            RobotStatus,
            f'/{robot_name}/robot_status',
            callback=self._update_robot_status,
        )

    def _update_pos(self, pos: CurCartesian):
        self.get_logger().debug(f'Got Pos: {pos.pose}')
        self.server.mapper.position = PosData(pos.pose)

    def _update_gripper(self, grip: CurGripper):
        self.get_logger().debug(f'Got Gripper State: {grip.open}')
        if grip.open:
            self.server.mapper.gripper = "open"
        else:
            self.server.mapper.gripper = "close"

    def _update_robot_status(self, status: RobotStatus):
        self.server.mapper.robot_status = status

def main():
    rclpy.init()
    node = ModbusServer()
    future = asyncio.wait([ros_loop(node), modbus_loop(node.server)])
    asyncio.get_event_loop().run_until_complete(future)

    node.destroy_node()
    rclpy.shutdown()

async def modbus_loop(server: CRX10ModbusServer):
    server.init_server()
    await server.server.serve_forever()

async def ros_loop(node: "ModbusServer"):
    print("Node started.")
    while rclpy.ok():
        rclpy.spin_once(node, timeout_sec=0)
        await asyncio.sleep(1e-4)

if __name__ == "__main__":
    main()



