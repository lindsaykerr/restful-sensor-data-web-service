from flask import render_template, request
import re
from utilities.validation import *
from utilities.verification import *


class DataRetrieval:

    def __init__(self, database_obj, query_obj):
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
                    'data': self.db.read_one(self.query.location_info()),
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
                q_result = self.db.read_one(self.query.location_measurements())
                q_result = q_result['measures']
                requested = {'status': 'success', 'data': q_result}
            else:
                requested = {'status': 'failure'}
        else:
            requested = render_template('403.html'), 403

        return requested

    def location_measurement_records(self, location, measurement):
        """
        Provides the data acquired at a location for a specific measure
        :param location: String
        :param measurement: String
        :return: json object
        """
        if not self._valid_token():
            return render_template('403.html'), 403

        measurement = measurement.upper()
        self.query.set_query_location(measurement)

        device_id = self._get_device_id(location)
        self.query.set_query_device(device_id)

        if not device_id:
            return {'status': 'failure'}

        # check to see if the client has entered any parameters
        if len(request.args) > 0:

            query_options = options_from_args(dict(request.args))
            final_query = self.query.location_measurement_records(
                device_id,
                query_options
            )

            # if None is returned client has entered an incorrect parameter key
            if query_options is None:
                return {'status': 'failure',
                        'client_error': 'invalid filter parameter',
                        'measure': measurement}

            if 'interval' in request.args:
                q_result = self.db.group_by(final_query)

                '''
                q_result = db.aggregate(
                    'data',
                    query_1,
                    group_by_interval(request.args, measurement)
                )
                '''
                # return a failure if the incorrect interval value  was provided
                if not q_result:
                    return {'status': 'failure',
                            'client_error': 'incorrect interval value',
                            'measure': measurement}

                # the following line extracts each record document from the
                # aggregated data and places them in a list, this done to
                # prevent an error being raised when data is returned to the
                # client
                q_result = [doc for doc in q_result]

                # format the data before giving it to the client
                # Todo the following must be refactored as it is too Mongodb
                #  specific
                for doc in q_result:
                    # round of calculated averages
                    doc['avg'] = round(doc['avg'], 2)
                    # remove the mongoDB document id
                    del doc['_id']
                    # rename the date/Time value holder
                    doc['timestamp'] = doc['ISODate']
                    del doc['ISODate']

                return {'status': 'success', 'measure': measurement,
                        'data': q_result}

        q_result = self.db.read_many(self.location_measurement_records(
            device_id,
            None)
        )
        # formats the data before sending it to client
        for doc in q_result:
            # move nested stats to root level of the document
            doc.update(doc[measurement])
            # remove the record which contains the nested stats
            del doc[measurement]
            doc['timestamp'] = doc['datetime']
            del doc['datetime']

        return {'status': 'success', 'measure': measurement, 'data': q_result}

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
            token = matched.group(2).encode()
            # check to see if the token exists
            result = self.db.read_one(self.query.search_for_token(token))
            if result:
                return True
        return False

    def _get_device_id(self, location):
        return get_device_id(location, self.db, self.query)
