// generated from rosidl_typesupport_introspection_c/resource/idl__type_support.c.em
// with input from modbus_interfaces:msg/CellStatus.idl
// generated code does not contain a copyright notice

#include <stddef.h>
#include "modbus_interfaces/msg/detail/cell_status__rosidl_typesupport_introspection_c.h"
#include "modbus_interfaces/msg/rosidl_typesupport_introspection_c__visibility_control.h"
#include "rosidl_typesupport_introspection_c/field_types.h"
#include "rosidl_typesupport_introspection_c/identifier.h"
#include "rosidl_typesupport_introspection_c/message_introspection.h"
#include "modbus_interfaces/msg/detail/cell_status__functions.h"
#include "modbus_interfaces/msg/detail/cell_status__struct.h"


#ifdef __cplusplus
extern "C"
{
#endif

void modbus_interfaces__msg__CellStatus__rosidl_typesupport_introspection_c__CellStatus_init_function(
  void * message_memory, enum rosidl_runtime_c__message_initialization _init)
{
  // TODO(karsten1987): initializers are not yet implemented for typesupport c
  // see https://github.com/ros2/ros2/issues/397
  (void) _init;
  modbus_interfaces__msg__CellStatus__init(message_memory);
}

void modbus_interfaces__msg__CellStatus__rosidl_typesupport_introspection_c__CellStatus_fini_function(void * message_memory)
{
  modbus_interfaces__msg__CellStatus__fini(message_memory);
}

static rosidl_typesupport_introspection_c__MessageMember modbus_interfaces__msg__CellStatus__rosidl_typesupport_introspection_c__CellStatus_message_member_array[7] = {
  {
    "process_state",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_INT8,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(modbus_interfaces__msg__CellStatus, process_state),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "error_code",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_INT8,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(modbus_interfaces__msg__CellStatus, error_code),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "error_state",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_INT8,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(modbus_interfaces__msg__CellStatus, error_state),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "dice_detected_qa",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_INT8,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(modbus_interfaces__msg__CellStatus, dice_detected_qa),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "dice_qa_pass",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_INT8,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(modbus_interfaces__msg__CellStatus, dice_qa_pass),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "dice_qa_replace",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_INT8,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(modbus_interfaces__msg__CellStatus, dice_qa_replace),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "hand_off_state",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_INT8,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(modbus_interfaces__msg__CellStatus, hand_off_state),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  }
};

static const rosidl_typesupport_introspection_c__MessageMembers modbus_interfaces__msg__CellStatus__rosidl_typesupport_introspection_c__CellStatus_message_members = {
  "modbus_interfaces__msg",  // message namespace
  "CellStatus",  // message name
  7,  // number of fields
  sizeof(modbus_interfaces__msg__CellStatus),
  modbus_interfaces__msg__CellStatus__rosidl_typesupport_introspection_c__CellStatus_message_member_array,  // message members
  modbus_interfaces__msg__CellStatus__rosidl_typesupport_introspection_c__CellStatus_init_function,  // function to initialize message memory (memory has to be allocated)
  modbus_interfaces__msg__CellStatus__rosidl_typesupport_introspection_c__CellStatus_fini_function  // function to terminate message instance (will not free memory)
};

// this is not const since it must be initialized on first access
// since C does not allow non-integral compile-time constants
static rosidl_message_type_support_t modbus_interfaces__msg__CellStatus__rosidl_typesupport_introspection_c__CellStatus_message_type_support_handle = {
  0,
  &modbus_interfaces__msg__CellStatus__rosidl_typesupport_introspection_c__CellStatus_message_members,
  get_message_typesupport_handle_function,
};

ROSIDL_TYPESUPPORT_INTROSPECTION_C_EXPORT_modbus_interfaces
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, modbus_interfaces, msg, CellStatus)() {
  if (!modbus_interfaces__msg__CellStatus__rosidl_typesupport_introspection_c__CellStatus_message_type_support_handle.typesupport_identifier) {
    modbus_interfaces__msg__CellStatus__rosidl_typesupport_introspection_c__CellStatus_message_type_support_handle.typesupport_identifier =
      rosidl_typesupport_introspection_c__identifier;
  }
  return &modbus_interfaces__msg__CellStatus__rosidl_typesupport_introspection_c__CellStatus_message_type_support_handle;
}
#ifdef __cplusplus
}
#endif
