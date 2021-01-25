from databases.interfaces.icrudcommands import ICRUDCommands
from datetime import datetime


class EnviroWSCommands(ICRUDCommands):
    collection = None
    client = None

    def set_client(self, client):
        self.client = client

    def set_collection(self, collection_name):
        self.collection = collection_name

    def create_one(self, query_dict):
        entry = {}
        if "match" in query_dict:
            entry = query_dict["match"]  # extract match

            if ("date_time" in query_dict) and \
                    (query_dict["date_time"] == True):
                entry['datetime'] = self._date_time(query_dict["date_time"])

        result = self._col_connect(query_dict).insert_one(entry)
        self._db_close()
        return result

    def create_many(self, query_dict):
        result = self._col_connect(query_dict).insert_many(query_dict["match"])
        self._db_close()
        return result

    def read_one(self, query_dict):
        q, p = self._get_query_and_projection(query_dict)
        result = self._col_connect(query_dict).find_one(q, p)
        self._db_close()
        return result


    def read_many(self, query_dict) -> list:
        q, p = self._get_query_and_projection(query_dict)
        results = self._col_connect(query_dict).find(q, p)
        self._db_close()
        return [i for i in results]

    def update_one(self, query_dict):

        query = query_dict["match"]
        self._col_connect(query_dict).update_one(query)
        self._db_close()

    def update_many(self, query_dict):
        if self.collection:
            query = query_dict["match"]
            self._col_connect(query_dict).update_many(query)
            self._db_close()

    def delete_one(self, query_dict):

        query = query_dict["match"]
        self._col_connect(query_dict).delete_one(query)
        self._db_close()

    def delete_many(self, query_dict):

        query = query_dict["match"]
        self._col_connect(query_dict).delete_many(query)
        self._db_close()

    def _col_connect(self, query_dict):

        col = query_dict["collection"]
        return self._db_connect()[col]

    def _db_connect(self):
        return self.client.connect()

    def _db_close(self):
        self.client.close()

    @staticmethod
    def _date_time(date_time_str):
        return datetime.strptime(date_time_str[:19], "%Y-%m-%dT%H:%M:%S")

    @staticmethod
    def _get_query_and_projection(query_dict):

        query = {}
        projection = {}

        if not (query_dict == {}):
            if "match" in query_dict:
                query = query_dict["match"]
            if "projection" in query_dict:
                projection = query_dict["projection"]

        return query, projection

    def group_by(self, query_dict):
        if "match" in query_dict and "group" in query_dict:
            match = {'$match': query_dict["match"]}
            group = {'$group': query_dict["group"]}
            if "sort_by" in query_dict:
                sort = {'$sort': query_dict["sort_by"]}
            else:
                sort = {'$sort': {'datetime': 1}}

            results = self._col_connect(
                query_dict
            ).aggregate([match, group, sort])

            self._db_close()
            return [item for item in results]

        return None

    def batch_submit(self, query_dict):
        result = self._col_connect(query_dict).insert_many(query_dict["query"])
        self._db_close()
        return result

    def delete_all_records(self, collection):
        self._db_connect()[collection].remove({})


'''
Other CRUD strategies for other applications MongoDB database 
can be added below 
'''