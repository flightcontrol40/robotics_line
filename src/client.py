#!/usr/bin/env python3
"""Pymodbus asynchronous client example.

usage::

    client_async.py [-h] [-c {tcp,udp,serial,tls}]
                    [-f {ascii,rtu,socket,tls}]
                    [-l {critical,error,warning,info,debug}] [-p PORT]
                    [--baudrate BAUDRATE] [--host HOST]

    -h, --help
        show this help message and exit
    -c, -comm {tcp,udp,serial,tls}
        set communication, default is tcp
    -f, --framer {ascii,rtu,socket,tls}
        set framer, default depends on --comm
    -l, --log {critical,error,warning,info,debug}
        set log level, default is info
    -p, --port PORT
        set port
    --baudrate BAUDRATE
        set serial device baud rate
    --host HOST
        set host, default is 127.0.0.1

The corresponding server must be started before e.g. as:
    python3 server_sync.py
"""
from __future__ import annotations

import asyncio
import logging

from pymodbus.client import AsyncModbusTcpClient

_logger = logging.getLogger(__file__)
_logger.setLevel("DEBUG")

async def run_async_client(client: AsyncModbusTcpClient, modbus_calls=None):
    """Run sync client."""
    _logger.info("### Client starting")
    await client.connect()
    assert client.connected
    if modbus_calls:
        await modbus_calls(client)
    client.close()
    _logger.info("### End of Program")


async def run_a_few_calls(client: AsyncModbusTcpClient):
    """Test connection works."""
    while True:

        rr = await client.read_input_registers(3000, count=12)
        data = rr.registers
        data = client.convert_from_registers(data, client.DATATYPE.FLOAT32)
        print(data)
        await asyncio.sleep(2)

async def main():
    """Combine setup and run."""

    client = AsyncModbusTcpClient("localhost",port=5020)
    await run_async_client(client, modbus_calls=run_a_few_calls)


if __name__ == "__main__":
    asyncio.run(main(), debug=True)