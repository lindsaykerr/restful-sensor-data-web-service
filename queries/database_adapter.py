from queries.interfaces.icrudcommands import ICRUDCommands


class DatabaseWrapper(ICRUDCommands):
    username = None
    host = None
    password = None
    database = None
    db_connection = None

    def set_database(self, db_obj):
        self.database = db_obj

    def create_one(self, query):
        print(self.database.queries)
        try:
            return self.database.queries.create_one(query)
        except Exception:
            print("Data submission failed")

    def create_many(self, query_parameters):
        try:
            self.database.queries.creat_many(query_parameters)
        except Exception:
            print("Database submission failed!")
            return None

    def read_one(self, query_parameters):
        try:
            return self.database.queries.read_one(query_parameters)
        except Exception:
            print("Database read failed!")
            return []

    def read_many(self, query_parameters) -> list:
        try:
            return self.database.queries.read_many(query_parameters)
        except Exception:
            print("Database read failed!")
            return []

    def update_one(self, query_parameters):
        try:
            self.database.queries.update_one(query_parameters)
        except Exception:
            print("Database update failed!")
            return None

    def update_many(self, query_parameters):
        try:
            self.database.queries.update_many(query_parameters)
        except Exception:
            print("Database update failed!")
            return None

    def delete_one(self, query_parameters):
        try:
            self.database.queries.delete_one(query_parameters)
        except Exception:
            print("Database delete entry operation failed!")
            return None

    def delete_many(self, query_parameters):
        try:
            self.database.queries.delete_many(query_parameters)
        except Exception:
            print("Database delete entries operation failed!")
            return None

    def group_by(self, query_parameters):
        try:
            self.database.queries.group_by(query_parameters)
        except:
            print("Database group by read operation failed")

    def set_username(self, username):
        self.database.username = username

    def set_password(self, password):
        self.database.password = password

    def set_server_host(self, host):
        self.database.host = host

    def command(self, command, value):
        self.database.command(command, value)