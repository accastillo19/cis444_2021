from flask import request, g
from flask_json import FlaskJSON, JsonError, json_response, as_json
from tools.token_tools import create_token
from psycopg2 import sql

from tools.logging import logger

import bcrypt

def handle_request():
    logger.debug("Login Handle Request")
    cur = g.db.cursor()
    entered_address = request.form['address']
    cur.execute("Insert into Locations(Location) Values('"+entered_address+"');");
    g.db.commit()
        return json_response(status_=401, message = 'Invalid credentials', authenticated =  False )
