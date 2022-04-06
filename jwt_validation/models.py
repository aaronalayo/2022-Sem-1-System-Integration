from pydantic import BaseModel
import redis
import json
import uuid

r = redis.StrictRedis()

redis = redis.Redis(host='localhost', port=6379, db=0)

class User(BaseModel):
    mobile:str
    code:str

# class Token(BaseModel):
#     token :str
#     user: User
    

def save(userId, user):
    r.execute_command('JSON.SET', userId, '.', json.dumps(user))
    print("Saved user")
    

def get_u(userId):
    user = json.loads(r.execute_command('JSON.GET', userId))
    return user






