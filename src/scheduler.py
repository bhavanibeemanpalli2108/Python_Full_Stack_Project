import time
from datetime import datetime, timezone
from src.logic import process_due_reminders, get_due_reminders
from src.db import update_reminder_status
from src.messaging import send_message

# scheduler.py snippet
# ... imports ...
# scheduler.py

# scheduler.py

# ... imports ...

def run_scheduler():
    print("🚀 Scheduler started, checking for reminders...")
    while True:
        try:
            # get_due_reminders now returns ONLY truly due reminders (filtered by DB)
            due_reminders = get_due_reminders() 
            
            # The manual time comparison block is REMOVED!
            
            for r in due_reminders:
                # Send reminder
                channel = r.get('channel_id')
                recipient = r.get('recipient')
                message = r.get('message')

                try:
                    success = send_message(recipient, message)
                    if success:
                        update_reminder_status(r['id'], "sent")
                        print(f"✅ Reminder sent to {recipient} via channel {channel}")
                    else:
                        update_reminder_status(r['id'], "failed")
                        print(f"❌ Failed reminder {r['id']} to {recipient}")
                except Exception as e:
                    update_reminder_status(r['id'], "failed")
                    print(f"❌ Error sending reminder {r['id']} to {recipient}: {e}")

        except Exception as e:
            print(f"⚠️ Scheduler error: {e}")

        time.sleep(60)  # Check every minute
# ... rest of scheduler.py ...

if __name__ == "__main__":
    run_scheduler()
