import sys
from twilio.rest import Client

def send_sms(to_number, message):
    # Replace these with your actual Twilio credentials
    account_sid = 'YOUR_TWILIO_SID'
    auth_token = 'YOUR_TWILIO_AUTH_TOKEN'
    from_number = 'YOUR_TWILIO_PHONE_NUMBER'

    client = Client(account_sid, auth_token)

    try:
        message = client.messages.create(
            body=message,
            from_=from_number,
            to=to_number
        )
        print(f"✅ Message sent to {to_number}. SID: {message.sid}")
    except Exception as e:
        print(f"❌ Failed to send message: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python sms_call.py <phone_number> <message>")
        sys.exit(1)

    phone_number = sys.argv[1]
    text_message = sys.argv[2]

    send_sms(phone_number, text_message)
