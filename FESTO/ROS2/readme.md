## ROS2 Implementation with FIROS 

This guide describes the ROS2 implementation with FIROS. The first step is to install ROS2 on the local computer. Ubuntu 20.04 is used on virtual machine and ROS is installed on it. Foxy distribution was used for the project that can be installed from: 

https://docs.ros.org/en/foxy/Installation/Ubuntu-Install-Debians.html  

The first step is to create a ROS 2 workspace in the system. First, we have to source the setup.bash file for the ROS distribution.
```source/opt/ros/foxy/setup.bash```

<img width="366" alt="ros2 " src="https://github.com/TAU-FASTLab/CHARM/assets/84769093/fc6aaacc-b763-4031-81c4-194a53b4c8ab">

If the installation is performed correctly, you can see the the 'foxy' version displayed after the rosversion command. Next, we can create the directory using the following commands. 
```
mkdir ros2_ws/src
cd src
```
The FIROS package is imported in the src folder
```
git clone --recursive https://github.com/iml130/firos.git

```
Since this package is developed for ROS 1, there are several changes that need to be made in order to make it compatible for ROS 2. The CMakeLists.txt and package.xml files need to be modified. 

ROS 2 uses ament based build system called using colcon as compared to catkin_make for ROS 1. Therefore, all catkin tools need to be converted to ament packages. In addition to this, the C++ and Python dependencies are also different. Instead of rospy and roscpp, rclpy and rclpp are used for the latter version. 
