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
from utils import CLIENT_USERNAME, CLIENT_PASSWORD


BUFFER_SIZE = 64
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
            # self.socket.settimeout(utils.TIMEOUT)
            test_print("Created server socket")

            # bind to the port
            self.socket.bind((self.host, self.port))
            test_print("Bind with host complete ")

            self.socket.listen(number_of_connections)
            test_print("Opened " + str(number_of_connections) + ' connection(s)')

            self.commands = utils.ServerCommands()
            self.client_commands = utils.ClientCommands()

            self.client = None
            self.client_name = None

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
        :param command: command to be sent as ServerCommand attribute from utils.
        :param extra: additional information about the command, if needed.
        :return: boolean True if ok, error occurred as string if not ok.
        """
        if self.client is not None:
            try:
                command = str(COMMAND_HEADER) + '\n' + str(command) + '\n' + str(extra)
                command = self.string_to_bytes(command)
                self.client.send(command)
                return True
            except Exception as err:
                error = "Error occurred while sending command to client:\ncommand: " + str(command) + '\n' + str(err)
                print(error)
                return error
        else:
            return None

    def decode_client_response(self, client_response):
        """
            Method decodes client's response.
        :param client_response: bytes received from client
        :return:
        """
        response = {"Type": None, "ID": None, "Content": None, "Valid": True, "Error": None}

        client_response = client_response.decode(self.default_encoding)
        client_response = client_response.split()
        response["Type"] = client_response[0]
        response["ID"] = client_response[1]

        # extract content - needed if content contains new line character
        content = ''
        for index, item in enumerate(client_response):
            if index > 1:
                content += '\n'
                content += str(item)

        response["Content"] = content

        # validate content
        if response["Valid"]:
            if (response["Type"]) == str(COMMAND_HEADER) or str(response["Type"]) == str(DATA_HEADER):
                response["Valid"] = True
            else:
                response["Valid"] = False
                if response["Error"] is None:
                    response["Error"] = "Invalid header ID!"
                else:
                    response["Error"] += '\n'
                    response["Error"] += "Invalid header ID!"

        if response["Valid"]:
            id_is_valid = False
            for command in self.client_commands.all_commands:
                if str(command) == str(response["ID"]):
                    id_is_valid = True
                    break

            if id_is_valid:
                response["Valid"] = True
            else:
                response["Valid"] = False
                if response["Error"] is None:
                    response["Error"] = "Invalid data/command ID!"
                else:
                    response["Error"] += '\n'
                    response["Error"] += "Invalid data/command ID!"

        # test_print("\nType: " + str(response["Type"]) + "\nID: " + str(response["ID"]) + "\nContent:" +
        #            str(response["Content"]) + "\nValid: " + str(response["Valid"]) + "\nErrors: " +
        #            str(response["Error"]))

        return response

    def ask_client_for_credentials(self):
        """
            Method asks the client requesting the connection for credentials.
        :return: None
        """
        command = self.commands.ask_for_credentials
        self.send_command_to_client(command)

    def verify_credentials(self, credentials):
        """
            Method checks if the credentials received from client are valid.
        :return: True if valid, false otherwise
        """
        credentials = self.decode_client_response(credentials)
        username = str(credentials["Content"].split()[0])[2:]
        password = str(credentials["Content"].split()[1])[2:]
        # test_print("client's username: " + str(username))
        # test_print("client's password: " + str(password))

        if username == utils.CLIENT_USERNAME and password == utils.CLIENT_PASSWORD:
            return True
        else:
            return False

    def connect_with_client(self):

        client_is_valid = False

        while not client_is_valid:

            # establish a connection
            test_print("Waiting for a connection request!")
            self.client, client_address = self.socket.accept()

            test_print("Got a connection request from " + str(client_address[0]), True)

            test_print("Asking client for credentials...")
            self.ask_client_for_credentials()

            client_response = self.client.recv(BUFFER_SIZE)
            test_print("Credentials received! verifying...", True)

            client_is_valid = self.verify_credentials(client_response)
            if client_is_valid:
                self.client_name = utils.CLIENT_USERNAME
                test_print("Valid credentials. Client " + str(self.client_name) + " connected!")
            else:
                test_print("Unknown client connection request! Connection refused!")
                self.client.shutdown(py_socket.SHUT_RDWR)
                self.client.close()
                self.client = None

    def run_forever(self):
        """
            Server communicates with client until closed.
        :return: None
        """
        while True:
            client_response = self.client.recv(BUFFER_SIZE)
            if client_response:
                test_print("Message received: " + str(client_response))
                self.decode_client_response(client_response)


server = ServerIPX(utils.PORT, ALLOWED_NUMBER_OF_CONNECTIONS)
server.connect_with_client()
server.run_forever()

