import time
from flask import Flask, request
import socket
import requests
import json
from dataConfigurator import DataConfigurator, getArguments
from subscriber import DataSubsriber
import logging


# create a logger
logger = logging.getLogger()
# log all messages, debug and up
logger.setLevel(logging.INFO)

app = Flask(__name__)

EP_SERVER_ADDRESS = None
EP_SERVER_PORT = None
config_file = None
Description = "Server Notifications"
id_type = "3:Simulation"
 
sub_address = "http://orion:1026/v2/subscriptions"
server_create = "http://orion:1026/v2/entities"
server_update = "http://orion:1026/v2/op/update"
headers = {"Content-Type": "application/json"}


# get arguments from environment variables
EP_SERVER_PORT, config_file = getArguments()


# check if config file is set
if config_file == None:
    config_file = 'attributescert.json'

#create entities data object
orion_server = DataConfigurator(config_file)
print(orion_server.create_entities_data)

url = orion_server.url
sub_nodes_list = orion_server.attr
attr = orion_server.attr

entity_id = orion_server.json_data['id']
entity_type = orion_server.json_data['type']

#Create subscriber object
orion_subscriber = DataSubsriber(orion_server.list_of_ids, url)

@app.route("/", methods=["POST"])
def process_data():
    response = request.json
    print(response)
    orion_subscriber.updateOpcuaServer(response, sub_nodes_list)
    return "Success"

# initailize
def init():
    global EP_SERVER_ADDRESS, EP_SERVER_PORT
    if EP_SERVER_ADDRESS == None:
        hostname = socket.gethostname()
        EP_SERVER_ADDRESS = socket.gethostbyname(hostname)

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
# check for subscriptions
# def check_subscriptions(sub_address):
#     r = requests.get(sub_address)
#     subscriptions = json.loads(r.content)
#     for subscription in subscriptions:
#         id = subscription['id']
#         if(subscription['subject']['entities'][0]['idPattern'] == entity_id):
#               logging.info(id)
#               response = requests.delete(sub_address +'/' + id)
#               logging.info("Server returned code " + str(response.status_code) + " when deleting subscription")
#
#
# #creates subscription on Orion
# def create_subscription(EP_SERVER_ADDRESS, EP_SERVER_PORT, Description="Server Notifications",\
#                         attr=[], entity_id="Simulation", entity_type="3:Simulation"):
#     sub_data = {
#                   "description": Description,
#                   "subject": {
#                     #"entities": [{"idPattern": ".*", "type": entity_type}],
#                     "entities": [{"idPattern": entity_id, "type": entity_type}],
#                     "condition": {
#                       #"attrs": [ "temperature" ]
#                       "attrs": attr
#                     }
#                   },
#                   "notification": {
#                     "http": {
#                       "url": "http://"+ EP_SERVER_ADDRESS + ':' + str(EP_SERVER_PORT)
#                     }
#                   }
#                 }
#     logging.info(json.dumps(sub_data))
#     try:
#         r = requests.post(sub_address, data=json.dumps(sub_data), headers=headers)
#         logging.info("successfully created subscription on Orion contex broker")
#     except:
#         logging.error("Orion Context broker server not running")
#         quit()
#
# def unsubscribe(sub_address, id):
#     response = requests.delete(sub_address +'/' + id)

if __name__ == '__main__':
    init()
    time.sleep(5)
    app.run(host='0.0.0.0', debug=True, port=EP_SERVER_PORT, use_reloader=False)