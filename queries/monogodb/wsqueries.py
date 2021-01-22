from abc import ABC

from queries.interfaces.iwsqueries import *
from datetime import timedelta
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
            'query': {'location': location, 'device_data': 'accessible'},
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

    def location_measurement_records(self, device, params=None):
        query = {
            'collection': self.collection['DATA'],
            'match': {'device_id': device},
            'projection': {'_id': 0, 'datetime': 1, self.measurement: 1}
        }

        if params:
            # group is only used when aggregating data
            if params["$group"]:
                query["match"] = {'$match:': query["match"]}
            query["match"] = {
                **query["match"],
                **(self.process_query_options(params))}

        return query

    def submit_device_data(self, query_data):
        return {
            'collection': self.collection['DATA'],
            'match': query_data
        }

    def process_query_options(self, options: dict):
        time_to = None
        time_from = None
        query_options = None
        group = None

        if not options["from"] is None:
            time_from = {'datetime': {'$gt': options["from"]}}
        if not options["to"] is None:
            date_value = options["to"] + timedelta(days=1)
            time_to = {'datetime': {'$lt': date_value}}

        if options["interval"] is not None:
            if options['interval'] == 'day':
                group = {'$dayOfYear': '$datetime'}
            elif options['interval'] == 'week':
                group = {'$week': '$datetime'}
            elif options['interval'] == 'month':
                group = {'$month': '$datetime'}
            elif options['interval'] == 'hour':
                group = {'day': {'$dayOfYear': '$datetime'},
                         'hour': {'$hour': '$datetime'}}
            if group:
                query_options["group"] = {
                    '$group': {
                        '_id': group,
                        'ISODate': {'$max': '$datetime'},
                        'avg': {'$avg': f'${self.measurement}.avg'},
                        'min': {'$min': f'${self.measurement}.min'},
                        'max': {'$max': f'${self.measurement}.max'}
                    }
                }

        if time_to or time_from:
            if time_to and time_from:
                query_options = {'$and': [time_from, time_to]}
            elif time_to:
                query_options = time_to
            else:
                query_options = time_from

        return query_options

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

    def search_for_token(self, token):
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