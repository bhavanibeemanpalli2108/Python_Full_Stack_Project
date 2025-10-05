from datetime import datetime

def format_datetime(dt):
    if isinstance(dt, str):
        dt = dt.rstrip("Z")  # remove trailing Z if exists
        dt = datetime.fromisoformat(dt)
    return dt.strftime("%d %b %Y, %I:%M %p")
