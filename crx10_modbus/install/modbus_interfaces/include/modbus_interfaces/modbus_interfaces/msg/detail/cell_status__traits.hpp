// generated from rosidl_generator_cpp/resource/idl__traits.hpp.em
// with input from modbus_interfaces:msg/CellStatus.idl
// generated code does not contain a copyright notice

#ifndef MODBUS_INTERFACES__MSG__DETAIL__CELL_STATUS__TRAITS_HPP_
#define MODBUS_INTERFACES__MSG__DETAIL__CELL_STATUS__TRAITS_HPP_

#include <stdint.h>

#include <sstream>
#include <string>
#include <type_traits>

#include "modbus_interfaces/msg/detail/cell_status__struct.hpp"
#include "rosidl_runtime_cpp/traits.hpp"

namespace modbus_interfaces
{

namespace msg
{

inline void to_flow_style_yaml(
  const CellStatus & msg,
  std::ostream & out)
{
  out << "{";
  // member: process_state
  {
    out << "process_state: ";
    rosidl_generator_traits::value_to_yaml(msg.process_state, out);
    out << ", ";
  }

  // member: error_code
  {
    out << "error_code: ";
    rosidl_generator_traits::value_to_yaml(msg.error_code, out);
    out << ", ";
  }

  // member: error_state
  {
    out << "error_state: ";
    rosidl_generator_traits::value_to_yaml(msg.error_state, out);
    out << ", ";
  }

  // member: dice_detected_qa
  {
    out << "dice_detected_qa: ";
    rosidl_generator_traits::value_to_yaml(msg.dice_detected_qa, out);
    out << ", ";
  }

  // member: dice_qa_pass
  {
    out << "dice_qa_pass: ";
    rosidl_generator_traits::value_to_yaml(msg.dice_qa_pass, out);
    out << ", ";
  }

  // member: dice_qa_replace
  {
    out << "dice_qa_replace: ";
    rosidl_generator_traits::value_to_yaml(msg.dice_qa_replace, out);
    out << ", ";
  }

  // member: hand_off_state
  {
    out << "hand_off_state: ";
    rosidl_generator_traits::value_to_yaml(msg.hand_off_state, out);
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const CellStatus & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: process_state
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "process_state: ";
    rosidl_generator_traits::value_to_yaml(msg.process_state, out);
    out << "\n";
  }

  // member: error_code
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "error_code: ";
    rosidl_generator_traits::value_to_yaml(msg.error_code, out);
    out << "\n";
  }

  // member: error_state
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "error_state: ";
    rosidl_generator_traits::value_to_yaml(msg.error_state, out);
    out << "\n";
  }

  // member: dice_detected_qa
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "dice_detected_qa: ";
    rosidl_generator_traits::value_to_yaml(msg.dice_detected_qa, out);
    out << "\n";
  }

  // member: dice_qa_pass
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "dice_qa_pass: ";
    rosidl_generator_traits::value_to_yaml(msg.dice_qa_pass, out);
    out << "\n";
  }

  // member: dice_qa_replace
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "dice_qa_replace: ";
    rosidl_generator_traits::value_to_yaml(msg.dice_qa_replace, out);
    out << "\n";
  }

  // member: hand_off_state
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "hand_off_state: ";
    rosidl_generator_traits::value_to_yaml(msg.hand_off_state, out);
    out << "\n";
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const CellStatus & msg, bool use_flow_style = false)
{
  std::ostringstream out;
  if (use_flow_style) {
    to_flow_style_yaml(msg, out);
  } else {
    to_block_style_yaml(msg, out);
  }
  return out.str();
}

}  // namespace msg

}  // namespace modbus_interfaces

namespace rosidl_generator_traits
{

[[deprecated("use modbus_interfaces::msg::to_block_style_yaml() instead")]]
inline void to_yaml(
  const modbus_interfaces::msg::CellStatus & msg,
  std::ostream & out, size_t indentation = 0)
{
  modbus_interfaces::msg::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use modbus_interfaces::msg::to_yaml() instead")]]
inline std::string to_yaml(const modbus_interfaces::msg::CellStatus & msg)
{
  return modbus_interfaces::msg::to_yaml(msg);
}

template<>
inline const char * data_type<modbus_interfaces::msg::CellStatus>()
{
  return "modbus_interfaces::msg::CellStatus";
}

template<>
inline const char * name<modbus_interfaces::msg::CellStatus>()
{
  return "modbus_interfaces/msg/CellStatus";
}

template<>
struct has_fixed_size<modbus_interfaces::msg::CellStatus>
  : std::integral_constant<bool, true> {};

template<>
struct has_bounded_size<modbus_interfaces::msg::CellStatus>
  : std::integral_constant<bool, true> {};

template<>
struct is_message<modbus_interfaces::msg::CellStatus>
  : std::true_type {};

}  // namespace rosidl_generator_traits

#endif  // MODBUS_INTERFACES__MSG__DETAIL__CELL_STATUS__TRAITS_HPP_
