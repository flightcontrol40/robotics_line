// generated from rosidl_generator_c/resource/idl__functions.h.em
// with input from modbus_interfaces:msg/CellStatus.idl
// generated code does not contain a copyright notice

#ifndef MODBUS_INTERFACES__MSG__DETAIL__CELL_STATUS__FUNCTIONS_H_
#define MODBUS_INTERFACES__MSG__DETAIL__CELL_STATUS__FUNCTIONS_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stdlib.h>

#include "rosidl_runtime_c/visibility_control.h"
#include "modbus_interfaces/msg/rosidl_generator_c__visibility_control.h"

#include "modbus_interfaces/msg/detail/cell_status__struct.h"

/// Initialize msg/CellStatus message.
/**
 * If the init function is called twice for the same message without
 * calling fini inbetween previously allocated memory will be leaked.
 * \param[in,out] msg The previously allocated message pointer.
 * Fields without a default value will not be initialized by this function.
 * You might want to call memset(msg, 0, sizeof(
 * modbus_interfaces__msg__CellStatus
 * )) before or use
 * modbus_interfaces__msg__CellStatus__create()
 * to allocate and initialize the message.
 * \return true if initialization was successful, otherwise false
 */
ROSIDL_GENERATOR_C_PUBLIC_modbus_interfaces
bool
modbus_interfaces__msg__CellStatus__init(modbus_interfaces__msg__CellStatus * msg);

/// Finalize msg/CellStatus message.
/**
 * \param[in,out] msg The allocated message pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_modbus_interfaces
void
modbus_interfaces__msg__CellStatus__fini(modbus_interfaces__msg__CellStatus * msg);

/// Create msg/CellStatus message.
/**
 * It allocates the memory for the message, sets the memory to zero, and
 * calls
 * modbus_interfaces__msg__CellStatus__init().
 * \return The pointer to the initialized message if successful,
 * otherwise NULL
 */
ROSIDL_GENERATOR_C_PUBLIC_modbus_interfaces
modbus_interfaces__msg__CellStatus *
modbus_interfaces__msg__CellStatus__create();

/// Destroy msg/CellStatus message.
/**
 * It calls
 * modbus_interfaces__msg__CellStatus__fini()
 * and frees the memory of the message.
 * \param[in,out] msg The allocated message pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_modbus_interfaces
void
modbus_interfaces__msg__CellStatus__destroy(modbus_interfaces__msg__CellStatus * msg);

/// Check for msg/CellStatus message equality.
/**
 * \param[in] lhs The message on the left hand size of the equality operator.
 * \param[in] rhs The message on the right hand size of the equality operator.
 * \return true if messages are equal, otherwise false.
 */
ROSIDL_GENERATOR_C_PUBLIC_modbus_interfaces
bool
modbus_interfaces__msg__CellStatus__are_equal(const modbus_interfaces__msg__CellStatus * lhs, const modbus_interfaces__msg__CellStatus * rhs);

/// Copy a msg/CellStatus message.
/**
 * This functions performs a deep copy, as opposed to the shallow copy that
 * plain assignment yields.
 *
 * \param[in] input The source message pointer.
 * \param[out] output The target message pointer, which must
 *   have been initialized before calling this function.
 * \return true if successful, or false if either pointer is null
 *   or memory allocation fails.
 */
ROSIDL_GENERATOR_C_PUBLIC_modbus_interfaces
bool
modbus_interfaces__msg__CellStatus__copy(
  const modbus_interfaces__msg__CellStatus * input,
  modbus_interfaces__msg__CellStatus * output);

/// Initialize array of msg/CellStatus messages.
/**
 * It allocates the memory for the number of elements and calls
 * modbus_interfaces__msg__CellStatus__init()
 * for each element of the array.
 * \param[in,out] array The allocated array pointer.
 * \param[in] size The size / capacity of the array.
 * \return true if initialization was successful, otherwise false
 * If the array pointer is valid and the size is zero it is guaranteed
 # to return true.
 */
ROSIDL_GENERATOR_C_PUBLIC_modbus_interfaces
bool
modbus_interfaces__msg__CellStatus__Sequence__init(modbus_interfaces__msg__CellStatus__Sequence * array, size_t size);

/// Finalize array of msg/CellStatus messages.
/**
 * It calls
 * modbus_interfaces__msg__CellStatus__fini()
 * for each element of the array and frees the memory for the number of
 * elements.
 * \param[in,out] array The initialized array pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_modbus_interfaces
void
modbus_interfaces__msg__CellStatus__Sequence__fini(modbus_interfaces__msg__CellStatus__Sequence * array);

/// Create array of msg/CellStatus messages.
/**
 * It allocates the memory for the array and calls
 * modbus_interfaces__msg__CellStatus__Sequence__init().
 * \param[in] size The size / capacity of the array.
 * \return The pointer to the initialized array if successful, otherwise NULL
 */
ROSIDL_GENERATOR_C_PUBLIC_modbus_interfaces
modbus_interfaces__msg__CellStatus__Sequence *
modbus_interfaces__msg__CellStatus__Sequence__create(size_t size);

/// Destroy array of msg/CellStatus messages.
/**
 * It calls
 * modbus_interfaces__msg__CellStatus__Sequence__fini()
 * on the array,
 * and frees the memory of the array.
 * \param[in,out] array The initialized array pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_modbus_interfaces
void
modbus_interfaces__msg__CellStatus__Sequence__destroy(modbus_interfaces__msg__CellStatus__Sequence * array);

/// Check for msg/CellStatus message array equality.
/**
 * \param[in] lhs The message array on the left hand size of the equality operator.
 * \param[in] rhs The message array on the right hand size of the equality operator.
 * \return true if message arrays are equal in size and content, otherwise false.
 */
ROSIDL_GENERATOR_C_PUBLIC_modbus_interfaces
bool
modbus_interfaces__msg__CellStatus__Sequence__are_equal(const modbus_interfaces__msg__CellStatus__Sequence * lhs, const modbus_interfaces__msg__CellStatus__Sequence * rhs);

/// Copy an array of msg/CellStatus messages.
/**
 * This functions performs a deep copy, as opposed to the shallow copy that
 * plain assignment yields.
 *
 * \param[in] input The source array pointer.
 * \param[out] output The target array pointer, which must
 *   have been initialized before calling this function.
 * \return true if successful, or false if either pointer
 *   is null or memory allocation fails.
 */
ROSIDL_GENERATOR_C_PUBLIC_modbus_interfaces
bool
modbus_interfaces__msg__CellStatus__Sequence__copy(
  const modbus_interfaces__msg__CellStatus__Sequence * input,
  modbus_interfaces__msg__CellStatus__Sequence * output);

#ifdef __cplusplus
}
#endif

#endif  // MODBUS_INTERFACES__MSG__DETAIL__CELL_STATUS__FUNCTIONS_H_
