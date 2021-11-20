from flask import request, g
from flask_json import FlaskJSON, JsonError, json_response, as_json
from tools.token_tools import create_token

from tools.logging import logger

def handle_request():
   # book_selection = request.form['book_id']
   # cur = g.db.cursor()
   # cur.execute("UPDATE purchases SET book_name = '"+book_selection+"' WHERE username_id =1;")
   # g.db.commit()
   # return json_response(status = "Purchase Succesful")
    logger.debug("Get Books Handle Request")
    cur = g.db.cursor()
    cur.execute("select book_name from books;")
    book_grab = cur.fetchall()
    return json_response( token = create_token(  g.jwt_data ) , books = book_grab)

