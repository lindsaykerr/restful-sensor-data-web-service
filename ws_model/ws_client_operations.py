import jwt
from flask import render_template, request, redirect, session


class ClientOperations:

    def __init__(self, database_obj, query_obj):
        self.db = database_obj
        self.query = query_obj


    def client_registration(self):
        values = {'title': 'Client Registration', 'errors': ""}
        # if there was and error with client registration use code to notify
        # user
        if len(request.args) > 0 and request.args['error-code']:
            error_val = request.args['error-code']
            if error_val:
                values['errors'] = 'Credenitials are taken'

        return render_template('registration.html', values=values)

    def process_client_registration(self):
        if (len(request.args) == 3) and \
                (request.args['password']) and \
                (request.args['email'] and request.args['username']):
            # strip any white spaces, if any from the ends of the data data
            password = request.args['password'].strip(" ")
            username = request.args['username'].strip(" ")
            email = request.args['email'].strip(" ")

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
            appkeys = {'key_list': [], 'user': username, 'limit': 3}

            # build a list of tokens and related app identifier
            for result in results:
                appkeys['key_list'].append(
                    [result['token'].decode('utf-8'), result['app_name']])

            return render_template("client-page.html", appkeys=appkeys)
        else:
            return render_template('403.html'), 403

    def gen_token(self, secret):
        # if there no active session respond with 403 code
        if not ('username' in session):
            return render_template('403.html'), 403

        # if the session username and username from the request form do not match
        # remove the session and respond with a 403 error code
        if not (request.form['username'] and
                request.form['username'] == session['username']):
            session.pop('username', None)
            return render_template('403.html'), 403

        # a username and app identifier is required
        if request.form['username'] and request.form['app-name']:

            username = request.form['username'].strip(" ")
            app_name = request.form['app-name'].strip(" ")

            # get a list of tokens which are assigned to a specific username
            token_list = self.db.read_one(
                self.query.retrieve_client_tokens(username)
            )

            # determine how many tokens exist within the db
            token_count = len(token_list)

            # only create a limited number of tokens
            if token_count < 3:

                # creates a JSON web token
                token = jwt.encode(
                    {
                        'username': username,
                        'app_name': app_name,
                        'app_num': token_count + 1
                    },
                    secret,
                    algorithm='HS256'
                )
                # insert the token into the token collection
                x = self.db.create_one(self.query.add_client_token(
                    username,
                    app_name,
                    token)
                )
                if not x:
                    return 'token submission failure'

            # return to the client page
            return redirect("/api/v1/client/" + username, code=307)
        else:
            return render_template('403.html'), 403

    def client_login(self):
        return render_template("login.html")

    def login_auth(self):
        if request.form['username'] and request.form['password']:

            username = request.form['username'].strip(" ")
            passwrd = request.form['password'].strip(" ")

            q_result = self.db.read_one(self.query.client_details_request(
                username=username, password=passwrd)
            )
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