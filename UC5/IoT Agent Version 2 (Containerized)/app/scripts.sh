#!/bin/bash

# Start the first process
python ./opcua_client.py &
  
# Start the second process
python ./cb_subscriber.py &
  
# Wait for any process to exit
wait -n
  
# Exit with status of process that exited first
exit $?

