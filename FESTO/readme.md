## OPC UA (Client) IoT Agent by TAU
Containerized and Un-Containerized Version of IoT Agents are available with detailed instruction for using it in your system
```
https://github.com/TAU-FASTLab/CHARM/tree/main/UC5
```

## WSL with Ubuntu
For running FIROS we need a Linux and ROS and to use Linux within Windows we will use WSL2 for Installing Ubuntu. I
```
https://ubuntu.com/tutorials/install-ubuntu-on-wsl2-on-windows-10#1-overview
```
We have installed Ubuntu-20.04, you can use this command by running it in Command Prompt in admininstrative Mode
```
wsl --install -d Ubuntu-20.04
```
## Installing ROS in WSL 
This implementation works with ROS1 only, for installing ROS1 go through following link

```
http://wiki.ros.org/noetic/Installation/Ubuntu
```
## Integration with Docker 
It is supposed that you have already installed Docker while installing IoT Agent in your system. However if you still not have installed yet, you can explore this link

Install Docker on your system depending on Operating System (Linux, Windows, Mac) https://www.docker.com/

![image](https://user-images.githubusercontent.com/106956110/235683106-7dbb7df9-92a8-4df0-96b5-bfcfa72d92b6.png)


After installing you can check your current Docker and Docker Compose versions using the following commands in bash terminal:
```
docker-compose -v
docker version
```
Open Docker Desktop in Windows and go to Settings>Resources> WSL Integration
Enable integration with additional distros with your install Ubuntu

image.png

## Environment setup for ROS
You must source this script in every bash terminal you use ROS in.
```
. ~/catkin_ws/devel/setup.bash
source /opt/ros/noetic/setup.bash
```
## Cloning with FIROS Repositry
After you have set up ROS and created a catkin-workspace you can finally clone this repository, install its dependencies and create the FIROS-Node as follows:

```
cd "catkin_ws"/src
git clone --recursive https://github.com/iml130/firos.git
cd "catkin_ws"/src/firos

# Install Dependencies
pip install -r requirements.txt

# Make Node
cd "catkin_ws"
catkin_make
```
### ROS Package and ROS Nodes 

You need rosnode that publish and subscribe your desire topic. For me I have used robot1 as package and getjoints.py and cartesianpoints.py as ROS nodes. You have to RUN your nodes to send data the topic to Orion

You fill find robot1 in the directory.

## Configration in FIROS

Make two config folder "config_1" and "config_2" with three files in each folder. config folder given can be seen as example for understanding

1. config.json
2. topics.json
3. whitelist.json

Each of the configuration folder do have the following files with the following content:

config.json :
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

whitelist.json :
```
{}
```
### NOTE config.json: The Context-Broker runs locally, so the configuration should be fine for you, as long as your Context-Broker is also locally.

Inside config_1 we add the file topics.json with the following content:
```
{
    "/rv_3sdb/showJointPosition": ["robot1/jointMessage", "publisher"],
    "/showCartesianPoints": ["robot1/cartesianMessage", "publisher"] 
}
```
  

and for config_2 the following swapped content:
```
{
    "/rv_3sdb/showJointPosition": ["robot1/jointMessage", "subscriber"],
    "/showCartesianPoints": ["robot1/cartesianMessage", "subscriber"]
}
```

### Run catkin_make so all packages are updated.
```
catkin_make
```


# Run Roscore, Orion and Mongo

Go to following directory through Linux Terminal
```
cd "catkin_ws"/src/firos/docker
```
Now enter this command to run the containers
```
docker-compose up
```
or

```
sudo docker-compose up
```

### Check if the Orion is Running 
```
http://localhost:1026/v2/entities
```
You will get response:
```
[]
```

## Running ros-nodes for Reading Joints and Cartiesian Points
### Terminal 1
```
rosrun robot1 getJoints.py
```
### Terminal 2

```
rosrun robot1 cartesianpoints.py
```

### After running node check rostopic list by:
```
rostopic list
```
You will get something like this:
```
/rosout
/rosout_agg
/rv_3sdb/showJointPosition
/showCartesianPoints

```

### Start FiROS Service to Subscribe to the topic published by Robot
```
python3 src/firos/firos/core.py --conf src/firos/config_1
```

### Start FiROS Service to Publish to the 2nd topic subscribed by Robot
```
python3 src/firos/firos/core.py --conf src/firos/config_2 -P 10101 --ros-node-name firos2
```
