# modules/Tools/Comms/Voip/modules/send_sms_twilio.py

import os
from twilio.rest import Client
from dotenv import load_dotenv
from modules.logging.logger import setup_logger

# Setup logger
logger = setup_logger('send_sms_twilio.py')

# Load environment variables
load_dotenv()

# Retrieve Twilio credentials from environment variables
auth_token = os.getenv("auth_token")
if auth_token is None:
    logger.error("The Twilio Auth Token not found. Please set the auth_token environment variable.")
    raise ValueError("The Twilio Auth Token not found. Please set the auth_token environment variable.")

account_sid = os.getenv("account_sid")
if account_sid is None:
    logger.error("The Twilio Account SID not found. Please set the account_sid environment variable.")
    raise ValueError("The Twilio Account SID not found. Please set the account_sid environment variable.")

phone_number = os.getenv("phone_number")
if phone_number is None:
    logger.error("The Twilio phone number was not found. Please set the phone_number environment variable.")
    raise ValueError("The Twilio phone number was not found. Please set the phone_number environment variable.")

# Initialize Twilio client
client = Client(account_sid, auth_token)

def send_sms(to, body):
    try:
        logger.info(f"Sending SMS to {to}")
        message = client.messages.create(
            body=body,
            from_=phone_number,
            to=to
        )
        logger.info(f"SMS sent successfully. Message SID: {message.sid}")
        return message.sid
    except Exception as e:
        logger.error(f"Failed to send SMS to {to}: {e}")
        raise