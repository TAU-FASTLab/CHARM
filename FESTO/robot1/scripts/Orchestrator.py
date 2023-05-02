import time
import requests
import json
#from dataConfigurator import DataConfigurator
import RV_3SDB
import time


TCP_IP = '10.1.1.110'
TCP_PORT = 10002
robot = RV_3SDB.RobotArm(TCP_IP, TCP_PORT)

# config_file = 'attributes.json'
# orion_data= DataConfigurator(config_file)



server_create = "http://localhost:1026/v2/entities"
server_update = "http://localhost:1026/v2/op/update"
headers = {"Content-Type": "application/json"}

def getEntities(server_address):
    r = requests.get(server_address)
    print(r.status_code)  # Press Ctrl+F8 to toggle the breakpoint.
    # print(r.headers)
    # print(r.content)
    # my_json = json.loads(r.content)
    # print(my_json)

    return r.content


def northBoundUpdate(data,node_name,plc_num,updated_value):
    # data2= orion_data.update_entities_data
    #
    # print(data2)
    #id= orion_data.json_data[]
    #print(id)
    update_entities = {"actionType": "update", "entities": []}
    update_entities ["entities"]= data
    #print(update_entities)
    #print("-_____",update_entities['entities'])
    value = update_entities['entities'][plc_num][node_name]['value']
    #print(value)

    #update_entities['entities'][plc_num][node_name]['value']= updated_value
    #print(data)



    r = requests.post(server_update, data=json.dumps(update_entities), headers=headers)
    print(r.status_code)

if __name__== "__main__":
    while True:

        content= getEntities(server_create)
        #print(content[0], ")))))000")
        #print(content)
        content_dict= json.loads(content)
        print("_________________________")
        print(content_dict)
        #Servo_OPCUA= content_dict[2]['3:test3']['value']
        Servo_OPCUA= content_dict[2]['3:start']['value']
        Servo_OPCUA= content_dict[0]['j1']['value']
        #stop_button = content_dict[1]['3:stop']['value']
        print(Servo_OPCUA)
        #print(stop_button)
        if Servo_OPCUA == True:
            robot.servoOn()
        elif Servo_OPCUA == False:
            robot.servoOff()
        # AUTOMA= True
        # plc_name = content_dict[0]['3:test3']
        # print(plc_name)

        #northBoundUpdate(content_dict,"3:test3", 0, False)


        time.sleep(2)