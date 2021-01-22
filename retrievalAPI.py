"""
Author: Lindsay Kerr
OUPI: F3424749
Project: TM470 Web Service solution
"""

from flask import Flask
from utilities.settings import db_server, db_rec_user, SECRET_KEY
# from utilities.logger import *
from queries.database_adapter import DatabaseWrapper
# if another database type is used, then exchange 'queries,mongodb' for
# 'queries.type'
from queries.monogodb.wsqueries import EnviroWSQueries
from queries.monogodb.database import Database
from ws_model.ws_data_retrieval import DataRetrieval
from ws_model.ws_client_operations import ClientOperations

app = Flask(__name__)

app.secret_key = SECRET_KEY

db = DatabaseWrapper()
db.set_database(Database(
    username=db_rec_user['username'],
    password=db_rec_user['password'],
    host=db_server['host'],
    database_name=db_server['db'],
))
q = EnviroWSQueries()
retrieve = DataRetrieval(db, q)
client = ClientOperations(db, q)


@app.route('/api/v1/locations', methods=['GET'])
def locations():
    """
    Provides a list of locations which can be queried
    """
    return retrieve.IoT_locations()


@app.route('/api/v1/locations/<location>', methods=['GET'])
def location_info(location):
    """
    Provides information about a given location
    """
    return retrieve.location_info(location)


@app.route('/api/v1/locations/<location>/measurements', methods=['GET'])
def location_measurements(location):
    """
    Provides the measurements which can be queried for a given location
    """
    return retrieve.location_measurements(location)

@app.route('/api/v1/locations/<location>/measurements/<measurement>',
           methods=['GET'])
def location_measurement_records(location, measurement):
    """
    Provides the data acquired at a location for a specific measure
    """
    return retrieve.location_measurement_records(location, measurement)


#####
# Client Web service interactions and operations
#####

@app.route("/api/v1/registration")
def client_registration():
    """
    Redirects New users to a registration page
    """
    return client.client_registration()


@app.route("/api/v1/registration/submit")
def process_client_registration():
    return client.process_client_registration()


@app.route("/api/v1/registration/success")
def successful_client_registration():
    return client.registration_sucess()


@app.route("/api/v1/client/<username>", methods=['POST'])
def client_page(username):
    # a session must exist before the client page can be accessed.
    return client.client_page(username)


@app.route("/api/v1/client/generate-app-key", methods=['POST'])
def gen_token():
    return client.gen_token(SECRET_KEY)


@app.route("/api/v1/login", methods=['GET'])
def client_login():
    return client.client_login()


@app.route("/api/v1/login-auth", methods=['POST'])
def login_auth():
    return client.client_login()


@app.route("/api/v1/logout")
def client_logout():
    return client.client_logout()


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
