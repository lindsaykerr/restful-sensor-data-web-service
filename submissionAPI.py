from flask import Flask

from databases.database_adapter import DatabaseWrapper
from databases.monogodb.database import Database
from databases.monogodb.wsqueries import EnviroWSQueries
from utilities.validation import WSMongoValidateSubmit
from utilities.settings import db_server, db_sub_user
from ws_model.ws_data_submission import DataSubmission

validation_stratagy = WSMongoValidateSubmit()

app = Flask(__name__)

db = DatabaseWrapper()
db.set_database(Database(
    username=db_sub_user['username'],
    password=db_sub_user['password'],
    host=db_server['host'],
    database_name=db_server['db'],
))
q = EnviroWSQueries()
submission = DataSubmission(db, q)


@app.route('/v1/devices/<device_id>/data/submit', methods=['POST', 'GET'])
def submit_device_data(device_id):
    return submission.submit_device_data(device_id, validation_stratagy)


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
    # app.run(debug=True)
