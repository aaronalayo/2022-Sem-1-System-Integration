from pydantic import BaseModel
import redis
import json
from redis.commands.json.path import Path
r = redis.StrictRedis()

redis = redis.Redis(host='localhost', port=6379, db=0)

class User(BaseModel):
    mobile:str
    code:str

# class Token(BaseModel):
#     token :str
#     user: User
    

def save(token, user):
    r.execute_command('JSON.SET', token, '.', json.dumps(user))
    print("Saved user")
    

def get_u(userToken):
    user = json.loads(r.execute_command('JSON.GET', userToken))
    return user






