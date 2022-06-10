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
    ttl = 120
   
    r.hset(f'user:{user_id}', mapping={"mobile":f"{user['mobile']}", "code":f"{user['code']}", "cpr": f"{user['cpr']}"})
    r.expire(f'user:{user_id}', time=ttl )
    print(f"Saved user: {user_id}")
    

def get_user(user_id):
    user = r.hexists(f'user:{user_id}', 'user')
    user = r.hgetall(f'user:{user_id}')
    print(user)
    return user





