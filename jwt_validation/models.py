from typing import Mapping
from pydantic import BaseModel
import redis
import json
import uuid
import time

r = redis.StrictRedis()

redis = redis.Redis(host='localhost', port=6379, db=0, charset="utf-8", decode_responses=True)

class User(BaseModel):
    mobile:str
    code:str
    cpr:str


# r.hset('user:12345', mapping={"id":"1", "email":"@a", "token":"12345"})
# r.hset('user:67890', mapping={"id":"2", "email":"@b", "token":"67890"})

def save(user_id, user):
    ttl = 240
   
    r.hset(f'user:{user_id}', mapping={"mobile":f"{user['mobile']}", "code":f"{user['code']}", "cpr": f"{user['cpr']}"})
    r.expire(f'user:{user_id}', time=ttl )
    print(f"Saved user: {user_id}")
    

def get_user(user_id):
    user_exist = r.hexists(f'user:{user_id}', 'code')
    if user_exist == True:
        user = r.hgetall(f'user:{user_id}')
        print(user)
        return user
    else:
        return False

def save_token(user_id,token):
    saved_token = r.hset(f'token:{token}', mapping={"user_id": f"{user_id}", "token":f"{token}"})
    print(f'token saved: {saved_token}')
    return saved_token

def get_token(token):
    try:
        token_exist = r.hgetall(f'token:{token}')
        if token_exist:
            return True
    except:
        return False


def get_message(message):
    pass

def create_message(message):
    pass

def update_message(message_id):
    pass

def delete_message(message_id):
    pass




