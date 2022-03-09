from bottle import default_app, request, get, post, redirect, response,run, view, template
import json
import jwt
import requests
from send_sms import send_sms
from secret import secret


@get("/")
@view("index")
def _():
    return



@post("/jwt")
def _():
    jwtdata = json.load(request.body)
    token =jwt.encode(jwtdata, secret, algorithm="HS256")
    
    try:
        json.loads(json.dumps(jwt.decode(token, key=secret, algorithms=['HS256', ])))
        send_sms()

        return redirect('/code')
    except jwt.InvalidSignatureError:
        return redirect('/')

@get("/code")
@view("code")
def _():
    return

try:
    #Server AWS (Production)
    import production
    application = default_app()
except:
    #local Machine(Development)
    run(host="127.0.0.1", port=3333, debug=True, reloader=True, server="paste")