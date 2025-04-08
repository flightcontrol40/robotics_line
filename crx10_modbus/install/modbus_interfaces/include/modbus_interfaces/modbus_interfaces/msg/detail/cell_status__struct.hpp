// generated from rosidl_generator_cpp/resource/idl__struct.hpp.em
// with input from modbus_interfaces:msg/CellStatus.idl
// generated code does not contain a copyright notice

#ifndef MODBUS_INTERFACES__MSG__DETAIL__CELL_STATUS__STRUCT_HPP_
#define MODBUS_INTERFACES__MSG__DETAIL__CELL_STATUS__STRUCT_HPP_

#include <algorithm>
#include <array>
#include <memory>
#include <string>
#include <vector>

#include "rosidl_runtime_cpp/bounded_vector.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


#ifndef _WIN32
# define DEPRECATED__modbus_interfaces__msg__CellStatus __attribute__((deprecated))
#else
# define DEPRECATED__modbus_interfaces__msg__CellStatus __declspec(deprecated)
#endif

namespace modbus_interfaces
{

namespace msg
{

// message struct
template<class ContainerAllocator>
struct CellStatus_
{
  using Type = CellStatus_<ContainerAllocator>;

  explicit CellStatus_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::DEFAULTS_ONLY == _init)
    {
      this->process_state = -1;
      this->error_code = -1;
      this->error_state = -1;
      this->dice_detected_qa = -1;
      this->dice_qa_pass = -1;
      this->dice_qa_replace = -1;
      this->hand_off_state = -1;
    } else if (rosidl_runtime_cpp::MessageInitialization::ZERO == _init) {
      this->process_state = 0;
      this->error_code = 0;
      this->error_state = 0;
      this->dice_detected_qa = 0;
      this->dice_qa_pass = 0;
      this->dice_qa_replace = 0;
      this->hand_off_state = 0;
    }
  }

  explicit CellStatus_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    (void)_alloc;
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::DEFAULTS_ONLY == _init)
    {
      this->process_state = -1;
      this->error_code = -1;
      this->error_state = -1;
      this->dice_detected_qa = -1;
      this->dice_qa_pass = -1;
      this->dice_qa_replace = -1;
      this->hand_off_state = -1;
    } else if (rosidl_runtime_cpp::MessageInitialization::ZERO == _init) {
      this->process_state = 0;
      this->error_code = 0;
      this->error_state = 0;
      this->dice_detected_qa = 0;
      this->dice_qa_pass = 0;
      this->dice_qa_replace = 0;
      this->hand_off_state = 0;
    }
  }

  // field types and members
  using _process_state_type =
    int8_t;
  _process_state_type process_state;
  using _error_code_type =
    int8_t;
  _error_code_type error_code;
  using _error_state_type =
    int8_t;
  _error_state_type error_state;
  using _dice_detected_qa_type =
    int8_t;
  _dice_detected_qa_type dice_detected_qa;
  using _dice_qa_pass_type =
    int8_t;
  _dice_qa_pass_type dice_qa_pass;
  using _dice_qa_replace_type =
    int8_t;
  _dice_qa_replace_type dice_qa_replace;
  using _hand_off_state_type =
    int8_t;
  _hand_off_state_type hand_off_state;

  // setters for named parameter idiom
  Type & set__process_state(
    const int8_t & _arg)
  {
    this->process_state = _arg;
    return *this;
  }
  Type & set__error_code(
    const int8_t & _arg)
  {
    this->error_code = _arg;
    return *this;
  }
  Type & set__error_state(
    const int8_t & _arg)
  {
    this->error_state = _arg;
    return *this;
  }
  Type & set__dice_detected_qa(
    const int8_t & _arg)
  {
    this->dice_detected_qa = _arg;
    return *this;
  }
  Type & set__dice_qa_pass(
    const int8_t & _arg)
  {
    this->dice_qa_pass = _arg;
    return *this;
  }
  Type & set__dice_qa_replace(
    const int8_t & _arg)
  {
    this->dice_qa_replace = _arg;
    return *this;
  }
  Type & set__hand_off_state(
    const int8_t & _arg)
  {
    this->hand_off_state = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    modbus_interfaces::msg::CellStatus_<ContainerAllocator> *;
  using ConstRawPtr =
    const modbus_interfaces::msg::CellStatus_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<modbus_interfaces::msg::CellStatus_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<modbus_interfaces::msg::CellStatus_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      modbus_interfaces::msg::CellStatus_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<modbus_interfaces::msg::CellStatus_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      modbus_interfaces::msg::CellStatus_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<modbus_interfaces::msg::CellStatus_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<modbus_interfaces::msg::CellStatus_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<modbus_interfaces::msg::CellStatus_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__modbus_interfaces__msg__CellStatus
    std::shared_ptr<modbus_interfaces::msg::CellStatus_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__modbus_interfaces__msg__CellStatus
    std::shared_ptr<modbus_interfaces::msg::CellStatus_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const CellStatus_ & other) const
  {
    if (this->process_state != other.process_state) {
      return false;
    }
    if (this->error_code != other.error_code) {
      return false;
    }
    if (this->error_state != other.error_state) {
      return false;
    }
    if (this->dice_detected_qa != other.dice_detected_qa) {
      return false;
    }
    if (this->dice_qa_pass != other.dice_qa_pass) {
      return false;
    }
    if (this->dice_qa_replace != other.dice_qa_replace) {
      return false;
    }
    if (this->hand_off_state != other.hand_off_state) {
      return false;
    }
    return true;
  }
  bool operator!=(const CellStatus_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct CellStatus_

// alias to use template instance with default allocator
using CellStatus =
  modbus_interfaces::msg::CellStatus_<std::allocator<void>>;

// constant definitions

}  // namespace msg

}  // namespace modbus_interfaces

#endif  // MODBUS_INTERFACES__MSG__DETAIL__CELL_STATUS__STRUCT_HPP_
