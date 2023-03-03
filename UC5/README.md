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

## Starting The Containers Individually (option 1)
Step 1: First pull the necessary Docker images from Docker Hub and create a network for our containers to connect to:
[Recommeded: GitBash/ Powershell]
```
docker pull mongo:4.2
docker pull fiware/orion
docker network create fiware_default
```
Step 2: A Docker container running a MongoDB database can be started and connected to the network with the following command:
```
docker run -d --name=mongo-db --network=fiware_default --expose=27017 mongo:4.2 --bind_ip_all
```
Step 3: The Orion Context Broker can be started and connected to the network with the following command:
```
docker run -d --name fiware-orion -h orion --network=fiware_default -p 1026:1026  fiware/orion -dbhost mongo-db


```
Step 4: You can check if the Orion Context Broker is running by making an HTTP request to the exposed port:
```
curl -X GET 'http://localhost:1026/version'
```
## Starting Containers Using Docker Compose file (option 2)
## This option is recommended when you you want to use PostgreSQL and Cygnus.

Step 1: Run this in the terminal
```
docker compose up -d

```
Step 2: You can check if the Orion Context Broker is running by making an HTTP request to the exposed port:
```
curl -X GET 'http://localhost:1026/version'
```

## Starting The Prosys Simulated Server
Download and Install Prosys OPC UA Server.

https://www.prosysopc.com/products/opc-ua-simulation-server/

Get the endpoint from the server and use it in the json file.
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
        "url": "opc.tcp://host.docker.internal:53530/OPCUA/SimulationServer",

        "subscriptions": ["3:test2"]
        }

}
```

Note: if you are using certificate and username/password encryption please go through below instructions for adding certificate details in Json file.

## Scripts 
*opcuaClient.py*:
It helps to connect with the Server with or without certificate:

*dataconfigurator.py*:
It reads the json file and store information e.g endpoint url, id, type and node ids etc. It also contain function to create, update entities.

*subscriber.py*:
It checks the update command from the client and check if the updated entry name, id or type is correct otherwise display the error.

*main.py*:
It connects with the server and check/create entities depending the json file and also update the entities after regular intervals. It also contain address of the Orion to create entities and subscriptions.



## Running the IoT Agent
Step 1: Step 1: Download the Python using following instruction
https://realpython.com/installing-python/


Step 2: Install all libraries given in the requirement.txt
```
pip install -r requirements.txt
``` 

Step 3: Create a json file for each agent as mentioned above. Each agent will run using different config file and port.
In order to run the agent write this command in the terminal

```
python main.py --Config=attributes1.json --Port=80
```
Similary for 2nd IoT agent you need to use different json file and Port

```
python main.py --Config=attributes2.json --Port=1001
```

Step 4: Check the orion using POSTMAN or Browser if you are getting entities:
```
http://localhost:1026/v2/entities
```

#### Running With Certificate 

### Introduction
The process of connecting IoT agent with Prosys Simulated OPC-UA Server using password and certificate is explained below:


### Loading the Certificate in Prosys Simulated OPCUA Server
Copy the certificate.pem file and paste it directory of your server.
```
C:[PATH].prosysopc\prosys-opc-ua-simulation-server\PKI\CA\private
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
