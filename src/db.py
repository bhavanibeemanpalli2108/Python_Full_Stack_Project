# db.py
import os
from supabase import create_client
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_KEY")

supabase = create_client(url, key)

# ---------------- USERS ----------------
def create_user(name: str, email: str, phone: str = None):
    data = {"name": name, 
            "email": email, 
            "phone": phone}
    response = supabase.table("users").insert(data).execute()
    return response.data

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
    data = {"name": name, 
            "description": description}
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
    data = {"reminder_id": reminder_id, 
            "status": status, 
            "response": response_text}
    response = supabase.table("logs").insert(data).execute()
    return response.data

def get_logs(reminder_id: str = None):
    query = supabase.table("logs").select("*")
    if reminder_id:
        query = query.eq("reminder_id", reminder_id)
    response = query.execute()
    return response.data

def delete_log(log_id: str):
    response = supabase.table("logs").delete().eq("id", log_id).execute()
    return response.data

# #--------run------
# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run("db:app", host="0.0.0.0",port=8000, reload=True)
#     # print("Supabase client initialized.")
#     # print("Users:", get_users())
#     # print("Channels:", get_channels())
#     # print("Reminders:", get_reminders())
#     # print("Logs:", get_logs())
