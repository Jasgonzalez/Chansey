# services/twilio_service.py

from twilio.rest import Client

def send_sms(med_name, reminder_time, am_pm, to_phone):
    account_sid = 'AC18fcb7f60606f09cd5cc54697dd946d8'  # Replace with actual SID
    auth_token = 'ee27f9237b85236f09b7eabb24101197'    # Replace with actual Auth Token
    client = Client(account_sid, auth_token)
    
    message = client.messages.create(
        body=f"Reminder: Take your medication '{med_name}' at {reminder_time} {am_pm}.",
        from_='+18885643524',
        to=to_phone
    )
    return message.sid





  