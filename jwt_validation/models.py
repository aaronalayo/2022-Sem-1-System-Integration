from re import M
from tracemalloc import start
from typing import Mapping
from pydantic import BaseModel
import pandas as pd
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


def save(user_id, user):
    r.hset(f'user:{user_id}', mapping={"mobile":f"{user['mobile']}", "code":f"{user['code']}", "cpr": f"{user['cpr']}"})
    # print(f"Saved user: {user_id}")
    

def get_user(user_id):
    user_exist = r.hexists(f'user:{user_id}', 'code')
    if user_exist == True:
        user = r.hgetall(f'user:{user_id}')
        # print(user)
        return user
    else:
        return False

def save_token(user_id,token):
    saved_token = r.hset(f'token:{token}', mapping={"user_id": f"{user_id}", "token":f"{token}"})
    # print(f'token saved: {saved_token}')
    return saved_token

def check_token(token):
    if r.hexists(f'token:{token}', 'token'):
        return True
    else:
        return False

def check_message(last_message_id):
    try:
        if r.hexists(f'message:{last_message_id}', 'id'):
            return True
        else:
            return False
    except Exception as ex:
        print(ex)
        return str(ex)   

def get_messages(last_message_id, limit, topic):
    messages =[]
    try:
        for key,value in enumerate(redis.scan_iter(match='message:*')):   
                message = redis.hgetall(value)
                if last_message_id not in message['id'] and topic in message['topic']:                  
                    messages.append(message)
        sorted_messages=sorted(messages, key= lambda x: uuid.UUID(x['id']).time)
        final_messages = sorted_messages[-int(limit):]
        return final_messages
    except Exception as ex:
        print(ex)
        return str(ex) 


def create_message(topic, message):
    try:
        ttl = 14600
        KEY_INDEX = 'index'
        id=uuid.uuid1()
        r.incr(KEY_INDEX, 1)  # If key doesn't exist it will get created
        index = r.get(KEY_INDEX).decode('utf-8')  # Decode from byte to string
        int_index = int(index)  # Convert from string to int
        # created_message = r.hset('message:%d' % int_index, mapping={"topic":f"{topic}", "message":f"{message}"})
        created_message = r.hset(f'message:{id}', mapping={"id":f"{id}","topic":f"{topic}", "message":f"{message}"})
        r.expire(f'message:{id}', time=ttl )
        print(f"Saved message")
        return created_message
    except Exception as ex:
        print(ex)
        return str(ex) 

def get_message(message_id):
    try:
        message_exist = r.hexists(f'message:{message_id}', 'id')
        if message_exist == True:
            message = r.hgetall(f'message:{message_id}')
            # df = pd.DataFrame.from_records(message, index=[message])
            # print(df)
            return message
        else:
            return False
    except Exception as ex:
        print(ex)
        return str(ex)

def update_message(message_id, topic, message):
    try:
        message_exist = r.hexists(f'message:{message_id}', 'id')
        if message_exist == True:
            r.hset(f'message:{message_id}', mapping={"topic":f"{topic}", "message":f"{message}"})
            return True
        else:
            return False
    except Exception as ex:
        print(ex)
        return str(ex)

def delete_message(message_id):
    try:
        message_exist = r.hexists(f'message:{message_id}', 'id')
        if message_exist == True:
            r.delete(f'message:{message_id}')
            return True
        else:
            return False
    except Exception as ex:
        print(ex)
        return str(ex)




