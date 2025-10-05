# db.py
import os
from supabase import create_client, Client
from dotenv import load_dotenv
import bcrypt
from datetime import datetime, timezone
import pytz

# Load environment variables
load_dotenv()
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# ---------------- USERS ----------------
def create_user(name: str, email: str, phone: str = None, password: str = None):
    if password is None:
        raise ValueError("Password is required for creating a user")
    hashed_pw = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    data = {"name": name, "email": email, "phone": phone, "password": hashed_pw}
    response = supabase.table("users").insert(data).execute()
    return response.data

def get_user_by_email(email, supabase):
    response = supabase.table("users").select("*").eq("email", email).execute()
    if response.data:
        return response.data[0]
    return None


def get_users():
    response = supabase.table("users").select("*").execute()
    return response.data

def update_user(user_id: str, updates: dict):
    response = supabase.table("users").update(updates).eq("id", user_id).execute()
    return response.data

def delete_user(user_id: str):
    response = supabase.table("users").delete().eq("id", user_id).execute()
    return response.data

# ---------------- CHANNELS ----------------
def create_channel(name: str, description: str = None):
    data = {"name": name, "description": description}
    response = supabase.table("channels").insert(data).execute()
    return response.data

def get_channels():
    response = supabase.table("channels").select("*").execute()
    return response.data

def update_channel(channel_id: int, updates: dict):
    response = supabase.table("channels").update(updates).eq("id", channel_id).execute()
    return response.data

def delete_channel(channel_id: int):
    response = supabase.table("channels").delete().eq("id", channel_id).execute()
    return response.data

# ---------------- REMINDERS ----------------
def create_reminder(user_id: str, recipient_name: str, recipient: str, message: str, channel_id: int, event_time: str):
    data = {
        "user_id": user_id,
        "recipient_name": recipient_name,
        "recipient": recipient,
        "message": message,
        "channel_id": channel_id,
        "event_time": event_time,
        "status": "pending"
    }
    response = supabase.table("reminders").insert(data).execute()
    return response.data

def get_reminders(user_id: str = None):
    query = supabase.table("reminders").select("*")
    if user_id:
        query = query.eq("user_id", user_id)
    response = query.execute()
    return response.data

def update_reminder(reminder_id: str, updates: dict):
    response = supabase.table("reminders").update(updates).eq("id", reminder_id).execute()
    return response.data

def delete_reminder(reminder_id: str):
    response = supabase.table("reminders").delete().eq("id", reminder_id).execute()
    return response.data

# ---------------- LOGS ----------------
def create_log(reminder_id: str, status: str, response_text: str = None):
    data = {"reminder_id": reminder_id, "status": status, "response": response_text}
    response = supabase.table("logs").insert(data).execute()
    return response.data

def get_logs(reminder_id: str = None):
    query = supabase.table("logs").select("*")
    if reminder_id:
        query = query.eq("reminder_id", reminder_id)
    response = query.execute()
    return response.data

def update_log(log_id: str, updates: dict):
    response = supabase.table("logs").update(updates).eq("id", log_id).execute()
    return response.data

def delete_log(log_id: str):
    response = supabase.table("logs").delete().eq("id", log_id).execute()
    return response.data

# ---------------- REMINDER HELPERS ----------------
# def get_due_reminders():
#     """
#     Fetch reminders where status='pending' and event_time <= now (UTC)
#     """
#     response = supabase.table("reminders").select("*").eq("status", "pending").execute()
#     reminders = response.data if response.data else []

#     now_utc = datetime.now(timezone.utc)
#     due_reminders = []

#     for r in reminders:
#         event_dt = datetime.fromisoformat(r['event_time'])
#         if event_dt.tzinfo is None:
#             event_dt = event_dt.replace(tzinfo=timezone.utc)
#         if event_dt <= now_utc:
#             due_reminders.append(r)

#     return due_reminders


# db.py
from datetime import datetime, timezone
# ... other code ...

# ---------------- REMINDER HELPERS ----------------
def get_due_reminders():
    """
    Fetch reminders where status='pending' AND event_time <= now (UTC).
    Uses efficient Supabase filtering.
    """
    # 1. Get current UTC time and truncate microseconds (matching the time saved by app.py)
    now_utc_dt = datetime.now(timezone.utc).replace(microsecond=0)
    
    # 2. Format the truncated time for the Supabase query.
    now_utc_iso = now_utc_dt.isoformat()
    
    # 3. Use the Supabase query to filter: status='pending' AND event_time <= now
    response = (
        supabase.table("reminders")
        .select("*")
        .eq("status", "pending")           
        .lte("event_time", now_utc_iso)    # The comparison is done here by the DB
        .execute()
    )
    
    return response.data if response.data else []

def update_reminder_status(reminder_id: str, status: str):
    supabase.table("reminders").update({"status": status}).eq("id", reminder_id).execute()
