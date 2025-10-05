# SmartNotify: Multi-Channel Event Reminder System

## Project Overview
**SmartNotify** is a smart, multi-channel reminder system designed to help users schedule and manage their events efficiently by sending timely notifications across multiple communication channels — **WhatsApp, Email, and SMS**.  

The system leverages a modern backend built with **Python** and **Supabase PostgreSQL** database to store user information, reminders, and message logs. Users can set reminders for themselves or others, specifying the recipient’s name, contact details, preferred notification channel, and scheduled time.  

The platform is designed to be **dynamic** and **scalable**:

- **Dynamic Channels:** New notification channels can be added without modifying the core database or backend logic.  
- **Personalized Messages:** Each reminder stores the recipient’s name and contact, enabling personalized notifications.  
- **Reliable Logging:** All notifications are tracked in a logs table, recording success or failure, providing audit and retry capabilities.  

---

## Features

- **Multi-Channel Notifications:** Send reminders via WhatsApp, Email, or SMS.  
- **Dynamic Channel Management:** Easily add or remove channels without affecting core logic.  
- **Personalized Messages:** Messages include recipient's name for a personal touch.  
- **Event Scheduling:** Notifications are sent at the exact scheduled time.  
- **Activity Logging:** Maintain logs of all sent reminders with status and response.  
- **Scalable Backend:** Built with Python and Supabase for efficient database operations.  
- **API-Driven Design:** Expose REST APIs for easy integration with frontend applications.  
- **Retry Mechanism:** Failed notifications can be retried automatically based on logs.  
- **Future-Ready:** New notification channels can be added without backend modifications.  

---

## Tech Stack

- **Backend:** Python (Flask for API endpoints)  
- **Frontend / Dashboard:** Streamlit (optional web interface for managing reminders)  
- **Database:** Supabase PostgreSQL  
- **Messaging Services:** Twilio (SMS/WhatsApp), SMTP (Email)  
- **Deployment:** Docker / Cloud Platforms (optional)  

---

## Database Design

- **Users Table:** Stores user information (name, email, phone).  
- **Reminders Table:** Stores reminder details, recipient info, scheduled time, and status.  
- **Channels Table (Dynamic):** Stores available notification channels.  
- **Logs Table:** Records every sent reminder, including response and status.  

---

## Use Cases

- **Personal Event Reminders:** Birthdays, meetings, tasks.  
- **Corporate Notifications:** Meeting alerts, updates.  
- **General Notifications:** Any scenario requiring timely notifications across multiple channels.  



## project  structure

SmartNotify/
│
├── api/                                # Backend API Layer (FastAPI)
│   ├── __init__.py
│   └── main.py                         # Defines REST API endpoints
│       - Routes for reminders, logs, and users
│       - Integrates core logic and database modules
│       - Manages request validation and responses
│
├── frontend/                           # Frontend Application (Streamlit or Tkinter)
│   ├── __init__.py
│   └── app.py                          # UI logic for users
│       - Interface for creating and managing reminders
│       - Displays reminder status and logs
│       - Connects with backend API endpoints
│
├── src/                                # Core Backend Logic
│   ├── __init__.py
│   ├── auth.py                         # User authentication and access control
│   ├── db.py                           # Database operations (Supabase/PostgreSQL)
│       - Handles CRUD for users, reminders, and logs
│       - Manages database connections and schema integrity
│   ├── logic.py                        # Core business logic
│       - Validates reminder data
│       - Handles retry logic and message formatting
│       - Bridges between scheduler and notifiers
│   ├── messaging.py                    # Central message routing
│       - Determines the correct communication channel
│       - Standardizes message payloads
│   ├── scheduler.py                    # Background scheduling system
│       - Scans pending reminders
│       - Triggers notification dispatch at the right time
│       - Includes retry and failure handling
│   ├── utils.py                        # Utility/helper functions
│       - Date/time conversions, logging, formatting, etc.
│
│   └── notifiers/                      # Multi-channel notification handlers
│       ├── __init__.py
│       ├── whatsapp.py                 # WhatsApp integration (Twilio API)
│       ├── email.py                    # Email integration (SMTP or other API)
│       └── sms.py                      # SMS integration (Twilio or other gateway)
│
├── .env                                # Environment variables
│   - API keys, database credentials, and service tokens
│
├── requirements.txt                    # Python dependencies
│   - fastapi, streamlit, supabase, twilio, schedule, etc.
│
├── README.md                           # Project documentation
│   - Overview, setup, API usage, and deployment guide
│
└── venv/                               # Virtual environment (excluded from version control)






## Quick Start

### Prerequisites

- Python 3.8 or higher
- A Supabase account
- Git(Push, cloning)


### 1.Clone or Download the Project
# Option 1: Clone with Git
git clone https://github.com/bhavanibeemanpalli2108/Python_Full_Stack_Project.git

# Option 2: Download and extract the ZIP file

### 2.Install Dependencies

# Install all required python packages
pip install -r requirements.txt


### 3.Set Up Supabase Database

1.Create a Supabase Project:
2.Create the users table:

- Go to the SQL Editor in  your Supabase
-Run this SQL command


```sql
CREATE TABLE IF NOT EXISTS users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name TEXT NOT NULL,
    email TEXT UNIQUE,
    phone TEXT,
    created_at TIMESTAMP DEFAULT now()
);


CREATE TABLE IF NOT EXISTS channels (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    description TEXT,
    created_at TIMESTAMP DEFAULT now()
);


CREATE TABLE IF NOT EXISTS logs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    reminder_id UUID REFERENCES reminders(id) ON DELETE CASCADE,
    sent_at TIMESTAMP DEFAULT now(),
    status TEXT CHECK (status IN ('sent','failed')),
    response TEXT
);


CREATE TABLE IF NOT EXISTS reminders (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    recipient_name TEXT NOT NULL,
    recipient TEXT NOT NULL,
    message TEXT NOT NULL,
    channel_id INT REFERENCES channels(id) ON DELETE SET NULL,
    event_time TIMESTAMP NOT NULL,
    status TEXT DEFAULT 'pending' CHECK (status IN ('pending','sent','failed')),
    created_at TIMESTAMP DEFAULT now()
);

```

3.**Get your  credentials

### 4. Configure Environment Variables

1. Create a ".env" file in the project root

2. Add your Supabase credentials to '.env':
SUPABASE_URL=`https://bcaasupopxyqhpbjcinl.supabase.co`
SUPABASE_KEY=`eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImJjYWFzdXBvcHh5cWhwYmpjaW5sIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTgwODEzMTksImV4cCI6MjA3MzY1NzMxOX0.ABgIgHsw34kGBXtK3x5hTcGbwHxLm042aYXJ48IfxkE`


###  5. Run the Application

### Streamlit Frontend
streamlit run frontend/app.py

The app  will open in your browser  at `http://localhost:8501`

## FASTAPI Backend

cd api
python main.py

The API  will be available at `http://localhos:8000`


## How to use

## Technical Details

### Technologies used

- **Frontend**: Streamlit (Python web freamework)
- **Backend**: FASTAPI (Python REST API framework)
 -**Database**: Supabase (PostgresSQL - based - backend-as-a-service)
- **Language**: Python 3.8+

## Key Components

1. **`src/db.py`** – Database Operations  
   - Manages all CRUD (Create, Read, Update, Delete) operations with Supabase.  
   - Handles connection pooling and query execution.  
   - Ensures schema consistency and handles database transactions safely.  

2. **`src/logic.py`** – Business Logic  
   - Validates reminder requests (time, channel, recipient info).  
   - Handles scheduling, retry logic, and status updates.  
   - Interfaces with notification services (WhatsApp, Email, SMS).  

3. **`api/main.py`** – Backend (FastAPI)  
   - Exposes REST API endpoints for reminders, users, logs, and channels.  
   - Provides endpoints to create, update, delete, and fetch reminders.  
   - Includes authentication and request validation.  

4. **`frontend/app.py`** – Frontend (Streamlit)  
   - User-friendly dashboard for managing reminders.  
   - Allows creating new reminders with recipient details and scheduling.  
   - Displays sent reminders, logs, and status updates.  

5. **`.env`** – Environment Variables  
   - Stores sensitive credentials (Supabase URL, Supabase API key, Twilio/SMTP keys).  
   - Ensures security by keeping them out of the codebase.  

---


## Troubleshooting

- **Database Connection Issues:**  
  - Verify your `.env` file contains the correct `SUPABASE_URL` and `SUPABASE_KEY`.  
  - Check if your Supabase project is active and not paused.  

- **Frontend Not Loading:**  
  - Ensure Streamlit is installed: `pip install streamlit`.  
  - Run the app from the correct directory: `streamlit run frontend/app.py`.  

- **Backend API Errors:**  
  - Make sure FastAPI and Uvicorn are installed:  
    ```bash
    pip install fastapi uvicorn
    ```  
  - Start the backend with:  
    ```bash
    uvicorn api.main:app --reload
    ```  

- **Notification Failures:**  
  - Verify Twilio or SMTP credentials in `.env`.  
  - Check if the recipient’s contact details are valid.  
  - Look into the `logs` table for error messages.  

---

## Common Issues

1. **"ModuleNotFoundError" when running the app**  
   - Cause: Missing dependencies.  
   - Solution: Run `pip install -r requirements.txt`.  

2. **Reminders not being delivered**  
   - Cause: Invalid API keys or blocked credentials.  
   - Solution: Double-check `.env` file values and retry.  

3. **Streamlit showing blank page**  
   - Cause: Running from the wrong directory.  
   - Solution: Navigate to the project root before running:  
     ```bash
     cd SmartNotify
     streamlit run frontend/app.py
     ```  

4. **Supabase "permission denied" errors**  
   - Cause: Row-Level Security (RLS) enabled without policies.  
   - Solution: Disable RLS for testing or create appropriate access policies.  

---

## Future Enhancements

- **Additional Channels:**  
  - Support for Slack, Microsoft Teams, Telegram, and Push Notifications.  

- **Recurring Reminders:**  
  - Ability to set reminders for daily/weekly/monthly events.  

- **Advanced Dashboard:**  
  - Analytics and reports on sent reminders, delivery rate, and failures.  

- **User Authentication:**  
  - Secure login with JWT-based authentication.  

- **Multi-Language Support:**  
  - Allow users to send reminders in different languages.  

- **AI-Powered Smart Scheduling:**  
  - Suggest best notification times based on user behavior.  

- **Cloud Deployment:**  
  - Dockerized deployment on AWS, GCP, or Heroku for scalability.  

---

## Support

If you encounter any issues or have questions:  

- 📌 **Report Bugs / Issues:** Open an issue in the [GitHub Issues](https://github.com/bhavanibeemanpalli2108/Python_Full_Stack_Project/issues) section.  
- 📧 **Email Support:** itsbhavanibheemanpally08@gmail.com  
- 📞 **Phone Support:** +91-7842472595  
- 💬 **Feature Requests / Feedback:** Use GitHub Discussions (if enabled) or include suggestions in the Issues tab.  

When reporting problems, please include:  
- ✅ Steps to reproduce the issue  
- ✅ Error logs or screenshots (if applicable)  
- ✅ Your environment details (OS, Python version, dependencies)  




SmartNotify simplifies the reminder process, ensuring messages are delivered reliably and on time, while maintaining flexibility and scalability for future expansions.


