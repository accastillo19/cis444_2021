from flask import request, g
from flask_json import FlaskJSON, JsonError, json_response, as_json
from tools.token_tools import create_token
from psycopg2 import sql

from tools.logging import logger

import bcrypt

def handle_request():
    logger.debug("Login Handle Request")
    #use data here to auth the user
    cur = g.db.cursor()
    user_name = request.form['username']
    password_from_user_form = request.form['password']
    user = {
            "sub" : request.form['username'] #sub is used by pyJwt as the owner of the token
            }
    if not user:
        return json_response(status_=401, message = 'Invalid credentials', authenticated =  False )

    cur.execute("select password from users where user_id = 1;")
    correct_password = cur.fetchone()[0]
    correct_password = bytes(correct_password, 'utf-8')
    if( bcrypt.checkpw( bytes(password_from_user_form, 'utf-8') , correct_password)):
        return json_response( token = create_token(user) , authenticated = True)
    else:
        return json_response( message = "Incorret Username or Password" , authenticated = False)
