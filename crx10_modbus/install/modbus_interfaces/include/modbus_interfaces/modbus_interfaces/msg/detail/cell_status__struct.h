// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from modbus_interfaces:msg/CellStatus.idl
// generated code does not contain a copyright notice

#ifndef MODBUS_INTERFACES__MSG__DETAIL__CELL_STATUS__STRUCT_H_
#define MODBUS_INTERFACES__MSG__DETAIL__CELL_STATUS__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>


// Constants defined in the message

/// Struct defined in msg/CellStatus in the package modbus_interfaces.
typedef struct modbus_interfaces__msg__CellStatus
{
  /// 33013  State Indicator
  int8_t process_state;
  /// 33014  Error Code
  int8_t error_code;
  /// 13005  1 Error, 0 Ok
  int8_t error_state;
  /// 13006  1 Die Detected, 0 Not Detected
  int8_t dice_detected_qa;
  /// 13007  1 QA Pass, 0 QA Fail
  int8_t dice_qa_pass;
  /// 13008  1 Getting Dice Replacement, 0 No QA Action
  int8_t dice_qa_replace;
  /// 13009  1 Ready to Handoff, 0 Not Ready
  int8_t hand_off_state;
} modbus_interfaces__msg__CellStatus;

// Struct for a sequence of modbus_interfaces__msg__CellStatus.
typedef struct modbus_interfaces__msg__CellStatus__Sequence
{
  modbus_interfaces__msg__CellStatus * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} modbus_interfaces__msg__CellStatus__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // MODBUS_INTERFACES__MSG__DETAIL__CELL_STATUS__STRUCT_H_
