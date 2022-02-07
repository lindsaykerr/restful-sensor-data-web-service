class DBSchema:
    """ 
    The schema provides name lookups for storage location (ie tables or collections) on a database.

    If the name of a data location changes on the database then the property values can be modified 
    to reflect such changes
    """
    device_locations = "locations"
    device_id = "device_id"
    data_storage = "DATA"
    clients = "CLIENTS"
    app_tokens = "TOKEN_KEYS"


class QueryObj:
    def __init__(self, search_in ="", search_for="") -> None:
        self._search_for = search_for
        self._search_in = search_in
    
    @property
    def search_for(self):
        return self._search_for

    @property
    def search_in(self):
        return self._search_in




class Interface_DbEntity:
    def __init__(self,username: str, password: str, host:str, database_name:str, schema:DBSchema) -> None:

        self.username = username
        self.password = password
        self.host = host
        self.database = database_name
        self.db_client = None
        self.db = None
        self.schema = schema
    
    def query(self, query:QueryObj):
        pass

    def set_client(self, client):
        self.db_client = client

    def open_db_connection(self):
        pass

    def close_db_connection(self):
        pass

    def create(self, location, data, **kwargs):
        pass
    
    def read(self, location, query, **kwargs):
        pass
    
    def update(self, location, items, data, **kwargs):
        pass

    def delete(self, location, items, **kwargs):
        pass

   