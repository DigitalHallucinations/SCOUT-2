 # modules/Tools/Comms/Voip/modules/voice_call_twilio.py

import os
from twilio.rest import Client
from dotenv import load_dotenv
from modules.logging.logger import setup_logger

logger = setup_logger('voice_call_twilio.py')

load_dotenv()

auth_token = os.getenv("TWILIO_AUTH_TOKEN")
if auth_token is None:
    logger.error("The Twilio Auth Token not found. Please set the auth_token environment variable.")
    raise ValueError("The Twilio Auth Token not found. Please set the auth_token environment variable.")

account_sid = os.getenv("TWILIO_ACCOUNT_SID")
if account_sid is None:
    logger.error("The Twilio Account SID not found. Please set the account_sid environment variable.")
    raise ValueError("The Twilio Account SID not found. Please set the account_sid environment variable.")
 
phone_number = os.getenv("phone_number")
if phone_number is None:
    logger.error("The Twilio phone number was not found. Please set the phone_number environment variable.")
    raise ValueError("The Twilio phone number was not found. Please set the phone_number environment variable.")

voice_twiml_bin_sid = os.getenv("voice_twiml_bin_sid")
if voice_twiml_bin_sid is None:
    logger.error("The Twilio voice_twiml_bin_sid was not found. Please set the voice_twiml_bin_sid environment variable.")
    raise ValueError("The Twilio voice_twiml_bin_sid was not found. Please set the voice_twiml_bin_sid environment variable.")

# Initialize Twilio client
client = Client(account_sid, auth_token)

def make_call(to):
    try:
        logger.info(f"Making call to {to}")
        voice_url = f"https://handler.twilio.com/twiml/{voice_twiml_bin_sid}?PhoneNumber={to}"
        call = client.calls.create(
            to=to,
            from_=phone_number,
            url=voice_url
        )
        logger.info(f"Call initiated successfully. Call SID: {call.sid}")
        return call.sid
    except Exception as e:
        logger.error(f"Failed to make call to {to}: {e}")
        raise

def end_call(call_sid):
    try:
        logger.info(f"Ending call with SID: {call_sid}")
        call = client.calls(call_sid).update(status="completed")
        logger.info(f"Call ended successfully. Call SID: {call.sid}")
    except Exception as e:
        logger.error(f"Failed to end call with SID {call_sid}: {e}")
        raise