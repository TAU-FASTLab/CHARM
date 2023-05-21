## ROS2 Implementation with FIROS 

This guide describes the proposed ROS2 implementation with FIROS. The first step is to install ROS2 on the local computer. Ubuntu 20.04 is used on virtual machine and ROS is installed on it. Foxy distribution was used for the project that can be installed from: 

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

The modified versions can be cloned from this repository. After this, run the following.
```
cd ros2_ws/src/firos

# Install Dependencies
pip install -r requirements.txt

# Make Node in base directory
cd ../../
colcon build
```
Use the CMakeLists.txt and package.xml files from this repository and replace it with the existing files. 

## Docker Setup

You will need Docker engine and desktop installed on the system in order to run the IoT agent. Docker engine can be installed from the following link. 
https://docs.docker.com/engine/install/ubuntu/

Docker desktop can be installed from the following link. 
https://docs.docker.com/desktop/install/ubuntu/

Run the following command:
```
sudo docker run hello world
```

If installed correctly, you will be able to see something like this. 

<img width="551" alt="docker" src="https://github.com/TAU-FASTLab/CHARM/assets/84769093/7534ded3-86d4-4c95-b582-3914606c642f">

## RT Toolbox Setup 

Open RT Toolbox and add a new robot model named RV-3SDB that corresponds the the FESTO line robot. You will get a window similar to this. 
![rt toolbox](https://github.com/TAU-FASTLab/CHARM/assets/84769093/3bbdf6d6-ae39-4107-b82f-0f855215c0ac)

Next, select the IP address and port address. 
![rt toolbox 2](https://github.com/TAU-FASTLab/CHARM/assets/84769093/72ee80ec-93ea-4078-a4c9-bb43779b067c)


## FIROS Config files 

In the firos directory, create two folders, config_1 and config_2 that contain the following files. 

![config](https://github.com/TAU-FASTLab/CHARM/assets/84769093/a21db96c-7a95-41a1-88ba-7c9f99c7048f)

The config.json file will have the following content. 

```
{
    "environment": "test",
    "test": {
        "contextbroker": {
            "address": "localhost",
            "port": 1026
        }
    }
}
```

The whitelist.json file will have the following content. '
```
{}
```
For config_1 files, add the following commands for the topics and messages. 
```
{
    "/rv_3sdb/showJointPosition": ["festo/jointMessage", "publisher"],
    "/showCartesianPoints": ["festo/cartesianMessage", "subscriber"] 
}
```

For config_2 file, add the following commands. '
```
{
    "/rv_3sdb/showJointPosition": ["festo/jointMessage", "subscriber"],
    "/showCartesianPoints": ["festo/cartesianMessage", "publisher"] 
}
```

Notice that the publisher and subsciber are swapped here. 

After making these changes, build the package again using colon_build. 

Move to the docker folder inside the directory and run. 
```
sudo docker compose up
```

Once all the containers are started, you can check if the Orion context broker is running from. 
```
http://localhost:1026/v2/entities
```
