HOST = "192.168.100.15"
PORT = 9999
TIMEOUT = 1

ASK_FOR_CREDENTIALS_SRV_COMMAND = '1'
ASK_FOR_CREDENTIALS_INFO = 'Ask client for credentials'

ALL_SERVER_COMMANDS = [
    ASK_FOR_CREDENTIALS_SRV_COMMAND,

]

ALL_SERVER_COMMANDS = sorted(ALL_SERVER_COMMANDS)


class ServerCommands:
    """
        Class used to store available commands for the ServerIPX.
    """
    def __init__(self):
        """
            Constructor
        """

        self.ask_for_credentials = ASK_FOR_CREDENTIALS_SRV_COMMAND
        self.ask_for_credentials_info = ASK_FOR_CREDENTIALS_INFO

        self.all_commands = ALL_SERVER_COMMANDS


CLIENT_USERNAME = 'RaspberryPIScorpionIPX'
CLIENT_PASSWORD = 'Qwerty123'

GET_HOST_TIME_CLT_COMMAND = '1'
GET_HOST_TIME_INFO = 'Ask server for current time (as seen by server)'

ALL_CLIENT_COMMANDS = [
    GET_HOST_TIME_CLT_COMMAND,

]
ALL_CLIENT_COMMANDS = sorted(ALL_CLIENT_COMMANDS)


class ClientCommands:
    """
        Class used to store available commands for ClientIPX
    """
    def __init__(self):
        """
            Constructor
        """

        self.get_host_time = GET_HOST_TIME_CLT_COMMAND
        self.get_host_time_info = GET_HOST_TIME_INFO

        self.all_commands = ALL_CLIENT_COMMANDS
