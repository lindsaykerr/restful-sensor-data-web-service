from datetime import datetime


def validate_data(data, query, database_obj, validation_strategy):
    # connect ot the db using the submission credentials

    expected = database_obj.read_one(query.submit_validation_params(data))

    return validation_strategy.is_valid(expected, data)


def options_from_args(request_args):
    options = {"from": None, "to": None}

    if 'from' in request_args:
        try:
            # convert the text value time data into a datetime object
            options["from"] = datetime.strptime(
                request_args['from'],
                '%d-%m-%Y')
        except Exception as e:
            print(e)
            return None

    if 'to' in request_args:
        try:
            options["to"] = datetime.strptime(
                request_args['to'], '%d-%m-%Y'
            )
        except Exception as e:
            print(e)
            return None

    if ('interval' in request_args) and \
            (request_args['interval'] in ['day','week', 'month', 'hour']):
        options["interval"] = request_args["interval"]

    if len(set(request_args.keys()) - {'interval', 'to', 'from'}) > 0:
        options = None

    return options


class IValidationStrategy:
    def is_valid(self, expected, submitted):
        pass


class WSMongoValidateSubmit(IValidationStrategy):
    def is_valid(self, expected, submitted):
        bool_val = False
        if expected:
            expected_keys = []
            submitted_keys = []

            for data_key in expected:
                if not (data_key == '_id' or data_key == 'template'):
                    expected_keys.append(data_key)

            for data_key in submitted:
                submitted_keys.append(data_key)

            if len(set(expected_keys) - set(submitted_keys)) == 0:
                bool_val = True

        return bool_val
