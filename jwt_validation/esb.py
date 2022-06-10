from bottle import default_app, request, get, post, redirect, response,run, view, template
import json
import jwt
import uuid
from models import get_token
messages = {
    "1": [
        {"id":"b225b785-4a54-4314-8f37-ea4a3f315e01", "message":"m1", "access":"*"},
        {"id":"777e9d68-47af-44c1-ac54-4c066872887e", "message":"m2", "access":"*"},
        {"id":"f0caf21c-051b-49c7-9255-318bc4e9467f", "message":"m3", "access":"*"},
        {"id":"d87bd821-6b78-479b-b41d-9ebfdea04abb", "message":"m4", "access":"*"},
    ]
}

@get("/read/topic/<topic>/from/<last_message_id>/limit/<limit:int>/token/<token>/format/<format>")
def _(topic, last_message_id, limit, token, format):
    print(topic, last_message_id, limit, token, format)
    output = {"messages": []}
    try:
        #validation
        if get_token(token) == False:
            raise Exception("Invalid Token")
        id = uuid.uuid4()
        messages = [id, topic, last_message_id, limit]
        if limit == 0: raise Exception(f"Limit cannot be {limit}")
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

run (host='127.0.0.1', port=9000, debug=True, reloader=True)