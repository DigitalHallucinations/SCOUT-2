# modules/Tools/Comms/Voip/modules/twilio_support.py

import os
import requests
from dotenv import load_dotenv
from modules.logging.logger import setup_logger

logger = setup_logger('contact_twilio_support.py')

load_dotenv()

auth_token = os.getenv("TWILIO_AUTH_TOKEN")
account_sid = os.getenv("TWILIO_ACCOUNT_SID")

if auth_token is None or account_sid is None:
    logger.error("Twilio credentials not found. Twilio support features will be disabled.")
    TWILIO_ENABLED = False
else:
    TWILIO_ENABLED = True

def contact_twilio_support(error_code, debug_event_sid, account_sid, call_sid, timestamp, description, contact_info):
    if not TWILIO_ENABLED:
        logger.error("Twilio support is disabled due to missing credentials.")
        return None

    try:
        logger.info("Contacting Twilio Support with error details.")
        url = "https://api.twilio.com/2010-04-01/Accounts/{account_sid}/Messages.json".format(account_sid=account_sid)
        data = {
            "ErrorCode": error_code,
            "DebugEventSid": debug_event_sid,
            "AccountSid": account_sid,
            "CallSid": call_sid,
            "Timestamp": timestamp,
            "Description": description,
            "ContactInfo": contact_info
        }
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {auth_token}"
        }
        response = requests.post(url, json=data, headers=headers)
        response.raise_for_status()
        logger.info(f"Support contacted successfully. Response: {response.json()}")
        return response.json()
    except requests.HTTPError as http_err:
        logger.error(f"HTTP error occurred: {http_err}")
        raise
    except Exception as e:
        logger.error(f"An error occurred: {e}")
        raise

# Example usage
if __name__ == "__main__":
    if TWILIO_ENABLED:
        error_code = "13225"
        debug_event_sid = "NO8336bec59aaa9c5e3fa319546fac0a91"
        call_sid = "CAfd2760a84e1b3d13ca339c5bd69bd891"
        timestamp = "2024-05-23 03:15:25"
        description = "The destination number is blocked by Twilio. If you have a legitimate need to call this number, please reach out to Twilio Support."
        contact_info = "jeremyshws@gmail.com"
        contact_twilio_support(error_code, debug_event_sid, account_sid, call_sid, timestamp, description, contact_info)
    else:
        logger.error("Twilio support is disabled. Example usage cannot proceed.")