# modules/Tools/Comms/Voip/modules/send_sms_twilio.py

import os
from twilio.rest import Client
from dotenv import load_dotenv
from modules.logging.logger import setup_logger

logger = setup_logger('send_sms_twilio.py')

load_dotenv()

auth_token = os.getenv("TWILIO_AUTH_TOKEN")
account_sid = os.getenv("TWILIO_ACCOUNT_SID")
phone_number = os.getenv("phone_number")

if auth_token is None or account_sid is None or phone_number is None:
    logger.error("Twilio credentials not found. SMS features will be disabled.")
    TWILIO_ENABLED = False
else:
    TWILIO_ENABLED = True
    client = Client(account_sid, auth_token)

def send_sms(to, body, media_url=None):
    if not TWILIO_ENABLED:
        logger.error("Twilio SMS is disabled due to missing credentials.")
        return None

    try:
        logger.info(f"Sending SMS/MMS to {to}")
        message_data = {
            'body': body,
            'from_': phone_number,
            'to': to
        }
        if media_url:
            message_data['media_url'] = media_url

        message = client.messages.create(**message_data)
        logger.info(f"SMS/MMS sent successfully. Message SID: {message.sid}")
        return message.sid
    except Exception as e:
        logger.error(f"Failed to send SMS/MMS to {to}: {e}")
        raise