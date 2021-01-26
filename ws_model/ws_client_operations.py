import jwt
from flask import render_template, request, redirect, session


def valid_session(username):
    """
    Determines if there is a current valid session for a given user
    :param username: a valid username
    :return: true or false depending on if a session exists or not
    """
    # Todo a more elaborate seesion is needed to improve security
    if not ("username" in session and username == session['username']):
        session.pop('username', None)
        return False
    return True


class ClientOperations:
    """
    Provides the bossiness logic for a given URI resource
    """
    def __init__(self, database_obj, query_obj):
        """
        The ClientOperations constructor
        :param database_obj: an object which implements the ICRUDCommands
        interface
        :param query_obj: a
        """
        self.db = database_obj
        self.query = query_obj

    def client_registration(self):
        values = {'title': 'Client Registration', 'errors': ""}
        # if there was and error with client registration use code to notify
        # user
        if len(request.args) > 0 and request.args['error-code']:
            error_val = request.args['error-code']
            if error_val:
                values['errors'] = 'Credentials are taken'

        return render_template('registration.html', values=values)

    def process_client_registration(self, password, username, email):

        # If all form fields were filled in
        if password and username and email:

            # see if the user name already exists
            q_result1 = self.db.read_one(self.query.client_details_request(
                username=username)
            )

            # see if the the hashed version of the email address exists
            q_result2 = self.db.read_one(self.query.client_details_request(
                email=email)
            )
            # if either the email or username exists redirect user back to
            # registration
            if q_result1 or q_result2:
                if q_result1 and q_result2:
                    code = 1
                elif q_result1:
                    code = 2
                else:
                    code = 3
                param = "error-code=" + str(code)
                return redirect("/api/v1/registration?" + param)
            else:
                # Todo code does not comply with GDPR, the email address
                #  should go through a process of anonymisation

                # register the user
                q_result = self.db.create_one(self.query.create_new_client(
                    username,
                    email,
                    password
                ))
                if q_result:
                    return redirect('success', user_name=username)

        return redirect("/api/v1/registration")

    def registration_sucess(self):
        return render_template("successful-registration.html")

    def client_page(self, username):
        # a session must exist before the client page can be accessed.
        if 'username' in session and session['username'] == username:

            # get all the token from the db for a specific username
            results = self.db.read_many(self.query.retrieve_client_tokens(
                username)
            )
            print("client page", results)
            appkeys = {'key_list': [], 'user': username, 'limit': 3}

            # build a list of tokens and related app identifier
            for result in results:
                appkeys['key_list'].append(
                    [result['token'], result['app_name']])

            return render_template("client-page.html", appkeys=appkeys)
        else:
            return render_template('403.html'), 403

    def gen_token(self, secret, username, app_label):

        if username and app_label:
            # get a list of tokens which are assigned to a specific username

            token_list = self.db.read_many(
                self.query.retrieve_client_tokens(username)
            )

            # determine how many tokens exist within the db
            if not token_list:
                token_list = []

            token_count = len(token_list)

            # only create a limited number of tokens
            if token_count < 3:

                # creates a JSON web token
                token = jwt.encode(
                    {
                        'username': username,
                        'app_label': app_label,
                        'app_num': token_count + 1
                    },
                    secret,
                    algorithm='HS256'
                )
                # insert the token into the token collection
                result = self.db.create_one(self.query.add_client_token(
                    username,
                    app_label,
                    token)
                )
                if not result:
                    return 'token submission failure'

            # return to the client page
            return redirect("/api/v1/client/" + username, code=307)
        else:
            return render_template('403.html'), 403

    def client_login(self):
        return render_template("login.html")

    def login_auth(self, username, password):
        if username and password:

            q_result = self.db.read_one(self.query.client_details_request(
                username=username, password=password)
            )
            #print(q_result)
            if q_result:
                session['username'] = username
                return redirect("/api/v1/client/" + username, code=307)

            # return { "username" : username, "password" : passwrd}

        # print(len(request.form))
        # return ""
        return render_template("login.html")

    def client_logout(self):
        if 'username' in session:
            session.pop('username', None)
        return redirect("/api/v1/login", code=307)
