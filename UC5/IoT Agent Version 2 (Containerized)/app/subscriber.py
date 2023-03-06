import logging
import sys
from opcua import Client, ua
import requests
import json
from opcuaClient import OpcuaClient
from opcua_client import opcua_data
from dataConfigurator import DataConfigurator

# create a logger testing 123
logger = logging.getLogger()
# log all messages, debug and up
logger.setLevel(logging.INFO)

print(opcua_data.server_uri)
#client = OpcuaClient(opcua_data)


class DataSubsriber():
    def __init__(self, list_of_ids, client):
        self.list_of_ids = list_of_ids
        self.client = OpcuaClient(opcua_data)
        try:
            self.client.client.connect()
            logging.info("opcua Client Connected for southbound traffic")
        except Exception as err:
            logging.error("Error while creating the opcua client connection for southbound traffic ")
            logging.error(err)
            sys.exit(1)

    def updateOpcuaNode(self, value, id, type):
        try:
            node = self.client.client.get_node(id)
        except:
            print("id does not exist", ValueError)

        try:
            if type == "String":
                node.set_value(
                    ua.DataValue(ua.Variant(str(value), ua.VariantType.String))
                )
            elif type == "Number":
                node.set_value(
                    ua.DataValue(ua.Variant(float(value), ua.VariantType.Double))
                )
            elif type == "Boolean":
                node.set_value(
                    ua.DataValue(ua.Variant(bool(value), ua.VariantType.Boolean))
                )
            elif type == "Double":
                node.set_value(
                    ua.DataValue(ua.Variant(bool(value), ua.VariantType.Double))
                )
            elif type == "Float":
                node.set_value(
                    ua.DataValue(ua.Variant(bool(value), ua.VariantType.Float))
                )
            elif type == "Int64":
                node.set_value(
                    ua.DataValue(ua.Variant(bool(value), ua.VariantType.Int64))
                )
            elif type == "Byte":
                node.set_value(
                    ua.DataValue(ua.Variant(bool(value), ua.VariantType.Byte))
                )
        except:
            print("Data Type is not correct, check json file")

    def updateOpcuaServer(self, json_sub_data, sub_nodes_lists):
        json_nodes = json_sub_data["data"][0]

        for node_name in sub_nodes_lists:
            id = self.list_of_ids[node_name]
            node_value = json_nodes[node_name]["value"]
            node_type = json_nodes[node_name]["type"]
            self.updateOpcuaNode(node_value, id, node_type)

    # check for subscriptions
    def check_subscriptions(self, sub_address, entity_id):
        r = requests.get(sub_address)
        subscriptions = json.loads(r.content)
        for subscription in subscriptions:
            id = subscription["id"]
            if subscription["subject"]["entities"][0]["idPattern"] == entity_id:
                logging.info(id)
                response = requests.delete(sub_address + "/" + id)
                logging.info(
                    "Server returned code "
                    + str(response.status_code)
                    + " when deleting subscription"
                )

    def getSubscriptionID(self, sub_address):
        r = requests.get(sub_address)
        content = json.loads(r.content)
        # subscriptionid = content
        print(content[0]["id"])
        return content[0]["id"]

    # creates subscription on Orion
    def create_subscription(
        self,
        EP_SERVER_ADDRESS,
        EP_SERVER_PORT,
        sub_address,
        Description="Server Notifications",
        attr=[],
        entity_id="Simulation",
        entity_type="3:Simulation",
    ):
        sub_data = {
            "description": Description,
            "subject": {
                # "entities": [{"idPattern": ".*", "type": entity_type}],
                "entities": [{"idPattern": entity_id, "type": entity_type}],
                "condition": {
                    # "attrs": [ "temperature" ]
                    "attrs": attr
                },
            },
            "notification": {
                "http": {
                    "url": "http://"
                    + str(EP_SERVER_ADDRESS)
                    + ":"
                    + str(EP_SERVER_PORT)
                }
            },
        }
        logging.info(json.dumps(sub_data))
        headers = {"Content-Type": "application/json"}
        try:
            r = requests.post(sub_address, data=json.dumps(sub_data), headers=headers)
            logging.info(str(sub_address))
            logging.info(str(sub_data))
            logging.info("successfully created subscription on Orion context broker")
        except:
            logging.error("Orion Context broker server not running")
            quit()

    def unsubscribe(self, sub_address, sub_id):
        response = requests.delete(str(sub_address) + "/" + str(sub_id))