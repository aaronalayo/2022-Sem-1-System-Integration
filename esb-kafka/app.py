from email import message
from os import access
from bottle import get, response, run
import json
import time
import redis




r = redis.Redis(host='localhost', port=6379, db=0)


# users = {
#     "12345":{"id":"1", "email":"@a", "token":"12345"},
#     "67890":{"id":"2", "email":"@b", "token":"67890"}
# }

r.hset('user:12345', mapping={"id":"1", "email":"@a", "token":"12345"})
r.hset('user:67890', mapping={"id":"2", "email":"@b", "token":"67890"})

messages = {
    "1": [
        {"id":"b225b785-4a54-4314-8f37-ea4a3f315e01", "message":"m1", "access":"*", "created_at":time.time()},
        {"id":"777e9d68-47af-44c1-ac54-4c066872887e", "message":"m2", "access":"*"},
        {"id":"f0caf21c-051b-49c7-9255-318bc4e9467f", "message":"m3", "access":"*"},
        {"id":"d87bd821-6b78-479b-b41d-9ebfdea04abb", "message":"m4", "access":"*"},
    ]
}



@get("/provider/<id>/from/<last_message_id>/limit/<limit:int>/token/<token>")
def _(id, last_message_id, limit, token):
    try:
        #validation
        if limit == 0: raise Exception(f"Limit cannot be {limit}")
        user = r.hexists(f'user:{token}', 'id')
        user1 = r.hgetall(f'user:{token}')
        print(user1)
        if not user: raise Exception("Token is invalid")
        start_index = -1
        for i in range(len(messages[id])):
            if last_message_id in messages[id][i].values():
                start_index = i + 1
                break
        #validate index
        if start_index == -1: raise Exception(f"no message with {last_message_id}")
        response.content_type = "application/json"
        #handle response
        return json.dumps(messages[id][start_index:limit+start_index])

    except Exception as ex:
        response.status = 400
        return str(ex)


run(host='127.0.0.1', port=3000, debug=True, reloader=True)