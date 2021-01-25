from abc import abstractmethod


class ICRUDCommands:
    """
    This interface provides the standard set of database CRUD commands used
    by the web service.

    This interface should rarely change regardless of what the web service is
    being used for.
    """
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