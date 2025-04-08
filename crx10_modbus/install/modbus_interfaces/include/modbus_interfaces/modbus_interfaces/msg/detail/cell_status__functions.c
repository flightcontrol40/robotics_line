// generated from rosidl_generator_c/resource/idl__functions.c.em
// with input from modbus_interfaces:msg/CellStatus.idl
// generated code does not contain a copyright notice
#include "modbus_interfaces/msg/detail/cell_status__functions.h"

#include <assert.h>
#include <stdbool.h>
#include <stdlib.h>
#include <string.h>

#include "rcutils/allocator.h"


bool
modbus_interfaces__msg__CellStatus__init(modbus_interfaces__msg__CellStatus * msg)
{
  if (!msg) {
    return false;
  }
  // process_state
  msg->process_state = -1;
  // error_code
  msg->error_code = -1;
  // error_state
  msg->error_state = -1;
  // dice_detected_qa
  msg->dice_detected_qa = -1;
  // dice_qa_pass
  msg->dice_qa_pass = -1;
  // dice_qa_replace
  msg->dice_qa_replace = -1;
  // hand_off_state
  msg->hand_off_state = -1;
  return true;
}

void
modbus_interfaces__msg__CellStatus__fini(modbus_interfaces__msg__CellStatus * msg)
{
  if (!msg) {
    return;
  }
  // process_state
  // error_code
  // error_state
  // dice_detected_qa
  // dice_qa_pass
  // dice_qa_replace
  // hand_off_state
}

bool
modbus_interfaces__msg__CellStatus__are_equal(const modbus_interfaces__msg__CellStatus * lhs, const modbus_interfaces__msg__CellStatus * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  // process_state
  if (lhs->process_state != rhs->process_state) {
    return false;
  }
  // error_code
  if (lhs->error_code != rhs->error_code) {
    return false;
  }
  // error_state
  if (lhs->error_state != rhs->error_state) {
    return false;
  }
  // dice_detected_qa
  if (lhs->dice_detected_qa != rhs->dice_detected_qa) {
    return false;
  }
  // dice_qa_pass
  if (lhs->dice_qa_pass != rhs->dice_qa_pass) {
    return false;
  }
  // dice_qa_replace
  if (lhs->dice_qa_replace != rhs->dice_qa_replace) {
    return false;
  }
  // hand_off_state
  if (lhs->hand_off_state != rhs->hand_off_state) {
    return false;
  }
  return true;
}

bool
modbus_interfaces__msg__CellStatus__copy(
  const modbus_interfaces__msg__CellStatus * input,
  modbus_interfaces__msg__CellStatus * output)
{
  if (!input || !output) {
    return false;
  }
  // process_state
  output->process_state = input->process_state;
  // error_code
  output->error_code = input->error_code;
  // error_state
  output->error_state = input->error_state;
  // dice_detected_qa
  output->dice_detected_qa = input->dice_detected_qa;
  // dice_qa_pass
  output->dice_qa_pass = input->dice_qa_pass;
  // dice_qa_replace
  output->dice_qa_replace = input->dice_qa_replace;
  // hand_off_state
  output->hand_off_state = input->hand_off_state;
  return true;
}

modbus_interfaces__msg__CellStatus *
modbus_interfaces__msg__CellStatus__create()
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  modbus_interfaces__msg__CellStatus * msg = (modbus_interfaces__msg__CellStatus *)allocator.allocate(sizeof(modbus_interfaces__msg__CellStatus), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(modbus_interfaces__msg__CellStatus));
  bool success = modbus_interfaces__msg__CellStatus__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
modbus_interfaces__msg__CellStatus__destroy(modbus_interfaces__msg__CellStatus * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    modbus_interfaces__msg__CellStatus__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
modbus_interfaces__msg__CellStatus__Sequence__init(modbus_interfaces__msg__CellStatus__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  modbus_interfaces__msg__CellStatus * data = NULL;

  if (size) {
    data = (modbus_interfaces__msg__CellStatus *)allocator.zero_allocate(size, sizeof(modbus_interfaces__msg__CellStatus), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = modbus_interfaces__msg__CellStatus__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        modbus_interfaces__msg__CellStatus__fini(&data[i - 1]);
      }
      allocator.deallocate(data, allocator.state);
      return false;
    }
  }
  array->data = data;
  array->size = size;
  array->capacity = size;
  return true;
}

void
modbus_interfaces__msg__CellStatus__Sequence__fini(modbus_interfaces__msg__CellStatus__Sequence * array)
{
  if (!array) {
    return;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();

  if (array->data) {
    // ensure that data and capacity values are consistent
    assert(array->capacity > 0);
    // finalize all array elements
    for (size_t i = 0; i < array->capacity; ++i) {
      modbus_interfaces__msg__CellStatus__fini(&array->data[i]);
    }
    allocator.deallocate(array->data, allocator.state);
    array->data = NULL;
    array->size = 0;
    array->capacity = 0;
  } else {
    // ensure that data, size, and capacity values are consistent
    assert(0 == array->size);
    assert(0 == array->capacity);
  }
}

modbus_interfaces__msg__CellStatus__Sequence *
modbus_interfaces__msg__CellStatus__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  modbus_interfaces__msg__CellStatus__Sequence * array = (modbus_interfaces__msg__CellStatus__Sequence *)allocator.allocate(sizeof(modbus_interfaces__msg__CellStatus__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = modbus_interfaces__msg__CellStatus__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
modbus_interfaces__msg__CellStatus__Sequence__destroy(modbus_interfaces__msg__CellStatus__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    modbus_interfaces__msg__CellStatus__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
modbus_interfaces__msg__CellStatus__Sequence__are_equal(const modbus_interfaces__msg__CellStatus__Sequence * lhs, const modbus_interfaces__msg__CellStatus__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!modbus_interfaces__msg__CellStatus__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
modbus_interfaces__msg__CellStatus__Sequence__copy(
  const modbus_interfaces__msg__CellStatus__Sequence * input,
  modbus_interfaces__msg__CellStatus__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    const size_t allocation_size =
      input->size * sizeof(modbus_interfaces__msg__CellStatus);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    modbus_interfaces__msg__CellStatus * data =
      (modbus_interfaces__msg__CellStatus *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!modbus_interfaces__msg__CellStatus__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          modbus_interfaces__msg__CellStatus__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!modbus_interfaces__msg__CellStatus__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}
