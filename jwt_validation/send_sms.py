import requests
from get_name import name
from get_last_name import last_name
from get_email import email
from get_phone import phone
from get_api_key import user_api_key

url="https://fatsms.com/send-sms"

def send_sms(code):  
    message = f"Hi {name} {last_name}, your code is {code}"
    payload ={"to_phone": phone, "message" : message, "api_key" : user_api_key}
    r = requests.post(url, data= payload, headers={'Connection':'close'})
    print("response status code :", r.content)
    return r.status_code



