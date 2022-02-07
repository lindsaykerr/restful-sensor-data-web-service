from flask import render_template, request
import re
from utilities.validation import *
from utilities.verification import *
from databases.interfaces.iwsqueries import IWSQueries
from databases.interfaces.icrudcommands import ICRUDCommands


class DataRetrieval:

    def __init__(self, database_obj:ICRUDCommands, query_obj: IWSQueries):
        self.db = database_obj
        self.query = query_obj

    def IoT_locations(self):
        if self._valid_token():
            q_result = self.db.read_many(self.query.list_locations())

            requested = {
                'status': 'success',
                'data': q_result
            }
        else:
            requested = render_template('403.html'), 403

        return requested

    def location_info(self, location):
        if self._valid_token():
            device_id = self._get_device_id(location)
            self.query.set_query_device(device_id)

            if not device_id:
                requested = {'status': 'failure',
                             'message': 'Location not found'}
            else:
                requested = {
                    'status': 'success',
                    'data': self.db.read_one(
                        self.query.location_info(location)),
                    'location': location
                }
        else:
            requested = render_template('403.html'), 403

        return requested

    def location_measurements(self, location):
        if self._valid_token():
            device_id = self._get_device_id(location)
            self.query.set_query_device(device_id)

            if device_id:
                q_result = self.db.read_one(
                    self.query.location_measurements(device_id)
                )
                q_result = q_result['measures']
                requested = {'status': 'success', 'data': q_result}
            else:
                requested = {'status': 'failure'}
        else:
            requested = render_template('403.html'), 403

        return requested

    def location_measurement_records(self, location: str, measurement: str):
        """
        Provides the data acquired at a location for a specific measure
        :param location: String
        :param measurement: String
        :return: json object
        """
        if not self._valid_token():
            return render_template('403.html'), 403

        device_id = self._get_device_id(location)
        if not device_id:
            return {
                'status': 'failure',
                'client_error': 'device location unknown'
            }

        # check for and validate query parameters
        if len(request.args) > 0:
            query_options = options_from_args(dict(request.args))
        else:
            query_options = None

            '''
            if query_options is None:
                return {'status': 'failure',
                        'client_error': 'invalid filter parameter',
                        'measure': measurement}
            '''

        # if a user defines a time interval, data will be aggregated
        if query_options and 'interval' in query_options:
            q_result = self.db.group_by(self.query.location_measurement_records(
                device_id,
                measurement,
                query_options
            ))

            if q_result:
                for doc in q_result:
                    # round of calculated averages
                    doc['avg'] = doc['avg']
                    doc['timestamp'] = doc['datetime']
                    # remove unused data
                    del doc['_id']
                    del doc['datetime']
                return {
                    'status': 'success',
                    'measure': measurement,
                    'data': q_result
                }
            else:
                return {
                    'status': 'failure',
                    'client_error': 'incorrect interval value',
                    'measure': measurement}

        q_result = self.db.read_many(self.query.location_measurement_records(
            device_id,
            measurement,
            query_options
        ))
        if q_result:
            # formats the data before sending it to client
            x = 0
            while x < len(q_result):
                q_result[x].update(q_result[x]['data'])
                q_result[x]['timestamp'] = q_result[x]['datetime']
                del q_result[x]['data']
                del q_result[x]['datetime']
                x += 1

            return {'status': 'success', 'data': q_result}
        else:
            return {'status': 'nothing found'}

    def _valid_token(self):
        # check the authorisation header for key values
        auth = request.headers.get('authorization')

        if not auth:
            return False
        # match the expected value format of the authorization header
        # i.e. Bearer tokenkey
        matched = re.match(r'^([^ ]+) *([^ ]+)$', auth)
        if matched and matched.group(1).lower() == 'bearer':
            # encode the token to bytecode, as tokens in the db are also
            # in bytecode
            token = matched.group(2)
            # check to see if the token exists
            result = self.db.read_one(self.query.search_for_token(token))
            if result:
                return True
        return False

    def _get_device_id(self, location):
        return get_device_id(location, db=self.db, query=self.query)
