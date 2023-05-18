cmake_minimum_required(VERSION 3.5)
project(firos)

## Required dependencies for firos
find_package(ament_cmake REQUIRED)
find_package(rclcpp REQUIRED)
find_package(std_msgs REQUIRED)
find_package(rosidl_default_generators REQUIRED)


#rosidl_generate_interfaces(firos 
#  ${msg_files}
#  DEPENDENCIES std_msgs 
#)

rosidl_generate_interfaces(firos 
#set(msg_files 
  "msgs/geometry_msgs/Twist.msg"
  "msgs/geometry_msgs/Vector3.msg"
  "msgs/std_msgs/Header.msg"
  "msgs/turtlesim/Pose.msg"
   )
	
## Include directories
include_directories(
  include
  ${rclcpp_INCLUDE_DIRS}
  ${std_msgs_INCLUDE_DIRS}
  #${message_generation_INCLUDE_DIRS}
)

## Declare a C++ library
add_library(firos src/firos.cpp)
ament_target_dependencies(firos rclcpp std_msgs)

## Install
install(
  DIRECTORY include/firos/
  DESTINATION include/firos/
)

install(
  TARGETS firos
  ARCHIVE DESTINATION lib
  LIBRARY DESTINATION lib
  RUNTIME DESTINATION bin
)

ament_export_dependencies(rosidl_default_runtime)

ament_package()

