#!/usr/bin/env python3
import asyncio
import logging

from pymodbus.constants import Endian  # noqa: F401
from pymodbus.device import ModbusDeviceIdentification
from pymodbus.logging import Log
from pymodbus.payload import BinaryPayloadBuilder, BinaryPayloadDecoder  # noqa: F401
from pymodbus.server import ModbusTcpServer

from data_block import (  # noqa: F401
    CRX10DiscreteInputs,
    CRX10InputRegisters,
    CRX10Mapper,
    PosData,
    convert_from_registers,
    convert_to_registers,
)

Log.setLevel(0)
_logger = logging.getLogger(__name__)
_logger.setLevel(0)


def read_robot_status() -> dict:
    return {}


test_address = [
    PosData(
        x=200.38920,
        y=150.2348,
        z=378.0932,
        p=180.09128,
        r=-0.44325,
        w=35.483204,
        t1=False,
        t2=False,
        t3=False,
    ),
    PosData(
        x=0.38920,
        y=246.2348,
        z=122.0932,
        p=-75.09128,
        r=-14.44325,
        w=64.483204,
        t1=False,
        t2=False,
        t3=False,
    ),
]

async def updating_task(mapper: CRX10Mapper):
    """Update values in server.

    This task runs continuously beside the server
    It will increment some values each two seconds.

    It should be noted that getValues and setValues are not safe
    against concurrent use.
    """
    # fc_as_hex = 0x04
    # device_id = 0x00
    # address = 0x1
    # count = 12
    print("STARTING")
    # s_context: ModbusSlaveContext = context[0]
    # s_context.setValues()
    # values = s_context.getValues(fc_as_hex,address,count)
    # values = [1 for v in values if v == 0 ]

    # context[device_id].setValues(fc_as_hex, address, values)
    # print("INIT")

    # txt = (
    #     f"updating_task: started: initialized values: {values!s} at address {address!s}"
    # )
    # print(txt)
    # _logger.debug(txt)
    temp = False
    # incrementing loop
    while True:
        await asyncio.sleep(2)
        if temp:
            mapper.position = test_address[0]
        else:
            mapper.position = test_address[1]
        pos = mapper.position
        print(pos)
        temp = not temp

        # values = context[device_id].getValues(fc_as_hex, address, count=count)
        # new_values = []
        # for v in values:
        #     if v:
        #         new_values.append(0)
        #     else:
        #         new_values.append(1)
        # values = new_values
        # context[device_id].setValues(fc_as_hex, address, values)

        # txt = f"updating_task: incremented values: {values!s} at address {address!s}"
        # print(txt)
        # _logger.debug(txt)

async def main():
    """Combine setup and run."""
    server = CRX10ModbusServer()

    try:
        server.start_server()
        temp = False
        while True:
            await asyncio.sleep(2)
            server.mapper.position
            if temp:
                server.mapper.position = test_address[0]
            else:
                server.mapper.position = test_address[1]
            print(server.mapper.position)
            temp = not temp
    finally:
        server.stop_server()

class CRX10ModbusServer():

    def __init__(self, host:str = '', port:int = 5020, identity:ModbusDeviceIdentification = None):
        self.host = host
        self.port = port
        if not identity:
            identity = ModbusDeviceIdentification(
                info_name={
                    "VendorName": "UofI-CDACS",
                    "ProductCode": "CDACSCR10",
                    "VendorUrl": "https://github.com/UofI-CDACS",
                    "ProductName": "CRX10 Modbus Server",
                    "ModelName": "CRX10 Modbus Server",
                }
            )
        self.identity = identity
        self.mapper = CRX10Mapper()
        self.server = ModbusTcpServer(
            context=self.mapper.server_context,  # Data storage
            identity=self.identity,  # server identify
            address=(self.host, self.port),  # listen address
            framer="socket",  # The framer strategy to use
        )
        self._server_task = None

    def start_server(self):
        self._server_task = asyncio.create_task(self.server.serve_forever())
        self._server_task.set_name("Modbus Server Task")

    def stop_server(self):
        if self._server_task is not None:
            self._server_task.cancel()



if __name__ == "__main__":
    asyncio.run(main(), debug=True)

