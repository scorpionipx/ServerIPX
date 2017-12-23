from __future__ import absolute_import
import socket as py_socket
from time import gmtime, strftime

import os
import sys
import inspect
current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

import utils


ALLOWED_NUMBER_OF_CONNECTIONS = 1
COMMAND_HEADER = 0
DATA_HEADER = 1

TEST_PRINT = True


def get_current_time():
    """
        Method gets current time as string.
    :return: current_time
    """
    current_time = strftime("%Y-%m-%d %H:%M:%S", gmtime())
    return current_time


def test_print(string_to_print, print_time=True):
    """
        Method prints the string_to_print content if TEST_PRINT is enabled.
    :param string_to_print: string to be printed
    :param print_time: boolean indicating if time print is desired
    :return: None
    """
    if TEST_PRINT:
        if print_time:
            string_to_print = str(get_current_time()) + ' -> ' + str(string_to_print)
        print(str(string_to_print))
    return


class ServerIPX:
    """
        Class used to handle IPX Server.
    """
    def __init__(self, port, number_of_connections=ALLOWED_NUMBER_OF_CONNECTIONS):
        """
            Constructor
        """

        test_print("Initiating ServerIPX...", True)

        try:
            # get local machine name
            self.host = py_socket.gethostname()
            test_print("HOST: " + str(self.host))

            self.port = port
            test_print("PORT: " + str(self.port))

            # create a socket object
            self.socket = py_socket.socket(py_socket.AF_INET, py_socket.SOCK_STREAM)
            test_print("Created server socket")

            # bind to the port
            self.socket.bind((self.host, self.port))
            test_print("Bind with host complete ")

            self.socket.listen(number_of_connections)
            test_print("Opened " + str(number_of_connections) + ' connection(s)')

            self.commands = utils.ServerCommands()

            self.client = None

            self.default_encoding = 'utf-8'

            test_print("ServerIPX is up and running!", True)
        except Exception as err:
            print("Error initiating ServerIPX: " + str(err))

    def get_host(self):
        return self.host

    def get_port(self):
        return self.port

    def string_to_bytes(self, _string, encoding=None):
        if encoding is None:
            encoding = self.default_encoding
        return bytes(_string, encoding)

    def send_command_to_client(self, command, extra=None):
        """
            Method sends a command to the connected client.
        :param command: command to be sent as integer.
        :param extra: additional information about the command, if needed.
        :return: boolean True if ok, error occurred as string if not ok.
        """
        if self.client is not None:
            try:
                command = str(COMMAND_HEADER) + '\n' + str(command) + '\n' + str(extra)
                command = self.string_to_bytes(command)
                self.client.send(command)
            except Exception as err:
                print("Error occurred while sending command to client:\ncommand: " + str(command) + '\n' + str(err))

    def ask_client_for_credentials(self):
        """
            Method asks the client requesting the connection for credentials.
        :return: True if credentials are ok, False otherwise.
        """
        command = self.commands.ask_for_credentials
        self.send_command_to_client(command)

    def connect_with_client(self):

        # establish a connection
        self.client, client_address = self.socket.accept()

        current_time = get_current_time()
        test_print("Got a connection request from " + str(client_address[0]), True)

        test_print("Asking client for credentials...")
        self.client.send(current_time.encode('ascii'))

        data = self.client.recv(1024)
        test_print("Data: " + str(data))

        self.client.shutdown(py_socket.SHUT_RDWR)
        self.client.close()


server = ServerIPX(9999, 1)
server.connect_with_client()

