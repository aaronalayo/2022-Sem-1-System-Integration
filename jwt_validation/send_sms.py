import requests
from get_name import name
from get_last_name import last_name
from get_email import email
from get_phone import phone
from get_api_key import user_api_key


url="https://fatsms.com/send-sms"
message = f"Hi {name} {last_name}, your email is {email}"
payload ={"to_phone": phone, "message" : message, "api_key" : user_api_key}


r = requests.post(url, data= payload)

print("response status code :", r.status_code)