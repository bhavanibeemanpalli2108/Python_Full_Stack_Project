# src/logic.py
import datetime, schedule, time
from datetime import timezone
#from src.db import DatabaseManager  # relative import
from src import db                 # relative import
# from twilio.rest import Client as TwilioClient
import smtplib
from email.mime.text import MIMEText
import os
from dotenv import load_dotenv
load_dotenv()
import datetime
from src.db import get_due_reminders, update_reminder_status
from src.notifiers.email import send_email
from src.notifiers.sms import send_sms
from src.notifiers.whatsapp import send_whatsapp
from src.db import create_reminder, get_channels, create_log

from datetime import datetime, timezone
from src.db import create_reminder, get_due_reminders, update_reminder_status, create_log
# src/logic.py (update process_due_reminders)
from datetime import datetime
from src.db import get_due_reminders, update_reminder_status, get_channels, create_log
from src.messaging import send_message
from datetime import timezone
import pytz
from dateutil import parser

def process_due_reminders():
    from src.messaging import send_message

    # fetch channels and make a mapping: id -> channel_type
    channels_list = get_channels()  # list of dicts
    channels = {c['id']: c['name'].lower() for c in channels_list}

    due_reminders = get_due_reminders()
    for r in due_reminders:
        try:
            channel_type = channels.get(r['channel_id'])
            if not channel_type:
                raise ValueError(f"Unknown channel_id {r['channel_id']}")

            recipient = r['recipient']
            message = f"Hi {r['recipient_name']},\n{r['message']}"

            send_message(recipient, message, channel=channel_type)

            update_reminder_status(r['id'], "sent")
            create_log(r['id'], "sent", f"Sent via {channel_type}")
            print(f"✅ Reminder sent to {recipient} via {channel_type}")

        except Exception as e:  
            update_reminder_status(r['id'], "failed")
            create_log(r['id'], "failed", str(e))
            print(f"❌ Failed reminder {r['id']}: {str(e)}")
        
            
# # process due reminders    
    
#     def process_due_reminders():
#         """
#         Fetch due reminders and send them via the appropriate channel.
#         """
#         from src.messaging import send_message  # your existing function
#         channels = ... # get channels mapping from DB

#         due_reminders = get_due_reminders()
#         for r in due_reminders:
#             try:
#                 channel_type = channels.get(r['channel_id'])
#                 recipient = r['recipient']
#                 message = f"Hi {r['recipient_name']},\n{r['message']}"

#                 send_message(recipient, message, channel=channel_type)

#                 update_reminder_status(r['id'], "sent")
#                 create_log(r['id'], "sent", f"Sent via {channel_type}")
#                 print(f"✅ Reminder sent to {recipient} via {channel_type}")

#             except Exception as e:
#                 update_reminder_status(r['id'], "failed")
#                 create_log(r['id'], "failed", str(e))
#                 print(f"❌ Failed reminder {r['id']}: {str(e)}")
# Schedule the job every minute

# --- WhatsApp/SMS via Twilio ---
# def send_sms_whatsapp(to, message, channel="sms"):
#     account_sid = os.getenv("TWILIO_SID")
#     auth_token = os.getenv("TWILIO_AUTH")
#     from_whatsapp = f"whatsapp:{os.getenv('TWILIO_WHATSAPP')}"
#     from_sms = os.getenv("TWILIO_PHONE")

#     client = TwilioClient(account_sid, auth_token)

#     sender = from_whatsapp if channel == "whatsapp" else from_sms
#     msg = client.messages.create(body=message, from_=sender, to=to)
#     return msg.sid

# --- Email ---
# def send_email(to, subject, body):
#     user = os.getenv("EMAIL_USER")
#     password = os.getenv("EMAIL_PASS")
#     msg = MIMEText(body)
#     msg["Subject"] = subject
#     msg["From"] = user
#     msg["To"] = to

#     with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
#         server.login(user, password)
#         server.sendmail(user, [to], msg.as_string())

class UserManager:
    """Acts as a bridge between frontend(Streamlit/FASTAPI) and database."""

    def __init__(self):
        # no DatabaseManager, we use db functions directly
        import src.db as db
        self.db = db

# ---------------- USER OPERATIONS ----------------
    # add user
    def add_user(self, name: str, email: str, phone: str = None):
        """Add a new user to the system.
        Returns a success message or error based on the activity."""
        if not name or not email:
            return{"Sucsess": False, "Message": "Name and email are required."}   
        
        # call db function to create user
        result= self.db.create_user(name, email, phone)

        # check if user creation was successful

        if result.get("Success"):
            return {"Success": True, "Message": "User created successfully."}
        else:
            return {"Success": False, "Message": f"Error:{result.get('Error')}"}

    # -------Retrieve------- 
    def list_users(self):
        """Get all the users from the database."""
        return self.db.get_users()  
    
    # # --------Update-------
    # def modify_user(self, user_id: str, updates: dict):        
    #     """Update user details."""
    #     result= self.db.update_user(user_id, updates)
    #     if result.self.get("Success"):
    #         return {"Success": True, "Message": "User updated successfully."}

    # ----update complete------
    def complete_user_update(self, user_id: str, updates: dict):
        """Finalize user update."""
        result = self.db.update_user(user_id, updates)
        if result.get("Success"):
            return {"Success": True, "Message": "User update finalized successfully."}
        else:
            return {"Success": False, "Message": f"Error: {result.get('Error')}"}

    #------update pending------
    def pending_user_update(self, user_id: str, updates: dict):
        """Mark user update as pending."""
        result = self.db.update_user(user_id, updates)
        if result.get("Success"):
            return {"Success": True, "Message": "User update marked as pending."}
        else:
            return {"Success": False, "Message": f"Error: {result.get('Error')}"}

    # -------Delete-------
    def remove_user(self, user_id: str):
        """Delete a user from the database."""
        result= self.db.delete_user(user_id)
        if result.get("Success"):
            return {"Success": True, "Message": "User deleted successfully."}
        else:
            return {"Success": False, "Message": f"Error: {result.get('Error')}"}
        
# ---------------- CHANNEL OPERATIONS ----------------
class ChannelManager:
    """Handles channel-related operations."""
    # add channel

    def __init__(self):
        # no DatabaseManager, we use db functions directly
        import src.db as db
        self.db = db


    def add_channel(self, name: str, description: str = None):
        """Add a new channel to the system.
        Returns a success message or error based on the activity."""
        if not name:
            return{"Success": False, "Message": "Channel name is required."}   
        
        # call db function to create channel
        result= self.db.create_channel(name, description)

        # check if channel creation was successful

        if result.get("Success"):
            return {"Success": True, "Message": "Channel created successfully."}
        else:
            return {"Success": False, "Message": f"Error:{result.get('Error')}"}
        
    # -------Retrieve-------
    def list_channels(self):
        """Get all the channels from the database."""
        return self.db.get_channels()

    # ----update complete------
    def complete_channel_update(self, channel_id: int, updates: dict):
        """Finalize channel update."""
        result = self.db.update_channel(channel_id, updates)
        if result.get("Success"):
            return {"Success": True, "Message": "Channel update finalized successfully."}
        else:
            return {"Success": False, "Message": f"Error: {result.get('Error')}"}

    # -----update pending------
    def pending_channel_update(self, channel_id: int, updates: dict):
        """Mark channel update as pending."""
        result = self.db.update_channel(channel_id, updates)
        if result.get("Success"):
            return {"Success": True, "Message": "Channel update marked as pending."}
        else:
            return {"Success": False, "Message": f"Error: {result.get('Error')}"}

    # --------Update-------    
    def modify_channel(self, channel_id: int, updates: dict):        
        """Update channel details."""
        result= self.db.update_channel(channel_id, updates)
        if result.get("Success"):
            return {"Success": True, "Message": "Channel updated successfully."}
        else:
            return {"Success": False, "Message": f"Error: {result.get('Error')}"}

    # -------Delete-------
    def remove_channel(self, channel_id: int):
        """Delete a channel from the database."""
        result= self.db.delete_channel(channel_id)
        if result.get("Success"):
            return {"Success": True, "Message": "Channel deleted successfully."}
        else:
            return {"Success": False, "Message": f"Error: {result.get('Error')}"}

# ---------------- REMINDER OPERATIONS ----------------
class ReminderManager:
    """Handles reminder-related operations."""

    def __init__(self):
        # no DatabaseManager, we use db functions directly
        import src.db as db
        self.db = db


    # add reminder
    # def add_reminder(self, user_id, recipient_name, recipient, message, channel_id, event_time):
    #     result = create_reminder(user_id, recipient_name, recipient, message, channel_id, event_time)
    #     # return result


    #     # Supabase usually returns a list of inserted rows
    #     if isinstance(result, list) and len(result) > 0:
    #         return {"Success": True, "data": result[0]}
    #     elif isinstance(result, dict) and result.get("Success"):
    #         return result
    #     else:
    #         return {"Success": False, "Error": "Failed to insert reminder"}


    from datetime import datetime, timezone
    from dateutil import parser
    import pytz

    def add_reminder(self, user_id, recipient_name, recipient, message, channel_id, event_time):
        """
        Adds a reminder to the database.
        Assumes event_time is in IST (local time) and converts it to UTC for DB.
        """
        try:
            # Parse event_time (string → datetime)
            if isinstance(event_time, str):
                try:
                    event_dt = parser.parse(event_time)
                except Exception:
                    raise ValueError(f"Invalid datetime format: {event_time}")
            elif isinstance(event_time, datetime):
                event_dt = event_time
            else:
                raise TypeError("event_time must be a string or datetime")

            # Step 1: Attach IST timezone if missing
            ist = pytz.timezone("Asia/Kolkata")
            if event_dt.tzinfo is None:
                event_dt = ist.localize(event_dt)

            # Step 2: Convert to UTC for storage
            event_time_utc = event_dt.astimezone(pytz.utc).isoformat()

            # 🧠 Debug logs
            print("🕒 Local input:", event_time)
            print("IST localized:", event_dt)
            print("UTC stored:", event_time_utc)

            # Step 3: Store in DB
            result = create_reminder(user_id, recipient_name, recipient, message, channel_id, event_time_utc)

            if result:
                return {"Success": True, "Message": "Reminder created successfully!", "Data": result[0]}
            else:
                return {"Success": False, "Message": "Failed to insert reminder."}

        except Exception as e:
            return {"Success": False, "Message": f"Error: {str(e)}"}



    

    # -------Retrieve-------
    def list_reminders(self, user_id: str = None):
        """Get all the reminders from the database. Optionally filter by user_id."""
        return self.db.get_reminders(user_id)
    
    # ----update complete------
    def complete_reminder_update(self, reminder_id: str, updates: dict):
        """Finalize reminder update."""
        result = self.db.update_reminder(reminder_id, updates)
        if result.get("Success"):
            return {"Success": True, "Message": "Reminder update finalized successfully."}
        else:
            return {"Success": False, "Message": f"Error: {result.get('Error')}"}

    # -----update pending------
    def pending_reminder_update(self, reminder_id: str, updates: dict):
        """Mark reminder update as pending."""
        result = self.db.update_reminder(reminder_id, updates)
        if result.get("Success"):
            return {"Success": True, "Message": "Reminder update marked as pending."}
        else:
            return {"Success": False, "Message": f"Error: {result.get('Error')}"}        

    # --------Update-------
    def modify_reminder(self, reminder_id: str, updates: dict):
        """Update reminder details."""
        result= self.db.update_reminder(reminder_id, updates)
        if result.get("Success"):
            return {"Success": True, "Message": "Reminder updated successfully."}
        else:
            return {"Success": False, "Message": f"Error: {result.get('Error')}"}
        
    # -------Delete-------

    def remove_reminder(self, reminder_id: str):
        """Delete a reminder from the database."""
        result= self.db.delete_reminder(reminder_id)
        if result.get("Success"):
            return {"Success": True, "Message": "Reminder deleted successfully."}
        else:
            return {"Success": False, "Message": f"Error: {result.get('Error')}"}
    
            

# ---------------- LOG OPERATIONS ----------------
class LogManager:
    """Handles log-related operations."""

    def __init__(self):
        # no DatabaseManager, we use db functions directly
        import src.db as db
        self.db = db

    # add log

    def log_reminder_activity(self, reminder_id: str, status: str, response_text: str = None):
        """Log activity related to a reminder."""
        result = self.db.create_log(reminder_id, status, response_text)
        if result.get("Success"):
            return {"Success": True, "Message": "Log entry created successfully."}
        else:
            return {"Success": False, "Message": f"Error: {result.get('Error')}"}
        

    # -------Retrieve-------

    def list_logs(self, reminder_id: str = None):
        """Get all the logs from the database. Optionally filter by reminder_id."""
        return self.db.get_logs(reminder_id)
    
    # --------Update completion-------

    def modify_log(self, log_id: str, updates: dict):
        """Update log details."""
        result= self.db.update_log(log_id, updates)
        if result.get("Success"):
            return {"Success": True, "Message": "Log updated successfully."}
        else:
            return {"Success": False, "Message": f"Error: {result.get('Error')}"}
        
    # -------Delete-------

    def remove_log(self, log_id: str):
        """Delete a log from the database."""
        result= self.db.delete_log(log_id)
        if result.get("Success"):
            return {"Success": True, "Message": "Log deleted successfully."}
        else:
            return {"Success": False, "Message": f"Error: {result.get('Error')}"}
        
        
