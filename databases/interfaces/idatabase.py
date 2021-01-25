from abc import abstractmethod


class IDatabase:
    @abstractmethod
    def connect(self):
        """
        Opens a connection to a database
        :return:
        """
        pass

    @abstractmethod
    def close(self):
        """
        Closes the connection to a database
        :return:
        """
        pass

    @abstractmethod
    def command(self, command, value):
        """
        The command method is used to pass commands or common database operation
        which are database specific and are not part of the ICRUDCommands
        interface.
        :param command: a custom string command
        :param value: a string command value
        :return:
        """
        pass
