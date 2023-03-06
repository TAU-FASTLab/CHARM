### Introduction
This is a containerised version of the OPC UA IoT Agent for connecting the OPC UA server to the cloud. The Orion Context Broker uses a mongo db to store context data. Orion is an API Server service from Fiware. 

This aplication allows to create multiple IoT containers from one Image, each representig one OPC UA server. Configuration files for each Server must be created and provided before creating the image

## Build an Image
```
docker build -t iotimage .

```
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

## Run Station 1
orion_network refers to the network on which orion is running
```
docker run -d --name=iot1 --network=iotagent__containerized_v2-postgresql_default --env Config=attributes.json iotimage

```

## Run Station 2
orion_network refers to the network on which orion is running
```
docker run -d --name=iot1 --network=iotagent__containerized_v2-postgresql_default --env Config=attributesRexygen.json iotimage

```
### Aproach 2: Creating all containers at one using a docker-compose file
## Open the docker compose file and add all IoT Agents specifying theier config file names as environment variables
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

