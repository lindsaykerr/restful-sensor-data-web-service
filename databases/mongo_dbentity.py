from pymongo import MongoClient

from  interface_dbentity import Interface_DbEntity
from interface_dbentity import DBSchema, QueryObj



class Mongo_DbEntity(Interface_DbEntity):
    def __init__(self, username: str, password: str, host: str, database_name: str, schema: DBSchema) -> None:
        super().__init__(username, password, host, database_name, schema)
        self.collection = None

    def query(self, query: QueryObj):
        pass

    def _set_collection(self, collection: str):
        self.collection = collection
    

    def open_db_connection(self):
        try:
            self.db_client = MongoClient(
                host=self.host,
                username=self.username,
                password=self.password,
                connect=False,
                authSource=self.database,
                # authMechanism='SCRAM-SHA-256'
            )
            self.db = self.db_client.get_database(self.database)
        except ConnectionError:
            raise ConnectionError("Database connection failure")

    def close_db_connection(self):
        self.db_client.close()
        self.db_client = None


    def create(self, location, data, batch_operation=False):
        self._parameter_validation(location)      
        if batch_operation:
            return self.db[location].insert_many(data)
        else:
            return self.db[location].insert_one(data)
            
    
    def read(self, location, query, batch_operation=False, filter=None):
        self._parameter_validation(location)
        if batch_operation:
            return self.db[location].find(query, filter)
        else:
            return self.db[location].find_one(query, filter)

    def update(self, location, filter, data, batch_operation=False):
        self._parameter_validation(location)
        if batch_operation:
            return self.db[location].update_many(filter, data)
        else:
            return self.db[location].update_one(filter, data)

    def delete(self, location, filter, batch_operation=False):
        self.close_db_connection(location)
        if batch_operation:
            return self.db[location].delete_one(filter)
        else:
            return self.db[location].delete_many(filter)

    def _parameter_validation(self, location):
        assert(self.db != None)
        assert(location in self.collection)
        

