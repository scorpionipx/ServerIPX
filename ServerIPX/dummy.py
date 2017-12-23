import socket

# create a socket object
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 

# get local machine name
host = "192.168.100.15"

data = "Hello, server!"
data = data.encode('utf-8')

port = 9999

# connection to hostname on the port.
s.connect((host, port))                               

# Receive no more than 1024 bytes
tm = s.recv(1024)

s.send(data)

s.close()

print("The time got from the server is %s" % tm.decode('ascii'))
