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

# The DatabaseWrapper implements the ICRUDCommands interface which provides the
# the basic set CRUD operations carried by most types of databases. In doing so
# it can accept a Database object which contains an implementation
# for connecting to a specific type of database such as MongoDB.
db = DatabaseWrapper()
db.set_database(Database(
    username=db_rec_user['username'],
    password=db_rec_user['password'],
    host=db_server['host'],
    database_name=db_server['db'],
))

# EnviroWSQueries implements the IWSQueries interface which contains query
# operations/methods for a tailored web service. EnviroWSQueries()
# contains a number of methods whose implementation return queries for a
# specific type of database. The intended database is indicated by viewing the
# package directory path for EnviroQueries. eg 'databases.mongodb.wsqueries'
q = EnviroWSQueries()

# Form maintainability purposes, the implementation processes for retrieval api
# and client site have been split and found within the  ws_model package. The
# additional benefit of doing so is that if the developer wishes to run the
# client site within a separate script they can do so without too much trouble
# by striping out the related elements. In many cases this may be the preferred
# solution.
retrieve = DataRetrieval(db, q)
client = ClientOperations(db, q)


@app.route('/api/v1/locations', methods=['GET'])
def locations():
    """
    Provides a list of locations which can be queried
    """
    return retrieve.locations()


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
# Client site for the Web service interactions and operations
#####

@app.route("/api/v1/registration")
def client_registration():
    """
    The page where users can register with the service
    """
    return client.client_registration()


@app.route("/api/v1/registration/submit", methods=['POST'])
def process_client_registration():
    """
    This resource is responsible for processing client registration
    """
    username = None
    email = None
    password = None
    args = request.args

    if 'password' in args and 'email' in args and 'username ' in args:
        username = Sanitize.scrub_form_input(args['username'])
        password = Sanitize.scrub_form_input(args['password'])
        email = Sanitize.scrub_form_input(args['email'])

    return client.process_client_registration(
        username=username,
        password=password,
        email=email
    )


@app.route("/api/v1/registration/success")
def successful_client_registration():
    """
    User is directed to a page which shows they have been successful registered
    """
    return client.registration_success()


@app.route("/api/v1/login", methods=['POST'])
def client_login():
    """
    Provides access to the user login page
    """
    return client.client_login()


@app.route("/api/v1/login-auth", methods=['POST'])
def login_auth():
    """
    Authenticates users credentials
    """
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
    """
    Provides a way for the user to logout from the system, deletes user session
    """
    return client.client_logout()


@app.route("/api/v1/client/<username>", methods=['POST'])
def client_page(username):
    """
    User page, provides a place for users to manage their account,
    a session must exist before the client page can be accessed.
    """
    #
    return client.client_page(username)


@app.route("/api/v1/client/generate-app-key", methods=['POST'])
def gen_token():
    """
    Provides the functionality fo generating new client app tokens
    """
    username = None
    app_label = None

    if "app-label" in request.form and "username" in request.form:
        username = Sanitize.scrub_form_input(request.form["username"])

        if valid_session(username):
            app_label = Sanitize.scrub_form_input(request.form["app-label"])

    return client.gen_token(SECRET_KEY, username, app_label)


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
