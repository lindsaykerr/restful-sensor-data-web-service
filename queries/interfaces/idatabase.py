from abc import abstractmethod


class IDatabase:
    @abstractmethod
    def connect(self):
        pass

    @abstractmethod
    def close(self):
        pass

    @abstractmethod
    def command(self, command, value):
        pass
