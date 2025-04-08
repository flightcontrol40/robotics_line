# generated from rosidl_generator_py/resource/_idl.py.em
# with input from modbus_interfaces:msg/CellStatus.idl
# generated code does not contain a copyright notice


# Import statements for member types

import builtins  # noqa: E402, I100

import rosidl_parser.definition  # noqa: E402, I100


class Metaclass_CellStatus(type):
    """Metaclass of message 'CellStatus'."""

    _CREATE_ROS_MESSAGE = None
    _CONVERT_FROM_PY = None
    _CONVERT_TO_PY = None
    _DESTROY_ROS_MESSAGE = None
    _TYPE_SUPPORT = None

    __constants = {
    }

    @classmethod
    def __import_type_support__(cls):
        try:
            from rosidl_generator_py import import_type_support
            module = import_type_support('modbus_interfaces')
        except ImportError:
            import logging
            import traceback
            logger = logging.getLogger(
                'modbus_interfaces.msg.CellStatus')
            logger.debug(
                'Failed to import needed modules for type support:\n' +
                traceback.format_exc())
        else:
            cls._CREATE_ROS_MESSAGE = module.create_ros_message_msg__msg__cell_status
            cls._CONVERT_FROM_PY = module.convert_from_py_msg__msg__cell_status
            cls._CONVERT_TO_PY = module.convert_to_py_msg__msg__cell_status
            cls._TYPE_SUPPORT = module.type_support_msg__msg__cell_status
            cls._DESTROY_ROS_MESSAGE = module.destroy_ros_message_msg__msg__cell_status

    @classmethod
    def __prepare__(cls, name, bases, **kwargs):
        # list constant names here so that they appear in the help text of
        # the message class under "Data and other attributes defined here:"
        # as well as populate each message instance
        return {
            'PROCESS_STATE__DEFAULT': -1,
            'ERROR_CODE__DEFAULT': -1,
            'ERROR_STATE__DEFAULT': -1,
            'DICE_DETECTED_QA__DEFAULT': -1,
            'DICE_QA_PASS__DEFAULT': -1,
            'DICE_QA_REPLACE__DEFAULT': -1,
            'HAND_OFF_STATE__DEFAULT': -1,
        }

    @property
    def PROCESS_STATE__DEFAULT(cls):
        """Return default value for message field 'process_state'."""
        return -1

    @property
    def ERROR_CODE__DEFAULT(cls):
        """Return default value for message field 'error_code'."""
        return -1

    @property
    def ERROR_STATE__DEFAULT(cls):
        """Return default value for message field 'error_state'."""
        return -1

    @property
    def DICE_DETECTED_QA__DEFAULT(cls):
        """Return default value for message field 'dice_detected_qa'."""
        return -1

    @property
    def DICE_QA_PASS__DEFAULT(cls):
        """Return default value for message field 'dice_qa_pass'."""
        return -1

    @property
    def DICE_QA_REPLACE__DEFAULT(cls):
        """Return default value for message field 'dice_qa_replace'."""
        return -1

    @property
    def HAND_OFF_STATE__DEFAULT(cls):
        """Return default value for message field 'hand_off_state'."""
        return -1


class CellStatus(metaclass=Metaclass_CellStatus):
    """Message class 'CellStatus'."""

    __slots__ = [
        '_process_state',
        '_error_code',
        '_error_state',
        '_dice_detected_qa',
        '_dice_qa_pass',
        '_dice_qa_replace',
        '_hand_off_state',
    ]

    _fields_and_field_types = {
        'process_state': 'int8',
        'error_code': 'int8',
        'error_state': 'int8',
        'dice_detected_qa': 'int8',
        'dice_qa_pass': 'int8',
        'dice_qa_replace': 'int8',
        'hand_off_state': 'int8',
    }

    SLOT_TYPES = (
        rosidl_parser.definition.BasicType('int8'),  # noqa: E501
        rosidl_parser.definition.BasicType('int8'),  # noqa: E501
        rosidl_parser.definition.BasicType('int8'),  # noqa: E501
        rosidl_parser.definition.BasicType('int8'),  # noqa: E501
        rosidl_parser.definition.BasicType('int8'),  # noqa: E501
        rosidl_parser.definition.BasicType('int8'),  # noqa: E501
        rosidl_parser.definition.BasicType('int8'),  # noqa: E501
    )

    def __init__(self, **kwargs):
        assert all('_' + key in self.__slots__ for key in kwargs.keys()), \
            'Invalid arguments passed to constructor: %s' % \
            ', '.join(sorted(k for k in kwargs.keys() if '_' + k not in self.__slots__))
        self.process_state = kwargs.get(
            'process_state', CellStatus.PROCESS_STATE__DEFAULT)
        self.error_code = kwargs.get(
            'error_code', CellStatus.ERROR_CODE__DEFAULT)
        self.error_state = kwargs.get(
            'error_state', CellStatus.ERROR_STATE__DEFAULT)
        self.dice_detected_qa = kwargs.get(
            'dice_detected_qa', CellStatus.DICE_DETECTED_QA__DEFAULT)
        self.dice_qa_pass = kwargs.get(
            'dice_qa_pass', CellStatus.DICE_QA_PASS__DEFAULT)
        self.dice_qa_replace = kwargs.get(
            'dice_qa_replace', CellStatus.DICE_QA_REPLACE__DEFAULT)
        self.hand_off_state = kwargs.get(
            'hand_off_state', CellStatus.HAND_OFF_STATE__DEFAULT)

    def __repr__(self):
        typename = self.__class__.__module__.split('.')
        typename.pop()
        typename.append(self.__class__.__name__)
        args = []
        for s, t in zip(self.__slots__, self.SLOT_TYPES):
            field = getattr(self, s)
            fieldstr = repr(field)
            # We use Python array type for fields that can be directly stored
            # in them, and "normal" sequences for everything else.  If it is
            # a type that we store in an array, strip off the 'array' portion.
            if (
                isinstance(t, rosidl_parser.definition.AbstractSequence) and
                isinstance(t.value_type, rosidl_parser.definition.BasicType) and
                t.value_type.typename in ['float', 'double', 'int8', 'uint8', 'int16', 'uint16', 'int32', 'uint32', 'int64', 'uint64']
            ):
                if len(field) == 0:
                    fieldstr = '[]'
                else:
                    assert fieldstr.startswith('array(')
                    prefix = "array('X', "
                    suffix = ')'
                    fieldstr = fieldstr[len(prefix):-len(suffix)]
            args.append(s[1:] + '=' + fieldstr)
        return '%s(%s)' % ('.'.join(typename), ', '.join(args))

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        if self.process_state != other.process_state:
            return False
        if self.error_code != other.error_code:
            return False
        if self.error_state != other.error_state:
            return False
        if self.dice_detected_qa != other.dice_detected_qa:
            return False
        if self.dice_qa_pass != other.dice_qa_pass:
            return False
        if self.dice_qa_replace != other.dice_qa_replace:
            return False
        if self.hand_off_state != other.hand_off_state:
            return False
        return True

    @classmethod
    def get_fields_and_field_types(cls):
        from copy import copy
        return copy(cls._fields_and_field_types)

    @builtins.property
    def process_state(self):
        """Message field 'process_state'."""
        return self._process_state

    @process_state.setter
    def process_state(self, value):
        if __debug__:
            assert \
                isinstance(value, int), \
                "The 'process_state' field must be of type 'int'"
            assert value >= -128 and value < 128, \
                "The 'process_state' field must be an integer in [-128, 127]"
        self._process_state = value

    @builtins.property
    def error_code(self):
        """Message field 'error_code'."""
        return self._error_code

    @error_code.setter
    def error_code(self, value):
        if __debug__:
            assert \
                isinstance(value, int), \
                "The 'error_code' field must be of type 'int'"
            assert value >= -128 and value < 128, \
                "The 'error_code' field must be an integer in [-128, 127]"
        self._error_code = value

    @builtins.property
    def error_state(self):
        """Message field 'error_state'."""
        return self._error_state

    @error_state.setter
    def error_state(self, value):
        if __debug__:
            assert \
                isinstance(value, int), \
                "The 'error_state' field must be of type 'int'"
            assert value >= -128 and value < 128, \
                "The 'error_state' field must be an integer in [-128, 127]"
        self._error_state = value

    @builtins.property
    def dice_detected_qa(self):
        """Message field 'dice_detected_qa'."""
        return self._dice_detected_qa

    @dice_detected_qa.setter
    def dice_detected_qa(self, value):
        if __debug__:
            assert \
                isinstance(value, int), \
                "The 'dice_detected_qa' field must be of type 'int'"
            assert value >= -128 and value < 128, \
                "The 'dice_detected_qa' field must be an integer in [-128, 127]"
        self._dice_detected_qa = value

    @builtins.property
    def dice_qa_pass(self):
        """Message field 'dice_qa_pass'."""
        return self._dice_qa_pass

    @dice_qa_pass.setter
    def dice_qa_pass(self, value):
        if __debug__:
            assert \
                isinstance(value, int), \
                "The 'dice_qa_pass' field must be of type 'int'"
            assert value >= -128 and value < 128, \
                "The 'dice_qa_pass' field must be an integer in [-128, 127]"
        self._dice_qa_pass = value

    @builtins.property
    def dice_qa_replace(self):
        """Message field 'dice_qa_replace'."""
        return self._dice_qa_replace

    @dice_qa_replace.setter
    def dice_qa_replace(self, value):
        if __debug__:
            assert \
                isinstance(value, int), \
                "The 'dice_qa_replace' field must be of type 'int'"
            assert value >= -128 and value < 128, \
                "The 'dice_qa_replace' field must be an integer in [-128, 127]"
        self._dice_qa_replace = value

    @builtins.property
    def hand_off_state(self):
        """Message field 'hand_off_state'."""
        return self._hand_off_state

    @hand_off_state.setter
    def hand_off_state(self, value):
        if __debug__:
            assert \
                isinstance(value, int), \
                "The 'hand_off_state' field must be of type 'int'"
            assert value >= -128 and value < 128, \
                "The 'hand_off_state' field must be an integer in [-128, 127]"
        self._hand_off_state = value
