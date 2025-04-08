// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from modbus_interfaces:msg/CellStatus.idl
// generated code does not contain a copyright notice

#ifndef MODBUS_INTERFACES__MSG__DETAIL__CELL_STATUS__BUILDER_HPP_
#define MODBUS_INTERFACES__MSG__DETAIL__CELL_STATUS__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "modbus_interfaces/msg/detail/cell_status__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace modbus_interfaces
{

namespace msg
{

namespace builder
{

class Init_CellStatus_hand_off_state
{
public:
  explicit Init_CellStatus_hand_off_state(::modbus_interfaces::msg::CellStatus & msg)
  : msg_(msg)
  {}
  ::modbus_interfaces::msg::CellStatus hand_off_state(::modbus_interfaces::msg::CellStatus::_hand_off_state_type arg)
  {
    msg_.hand_off_state = std::move(arg);
    return std::move(msg_);
  }

private:
  ::modbus_interfaces::msg::CellStatus msg_;
};

class Init_CellStatus_dice_qa_replace
{
public:
  explicit Init_CellStatus_dice_qa_replace(::modbus_interfaces::msg::CellStatus & msg)
  : msg_(msg)
  {}
  Init_CellStatus_hand_off_state dice_qa_replace(::modbus_interfaces::msg::CellStatus::_dice_qa_replace_type arg)
  {
    msg_.dice_qa_replace = std::move(arg);
    return Init_CellStatus_hand_off_state(msg_);
  }

private:
  ::modbus_interfaces::msg::CellStatus msg_;
};

class Init_CellStatus_dice_qa_pass
{
public:
  explicit Init_CellStatus_dice_qa_pass(::modbus_interfaces::msg::CellStatus & msg)
  : msg_(msg)
  {}
  Init_CellStatus_dice_qa_replace dice_qa_pass(::modbus_interfaces::msg::CellStatus::_dice_qa_pass_type arg)
  {
    msg_.dice_qa_pass = std::move(arg);
    return Init_CellStatus_dice_qa_replace(msg_);
  }

private:
  ::modbus_interfaces::msg::CellStatus msg_;
};

class Init_CellStatus_dice_detected_qa
{
public:
  explicit Init_CellStatus_dice_detected_qa(::modbus_interfaces::msg::CellStatus & msg)
  : msg_(msg)
  {}
  Init_CellStatus_dice_qa_pass dice_detected_qa(::modbus_interfaces::msg::CellStatus::_dice_detected_qa_type arg)
  {
    msg_.dice_detected_qa = std::move(arg);
    return Init_CellStatus_dice_qa_pass(msg_);
  }

private:
  ::modbus_interfaces::msg::CellStatus msg_;
};

class Init_CellStatus_error_state
{
public:
  explicit Init_CellStatus_error_state(::modbus_interfaces::msg::CellStatus & msg)
  : msg_(msg)
  {}
  Init_CellStatus_dice_detected_qa error_state(::modbus_interfaces::msg::CellStatus::_error_state_type arg)
  {
    msg_.error_state = std::move(arg);
    return Init_CellStatus_dice_detected_qa(msg_);
  }

private:
  ::modbus_interfaces::msg::CellStatus msg_;
};

class Init_CellStatus_error_code
{
public:
  explicit Init_CellStatus_error_code(::modbus_interfaces::msg::CellStatus & msg)
  : msg_(msg)
  {}
  Init_CellStatus_error_state error_code(::modbus_interfaces::msg::CellStatus::_error_code_type arg)
  {
    msg_.error_code = std::move(arg);
    return Init_CellStatus_error_state(msg_);
  }

private:
  ::modbus_interfaces::msg::CellStatus msg_;
};

class Init_CellStatus_process_state
{
public:
  Init_CellStatus_process_state()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_CellStatus_error_code process_state(::modbus_interfaces::msg::CellStatus::_process_state_type arg)
  {
    msg_.process_state = std::move(arg);
    return Init_CellStatus_error_code(msg_);
  }

private:
  ::modbus_interfaces::msg::CellStatus msg_;
};

}  // namespace builder

}  // namespace msg

template<typename MessageType>
auto build();

template<>
inline
auto build<::modbus_interfaces::msg::CellStatus>()
{
  return modbus_interfaces::msg::builder::Init_CellStatus_process_state();
}

}  // namespace modbus_interfaces

#endif  // MODBUS_INTERFACES__MSG__DETAIL__CELL_STATUS__BUILDER_HPP_
