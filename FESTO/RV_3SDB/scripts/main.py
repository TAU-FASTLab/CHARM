import socket
import struct


TCP_IP = '153.1.165.72'
TCP_PORT = 10001
BUFFER_SIZE = 1024
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((TCP_IP, TCP_PORT))

# request = struct.pack('12B', 0x00, 0x00, 0x00, 0x00, 0x00, 0x06, int(unitId), functionCode, 0x00,
#                      dataAddress,
#                      on_off,
#                      0x00)
command1 = 'OPEN=NARCUSR'
command2 = 'CNTLON'
command3 = 'SRVON'

command4 = 'CNTLON'
command5 = 'SRVOFF'
command6 = 'STATE'
command7 = 'CNTLOFF'

# request = (('1;1;' + command1 + '\r').encode())
# sock.send(request)
# data_response = sock.recv(BUFFER_SIZE)
# print(data_response)
#
# request = (('1;1;' + command2 + '\r').encode())
# sock.send(request)
# data_response = sock.recv(BUFFER_SIZE)
# print(data_response)
#
# request = (('1;1;' + command3 + '\r').encode())
# sock.send(request)
# data_response = sock.recv(BUFFER_SIZE)
# print(data_response)

request = (('1;1;' + command4 + '\r').encode())
sock.send(request)
data_response = sock.recv(BUFFER_SIZE)
print(data_response)

request = (('1;1;' + command5 + '\r').encode())
sock.send(request)
data_response = sock.recv(BUFFER_SIZE)
print(data_response)

request = (('1;1;' + command6 + '\r').encode())
sock.send(request)
data_response = sock.recv(BUFFER_SIZE)
print(data_response)

request = (('1;1;' + command7 + '\r').encode())
sock.send(request)
data_response = sock.recv(BUFFER_SIZE)
print(data_response)

# send request
# sock.send(request)

# receive response
# data_response = sock.recv(BUFFER_SIZE)

# close socket
sock.close()

# print response
#print(data_response)
