 # modules/Tools/Comms/Voip/modules/voice_call_twilio.py

import os
from twilio.rest import Client
from dotenv import load_dotenv
from modules.logging.logger import setup_logger

logger = setup_logger('voice_call_twilio.py')

load_dotenv()

auth_token = os.getenv("TWILIO_AUTH_TOKEN")
account_sid = os.getenv("TWILIO_ACCOUNT_SID")
phone_number = os.getenv("phone_number")
voice_twiml_bin_sid = os.getenv("voice_twiml_bin_sid")

if auth_token is None or account_sid is None or phone_number is None or voice_twiml_bin_sid is None:
    logger.error("Twilio credentials not found. Voice call features will be disabled.")
    TWILIO_ENABLED = False
else:
    TWILIO_ENABLED = True
    client = Client(account_sid, auth_token)

def make_call(to):
    if not TWILIO_ENABLED:
        logger.error("Twilio voice call is disabled due to missing credentials.")
        return None

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
    if not TWILIO_ENABLED:
        logger.error("Twilio voice call is disabled due to missing credentials.")
        return None

    try:
        logger.info(f"Ending call with SID: {call_sid}")
        call = client.calls(call_sid).update(status="completed")
        logger.info(f"Call ended successfully. Call SID: {call.sid}")
    except Exception as e:
        logger.error(f"Failed to end call with SID {call_sid}: {e}")
        raise