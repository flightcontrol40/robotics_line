// generated from rosidl_generator_py/resource/_idl_support.c.em
// with input from modbus_interfaces:msg/CellStatus.idl
// generated code does not contain a copyright notice
#define NPY_NO_DEPRECATED_API NPY_1_7_API_VERSION
#include <Python.h>
#include <stdbool.h>
#ifndef _WIN32
# pragma GCC diagnostic push
# pragma GCC diagnostic ignored "-Wunused-function"
#endif
#include "numpy/ndarrayobject.h"
#ifndef _WIN32
# pragma GCC diagnostic pop
#endif
#include "rosidl_runtime_c/visibility_control.h"
#include "modbus_interfaces/msg/detail/cell_status__struct.h"
#include "modbus_interfaces/msg/detail/cell_status__functions.h"


ROSIDL_GENERATOR_C_EXPORT
bool modbus_interfaces__msg__cell_status__convert_from_py(PyObject * _pymsg, void * _ros_message)
{
  // check that the passed message is of the expected Python class
  {
    char full_classname_dest[46];
    {
      char * class_name = NULL;
      char * module_name = NULL;
      {
        PyObject * class_attr = PyObject_GetAttrString(_pymsg, "__class__");
        if (class_attr) {
          PyObject * name_attr = PyObject_GetAttrString(class_attr, "__name__");
          if (name_attr) {
            class_name = (char *)PyUnicode_1BYTE_DATA(name_attr);
            Py_DECREF(name_attr);
          }
          PyObject * module_attr = PyObject_GetAttrString(class_attr, "__module__");
          if (module_attr) {
            module_name = (char *)PyUnicode_1BYTE_DATA(module_attr);
            Py_DECREF(module_attr);
          }
          Py_DECREF(class_attr);
        }
      }
      if (!class_name || !module_name) {
        return false;
      }
      snprintf(full_classname_dest, sizeof(full_classname_dest), "%s.%s", module_name, class_name);
    }
    assert(strncmp("modbus_interfaces.msg._cell_status.CellStatus", full_classname_dest, 45) == 0);
  }
  modbus_interfaces__msg__CellStatus * ros_message = _ros_message;
  {  // process_state
    PyObject * field = PyObject_GetAttrString(_pymsg, "process_state");
    if (!field) {
      return false;
    }
    assert(PyLong_Check(field));
    ros_message->process_state = (int8_t)PyLong_AsLong(field);
    Py_DECREF(field);
  }
  {  // error_code
    PyObject * field = PyObject_GetAttrString(_pymsg, "error_code");
    if (!field) {
      return false;
    }
    assert(PyLong_Check(field));
    ros_message->error_code = (int8_t)PyLong_AsLong(field);
    Py_DECREF(field);
  }
  {  // error_state
    PyObject * field = PyObject_GetAttrString(_pymsg, "error_state");
    if (!field) {
      return false;
    }
    assert(PyLong_Check(field));
    ros_message->error_state = (int8_t)PyLong_AsLong(field);
    Py_DECREF(field);
  }
  {  // dice_detected_qa
    PyObject * field = PyObject_GetAttrString(_pymsg, "dice_detected_qa");
    if (!field) {
      return false;
    }
    assert(PyLong_Check(field));
    ros_message->dice_detected_qa = (int8_t)PyLong_AsLong(field);
    Py_DECREF(field);
  }
  {  // dice_qa_pass
    PyObject * field = PyObject_GetAttrString(_pymsg, "dice_qa_pass");
    if (!field) {
      return false;
    }
    assert(PyLong_Check(field));
    ros_message->dice_qa_pass = (int8_t)PyLong_AsLong(field);
    Py_DECREF(field);
  }
  {  // dice_qa_replace
    PyObject * field = PyObject_GetAttrString(_pymsg, "dice_qa_replace");
    if (!field) {
      return false;
    }
    assert(PyLong_Check(field));
    ros_message->dice_qa_replace = (int8_t)PyLong_AsLong(field);
    Py_DECREF(field);
  }
  {  // hand_off_state
    PyObject * field = PyObject_GetAttrString(_pymsg, "hand_off_state");
    if (!field) {
      return false;
    }
    assert(PyLong_Check(field));
    ros_message->hand_off_state = (int8_t)PyLong_AsLong(field);
    Py_DECREF(field);
  }

  return true;
}

ROSIDL_GENERATOR_C_EXPORT
PyObject * modbus_interfaces__msg__cell_status__convert_to_py(void * raw_ros_message)
{
  /* NOTE(esteve): Call constructor of CellStatus */
  PyObject * _pymessage = NULL;
  {
    PyObject * pymessage_module = PyImport_ImportModule("modbus_interfaces.msg._cell_status");
    assert(pymessage_module);
    PyObject * pymessage_class = PyObject_GetAttrString(pymessage_module, "CellStatus");
    assert(pymessage_class);
    Py_DECREF(pymessage_module);
    _pymessage = PyObject_CallObject(pymessage_class, NULL);
    Py_DECREF(pymessage_class);
    if (!_pymessage) {
      return NULL;
    }
  }
  modbus_interfaces__msg__CellStatus * ros_message = (modbus_interfaces__msg__CellStatus *)raw_ros_message;
  {  // process_state
    PyObject * field = NULL;
    field = PyLong_FromLong(ros_message->process_state);
    {
      int rc = PyObject_SetAttrString(_pymessage, "process_state", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }
  {  // error_code
    PyObject * field = NULL;
    field = PyLong_FromLong(ros_message->error_code);
    {
      int rc = PyObject_SetAttrString(_pymessage, "error_code", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }
  {  // error_state
    PyObject * field = NULL;
    field = PyLong_FromLong(ros_message->error_state);
    {
      int rc = PyObject_SetAttrString(_pymessage, "error_state", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }
  {  // dice_detected_qa
    PyObject * field = NULL;
    field = PyLong_FromLong(ros_message->dice_detected_qa);
    {
      int rc = PyObject_SetAttrString(_pymessage, "dice_detected_qa", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }
  {  // dice_qa_pass
    PyObject * field = NULL;
    field = PyLong_FromLong(ros_message->dice_qa_pass);
    {
      int rc = PyObject_SetAttrString(_pymessage, "dice_qa_pass", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }
  {  // dice_qa_replace
    PyObject * field = NULL;
    field = PyLong_FromLong(ros_message->dice_qa_replace);
    {
      int rc = PyObject_SetAttrString(_pymessage, "dice_qa_replace", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }
  {  // hand_off_state
    PyObject * field = NULL;
    field = PyLong_FromLong(ros_message->hand_off_state);
    {
      int rc = PyObject_SetAttrString(_pymessage, "hand_off_state", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }

  // ownership of _pymessage is transferred to the caller
  return _pymessage;
}
