from flask import request, g
from flask_json import FlaskJSON, JsonError, json_response, as_json
from tools.token_tools import create_token

from tools.logging import logger

def handle_request():
    logger.debug("Purchase Handle Request")

      book_selection = request.form['books']
      buy_time =request.form['purchase_date']
      cur = g.db.cursor()
      cur.execute("UPDATE purchases SET book_name = '"+book_selection+"' WHERE username_id = 1;")
      cur.execute("UPDATE purchases SET date_time = '"+buy_time+"' WHERE username_id = 1;")
      g.db.commit()
      return json_response(status = "Purchase Succesful", authenticated = True)
