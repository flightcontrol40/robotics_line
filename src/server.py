#!/usr/bin/env python3
import asyncio
import logging

from pymodbus import __version__ as pymodbus_version
from pymodbus.datastore import (
    ModbusServerContext,
    ModbusSlaveContext,
    ModbusSparseDataBlock,
)
from pymodbus.device import ModbusDeviceIdentification
from pymodbus.logging import Log
from pymodbus.server import ModbusTcpServer, StartAsyncTcpServer

Log.setLevel(0)
_logger = logging.getLogger(__name__)
_logger.setLevel(0)


def read_robot_status() -> dict:
    return {}

async def updating_task(context: ModbusServerContext):
    """Update values in server.

    This task runs continuously beside the server
    It will increment some values each two seconds.

    It should be noted that getValues and setValues are not safe
    against concurrent use.
    """
    fc_as_hex = 0x01
    device_id = 0x00
    address = 0x0
    count = 5
    print("STARTING")
    # set values to zero
    for s in context:
        print(s)
        print(context[device_id])
    print(context[device_id].validate(fc_as_hex, address, count=count))
    values = context[device_id].getValues(fc_as_hex, address, count=count)
    print("INIT")

    values = [1 for v in values if v == 0 ]
    context[device_id].setValues(fc_as_hex, address, values)
    print("INIT")

    txt = (
        f"updating_task: started: initialised values: {values!s} at address {address!s}"
    )
    print(txt)
    _logger.debug(txt)

    # incrementing loop
    while True:
        await asyncio.sleep(2)

        values = context[device_id].getValues(fc_as_hex, address, count=count)
        new_values = []
        for v in values:
            if v:
                new_values.append(0)
            else:
                new_values.append(1)
        values = new_values
        context[device_id].setValues(fc_as_hex, address, values)

        txt = f"updating_task: incremented values: {values!s} at address {address!s}"
        print(txt)
        _logger.debug(txt)

async def run():
# X Position​      32001​    2​    R​    FLOAT32​    mm​    X position​
# Y Position​      32003​    2​    R​    FLOAT32​    mm​    Y position​
# Z Position​      32005​    2​    R​    FLOAT32​    mm​    Z position​
# X​               32007​    2​    R​    FLOAT32​    radians​    X (Quaternion)​
# Y​               32009​    2​    R​    FLOAT32​    radians​    Y (Quaternion)​
# Z​               32011​    2​    R​    FLOAT32​    radians​    Z (Quaternion)​
# W​               32013​    2​    R​    FlOAT32​    radians​    W (Quaternion)​
# Process State​   32015​    1​    R​    UINT​    ​    State Indicator​
# Error Code​      32016​    1​    R​    UNIT​    ​    Error Code​
# Gripper State​   12004​    1​    R​    BIT​    bool​    1 Close, 0 Open​
# Error Status​    12005​    1​    R​    BIT​    bool​    1 Error, 0 Ok​
# Die Detected​    12006​    1​    R​    BIT​    bool​    1 Die Detected, 0 Not Detected​
# Handoff​         12007​    1​    R​    BIT​    bool​    1 Ready to Handoff, 0 Not Ready​

    def get_data_block():
        return ModbusSparseDataBlock({0: [0]*20}, mutable=True)


    holding_registers = ModbusSparseDataBlock(
        {

        }
    )
    # Build data storage
    context = ModbusServerContext(
        slaves = ModbusSlaveContext(
                di=get_data_block(),
                co=get_data_block(),
                hr=get_data_block(),
                ir=get_data_block()
        ),
        single=True
    )
    identity = ModbusDeviceIdentification(
        info_name={
            "VendorName": "Pymodbus",
            "ProductCode": "PM",
            "VendorUrl": "https://github.com/pymodbus-dev/pymodbus/",
            "ProductName": "Pymodbus Server",
            "ModelName": "Pymodbus Server",
            "MajorMinorRevision": pymodbus_version,
        }
    )

    task = asyncio.create_task(updating_task(context))
    task.set_name("example updating task")
    address = ('', 5020)

    server = ModbusTcpServer(
        context=context,
        framer="socket",
        identity=identity,
        address=address
    )

    server.serve_forever()
    await StartAsyncTcpServer(   # start the server
        context=context,  # Data storage
        identity=identity,  # server identify
        address=address,  # listen address
        # custom_functions=[],  # allow custom handling
        framer="socket",  # The framer strategy to use
        # ignore_missing_slaves=True,  # ignore request to a missing slave
        # broadcast_enable=False,  # treat slave 0 as broadcast address,
        # timeout=1,  # waiting time for request to complete
    )
    task.cancel()

async def main():
    """Combine setup and run."""
    await run()


if __name__ == "__main__":
    asyncio.run(main(), debug=True)

