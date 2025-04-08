
import asyncio  # noqa: F401
import logging

from pymodbus.client import ModbusBaseClient
from pymodbus.datastore import (
    ModbusServerContext,
    ModbusSlaveContext,
)
from pymodbus.datastore.store import ModbusSparseDataBlock
from pymodbus.device import ModbusDeviceIdentification
from pymodbus.logging import Log
from pymodbus.server import ModbusTcpServer

from .async_reader_writer import ThreadSafeDataBlock

convert_from_registers = ModbusBaseClient.convert_from_registers
convert_to_registers = ModbusBaseClient.convert_to_registers
DATATYPE = ModbusBaseClient.DATATYPE
Log.setLevel(0)
_logger = logging.getLogger(__name__)
_logger.setLevel(0)


def _set_prop(idx, data_name):
    def _fget(self):
        return getattr(self, f"_{data_name}")[idx]
    def _fset(self, _value):
        _data = getattr(self, f"_{data_name}")
        _data[idx] = _value
        setattr(self, f"_{data_name}",_data)
    return property(fget=_fget,fset=_fset)

class AutoProp(type):
    def __new__(cls, name, bases, attrs):
        if "__auto_props__" not in attrs:
            print("Skipping")
            return super(AutoProp, cls).__new__(
                cls, name, bases, attrs
            )
        
        auto_props = attrs.get("__auto_props__", None)
        if auto_props is not None:
            if isinstance(auto_props, tuple) and len(auto_props) == 2:
                data_name, args = auto_props
                data_name: str
                args: list[str]
                def init(self, values: list):
                    setattr(self, f"_{data_name}", values)
                attrs["__init__"] = init
                for idx, key in enumerate(args):
                    attrs[key] = _set_prop(idx, data_name)
        return super(AutoProp, cls).__new__(
            cls, name, bases, attrs
        )

class PosData(metaclass=AutoProp):
    __auto_props__ = (
        "pos_data",
        ['x','y','z','w','p','r','t1','t2','t3']
    )


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
        data = []
        raw = self.ir.getValues(3001,12)
        data.extend(convert_from_registers(raw,data_type=DATATYPE.FLOAT32))
        raw = self.di.getValues(3001,3)
        data.extend( convert_from_registers(raw,data_type=DATATYPE.BITS))
        return PosData(data)

    @position.setter
    def position(self, _pos: PosData) -> None:
        data = [_pos.x, _pos.y, _pos.z, _pos.p, _pos.r, _pos.w]
        encode_pos = convert_to_registers(data,data_type= DATATYPE.FLOAT32)
        self.ir.setValues(3001,encode_pos)
        data = [_pos.t1,_pos.t2,_pos.t3]
        encode_pos = convert_to_registers(data,data_type=DATATYPE.BITS)
        self.di.setValues(3001,encode_pos)

# test_address = [
#     PosData(
#         x=200.38920,
#         y=150.2348,
#         z=378.0932,
#         p=180.09128,
#         r=-0.44325,
#         w=35.483204,
#         t1=False,
#         t2=False,
#         t3=False,
#     ),
#     PosData(
#         x=0.38920,
#         y=246.2348,
#         z=122.0932,
#         p=-75.09128,
#         r=-14.44325,
#         w=64.483204,
#         t1=False,
#         t2=False,
#         t3=False,
#     ),
# ]


class CRX10ModbusServer():

    def __init__(self):
        self.host = ''
        self.port = 5020
        self.identity = ModbusDeviceIdentification(
                info_name={
                    "VendorName": "UofI-CDACS",
                    "ProductCode": "CDACSCR10",
                    "VendorUrl": "https://github.com/UofI-CDACS",
                    "ProductName": "CRX10 Modbus Server",
                    "ModelName": "CRX10 Modbus Server",
                }
            )
        self.mapper = CRX10Mapper()

    def init_server(self):
        self.server = ModbusTcpServer(
            context=self.mapper.server_context,  # Data storage
            identity=self.identity,  # server identify
            address=(self.host, self.port),  # listen address
            framer="socket",  # The framer strategy to use
        )




