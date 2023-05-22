## FESTO Architecture of Implementation 

![MicrosoftTeams-image (8)](https://user-images.githubusercontent.com/106956110/236144278-a329aa69-8c6c-4b38-a0ee-a32996d88160.png)

## OPC UA (Client) IoT Agent by TAU
Containerized and Un-Containerized Version of IoT Agents are available with detailed instruction for using it in your system. (follow the below guidance, until the image build?, do not run the images yet)
```
https://github.com/TAU-FASTLab/CHARM/tree/main/UC5 
```

Once you have build an image explained in above link, You will find the json files in the folder IoT_agent (e.g. UC5/IoT Agent Version 2 (Containerized)) you can changes json depending on your server and run using the following sentence, which is a generic form how to run station. For detail steps, follow the link  e.g. for one station (MPS) https://github.com/TAU-FASTLab/CHARM/tree/main/UC5/IoT%20Agent%20Version%202%20(Containerized)#run-station-1 (In the same folder that the image was built)
```
#Generic example (for Option 1 in IoT Agent)
docker run -d --name=Processing_PLC --network=<network_name> --env Config=<json_file_name>.json iotimage
```

```
# To be updated
#Generic example (for Option 2 in IoT Agent)
  # IoT Agent
  iot-agent:
    labels:
      org.fiware: 'tutorial'
    image: iotimage
    hostname: app
    container_name: app-iot
    depends_on: 
      - orion
    networks:
      - default
    extra_hosts:
      - "opcuaserver:127.0.0.1" 
    environment:
      - Config=attributesPLC1.json
      - Port=80
```

![tempsnip](https://user-images.githubusercontent.com/106956110/235911166-bca1d333-b235-4725-9842-266fcd72a9b0.png)



## WSL with Ubuntu
For running FIROS we need a Linux and ROS and to use Linux within Windows we will use WSL2 for Installing Ubuntu. I
```
https://ubuntu.com/tutorials/install-ubuntu-on-wsl2-on-windows-10#1-overview
```
We have installed Ubuntu-20.04, you can use this command by running it in Command Prompt in admininstrative Mode
```
wsl --install -d Ubuntu-20.04
```
![image](https://user-images.githubusercontent.com/106956110/236154543-b269dc27-a554-4fd9-b167-9150683c5f95.png)

## Installing ROS in WSL 
This implementation works with ROS1 only, for installing ROS1 go through following link

```
http://wiki.ros.org/noetic/Installation/Ubuntu
```
For this implementation we have used this 

**Desktop-Full Install: (Recommended) :** Everything in Desktop plus 2D/3D simulators and 2D/3D perception packages

```
sudo apt install ros-noetic-desktop-full
```

if you face an error : **_"Temporary failure in name resolution"_** go through following link:

https://phoenixnap.com/kb/temporary-failure-in-name-resolution


Make sure you have installed ros correctly
You must source this script in every bash terminal you use ROS in.
```
source /opt/ros/noetic/setup.bash
```
You can check ROS version installed:
```
rosversion -d
```
roscore is a collection of nodes and programs that are pre-requisites of a ROS-based system. You must have a roscore running in order for ROS nodes to communicate. It is launched using the roscore command.
```
roscore
```
![image](https://user-images.githubusercontent.com/106956110/236155230-34f29580-40e6-4084-aa0b-e58fa548294e.png)


## Integration with Docker 
It is supposed that you have already installed Docker while installing IoT Agent in your system. However if you still not have installed yet, you can explore this link

Install Docker on your system depending on Operating System (Linux, Windows, Mac) https://www.docker.com/

Open Docker Desktop in Windows and go to Settings>Resources> WSL Integration
Enable integration with additional distros with your install Ubuntu

![image](https://user-images.githubusercontent.com/106956110/235683106-7dbb7df9-92a8-4df0-96b5-bfcfa72d92b6.png)


After installing you can check your current Docker and Docker Compose versions using the following commands in bash terminal:
```
docker-compose -v
docker version
```


## RT ToolBox Configration


Select New from the RT-ToolBox window and follow the following steps:

1. Select robot model that you want to use. We are using RV-3SDB for this implementation for both Simulation and Real Robot
![image](https://user-images.githubusercontent.com/106956110/236159208-778e666e-fdbd-465c-af69-01686ac6c9d0.png)

2. Communication with Robot Controller is important step. Here we are using IP address and PORT at which Robot controller is configured in FESTO line

![image](https://user-images.githubusercontent.com/106956110/236159508-6613041f-bf81-47a1-bfa8-89c4d2037ef4.png)

3. After completing other basic setting you will get the windows something like this

![image](https://user-images.githubusercontent.com/106956110/236159138-a29be089-9173-49df-8957-8aba5aa5cad0.png)


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
## ROS Package and ROS Nodes for communicating with RT-ToolBox

Download robot1 folder given in the repositry. Change the configrations in scripts i.e (TCP IP and TCP Port) to connect with RT ToolBox. Do it for all scripts, current configrations are according to FESTO line Robot Controller connected to RT-Toolbox

![tempsnip1](https://user-images.githubusercontent.com/106956110/236164001-cdd6035b-57b1-4705-83f7-4a59eec5bb03.png)


You need rosnode that publish and subscribe your desire topic. For this implementation have used robot1 as package and getjoints.py and cartesianpoints.py as ROS nodes. You have to RUN your nodes to send data the topic to Orion.


## Configration in FIROS

Make two config folder "config_1" and "config_2" with three files in each folder. config folder in the reposity given can be seen as example for understanding

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
![image](https://user-images.githubusercontent.com/106956110/236196102-0e41477b-727d-48c9-a557-131f8456da24.png)

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
![Screenshot (13)](https://user-images.githubusercontent.com/106956110/236203047-7d8d0b66-104e-441d-bda0-c5f6a15c9800.png)


### Start FiROS Service to Subscribe to the topic published by Robot
```
python3 src/firos/firos/core.py --conf src/firos/config_1
```

### Start FiROS Service to Publish to the 2nd topic subscribed by Robot
```
python3 src/firos/firos/core.py --conf src/firos/config_2 -P 10101 --ros-node-name firos2
```
![image](https://user-images.githubusercontent.com/106956110/236204113-b1d9ff72-cc23-4160-a9e4-e8423dd97349.png)

## Simulated OPC UA Server with IoT Agent Sending Entities to Orion
![Screenshot (6)](https://user-images.githubusercontent.com/106956110/236204359-fa202acd-5d46-415b-80c6-c83f62cbf5b9.png)

## Docker Container Running
![Screenshot (5)](https://user-images.githubusercontent.com/106956110/236204261-82900e07-c51c-4b99-b8e3-cb364d5580fe.png)

## Simulated Robot with FIROS Sending Joints and Cartesian Points to Orion
![Screenshot (3)](https://user-images.githubusercontent.com/106956110/236204192-0b8efcac-f392-4b94-8ff3-c1fca01400c4.png)

