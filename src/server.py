#!/usr/bin/env python3
"""Pymodbus asynchronous Server with updating task Example.

An example of an asynchronous server and
a task that runs continuously alongside the server and updates values.

usage::

    server_updating.py [-h] [--comm {tcp,udp,serial,tls}]
                       [--framer {ascii,rtu,socket,tls}]
                       [--log {critical,error,warning,info,debug}]
                       [--port PORT] [--store {sequential,sparse,factory,none}]
                       [--device_ids DEVICE_IDS]

    -h, --help
        show this help message and exit
    -c, --comm {tcp,udp,serial,tls}
        set communication, default is tcp
    -f, --framer {ascii,rtu,socket,tls}
        set framer, default depends on --comm
    -l, --log {critical,error,warning,info,debug}
        set log level, default is info
    -p, --port PORT
        set port
        set serial device baud rate
    --store {sequential,sparse,factory,none}
        set datastore type
    --device_ids DEVICE_IDS
        set number of devices to respond to

The corresponding client can be started as:
    python3 client_sync.py
"""
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
from pymodbus.server import (
    StartAsyncTcpServer,
)

Log.setLevel(0)
_logger = logging.getLogger(__name__)
_logger.setLevel(0)


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
    def get_data_block():
        return ModbusSparseDataBlock({0: [0]*20}, mutable=True)
    
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


async def main(cmdline=None):
    """Combine setup and run."""
    # run_args = setup_updating_server(cmdline=cmdline)
    await run()



if __name__ == "__main__":
    asyncio.run(main(), debug=True)