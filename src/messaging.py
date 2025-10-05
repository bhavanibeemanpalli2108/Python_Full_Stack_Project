import smtplib
from email.mime.text import MIMEText
import os
from dotenv import load_dotenv
load_dotenv()

EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASS = os.getenv("EMAIL_PASS")

from src.notifiers.email import send_email


def send_message(recipient, message, channel="email"):
    if channel == "email":
        return send_email(recipient, "Reminder", message)
