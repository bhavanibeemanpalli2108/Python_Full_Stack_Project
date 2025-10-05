from twilio.rest import Client
import os
from dotenv import load_dotenv

load_dotenv()

TWILIO_SID = os.getenv("TWILIO_SID")
TWILIO_AUTH = os.getenv("TWILIO_AUTH")
TWILIO_WHATSAPP = os.getenv("TWILIO_WHATSAPP")

client = Client(TWILIO_SID, TWILIO_AUTH)

def send_whatsapp(to, message):
    client.messages.create(
        body=message,
        from_=f"whatsapp:{TWILIO_WHATSAPP}",
        to=f"whatsapp:{to}"
    )
