from utilities.settings import db_rec_user, db_server, db_sub_user
from queries.database_adapter import DatabaseWrapper
from queries.monogodb.database import Database
from queries.monogodb.wsqueries import EnviroWSQueries
from datetime import datetime


db = DatabaseWrapper()
db.set_database(Database(
    username="pythontester",
    password="password1234",
    database_name="querytesting",
    host=db_server["host"],
))

query = EnviroWSQueries()
db.command("remove_collection", "devices")
db.command("remove_collection", "data")

data_list = [
    {
        "device_id": "001",
        "location": "place_A",
        "geolocation": [1, 2],
        "measures": ["A", "B", "C"],
        "device_data": 'accessible'
    },
    {
        "device_id": "002",
        "location": "place_B",
        "geolocation": [4, 2],
        "measures": ["A", "B", "C", "D"],
        "device_data": 'accessible'
    },
    {
        "device_id": "003",
        "location": "place_C",
        "geolocation": [33, 2],
        "measures": ["A", "B", "C", "E", "F"],
        "device_data": 'accessible'
    },
    {
        "device_id": "004",
        "location": "place_D",
        "geolocation": [44, 2],
        "measures": ["B", "C", "messages"],
        "device_data": 'hidden'
    },
    {
        "device_id": "005",
        "location": "place_E",
        "geolocation": [33, 5],
        "measures": ["B", "C", "E"],
        "device_data": 'accessible'
    },
    {
        "device_id": "006",
        "location": "place_F",
        "geolocation": [52, 2],
        "measures": ["B", "C", "E", "F"],
        "device_data": 'hidden'
    }
]

db.command("batch_submit", query.device_batch_submit(data_list))

data_list = [
    {
        "device_id": "template",
        "data":{
            "A": 0,
            "B": 0,
            "C": 0,
            "D": 0,
            "E": 0,
            "F": 0,
            "message": ""
        },
        "ISODate": datetime.utcnow()
    },
    {
        "device_id": "001",
        "data":{
            "A": 1,
            "B": 2,
            "C": 3
        },
        "ISODate": datetime.utcnow()
    },
    {
        "device_id": "002",
        "data": {
            "A": 1,
            "B": 2,
            "C": 3,
            "D": 4
        },
        "ISODate": datetime.utcnow()
    },
    {
        "device_id": "001",
        "data": {
            "A": 10,
            "B": 20,
            "C": 30
        },
        "ISODate": datetime.utcnow()
    },
    {
        "device_id": "001",
        "data": {
            "A": 1.1,
            "B": 2.2,
            "C": 3.3
        },
        "ISODate": datetime.utcnow()
    },
    {
        "device_id": "004",
        "data": {
            "B": 2,
            "C": 3,
            "message": "this should be hidden"
        },
        "ISODate": datetime.utcnow()
    },
    {
        "device_id": "005",
        "data": {
            "B": 2,
            "C": 3,
            "E": 0.000000012344
        },
        "ISODate": datetime.utcnow()
    },

]
db.command("batch_submit", query.records_batch_submit(data_list))


