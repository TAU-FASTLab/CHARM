from dataConfigurator import DataConfigurator, getArguments
from opcua import Client
import time
import requests
import json
import sys
import logging
from opcuaClient import OpcuaClient
import os
from sys import stdout

config_file = None
# create a logger
logger = logging.getLogger()
# log all messages, debug and up
logger.setLevel(logging.INFO)

cb_server_subscribe = "http://orion:1026/v2/subscriptions"
cb_server_create = "http://orion:1026/v2/entities"
cb_server_update = "http://orion:1026/v2/op/update"
headers = {"Content-Type": "application/json"}

# get commandline arguments
EP_SERVER_PORT, config_file = getArguments()

# check if config file is set
if config_file is None:
    config_file = "attributescert.json"

#create entities opcua client data object
opcua_data = DataConfigurator(config_file)
print(opcua_data.create_entities_data)
print(opcua_data.update_entities_data)

# set entity ID and type
entity_id = opcua_data.json_data["id"]
entity_type = opcua_data.json_data["type"]

url = opcua_data.url
sub_nodes_list = opcua_data.attr
attr = opcua_data.attr
client = OpcuaClient(opcua_data)
try:
    client.client.connect()
    logging.info("opcua Client Connected for northbound traffic")
except Exception as err:
    logging.error("Error while creating the opcua client connection for northbound traffic")
    logging.error(err)
    sys.exit(1)

def getEntities(server_address):
    try:
        r = requests.get(server_address)
    except Exception as err:
        logging.info("Problem connecting to context broker ",err)
        quit()
    logging.info(r.status_code)
    logging.info(r.headers)
    logging.info(r.content)
    return r.status_code


def northBoundCreate():
    try:
        r = requests.post(cb_server_create, data=json.dumps(opcua_data.json_data), headers=headers)
        logging.info("Context broker returned code " + str(r.status_code) + " while creating entity")
    except:
        logging.error("Problem connecting to context broker while creating entity")


class EventHandler(object):
    def datachange_notification(self, node, val, data):
        # Getting names and Values using opcua_ids
        print("---------------------------------------------")
        print(val)
        print(node)
        print(type(node))
        print(data)
        print("------------------------------------------------")

        opcua_data.updateNode(node, val)
        opcua_data.updateEntities()
        r = requests.post(
            cb_server_update,
            data=json.dumps(opcua_data.update_entities_data),
            headers=headers,
        )
        t = time.localtime()
        current_time = time.strftime("%H:%M:%S", t)
        print(r.status_code, "Entities Updated", current_time)


def northBoundUpdate():
    nodes = []
    for key, value in opcua_data.list_of_ids.items():
        opcua_id = value
        node = client.client.get_node(opcua_id)
        nodes.append(node)
    test_values = client.client.get_values(nodes)
    print(test_values)
    handler = EventHandler()
    sub = client.client.create_subscription(5000, handler)
    handle = sub.subscribe_data_change(nodes)

def initNorthBound():
    code = getEntities((cb_server_create + "/" + entity_id))
    print("-------------------- code -------------------", code)
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
    

if __name__ == "__main__":
    initNorthBound()
    northBoundUpdate()






