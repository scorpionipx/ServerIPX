import socket

def send():
    UDP_IP = "127.0.0.1"
    UDP_PORT = 5005
    MESSAGE = bytes("Hello, World!", 'utf-8')

    ipx_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # ipx_socket.bind((IPX_IP_ADDRESS, IPX_PORT))

    ipx_socket.sendto(MESSAGE, (UDP_IP, UDP_PORT))
    ipx_socket.shutdown()
    ipx_socket.close()



def receive():

    UDP_IP = "127.0.0.1"
    UDP_PORT = 5005

    sock = socket.socket(socket.AF_INET,  # Internet
                         socket.SOCK_DGRAM)  # UDP
    sock.bind((UDP_IP, UDP_PORT))

    while True:
        data, addr = sock.recvfrom(1024)  # buffer size is 1024 bytes
        print ("received message:", data)


def server():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(("localhost", 8081))
    sock.listen(2)
    conn, addr = sock.accept()
    data = conn.recv(1024).decode("ascii")

server()
