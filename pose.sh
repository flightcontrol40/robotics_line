ros2 topic pub "/beaker/cur_cartesian" fanuc_interfaces/CurCartesian "{\
pose: [
 465.18743896484375,
 300.421142578125,
 -148.9210662841797,
 94.78654479980469,
 -64.60704803466797,
 175.4700164794922
 ]
}"

ros2 topic pub "/beaker/grip_status" fanuc_interfaces/CurGripper "{open: true}"


ros2 topic pub "/beaker/robot_status" robot_3_interfaces/RobotStatus "{\
process_state: 4
error_code: 0
error_status: false
die_qa: true
r2_handoff: true
}"
