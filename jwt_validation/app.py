from bottle import default_app, request, get, post, redirect, response,run, view, template
import json
import jwt
import uuid
from send_sms import send_sms
from send_email import send_email
from secret import secret
from models import User, save, get_user
from get_phone import phone
from get_code import generate_code


@get("/")
@view("index")
def _():
    return



@post("/validate_token")
@view("code")
def _():
    jwtdata = json.load(request.body)
    try:
        data = jwt.decode(jwtdata, key=secret, algorithms=['HS256', ])
        print(data)
        code = generate_code()
        res = send_sms(code)
        res = send_email(code)
        
        user = User(mobile= str(phone), code= str(code), cpr=data['cpr'])
        
        # print(user.dict())
        user_id = str(uuid.uuid4())
        save(user_id, dict(user))   
        response.set_cookie(name='userId', value=user_id)
        return redirect("code")          
    except jwt.InvalidSignatureError:
        return redirect('/')

@get("/code")
@view("code")
def _():
    return

@post("/validate_code")
def _():
    user_id = request.get_cookie("userId")
    print(user_id)
    code = request.forms.get("code")
    print(code)
    user = get_user(user_id)
    user_code = user[b"code"].decode()
    if user_code == code:
        print(f'this is the code: {code}')
        return redirect("/welcome")
    else:
        print(f'code not found')
        return redirect('/')

@get("/welcome")
@view("welcome")
def _():
    return

try:
    #Server AWS (Production)
    import production
    application = default_app()
except:
    #local Machine(Development)
    run(host="127.0.0.1", port=8000, debug=True, reloader=True, server="paste")