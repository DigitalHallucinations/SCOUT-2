# modules/Tools/Comms/Voip/modules/Twilio_verify.py

import os
from twilio.rest import Client
from dotenv import load_dotenv
from modules.logging.logger import setup_logger

logger = setup_logger('Twilio_verify.py')

load_dotenv()

auth_token = os.getenv("TWILIO_AUTH_TOKEN")
account_sid = os.getenv("TWILIO_ACCOUNT_SID")
verify_service_sid = os.getenv("verify_service_sid")

if auth_token is None or account_sid is None or verify_service_sid is None:
    logger.error("Twilio credentials not found. Verification features will be disabled.")
    TWILIO_ENABLED = False
else:
    TWILIO_ENABLED = True
    client = Client(account_sid, auth_token)

class TwilioVerify:
    def __init__(self, account_sid, auth_token, verify_service_sid):
        if not TWILIO_ENABLED:
            logger.error("Twilio verification is disabled due to missing credentials.")
            return

        self.client = Client(account_sid, auth_token)
        self.verify_service_sid = verify_service_sid

    def send_verification_request(self, phone_number):
        if not TWILIO_ENABLED:
            logger.error("Twilio verification is disabled due to missing credentials.")
            return None

        try:
            verification = self.client.verify \
                .services(self.verify_service_sid) \
                .verifications \
                .create(to=phone_number, channel='sms')

            logger.info(f"Verification request sent to {phone_number}")
            return verification.sid
        except Exception as e:
            logger.error(f"Failed to send verification request: {e}")
            return None

    def check_verification_status(self, phone_number, code):
        if not TWILIO_ENABLED:
            logger.error("Twilio verification is disabled due to missing credentials.")
            return False

        try:
            verification_check = self.client.verify \
                .services(self.verify_service_sid) \
                .verification_checks \
                .create(to=phone_number, code=code)

            if verification_check.status == 'approved':
                logger.info(f"Verification successful for {phone_number}")
                return True
            else:
                logger.warning(f"Verification failed for {phone_number}")
                return False
        except Exception as e:
            logger.error(f"Failed to check verification status: {e}")
            return False