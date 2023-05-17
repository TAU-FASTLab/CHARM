## ROS2 Implementation with FIROS 

This guide describes the ROS2 implementation with FIROS. The first step is to install ROS2 on the local computer. Ubuntu 20.04 is used on virtual machine and ROS is installed on it. Foxy distribution was used for the project that can be installed from: 

https://docs.ros.org/en/foxy/Installation/Ubuntu-Install-Debians.html  

The first step is to create a ROS 2 workspace in the system. First, we have to source the setup.bash file for the ROS distribution.
```source/opt/ros/foxy/setup.bash```

Next, we can create the directory using the following command. 
```
mkdir ros2_ws/src
cd src
```
