# modules/Tools/Comms/Voip/modules/send_sms_twilio.py

import os
from twilio.rest import Client
from dotenv import load_dotenv

load_dotenv()

auth_token = os.getenv("auth_token")
if auth_token is None:
    raise ValueError("The Twilio Auth Token not found. Please set the auth_token environment variable.")

account_sid = os.getenv("account_sid")
if account_sid is None:
    raise ValueError("The Twilio Account SID not found. Please set the account_sid environment variable.")

phone_number = os.getenv("phone_number")
if phone_number is None:
    raise ValueError("The Twilio phone number was not found. Please set the phone_number environment variable.")

client = Client(account_sid, auth_token)

def send_sms(to, body):
    message = client.messages.create(
        body=body,
        from_=phone_number,
        to=to
    )
    print(message.sid)