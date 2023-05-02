import socket

class Communication:
    def __init__(self, TCP_IP, TCP_PORT):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((TCP_IP, TCP_PORT))
        self.BUFFER_SIZE = 1024

    def __disconnect__(self):
        self.sock.close()

    def send(self, list_of_commands, read_commands=[]):
        response = []
        for command in list_of_commands:
            request = (('1;1;' + command + '\r').encode())
            sent = self.sock.send(request)
            if command in read_commands:
                response.append(self.sock.recv(self.BUFFER_SIZE).decode())
            else:
                data = self.sock.recv(self.BUFFER_SIZE).decode()
            if sent == 0:
                raise RuntimeError("socket connection broken")
        return response

    def read(self):
        response = self.sock.recv(self.BUFFER_SIZE)
        if response == b'':
            raise RuntimeError("socket connection broken")

        response_list = list(response)
        return response
