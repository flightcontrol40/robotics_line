
import asyncio  # noqa: F401
import logging

from pydantic import BaseModel, Field
from pymodbus.client import ModbusBaseClient
from pymodbus.datastore import (
    ModbusServerContext,
    ModbusSlaveContext,
)
from pymodbus.datastore.store import ModbusSparseDataBlock
from pymodbus.device import ModbusDeviceIdentification
from pymodbus.logging import Log
from pymodbus.server import ModbusTcpServer

from async_reader_writer import ThreadSafeDataBlock

convert_from_registers = ModbusBaseClient.convert_from_registers
convert_to_registers = ModbusBaseClient.convert_to_registers
DATATYPE = ModbusBaseClient.DATATYPE
Log.setLevel(0)
_logger = logging.getLogger(__name__)
_logger.setLevel(0)


class PosData(BaseModel):
    x: float = Field()
    y: float = Field()
    z: float = Field()
    p: float = Field(ge=-360, le=360)
    r: float = Field(ge=-360, le=360)
    w: float = Field(ge=-360, le=360)
    t1: bool
    t2: bool
    t3: bool


# X Position                  33001    2    R    FLOAT32    mm    X position
# Y Position                  33003    2    R    FLOAT32    mm    Y position
# Z Position                  33005    2    R    FLOAT32    mm    Z position
# Roll                        33007    2    R    FLOAT32    degrees    Roll
# Pitch                       33009    2    R    FLOAT32    degrees    Pitch
# Yaw                         33011    2    R    FLOAT32    degrees    Yaw
# Process State               33013    1    R    UINT        State Indicator
# Error Code                  33014    1    R    UNIT        Error Code

class CRX10InputRegisters(ThreadSafeDataBlock):

    def __init__(self, values = {}):
        block = ModbusSparseDataBlock(values=values, mutable=True)
        super().__init__(block=block)


# Turn 1                      13001    1    R    BIT    bool    Turn 1 
# Turn 2                      13002    1    R    BIT    bool    Turn 2 
# Turn 3                      13003    1    R    BIT    bool    Turn 3 
# Gripper State               13004    1    R    BIT    bool    1 Close, 0 Open 
# Error Status                13005    1    R    BIT    bool    1 Error, 0 Ok 
# Die Detected For QA         13006    1    R    BIT    bool    1 Die Detected, 0 Not Detected 
# Die QA Pass Fail            13007    1    R    BIT    bool    1 R BIT bool 1 QA Pass, 0 QA Fail
# QA Replacement              13008    1    R    BIT    bool    1 Getting Dice Replacement, 0 No QA Action 
# Handoff                     13009    1    R    BIT    bool    1 Ready to Handoff, 0 Not Ready 
# Conveyor Status             13010    1    R    Bit    Bool    1 On, 0 Off 
# Conveyor Right Detection    13011    1    R    Bit    Bool    1 Detected, 0 Not Detected 
# Conveyor Left Detection     13012    1    R    Bit    Bool    1 Detected, 0 Not Detected 
class CRX10DiscreteInputs(ThreadSafeDataBlock):
    def __init__(self, values= {}):
        block = ModbusSparseDataBlock(values=values, mutable=True)
        super().__init__(block=block)


class CRX10Mapper:

    def __init__(self):
        self.ir: CRX10InputRegisters = CRX10InputRegisters(values= {k:0 for k in range(3001, 3014)})
        self.di: CRX10DiscreteInputs = CRX10DiscreteInputs(values={k:0 for k in range(3001, 3012)})
        self.server_context = self._build_context()

    def _build_context(self):
        # Build data storage
        return ModbusServerContext(
            slaves = ModbusSlaveContext(
                    di=self.di,
                    ir=self.ir
            ),
            single=True
        )

    @property
    def position(self) -> PosData:
        raw = self.ir.getValues(3001,12)
        decoded_pos = convert_from_registers(raw,data_type= DATATYPE.FLOAT32)
        raw = self.di.getValues(3001,3)
        decoded_turn = convert_from_registers(raw,data_type=DATATYPE.BITS)
        return PosData(
            x=decoded_pos[0],
            y=decoded_pos[1],
            z=decoded_pos[2],
            p=decoded_pos[3],
            r=decoded_pos[4],
            w=decoded_pos[5],
            t1=decoded_turn[0],
            t2=decoded_turn[1],
            t3=decoded_turn[2],
        )

    @position.setter
    def position(self, _pos: PosData) -> None:
        data = [_pos.x, _pos.y, _pos.z, _pos.p, _pos.r, _pos.w]
        encode_pos = convert_to_registers(data,data_type= DATATYPE.FLOAT32)
        self.ir.setValues(3001,encode_pos)
        data = [_pos.t1,_pos.t2,_pos.t3]
        encode_pos = convert_to_registers(data,data_type=DATATYPE.BITS)
        self.di.setValues(3001,encode_pos)


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


async def updating_task(server: CRX10ModbusServer):
    """Update values in server.

    This task runs continuously beside the server

    """
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


async def main():
    """Combine setup and run."""
    server = CRX10ModbusServer()

    try:
        server.start_server()
    finally:
        server.stop_server()


if __name__ == "__main__":
    asyncio.run(main(), debug=True)

