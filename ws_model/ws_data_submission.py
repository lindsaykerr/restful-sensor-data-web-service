from flask import request, render_template
from utilities.verification import verify_device
from utilities.validation import validate_data
from utilities.logger import *


class DataSubmission:

    def __init__(self, database_obj, query_obj):
        self.db = database_obj
        self.query = query_obj

    def submit_device_data(self, device_id, validation_strategy):
        self.query.set_query_device(device_id)

        response = ""
        if request.method == "GET" and self._verify_device(device_id):
            # Test to see the client request data is json, if not log error
            data = request.get_json(cache=False, silent=True)

            if not data:
                ErrorDataVailidation(
                    device_id,
                    "JSON data was not received",
                    ExtraNothing()
                ).log_it()

                return response

            # check to see if the JSON object is empty, if it is log error
            if data == {}:
                ErrorDataVailidation(
                    device_id,
                    "JSON data is empty",
                    ExtraNothing()
                ).log_it()

                return response
            # turn the json object into a string
            # print(data_str)
            # turn the string into a dict
            # data_raw = json.loads(data_str)
            data['device_id'] = device_id

            # check to see if if the data data passes validation,
            # if not log error

            if self._validate_data(data, validation_strategy) is False:
                error_str = data.replace(",", "")
                ErrorDataVailidation(
                    device_id,
                    error_str,
                    ExtraNothing()
                ).log_it()
                return response

            # print(data)
            # open a connection to the db and insert a record

            x = self.db.create_one(self.query.submit_device_data(data))
            response = str(x)

        else:
            ErrorDeviceVerfication(device_id,
                                   "verification failure",
                                   ExtraNothing()
                                   ).log_it()
            response = render_template('403.html'), 403
        return response

    def _verify_device(self, device):
        return verify_device(self.db, self.query, device)

    def _validate_data(self, data, validation_strategy):
        return validate_data(data, self.query, self.db, validation_strategy)
