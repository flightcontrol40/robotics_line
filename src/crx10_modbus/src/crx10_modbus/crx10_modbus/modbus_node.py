import asyncio

import rclpy
from fanuc_interfaces.msg import CurCartesian, CurGripper
from rclpy.node import Node

from crx10_modbus.modbus import CRX10ModbusServer, PosData
from robot_3_interfaces.msg import RobotStatus
# from pymodbus.payload import BinaryPayloadBuilder

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
            qos_profile=10,
            callback=self._update_pos,
            
        )
        self._gripper_sub = self.create_subscription(
            CurGripper,
            f'/{robot_name}/grip_status',
            qos_profile=10,

            callback=self._update_gripper,
        )
        self._robot_status_sub = self.create_subscription(
            RobotStatus,
            f'/{robot_name}/robot_status',
            qos_profile=10,
            callback=self._update_robot_status,
        )

    def _update_pos(self, pos: CurCartesian):
        self.get_logger().info(f'Got Pos: {pos.pose}')
        pos.pose
        encode_pos = self.server.mapper.convert_to_registers(
            list(pos.pose),
            data_type=self.server.mapper.DATATYPE.FLOAT32
        )
        self.get_logger().info(f'encoded values: {encode_pos}')

        self.server.mapper.ir.setValues(3001, encode_pos)
        
        # self.server.mapper.position = PosData(pos.pose)

    def _update_gripper(self, grip: CurGripper):
        self.get_logger().info(f'Got Gripper State: {grip.open}')

        if grip.open:
            grip_encode = self.server.mapper.convert_to_registers(
                [1],
                data_type=self.server.mapper.DATATYPE.BITS
            )
            self.server.mapper.di.setValues(3004, grip_encode)
        else:
            grip_encode = self.server.mapper.convert_to_registers(
                [0],
                data_type=self.server.mapper.DATATYPE.BITS
            )
            self.server.mapper.di.setValues(3004, grip_encode)


    def _update_robot_status(self, status: RobotStatus):
        self.get_logger().info(f'Got robot State: {status}')
        encode = self.server.mapper.convert_to_registers(
            [
                status.process_state,
                status.error_code,
                1 if status.die_qa else 0,
                1 if status.r2_handoff else 0
            ],
            data_type=self.server.mapper.DATATYPE.UINT16
        )
        self.server.mapper.ir.setValues(3013, encode)



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
        rclpy.spin_once(node)
        await asyncio.sleep(1e-4)

if __name__ == "__main__":
    main()



