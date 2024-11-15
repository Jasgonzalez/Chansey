from dotenv import load_dotenv
import os
from twilio.rest import Client

# Load environment variables from .env
load_dotenv()

def send_sms(med_name, reminder_time, am_pm, to_phone):
    account_sid = os.getenv('TWILIO_ACCOUNT_SID')  # Get SID from .env
    auth_token = os.getenv('TWILIO_AUTH_TOKEN')    # Get Token from .env

    if not account_sid or not auth_token:
        raise ValueError("Twilio account SID and auth token must be set.")

    client = Client(account_sid, auth_token)
    
    message = client.messages.create(
        body=f"Reminder: Take your medication '{med_name}' at {reminder_time} {am_pm}.",
        from_='+18885643524',  # Replace with your Twilio phone number
        to=to_phone
    )
    return message.sid




  