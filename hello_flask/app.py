from flask import Flask,render_template,request,jsonify
from flask_json import FlaskJSON, JsonError, json_response, as_json
import jwt

import datetime
import bcrypt


from db_con import get_db_instance, get_db

app = Flask(__name__)
FlaskJSON(app)

USER_PASSWORDS = { "cjardin": "strong password"}

IMGS_URL = {
            "DEV" : "/static",
            "INT" : "https://cis-444-fall-2021.s3.us-west-2.amazonaws.com/images",
            "PRD" : "http://d2cbuxq67vowa3.cloudfront.net/images"
            }

CUR_ENV = "PRD"
JWT_SECRET = None

global_db_con = get_db()


with open("secret", "r") as f:
    JWT_SECRET = f.read()

@app.route('/') #endpoint
def index():
    return 'Web App with Python Caprice!' + USER_PASSWORDS['cjardin']

@app.route('/buy') #endpoint
def buy():
    return 'Buy'

@app.route('/hello') #endpoint
def hello():
    return render_template('hello.html',img_url=IMGS_URL[CUR_ENV] )

@app.route('/back',  methods=['GET']) #endpoint
def back():
    return render_template('backatu.html',input_from_browser=request.args.get('usay', default = "nothing", type = str) )

@app.route('/backp',  methods=['POST']) #endpoint
def backp():
    print(request.form)
    salted = bcrypt.hashpw( bytes(request.form['fname'],  'utf-8' ) , bcrypt.gensalt(10))
    print(salted)

    print(  bcrypt.checkpw(  bytes(request.form['fname'],  'utf-8' )  , salted ))

    return render_template('backatu.html',input_from_browser= str(request.form) )

@app.route('/auth',  methods=['POST']) #endpoint
def auth():
        print(request.form)
        return json_response(data=request.form)

@app.route('/login', methods=['POST']) #endpoint
def login():
    user_name = request.form['username']
    cur = global_db_con.cursor()
    cur.execute("select username from users where user_id = 1;")
    correct_username = cur.fetchone()[0]
    salted = bcrypt.hashpw( bytes(request.form['password'], 'utf-8' ), bcrypt.gensalt(10))
    print(salted)
    cur.execute("select password from users where user_id = 1;")
    correct_password = cur.fetchone()[0]
    correct_password = bytes(correct_password, 'utf-8')
    print("entered username:")
    print(user_name)
    print("correct username:")
    print(correct_username)
    print("correct password:")
    print(correct_password)
    if( bcrypt.checkpw( bytes(request.form['password'], 'utf-8') , correct_password)): #compare password with correct password
      print("correct username and password")
      #encoding user name and passing a jwt token
      token = jwt.encode({"username": correct_username}, JWT_SECRET, algorithm="HS256")
      return json_response(jwt_token = token) #setting token as jwt_token and passing
    else:
      return jsonify(status = "Bad", data = "Invalid Username or Password")

@app.route('/bookstore', methods=['GET']) #endpoint
def bookstore():
    cur = global_db_con.cursor()
    cur.execute(" select book_name from books;")
    book_grab = cur.fetchall()
    print(book_grab)
    cur.execute("select book_price from books;")
    price_grab = cur.fetchall()
    passtoken = request.headers.get('Authorization') #get access to header authorization and jwt token from html file
    if decodeToken(passtoken) == True: #if decoded username is true using decode function
    	print("User is A Valid User Insert Books")
    	print(passtoken)
    	return json_response(jwtToken_key = passtoken,book_library = book_grab,price_library = price_grab) #return jwttoken key decoded which is the authenticated user and pass the books
    else:

   	 return json_response(status = "Error")

def decodeToken(jwtToken_key):
    print("Passing Through Decode Function")
    jwtTokenkey_decode = jwt.decode(jwtToken_key,JWT_SECRET, algorithms="HS256") #decode encoded jwtToken_key
    print(jwtTokenkey_decode.get('username')) 
    strUser = jwtTokenkey_decode.get('username') #store decoded username
    cur = global_db_con.cursor()
    cur.execute("select username from users where user_id =1;")
    valid_user = cur.fetchone()[0]
    print(valid_user)
    if valid_user == strUser: #check if decoded username is equal to valid username
   	 print("JWT Token Success")
   	 return True
    else:
    	return False

@app.route('/buybooks',methods = ['POST']) #endpoint
def buybooks():
    print("Requestform['books'] value:")
    print(request.form['books'])
    book_selection = request.form['books'] #storing selected book from request form
    print("Selected Book:")
    print(book_selection)
    print("Requestform['purchase_date'] value:") 
    print(request.form['purchase_date'])
    buy_time =request.form['purchase_date']  #storing purchase time from request form
    print("buy time:")
    print(buy_time)
    cur = global_db_con.cursor()
    cur.execute("update purchases set book_name = "+book_selection+" where username_id = 1;")
    cur.execute("update purchases set date_time = "+buy_time+" where username_id = 1;") 
    return json_response(status = "Purchase Succesful")

#Assigment 2
@app.route('/ss1') #endpoint
def ss1():
    return render_template('server_time.html', server_time= str(datetime.datetime.now()) )

@app.route('/getTime') #endpoint
def get_time():
    return json_response(data={"password" : request.args.get('password'),
                                "class" : "cis44",
                                "serverTime":str(datetime.datetime.now())
                            }
                )

@app.route('/auth2') #endpoint
def auth2():
    jwt_str = jwt.encode({"username" : "cary",
                            "age" : "so young",
                            "books_ordered" : ['f', 'e'] } 
                            , JWT_SECRET, algorithm="HS256")
    #print(request.form['username'])
    return json_response(jwt=jwt_str)

@app.route('/exposejwt') #endpoint
def exposejwt():
    jwt_token = request.args.get('jwt')
    print(jwt_token)
    return json_response(output=jwt.decode(jwt_token, JWT_SECRET, algorithms=["HS256"]))


@app.route('/hellodb') #endpoint
def hellodb():
    cur = global_db_con.cursor()
    cur.execute("insert into music values( 'dsjfkjdkf', 1);")
    global_db_con.commit()
    return json_response(status="good")


app.run(host='0.0.0.0', port=80)













