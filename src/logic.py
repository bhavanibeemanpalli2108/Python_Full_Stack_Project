# src/logic.py

from src.db import DatabaseManager
from datetime import datetime, timedelta

class UserManager:
    """Acts as a bridge between frontend(Streamlit/FASTAPI) and database."""

    def __init__(self):
        # create a database manager instance (this will handle actul db operations).
        self.db = DatabaseManager()

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
        # create a database manager instance (this will handle actul db operations).
        self.db = DatabaseManager()

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
        # create a database manager instance (this will handle actul db operations).
        self.db = DatabaseManager()


    # add reminder
    def add_reminder(self, user_id: str, recipient_name: str, recipient: str, message: str, channel_id: int, event_time: str):
        """Add a new reminder to the system.
        Returns a success message or error based on the activity."""
        if not user_id or not recipient_name or not recipient or not message or not channel_id or not event_time:
            return{"Success": False, "Message": "All fields except optional ones are required."}   
        
        # call db function to create reminder
        result= self.db.create_reminder(user_id, recipient_name, recipient, message, channel_id, event_time)

        # check if reminder creation was successful
        if result.get("Success"):
            return {"Success": True, "Message": "Reminder created successfully."}
        else:
            return {"Success": False, "Message": f"Error:{result.get('Error')}"}
        

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
        # create a database manager instance (this will handle actul db operations).
        self.db = DatabaseManager()
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