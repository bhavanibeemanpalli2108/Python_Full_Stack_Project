# api/main.py
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import sys, os

# Add src path
sys.path.append(os.path.join(os.path.dirname(__file__), "src"))

# Import Managers
from logic import UserManager, ChannelManager, ReminderManager, LogManager

# ------------------- APP SETUP -------------------
app = FastAPI(title="User Management API", version="1.0")

# Allow frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # adjust in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# ------------------- MANAGER INSTANCES -------------------
user_manager = UserManager()
channel_manager = ChannelManager()
reminder_manager = ReminderManager()
log_manager = LogManager()

# ------------------- DATA MODELS -------------------
class UserCreate(BaseModel):
    name: str
    email: str
    phone: str | None = None

class ChannelCreate(BaseModel):
    name: str
    description: str | None = None

class ReminderCreate(BaseModel):
    user_id: str
    recipient_name: str
    recipient: str
    message: str
    channel_id: int
    event_time: str  # ISO datetime

class LogCreate(BaseModel):
    reminder_id: str
    status: str
    response_text: str | None = None

# ------------------- ROOT -------------------
@app.get("/")
def home():
    return {"message": "User Management API is running"}

# ------------------- USERS -------------------
@app.get("/users")
def get_all_users():
    return user_manager.list_users()

@app.post("/users")
def create_user(user: UserCreate):
    result = user_manager.add_user(user.name, user.email, user.phone)
    if not result.get("Success"):
        raise HTTPException(status_code=400, detail=result.get("Message"))
    return result

@app.put("/users/{user_id}")
def update_user(user_id: str, user: UserCreate):
    updates = user.dict(exclude_unset=True)
    result = user_manager.complete_user_update(user_id, updates)
    if not result.get("Success"):
        raise HTTPException(status_code=400, detail=result.get("Message"))
    return result

@app.delete("/users/{user_id}")
def delete_user(user_id: str):
    result = user_manager.remove_user(user_id)
    if not result.get("Success"):
        raise HTTPException(status_code=400, detail=result.get("Message"))
    return result

# ------------------- CHANNELS -------------------
@app.get("/channels")
def get_channels():
    return channel_manager.list_channels()

@app.post("/channels")
def create_channel(channel: ChannelCreate):
    result = channel_manager.add_channel(channel.name, channel.description)
    if not result.get("Success"):
        raise HTTPException(status_code=400, detail=result.get("Message"))
    return result

@app.put("/channels/{channel_id}")
def update_channel(channel_id: int, channel: ChannelCreate):
    updates = channel.dict(exclude_unset=True)
    result = channel_manager.modify_channel(channel_id, updates)
    if not result.get("Success"):
        raise HTTPException(status_code=400, detail=result.get("Message"))
    return result

@app.delete("/channels/{channel_id}")
def delete_channel(channel_id: int):
    result = channel_manager.remove_channel(channel_id)
    if not result.get("Success"):
        raise HTTPException(status_code=400, detail=result.get("Message"))
    return result

# ------------------- REMINDERS -------------------
@app.get("/reminders")
def get_reminders(user_id: str = None):
    return reminder_manager.list_reminders(user_id)

@app.post("/reminders")
def create_reminder(reminder: ReminderCreate):
    result = reminder_manager.add_reminder(
        reminder.user_id,
        reminder.recipient_name,
        reminder.recipient,
        reminder.message,
        reminder.channel_id,
        reminder.event_time
    )
    if not result.get("Success"):
        raise HTTPException(status_code=400, detail=result.get("Message"))
    return result

@app.put("/reminders/{reminder_id}")
def update_reminder(reminder_id: str, reminder: ReminderCreate):
    updates = reminder.dict(exclude_unset=True)
    result = reminder_manager.modify_reminder(reminder_id, updates)
    if not result.get("Success"):
        raise HTTPException(status_code=400, detail=result.get("Message"))
    return result

@app.delete("/reminders/{reminder_id}")
def delete_reminder(reminder_id: str):
    result = reminder_manager.remove_reminder(reminder_id)
    if not result.get("Success"):
        raise HTTPException(status_code=400, detail=result.get("Message"))
    return result

# ------------------- LOGS -------------------
@app.get("/logs")
def get_logs(reminder_id: str = None):
    return log_manager.list_logs(reminder_id)

@app.post("/logs")
def create_log(log: LogCreate):
    result = log_manager.log_reminder_activity(log.reminder_id, log.status, log.response_text)
    if not result.get("Success"):
        raise HTTPException(status_code=400, detail=result.get("Message"))
    return result

@app.delete("/logs/{log_id}")
def delete_log(log_id: str):
    result = log_manager.remove_log(log_id)
    if not result.get("Success"):
        raise HTTPException(status_code=400, detail=result.get("Message"))
    return result