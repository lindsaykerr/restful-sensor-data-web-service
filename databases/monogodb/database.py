import pymongo
from databases.interfaces.idatabase import IDatabase
from databases.monogodb.crudcommands import EnviroWSCommands

# following line allows the default CRUD strategy to be swapped if needed
db_crud_strategy = EnviroWSCommands


class Database(IDatabase):
    client = None

    def __init__(self, username, password,
                 host, database_name, crud_strategy=None):
        self.username = username
        self.password = password
        self.host = host
        self.database = database_name

        if crud_strategy:
            global db_crud_strategy
            db_crud_strategy = crud_strategy

        self.queries = db_crud_strategy()
        self.queries.set_client(self)

    def connect(self):
        try:
            self.client = pymongo.MongoClient(
                host=self.host,
                username=self.username,
                password=self.password,
                connect=False,
                authSource=self.database,
                # authMechanism='SCRAM-SHA-256'
            )
            return self.client.get_database(self.database)
        except ConnectionError:
            raise ConnectionError("Database connection failure")

    def close(self):
        self.client.close()
        self.client = None

    def command(self, command, value):
        # changes the current collection of a MongoDB database
        if 'change_collection' == command:
            self.queries.set_collection(value)

        # batch submit multiple records into collection
        elif 'batch_submit' == command:
            self.queries.batch_submit(value)

        # delete all records from a given collection
        elif 'delete_all_records' == command:
            self.queries.delete_all_records(value)
