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
from opcua.crypto import uacrypto
from opcuaClient import OpcuaClient
import logging

# create a logger
logger = logging.getLogger()
# log all messages, debug and up
logger.setLevel(logging.INFO)

args_list = sys.argv
app = Flask(__name__)

EP_SERVER_ADDRESS = None
EP_SERVER_PORT = None
subscription_id = None
config_file = None
Description = "Server Notifications"
entity_id = "Simulation"
entity_type = "3:Simulation"

sub_address = "http://localhost:1026/v2/subscriptions"
server_create = "http://localhost:1026/v2/entities"
server_update = "http://localhost:1026/v2/op/update"
headers = {"Content-Type": "application/json"}

# get commandline arguments
EP_SERVER_PORT, config_file = getArguments(args_list)

# check if config file is set
if config_file == None:
    config_file = "attributescert.json"


# create entities data object
orion_server = DataConfigurator(config_file)
print(orion_server.create_entities_data)
print(orion_server.update_entities_data)

# set entity ID and type
entity_id = orion_server.json_data["id"]
entity_type = orion_server.json_data["type"]

url = orion_server.url
print("OPCUA Server Endpoint: ", url)
sub_nodes_list = orion_server.attr
attr = orion_server.attr
client = OpcuaClient(orion_server)

# create opc ua client and connect to opc ua server
try:
    client.client.connect()
    print("Client Connected Successfully to OPCUA Server")

except Exception as err:
    print("Error while creating the connection with OPCUA-Server ", err)
    sys.exit(1)

# create context broker server subscriber
orion_subscriber = DataSubsriber(orion_server.list_of_ids, client)


def northBoundCreate():
    r = requests.post(
        server_create, data=json.dumps(orion_server.json_data), headers=headers
    )
    print(r.status_code)


class EventHandler(object):
    def datachange_notification(self, node, val, data):
        # Getting names and Values using opcua_ids
        print("---------------------------------------------")
        print(val)
        print(node)
        print(type(node))
        print(data)
        print("------------------------------------------------")

        orion_server.updateNode(node, val)
        orion_server.updateEntities()
        r = requests.post(
            server_update,
            data=json.dumps(orion_server.update_entities_data),
            headers=headers,
        )
        t = time.localtime()
        current_time = time.strftime("%H:%M:%S", t)
        print(r.status_code, "Entities Updated", current_time)


def northBoundUpdate():
    nodes = []

    for key, value in orion_server.list_of_ids.items():
        opcua_id = value
        node = client.client.get_node(opcua_id)
        nodes.append(node)
    test_values = client.client.get_values(nodes)
    print(test_values)

    handler = EventHandler()
    sub = client.client.create_subscription(5000, handler)
    handle = sub.subscribe_data_change(nodes)


def getEntities(server_address):
    r = requests.get(server_address)
    print(r.status_code)
    print(r.headers)
    print(r.content)
    my_json = json.loads(r.content)
    print(my_json)
    return r.status_code


@app.route("/", methods=["POST"])
def process_data():
    response = request.json
    print(response)
    orion_subscriber.updateOpcuaServer(response, sub_nodes_list)
    return "Success"


# initailize
def initSouthBound():
    global EP_SERVER_ADDRESS, EP_SERVER_PORT
    if EP_SERVER_ADDRESS == None:
        hostname = socket.gethostname()
        EP_SERVER_ADDRESS = socket.gethostbyname(hostname)
        print(EP_SERVER_ADDRESS)

    if EP_SERVER_PORT == None:
        EP_SERVER_PORT = 80

    # check for duplicate subscriptions
    orion_subscriber.check_subscriptions(sub_address, entity_id)

    # create subscription
    orion_subscriber.create_subscription(
        EP_SERVER_ADDRESS,
        EP_SERVER_PORT,
        sub_address,
        Description,
        attr,
        entity_id,
        entity_type,
    )


def initNorthBound():
    code = getEntities((server_create + "/" + entity_id))
    if code == 400:
        print("Bad Request HTTP Error 400")
        sys.exit(1)

    elif code == 404:
        print("Entity ID Not Found HTTP Error 404")

    elif code == 200:
        print("Standard response for successful HTTP requests, 200")

    if code != 200:
        # create entity
        northBoundCreate()


def runClient():
    initNorthBound()
    northBoundUpdate()
    print("Unsubscribing !!")
    # orion_subscriber.unsubscribe(sub_address, subscription_id)


def runSubcriber():
    initSouthBound()
    time.sleep(5)
    app.run(host="0.0.0.0", debug=True, port=EP_SERVER_PORT, use_reloader=False)


if __name__ == "__main__":
    t1 = threading.Thread(target=runClient)
    t2 = threading.Thread(target=runSubcriber)
    t1.start()
    time.sleep(5)
    t2.start()
    t1.join()
    t2.join()
