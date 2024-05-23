# modules/Tools/Comms/Voip/modules/Twilio_verify.py

import os
from twilio.rest import Client
from dotenv import load_dotenv
from modules.logging.logger import setup_logger

# Setup logger
logger = setup_logger('Twilio_verify.py')

# Load environment variables
load_dotenv()

# Retrieve Twilio credentials from environment variables
auth_token = os.getenv("TWILIO_AUTH_TOKEN")
if auth_token is None:
    logger.error("The Twilio Auth Token not found. Please set the auth_token environment variable.")
    raise ValueError("The Twilio Auth Token not found. Please set the auth_token environment variable.")

account_sid = os.getenv("TWILIO_ACCOUNT_SID")
if account_sid is None:
    logger.error("The Twilio Account SID not found. Please set the account_sid environment variable.")
    raise ValueError("The Twilio Account SID not found. Please set the account_sid environment variable.")

verify_service_sid = os.getenv("verify_service_sid")
if verify_service_sid is None:
    logger.error("The Twilio Verify Service SID not found. Please set the verify_service_sid environment variable.")
    raise ValueError("The Twilio Verify Service SID not found. Please set the verify_service_sid environment variable.")

# Initialize Twilio client
client = Client(account_sid, auth_token)

class TwilioVerify:
    def __init__(self, account_sid, auth_token, verify_service_sid):
        self.client = Client(account_sid, auth_token)
        self.verify_service_sid = verify_service_sid

    def send_verification_request(self, phone_number):
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