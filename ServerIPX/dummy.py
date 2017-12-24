from __future__ import absolute_import
import socket as py_socket
from time import gmtime, strftime, sleep

import os
import sys
import inspect
current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

import utils
from utils import CLIENT_USERNAME, CLIENT_PASSWORD, HOST, PORT


BUFFER_SIZE = 64
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


class ClientIPX:
    """
        Class used to handle IPX Server.
    """
    def __init__(self, host, port, username, password):
        """
            Constructor
        """

        test_print("Initiating ClientIPX...", True)

        try:
            # create a socket object
            self.socket = py_socket.socket(py_socket.AF_INET, py_socket.SOCK_STREAM)
            # self.socket.settimeout(utils.TIMEOUT)

            self.host = host
            self.port = port

            self.username = username
            self.password = password

            self.commands = utils.ClientCommands()
            self.server_commands = utils.ServerCommands()

            self.default_encoding = 'utf-8'

            test_print("ClientIPX is up and running!", True)
        except Exception as err:
            print("Error initiating ServerIPX: " + str(err))

    def string_to_bytes(self, _string, encoding=None):
        if encoding is None:
            encoding = self.default_encoding
        return bytes(_string, encoding)

    def decode_server_response(self, server_response):
        """
            Method decodes client's response.
        :param server_response: bytes received from client
        :return:
        """
        response = {"Type": None, "ID": None, "Content": None, "Valid": True, "Error": None}

        server_response = server_response.decode(self.default_encoding)
        server_response = server_response.split()
        response["Type"] = server_response[0]
        response["ID"] = server_response[1]

        # extract content - needed if content contains new line character
        content = ''
        for index, item in enumerate(server_response):
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
            for command in self.server_commands.all_commands:
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

    def send_command_to_host(self, command, extra=None):
        """
            Method sends a command to the host.
        :param command: command to be sent as ClientCommand attribute from utils.
        :param extra: additional information about the command, if needed.
        :return: boolean True if ok, error occurred as string if not ok.
        """
        try:
            command = str(COMMAND_HEADER) + '\n' + str(command) + '\n' + str(extra)
            command = self.string_to_bytes(command)
            self.socket.send(command)
            return True
        except Exception as err:
            error = "Error occurred while sending command to client:\ncommand: " + str(command) + '\n' + str(err)
            print(error)
            return error

    def send_data_to_host(self, data_id, data):
        """
            Method sends a data to the host.
        :param data_id: specifies the data type that is sent to server.
        :param data: actual data
        :return: boolean True if ok, error occurred as string if not ok.
        """
        try:
            data = str(DATA_HEADER) + '\n' + str(data_id) + '\n' + str(data)
            data = self.string_to_bytes(data)
            self.socket.send(data)
            return True
        except Exception as err:
            error = "Error occurred while sending data to client:\ndata_id: " + str(data_id) + '\ndata: ' + str(data)\
                    + '\n' + str(err)
            print(error)
            return error

    def send_credentials(self):
        """
            Method sends credentials required to connect to the server.
        :return: None
        """
        test_print("Sending credentials...")
        data = 'u:' + str(self.username) + '\np:' + str(self.password)
        self.send_data_to_host(1, data)

    def connect_to_server(self):
        """
            Method establishes connection to the server.
        :return: True if connection established, False otherwise
        """
        test_print("Connecting to host " + str(HOST) + '...')
        self.socket.connect((self.host, self.port))

        server_response = self.socket.recv(BUFFER_SIZE)

        test_print("Server's response: " + str(server_response))

        self.send_credentials()


client = ClientIPX(HOST, PORT, CLIENT_USERNAME, CLIENT_PASSWORD)
client.connect_to_server()
sleep(3)
command = client.commands.get_host_time
client.send_command_to_host(command)
sleep(2)
client.send_credentials()
client.socket.close()



