from typing import Any

from pymodbus.client import ModbusBaseClient, ModbusTcpClient
from pymodbus.datastore.store import BaseModbusDataBlock, ModbusSparseDataBlock

from async_reader_writer import ThreadSafeDataBlock

ModbusTcpClient.write_registers
convert_from_registers = ModbusBaseClient.convert_from_registers
convert_to_registers = ModbusBaseClient.convert_to_registers


# X Position                  33001    2    R    FLOAT32    mm    X position
# Y Position                  33003    2    R    FLOAT32    mm    Y position
# Z Position                  33005    2    R    FLOAT32    mm    Z position
# Roll                        33007    2    R    FLOAT32    degrees    Roll
# Pitch                       33009    2    R    FLOAT32    degrees    Pitch
# Yaw                         33011    2    R    FLOAT32    degrees    Yaw
# Process State               33013    1    R    UINT        State Indicator
# Error Code                  33014    1    R    UNIT        Error Code

@ThreadSafeDataBlock
class CRX10InputRegisters(ModbusSparseDataBlock):

    def __init__(self):
        super().__init__(values={k:0 for k in range(3001, 3014)}, mutable=True)


# Turn 1                      13001    1    R    BIT    bool    Turn 1
# Turn 2                      13002    1    R    BIT    bool    Turn 2
# Turn 3                      13003    1    R    BIT    bool    Turn 3
# Gripper State               13004    1    R    BIT    bool    1 Close, 0 Open
# Error Status                13005    1    R    BIT    bool    1 Error, 0 Ok
# Die Detected                13006    1    R    BIT    bool    1 Die Detected, 0 Not Detected
# Handoff                     13007    1    R    BIT    bool    1 Ready to Handoff, 0 Not Ready
# Conveyor Status             13008    1    R    Bit    Bool    1 On, 0 Off
# Conveyor Right Detection    13009    1    R    Bit    Bool    1 Detected, 0 Not Detected
# Conveyor Left Detection     13010    1    R    Bit    Bool    1 Detected, 0 Not Detected

@ThreadSafeDataBlock
class CRX10DiscreteInputs(BaseModbusDataBlock[dict[int, Any]]):

    def __init__(self):
        super().__init__(values={k:0 for k in range(3001, 3010)}, mutable=True)


