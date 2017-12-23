ASK_FOR_CREDENTIALS_SRV_COMMAND = '1'
ASK_FOR_CREDENTIALS_INFO = 'Ask client for credentials'

ALL_SERVER_COMMANDS = [
    ASK_FOR_CREDENTIALS_SRV_COMMAND,

]

ALL_COMMANDS = sorted(ALL_SERVER_COMMANDS)


class ServerCommands:
    """
        Class used to store available commands for the ServerIPX.
    """
    def __init__(self):
        """
            Constructor
        """

        self.ask_for_credentials = ASK_FOR_CREDENTIALS_SRV_COMMAND
        self.ask_for_credentials_details = ASK_FOR_CREDENTIALS_INFO

        self.all_commands = ALL_COMMANDS




