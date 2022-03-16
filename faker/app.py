from bottle import default_app, request, get, post, redirect, response,run, view, template
from faker import Faker
fake = Faker()
import uuid
import sqlite3
import json
import jwt

# print(fake.name()) #Dylan Garcia
# print(fake.first_name())
# print(fake.email())

# :user_id

@get("/")
@view("index")
def _():
    return

@post("/validate")
@view("nice")
def _():
    jwtdata = json.load(request.body)
    print(jwtdata)
    try:
        jwt.decode(jwtdata, key="secret", algorithms=['HS256', ])
        
        
        return redirect("nice")

    except jwt.InvalidSignatureError:
        return redirect('/')
    
@get("/nice")
@view("nice")
def _():
    return

# users = [ {
#     "user_id": str(uuid.uuid4()),
#     "user_name": fake.first_name(),
#     "user_email": fake.email(),

# } for _ in range(100000)]
    

# try:
#     db = sqlite3.connect("database.db")
#     counter = db.executemany("INSERT INTO users VALUES(:user_id, :user_name, :user_email, :user_password)", users).rowcount
#     if not counter: print("Nothing was inserted...")
#     print(f'Rows added {counter}')
#     db.commit()
# except Exception as ex:
#     print(ex)
# finally:
#     db.close()



run(host="127.0.0.1", port=3333, debug=True, reloader=True, server="paste")