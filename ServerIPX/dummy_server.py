import socket
import time

ALLOWED_NUMBER_OF_CONNECTIONS = 1

# create a socket object
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# get local machine name
host = socket.gethostname()

port = 9999

# bind to the port
server_socket.bind((host, port))

# queue up to 5 requests
server_socket.listen(ALLOWED_NUMBER_OF_CONNECTIONS)

print("Starting server...")
print("Host:", format(host))
print("Port:", format(port))

while True:
    # establish a connection
    client_socket, addr = server_socket.accept()

    print("Got a connection from %s" % str(addr))
    currentTime = time.ctime(time.time()) + "\r\n"
    client_socket.send(currentTime.encode('ascii'))
    client_socket.close()

