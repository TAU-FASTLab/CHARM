from opcua import Client
import requests
import json
import sys, getopt
import time
import socket
from flask import Flask, render_template, request
from dataConfigurator import DataConfigurator, getArguments
from subscriber import DataSubsriber
import threading
import logging

args_list = sys.argv
app = Flask(__name__)

EP_SERVER_ADDRESS = "app"
EP_SERVER_PORT = None

config_file = None
Description = "Server Notifications"
entity_id = "Simulation"
entity_type = "3:Simulation"

sub_address = 'http://orion:1026/v2/subscriptions'
server_create = "http://orion:1026/v2/entities"
server_update = "http://orion:1026/v2/op/update"

#sub_address = 'http://localhost:1026/v2/subscriptions'
#server_create = "http://localhost:1026/v2/entities"
#server_update = "http://localhost:1026/v2/op/update"

headers = {"Content-Type": "application/json"}

# get commandline arguments
EP_SERVER_PORT, config_file = getArguments(args_list)

# check if config file is set
if config_file == None:
    config_file = 'attributes.json'


#create entities data object
orion_server = DataConfigurator(config_file)
print(orion_server.entity_data_create)

# set entity ID and type
entity_id = orion_server.json_data['id']
entity_type = orion_server.json_data['type']
print(entity_id)
print(entity_type)

url = orion_server.url
sub_nodes_list = orion_server.attr
attr = orion_server.attr

#create opc ua client and connect to opc ua server
try:
    client = Client(orion_server.url)
    client.connect()
    print("Client Connected")
except Exception as err:
    print("Error while creating the connection ", err)
    sys.exit(1)

# create context broker server subscriber
orion_subscriber = DataSubsriber(orion_server.list_of_ids, client)

def getEntities(server_address):
    r = requests.get(server_address)
    print(r.status_code)  # Press Ctrl+F8 to toggle the breakpoint.
    print(r.headers)
    print(r.content)
    my_json = json.loads(r.content)
    print(my_json)
    return r.status_code

################## To Do ########################################
code = getEntities((server_create +'/'+entity_id))


def northBoundCreate():
    r = requests.post(server_create, data=json.dumps(orion_server.json_data), headers=headers)
    print(r.status_code)


def northBoundUpdate():
    node_values = {}
    for key, value in orion_server.list_of_ids.items():
        opcua_id = value
        node = client.get_node(opcua_id)
        node_values[key] = node.get_value()

    # Getting names and Values using opcua_ids
    orion_server.updateEntity(node_values)
    orion_server.generateUpdateEntityData()
    r = requests.post(server_update, data=json.dumps(orion_server.entity_data_update), headers=headers)
    sys.stderr.write(str(r.status_code))
    sys.stdout.write("now logging")

if code != 200:
    #create entity
    northBoundCreate()
else:
    #update entity
    northBoundUpdate()

@app.route('/', methods=['POST'])
def process_data():
    response = request.json
    orion_subscriber.processSubData(response, sub_nodes_list)
    #print(result)
    return "Success"

# initailize
#@app.before_first_request
def init():
    global EP_SERVER_PORT
    #if EP_SERVER_ADDRESS == None:
        #hostname = socket.gethostname()
        #EP_SERVER_ADDRESS = socket.gethostbyname(hostname)

    if EP_SERVER_PORT == None:
        EP_SERVER_PORT = 80

    create_subscription(EP_SERVER_ADDRESS, EP_SERVER_PORT,\
                        Description, attr, entity_type)


#creates subscription on Context brocker
def create_subscription(EP_SERVER_ADDRESS, EP_SERVER_PORT, Description="Server Notifications",\
                        attr=[], entity_type="3:Simulation"):
    sub_data = {
                  "description": Description,
                  "subject": {
                    "entities": [{"idPattern": ".*", "type": entity_type}],
                    "condition": {
                      "attrs": attr
                    }
                  },
                  "notification": {
                    "http": {
                      "url": "http://"+ EP_SERVER_ADDRESS + ':' + str(EP_SERVER_PORT)
                    }
                  }
                }

    print(json.dumps(sub_data))
    headers = {"Content-Type": "application/json"}
    r = requests.post(sub_address, data=json.dumps(sub_data), headers=headers)
    print(r.status_code)
    print(r.content, '####################')


def runClient():
    while True:
        northBoundUpdate()
        time.sleep(5)

def runSubcriber():
    init()
    time.sleep(5)
    #app.run(host='0.0.0.0', debug=True, port=EP_SERVER_PORT, use_reloader=False)
    app.run(host='0.0.0.0', debug=True, port=EP_SERVER_PORT)


#t1 = threading.Thread(target=runClient)
#t1.start()

#runClient()


#if __name__== "__main__" :
    t1 = threading.Thread(target=runClient)
    #t2 = threading.Thread(target=runSubcriber)

    t1.start()
    #time.sleep(5)
    #t2.start()

    #t1.join()
    #t2.join()


