from abc import ABC

from databases.interfaces.iwsqueries import IWSQueries
from datetime import timedelta, datetime
import hashlib


class EnviroWSQueries(IWSQueries, ABC):
    """
    Contains MongoDB specific commands required for reading and writing data
    to a database
    """
    # listing of mongo collections used in the database
    collection = {
        'DEVICES': 'devices',       # info about IoT devices
        'DATA': 'data',             # main data collection for all devices
        'CLIENTS': 'clients',       # info on registered clients
        'TOKEN_KEYS': 'tokenkeys'   # contains client token keys
    }

    def __init__(self):
        self.device = None
        self.measurement = None
        self.location = None

    def set_query_device(self, device_name):
        self.device = device_name

    def set_query_measurement(self, measurement):
        self.measurement = measurement

    def set_query_location(self, location):
        self.location = location

    def verify_device(self, device):
        return {
            'collection': self.collection['DEVICES'],
            'match': {'device_id': self.device}
        }

    def get_device_id(self, location):
        return {
            'collection': self.collection['DEVICES'],
            'match': {'location': location, 'device_data': 'accessible'},
            'projection': {'device_id': 1, '_id': 0}
        }

    def list_locations(self):
        return {
            'collection': self.collection['DEVICES'],
            'match': {'device_data': 'accessible'},
            'projection': {'_id': 0, 'location': 1}
        }

    def location_info(self, device):
        return {
            'collection': self.collection['DEVICES'],
            'match': {'device_id': self.device},
            'projection': {'_id': 0, 'geolocation': 1, 'device_status': 1}
        }

    def location_measurements(self, device):
        return {
            'collection': self.collection['DEVICES'],
            'match': {'device_id': device},
            'projection': {'_id': 0, 'measures': 1}
        }

    def location_measurement_records(self, device:str, measurement:str, params=None):
        query = {
            'collection': self.collection['DATA'],
            'match': {'device_id': device},
            'projection': {'_id': 0, 'datetime': 1, "data." + measurement: 1}
        }

        if params:
            for_match, for_group = self.process_query_options(
                params, measurement.upper()
            )
            if for_match:
                query['match'] = {**query["match"], **for_match}
            if for_group:
                query["group"] = for_group

        return query

    def submit_device_data(self, query_data):
        return {
            'collection': self.collection['DATA'],
            'match': query_data
        }

    def process_query_options(self, options: dict, measurement):

        for_match = None
        for_group = None
        if "from" in options and options["from"] and "to" in options and options["to"]:
            if (isinstance(options["from"], datetime)) and \
                    (isinstance(options["to"], datetime)):
                    for_match = {
                        '$and': [
                            {'datetime': {'$gt': options["from"]}},
                            {'datetime': {
                                '$lt': options["to"] + timedelta(days=1)
                            }}
                        ]
                    }
        elif "from" in options and options["from"]:

            for_match = {'datetime': {'$gt': options["from"]}}
        elif "to" in options and \
                options["to"] and \
                isinstance(options["to"], datetime):
            for_match = {'datetime': {'$lt': options["to"] + timedelta(days=1)}}

        if "interval" in options:
            if options['interval'] == 'day':
                for_group = {'$dayOfYear': '$datetime'}
            elif options['interval'] == 'week':
                for_group = {'$week': '$datetime'}
            elif options['interval'] == 'month':
                for_group = {'$month': '$datetime'}
            elif options['interval'] == 'hour':
                for_group = {'day': {'$dayOfYear': '$datetime'},
                         'hour': {'$hour': '$datetime'}}

            if for_group:
                for_group = {
                        '_id': for_group,
                        'datetime': {'$max': '$datetime'},
                        'avg': {'$avg': f'$data.{measurement}'},
                        'min': {'$min': f'$data.{measurement}'},
                        'max': {'$max': f'$data.{measurement}'}
                }

        return for_match, for_group

    def submission_validation_params(self):
        return {
            'collection': self.collection['DATA'],
            'match': {'template': 'submit_reading'}
        }

    def client_details_request(self, username=None, email=None, password=None):
        match = {}
        if username:
            match['username'] = username

        if password:
            match['password'] = password
        if email:
            match['emailhash'] = hashlib.sha1(str.encode(email)).digest()

        return {
            'collection': self.collection['CLIENTS'],
            'match': match,
            'projections': {'_id': 0, 'username': 1}
        }

    def create_new_client(self, username, email, password):
        return {
            'collection': self.collection['CLIENTS'],
            'match': {
                'username': username,
                'emaihash': hashlib.sha1(str.encode(email)).digest(),
                'password': password,
                'appKeys': []
            }
        }

    def retrieve_client_tokens(self, username):
        return {
            'collection': self.collection['TOKEN_KEYS'],
            'match': {'username': username},
            'projection': {'_id': 0}
        }

    def add_client_token(self, username, app_name, token):
        return {
            'collection': self.collection['TOKEN_KEYS'],
            'match': {
                'token': token,
                'app_name': app_name,
                'username': username
            }
        }

    def search_for_token(self, token: str):
        return {
            'collection': self.collection['TOKEN_KEYS'],
            'match': {'token': token}
        }

    def device_batch_submit(self, device_list):
        return {
            'collection': self.collection['DEVICES'],
            'query': device_list
        }

    def records_batch_submit(self, data_list):
        return {
            'collection': self.collection['DATA'],
            'query': data_list
        }