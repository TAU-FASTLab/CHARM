The overall layout of the framework looks like this:
![Picture1a](https://user-images.githubusercontent.com/106956110/223063503-fa8de3c7-4390-49e7-b811-b12569cf7a29.png)

### Installation of Windows 
You can install your desire version of windows using following link:
https://support.microsoft.com/en-us/windows/create-installation-media-for-windows-99a58364-8c02-206f-aa6f-40c3b507420d

### Installing Docker on your system
Install Docker on your system depending on Operating System (Linux, Windows, Mac)
https://www.docker.com/

After installing you can check your current Docker and Docker Compose versions using the following commands in bash terminal:
```
docker-compose -v
docker version
```

## Introduction to Containerized Version of IoT Agent
This is a containerised version of the OPC UA IoT Agent for connecting the OPC UA server to the cloud. The Orion Context Broker uses a mongo db to store context data. Orion is an API Server service from Fiware. 

This aplication allows to create multiple IoT containers from one Image, each representig one OPC UA server. Configuration files for each Server must be created and provided before creating the image

## Starting The Prosys Simulated Server
Download and Install Prosys OPC UA Server.

https://www.prosysopc.com/products/opc-ua-simulation-server/

Get the endpoint from the server and use it in the json file (UC5/IoT Agent Version 2 (Containerized)/app/attributes.json).
It will be similar to this: "opc.tcp://<user>:53530/OPCUA/SimulationServer"

Analyze the attributes (Counters, Random ....) you want to read/write, you can add more attributes if you want.

## Or Setting up OPC UA Server in PLC
Open the PLC via TIA Portal and go to device configration
Go to properties and Activate OPCUA Server 
Use the OPCUA endpoint in the json file.
If there is certicate encryption, get the certificate and save it in the directory of IoT Agent (IOT_AGENT_V2/Certificate) and follow the instructions given for connection using certificate 
Go to tags to see attributes and node id and name.

## Json file

In order to read attributes from OPCUA Server we need to make a json file containing all attributes node names, namespace-ids and types along with Id and type of the Server. The Server endpoint and subscriptions must be highlighted in the json file. In subscriptions you have to mention those attributes for which you want to get notified if there is any change in them. Example of syntax:

```
{
     "data": {
        "id": "Simulation",
         "type": "3:Simulation",
         "3:Counter": {
             "type": "Int32",
             "opcua_id" : "ns=3;i=1001",
             "value": "10",
             "metadata": {}
         	},
         "3:test2": {
             "type": "Double",
             "opcua_id" : "ns=3;i=1002",
             "value": "10",
             "metadata": {}
         	}
     },
        "Config": {
        "url": "opc.tcp://<hostname>:53530/OPCUA/SimulationServer",

        "subscriptions": ["3:test2"]
        }

}
```

Note: if you are using certificate and username/password encryption please go through below instructions for adding certificate details in Json file.

# Running With Certificate 

Note: If you want to run without certificate, please jump to section "Build an Image"

### Introduction
The process of connecting IoT agent with Prosys Simulated OPC-UA Server using password and certificate is explained below:


### Loading the Certificate in Prosys Simulated OPCUA Server
Copy the certificate.pem file and paste it directory of your server.
```
C:[PATH].prosysopc\prosys-opc-ua-simulation-server\PKI\CA\private
C:[PATH].prosysopc\prosys-opc-ua-simulation-server\PKI\CA\certs
```

It will add certificate in your server and you can verify this by looking at certificate tab of your server. You will see the certificate with the name you have given to it with tagline as "Trusted"

## Setting the username and password & Certificate 
Open the "user" tab from your server and uncheck "Anonymous" & "IssuedToken/External System" and check "Username & Passoword" and "Certificate" save it and restart your server.


## Adding the Certificate Details in Json File
Add all details including, urn, username, password, security_policy, security_mode, certificate path and key path where you have saved the certificate and key in your system. You can make changes according to your requirements
```
  "certificate": {
        "uri": "urn:WKS-98992-LT.mshome.net:OPCUA:SimulationServer",
        "ip": "127.0.0.1",
        "username": "<username>",
        "password": "<password>",
        "security_policy": "Basic256Sha256",
        "security_mode": "SignAndEncrypt",
        "cert_path": "Certificate/certificate.pem", 
        "key_path": "Certificate/key.pem"

        
    }
```

## Build an Image
```
docker build -t iotimage .

```
Note: Incase you find any issue while building an image, make sure you have installed correct version of **python** and also **Docker Desktop** is installed properly.

## Selection of Approach to run the IoT Agent:
1. One at a time via command line
2. Running all container using docker-compose file
     
### Aproach 1: Creating containers one at a time via command line

## Start the Orion Context Brocker
```
docker-compose -f docker-compose-orion.yml up -d
```

## Get the network on Which Orion is running
```
docker network ls
```

## Result Should look something like this
```
NETWORK ID     NAME                            DRIVER    SCOPE
f56cc2696b38   bridge                          bridge    local
96f8515c9c47   host                            host      local
005d2e84fb3e   iotagentcontainerized_default   bridge    local
c074378cef3c   none                            null      local

```
## To add Why two stations, not one, not five, what is the difference between these two, which is the main difference between, both interact with the same components?
     
## Run Station 1
In the app folder there are some json files (_**attributes.json, attributesRexygen.json**_). You can edit these json files according to your server by putting attributes and endpoint of your server.

orion_network refers to the network on which orion is running
```
docker run -d --name=iot1 --network=iotagentcontainerized_default --env Config=attributes.json iotimage

```

## Run Station 2

In the app folder there are some json files (_**attributes.json, attributesRexygen.json**_). You can edit these json files according to your server by putting attributes and endpoint of your server.
orion_network refers to the network on which orion is running
```
docker run -d --name=iot2 --network=iotagentcontainerized_default --env Config=attributesRexygen.json iotimage

```


### Aproach 2: Creating all containers at one using a docker-compose file
## Open the docker compose file and add all IoT Agents specifying their config file names as environment variables
```
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
## Run the docker-compose file
```
docker-compose up -d
```
## Checking Entities in the Orion
If your containers and IoT Agents are running fine you can check **entities** from this link
```
localhost:1026/v2/entities
```
**Subscriptions** can be checked using this link
```
localhost:1026/v2/subscriptions
```
If you want to update any entities in Orion and Server you have to **Post** to following link 
```
localhost:1026/v2/op/update
```
Make sure you follow the same format for sending the update
```
{
"actionType": "update",
"entities": [
{
        "id": "Simulation",
        "type": "3:Simulation",
        "3:test2": {
            "type": "Number",
            "value": 90,
            "metadata": {}
        }
}
]
}
```   
# For accessing PostgreSQL DB use following commands

## Checking The Cygnus Service Health
### Request
```
curl -X GET \
  'http://localhost:5080/v1/version'
```
### Response will be like this one if its running fine
```
{
    "success": "true",
    "version": "'2.16.etc"
}
```

## Subscribing To Context Changes
### Request
```
'
curl -iX POST \
  'http://localhost:1026/v2/subscriptions' \
  -H 'Content-Type: application/json' \
  -d '{
  "description": "Notify Cygnus Postgres of all context changes",
  "subject": {
    "entities": [
      {
        "idPattern": ".*"
      }
    ]
  },
  "notification": {
    "http": {
      "url": "http://cygnus:5055/notify"
    }
  },
  "throttling": 5
}'
```

### The response will be 201 - Created

## PostgreSQL - Reading Data From A Database
```
winpty docker run -it --rm  --network iot_agent_v2_default jbergknoff/postgresql-client postgresql://<username>:<password>@postgres-db:5432/postgres
```

## Show Available Databases On The PostgreSQL Server
### To show the list of available databases, run the statement as shown:

### Query:
```
\list 
```
### To show the list of available schemas, run the statement as shown:

```
\dn
```
## Read Historical Context From The PostgreSQL Server 
```
SELECT table_schema,table_name
FROM information_schema.tables
WHERE table_schema ='default_service'
ORDER BY table_schema,table_name;
```
```
SELECT * FROM default_service.simulation_3_simulation limit 10;
```

For more information and details you can visit the fiware tutorial for postgreSQL:
https://fiware-tutorials.readthedocs.io/en/latest/historic-context-flume.html#postgresql-start-up
