import csv
from bottle import default_app, request, get, post, put, delete,redirect, response,run, view, template
import json
import jwt
import uuid
import xmltodict
import yaml
from handle_files import read_tsv, read_csv,write_csv,write_tsv
from models import check_token, check_message, get_messages, create_message, get_message, update_message, delete_message


@get("/get_messages/topic/<topic>/from/<last_message_id>/limit/<limit:int>/token/<token>/format/<format>")
def _(topic, last_message_id, limit, token, format):
    output = {"messages": []}
    try:
        #validation
        if check_token(token) == False:raise Exception("Invalid Token")
        messages = []
        if limit <= 0: raise Exception(f"Limit cannot be {limit}")
        if check_message(last_message_id) == False: raise Exception(f"There is no message with this id:{last_message_id}")
        messages = get_messages(last_message_id, limit, topic)
                
        if not len(messages):raise Exception(f"there are no messages")
           
        for message in messages:
            output["messages"].append(message)

            
        if format == "json":
            response.content_type = 'application/json'
            return json.dumps(output, default=str)
        elif format == "yaml":
            return yaml.dump(output)
        elif format == "xml":
            response.content_type = 'text/xml'
            return xmltodict.unparse(output, pretty=True, full_document=False)
        elif format == "csv":
            response.content_type = 'text/csv'
            return write_csv(output)
        elif format == "tsv":
            return write_tsv(output)

       
    except Exception as ex:
        response.status = 400
        print(ex)
        return str(ex)

@post("/create_message/topic/<topic>/token/<token>/format/<format>")
def _(topic,token, format):
    try:
        if check_token(token):
            
            message = request.body.read()
            print(f'message from body: {message}')
            if format == "json":
                message = json.loads(message)
                message = message["message"]
            elif format == "xml":
                message = json.dumps(xmltodict.parse(message)["message"])
                message = message.strip('"')
            elif format == "yaml":
                message =  yaml.safe_load(stream=message)["message"]
            elif format == "csv":
                message = read_csv(message)
            elif format == "tsv":
                message = read_tsv(message)
            
            if create_message(topic, message):
                return "Message created"
        else:
            raise Exception("Invalid Token")
    except Exception as ex:
        response.status = 400
        return str(ex)

@get("/get_message/message_id/<message_id>/token/<token>/format/<format>")
def _(message_id, token, format):
    try:
        #validation
        if check_token(token):
            message = get_message(message_id)
            message = {k.decode('utf8'): v.decode('utf8') for k, v in message.items()}
            
        else:
            raise Exception("Invalid Token")
        if format == "json":
            response.content_type = 'application/json'
            print(message)
            return json.dumps(message, default=str)
        elif format == "yaml":
            return yaml.dump(message)
        elif format == "xml":
            response.content_type = 'text/xml'
            return xmltodict.unparse(message, pretty=True, full_document=False)
        elif format == "csv":
            response.content_type = 'text/csv'
            return write_csv(message)
        elif format == "tsv":
            return write_tsv(message)
        else:
            raise Exception("Invalid Token")

       
    except Exception as ex:
        response.status = 400
        print(ex)
        return str(ex)


@put("/update_message/topic/<topic>/message_id/<message_id>/token/<token>/format/<format>")
def _(message_id, topic, token, format):
    print(message_id, token, topic, format)
    try:
        if check_token(token):
                
                message = request.body.read()
                # print(f'message from body: {message}')
                if format == "json":
                    message = json.loads(message)
                    message = message["message"]
                elif format == "xml":
                    message = json.dumps(xmltodict.parse(message)["message"])
                    message = message.strip('"')
                    print(message)
                elif format == "yaml":
                    message =  yaml.safe_load(stream=message)["message"]
                    print(message)
                elif format == "csv":
                    message = read_csv(message)
                elif format == "tsv":
                    message = read_tsv(message)
                
                if update_message(message_id, topic, message) == False:
                    return "There was a problem updating the message"
                else:
                    return "Message updated"
        else:
            raise Exception("Invalid Token")

       
    except Exception as ex:
        response.status = 400
        print(ex)
        return str(ex)


@delete("/delete_message/message_id/<message_id>/token/<token>")
def _(message_id, token):
    try:
        if check_token(token) == False:
            raise Exception("Invalid Token")

        if delete_message(message_id):
            return "Message deleted"
        else:
            raise Exception("Message could not be deleted")

    except Exception as e:
        response.status = 400
        return "Error: " + str(e)


run (host='127.0.0.1', port=9000, debug=True, reloader=True)