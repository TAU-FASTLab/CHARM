import json
import getopt
import logging
import os

# create a logger
logger = logging.getLogger()
# log all messages, debug and up
logger.setLevel(logging.INFO)


class DataConfigurator:
    def __init__(self, json_file):
        self.json_file = json_file
        self.json_data_raw = None
        self.json_data = None
        self.create_entities_data = {}
        self.list_of_types = {}
        self.update_entities_data = {"actionType": "update", "entities": []}
        self.list_of_ids = {}
        self.url = ""
        self.attr = []
        self.server_uri = ""
        self.server_username = ""
        self.server_password = ""
        self.server_security_policy = ""
        self.server_security_mode = ""
        self.server_certificate_path = ""
        self.server_key_path = ""
        self.readConfigFile()
        self.createEntities()
        self.updateEntities()

    def readConfigFile(self):
        try:
            f = open(self.json_file)
            self.json_data_raw = json.load(f)
            f.close()
        except:
            logging.critical("Cannot open file, check file name or configuration")
            quit()
        self.json_data = self.json_data_raw["data"]
        self.url = self.json_data_raw["Config"]["url"]
        self.attr = self.json_data_raw["Config"]["subscriptions"]
        if "certificate" in self.json_data_raw:
            print("certifcate Exist")
            self.server_uri = self.json_data_raw["certificate"]["uri"]
            self.server_username = self.json_data_raw["certificate"]["username"]
            self.server_password = self.json_data_raw["certificate"]["password"]
            self.server_certificate_path = self.json_data_raw["certificate"][
                "cert_path"
            ]
            self.server_key_path = self.json_data_raw["certificate"]["key_path"]
            self.server_security_policy = self.json_data_raw["certificate"][
                "security_policy"
            ]
            self.server_security_mode = self.json_data_raw["certificate"][
                "security_mode"
            ]

    def createEntities(self):
        for key, value in self.json_data.items():
            if key != "id" and key != "type":
                # extracting entities from json files.
                self.create_entities_data[key] = value
                # getting all opc_ua node ids and saving in a list
                self.list_of_ids[key] = value["opcua_id"]
                self.list_of_types[key] = value["type"]
                # Remove opc_ua node ids from entities data
                del self.create_entities_data[key]["opcua_id"]

    def updateEntities(self):
        self.update_entities_data["entities"] = [self.json_data]
        return self.update_entities_data

    def update_value(self, list_of_values):
        for key, value in list_of_values.items():
            node = key
            self.create_entities_data[node]["value"] = value

    def updateNode(self, node, val):
        for key, value in self.list_of_ids.items():
            if str(node) == value:
                print(node)
                self.create_entities_data[key]["value"] = val


def getArguments():
    try:
        PORT = os.getenv("Port")
        CONFIG_FILE = os.getenv("Config")
        logging.warning("Reading environment variables")
        logging.warning(PORT)
        logging.warning(CONFIG_FILE)
    except:
        PORT = None
        CONFIG_FILE = None
        logging.warning('No environmentvariables found')

    return PORT, CONFIG_FILE
