from abc import abstractmethod


class ICRUDCommands:

    @abstractmethod
    def create_one(self, query_parameters):
        pass

    @abstractmethod
    def create_many(self, query_parameters):
        pass

    @abstractmethod
    def read_one(self, query_parameters):
        pass

    @abstractmethod
    def read_many(self, query_parameters) -> list:
        pass

    @abstractmethod
    def update_one(self, query_parameters):
        pass

    @abstractmethod
    def update_many(self, query_parameters):
        pass

    @abstractmethod
    def delete_one(self, query_parameters):
        pass

    @abstractmethod
    def delete_many(self, query_parameters):
        pass

    @abstractmethod
    def group_by(self, query_parameters):
        pass