from opcua import Server
from time import sleep
import random

# create server object 
server = Server()

# create endpoint
url = "opc.tcp://0.0.0.0:4840/opcua/server"
server.set_endpoint(url)

#create server namespace
name = "OPCUA_SERVER"
idx = server.register_namespace(name)

# get server objects node
objects = server.get_objects_node()

# add objects {namespace, object name}
param = objects.add_object(idx, "Parameters")

# add and initialise a variable to a specific object
temp = param.add_variable(idx, "Temperature", 0)

# set read write privileges for a variable
temp.set_writable()

# start server
server.start()

print()
print(f"Server started at {url}")
print()

while True:
    # generate random temperature values
    Temperature = random.uniform(22, 25)

    # update the temp variable
    temp.set_value(Temperature)
    print(f"New Temperature:  {temp.get_value():.2f}")
    print()
    sleep(2)