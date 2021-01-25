"""
Author: Lindsay Kerr
OUPI: F3424749
Project: TM470 Web Service solution
"""

from flask import Flask, request
from time import sleep
from utilities.settings import db_server, db_rec_user, SECRET_KEY
from utilities.sanitize import Sanitize
# from utilities.logger import *
from databases.database_adapter import DatabaseWrapper
# if another database type is used, then exchange 'databases,mongodb' for
# 'databases.type'
from databases.monogodb.wsqueries import EnviroWSQueries
from databases.monogodb.database import Database
from ws_model.ws_data_retrieval import DataRetrieval
from ws_model.ws_client_operations import ClientOperations, valid_session

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
    return retrieve.location_measurement_records(location, measurement.upper())


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

    username = None
    app_label = None

    if "app-label" in request.form and "username" in request.form:
        username = Sanitize.scrub_form_input(request.form["username"])

        if valid_session(username):
            app_label = Sanitize.scrub_form_input(request.form["app-label"])

    return client.gen_token(SECRET_KEY, username, app_label)


@app.route("/api/v1/login", methods=['GET'])
def client_login():
    return client.client_login()


@app.route("/api/v1/login-auth", methods=['POST'])
def login_auth():
    if 'username' in request.form and 'password' in request.form:
        username = Sanitize.scrub_form_input(request.form['username'])
        password = Sanitize.scrub_form_input(request.form['password'])
    else:
        username = None
        password = None

    sleep(.5)

    return client.login_auth(username, password)


@app.route("/api/v1/logout")
def client_logout():
    return client.client_logout()



if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)


