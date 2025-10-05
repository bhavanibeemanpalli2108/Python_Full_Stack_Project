# import streamlit as st
# import sys, os
# from datetime import datetime
# from dotenv import load_dotenv
# import pytz

# # Load environment variables
# load_dotenv()

# # Add src to path
# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# # Import Managers from logic.py
# from src.logic import UserManager, ChannelManager, ReminderManager
# from src.utils import format_datetime
# from src.auth import login, signup, logout, get_current_user

# # Initialize managers
# user_manager = UserManager()
# channel_manager = ChannelManager()
# reminder_manager = ReminderManager()

# # Streamlit page config
# st.set_page_config(page_title="SmartNotify", layout="wide")

# # --- Utility function to format UTC to local IST ---
# def format_datetime_local(utc_str):
#     utc_dt = datetime.fromisoformat(utc_str)
#     if utc_dt.tzinfo is None:
#         from datetime import timezone
#         utc_dt = utc_dt.replace(tzinfo=timezone.utc)
#     ist = pytz.timezone("Asia/Kolkata")
#     local_dt = utc_dt.astimezone(ist)
#     return local_dt.strftime("%d %b %Y, %I:%M %p")

# # --- CSS ---
# def add_custom_css():
#     st.markdown(
#         """
#         <style>
#         /* Global background */
#         .stApp { background: linear-gradient(to right, #fffde7, #fff9c4, #ffe082); color: #2c2c2c !important; font-family: "Comic Sans MS", cursive, sans-serif !important;}
#         /* Sidebar */
#         [data-testid="stSidebar"] { background: linear-gradient(to bottom, #ffeb3b, #fbc02d); color: #2c2c2c !important;}
#         [data-testid="stSidebar"] * { color: #FF1493 !important; font-family: "Comic Sans MS", cursive, sans-serif !important;}
#         /* Headings */
#         h1, h2, h3, h4, h5, h6 { color: #4B0082 !important;}
#         /* Form labels */
#         label, .css-16idsys, .css-1n76uvr { color: #4e342e !important; font-weight: 600 !important; font-size: 0.95rem !important;}
#         /* Input fields */
#         input, textarea, select { background-color: #ffffff !important; color: #2c2c2c !important; border: 1px solid #fbc02d !important; border-radius: 8px !important; padding: 10px !important;}
#         input:focus, textarea:focus, select:focus { border: 1px solid #e65100 !important; box-shadow: 0 0 5px #ffb74d !important;}
#         /* Buttons */
#         div.stButton > button { background: linear-gradient(to right, #ff9800, #f57c00); color: white !important; border-radius: 10px; padding: 0.6em 1.2em; font-weight: bold; border: none; transition: 0.3s;}
#         div.stButton > button:hover { background: linear-gradient(to right, #e65100, #ef6c00); transform: scale(1.05);}
#         /* Expanders */
#         .streamlit-expanderHeader { background-color: #ffe082 !important; color: #e65100 !important; font-weight: bold; border-radius: 6px;}
#         /* Success & error messages */
#         .stSuccess { background-color: #c8e6c9 !important; color: #1b5e20 !important; padding: 10px; border-radius: 8px;}
#         .stError { background-color: #ffcdd2 !important; color: #b71c1c !important; padding: 10px; border-radius: 8px;}
#         /* Card styling */
#         .custom-card { background: white; border-radius: 12px; padding: 15px 20px; margin-bottom: 15px; box-shadow: 0 4px 8px rgba(0,0,0,0.1); transition: transform 0.2s;}
#         .custom-card:hover { transform: translateY(-3px); box-shadow: 0 6px 12px rgba(0,0,0,0.15);}
#         .custom-card h4 { margin: 0; color: #e65100;}
#         .custom-card small { color: #555;}
#         .reminder-pending {background-color:#fff9c4;}
#         .reminder-sent {background-color:#c8e6c9;}
#         .reminder-failed {background-color:#ffcccb;}
#         </style>
#         """,
#         unsafe_allow_html=True
#     )

# # Apply custom CSS
# add_custom_css()

# st.title("SmartNotify")

# # Sidebar menu
# menu = ["Home", "Login", "Sign Up", "Dashboard", "Logout"]
# choice = st.sidebar.selectbox("Menu", menu)

# # --- Home ---
# if choice == "Home":
#     st.subheader(" Home")
#     st.write("Welcome to SmartNotify! Please log in or sign up to continue.")

# # --- Login ---
# elif choice == "Login":
#     st.subheader(" Login")
#     login()

# # --- Sign Up ---
# elif choice == "Sign Up":
#     st.subheader(" Sign Up")
#     signup()

# # --- Dashboard ---
# elif choice == "Dashboard":
#     user = get_current_user()
#     if user:
#         st.subheader(f" Welcome, {user['name']}!")
#         tabs = ["Users", "Channels", "Reminders"]
#         tab_choice = st.sidebar.selectbox("Dashboard Sections", tabs)

#         # --- Users Management ---
#         if tab_choice == "Users":
#             st.subheader("Manage Users")

#             # Add User
#             with st.expander("➕ Add User"):
#                 with st.form("Add User Form"):
#                     name = st.text_input("Name")
#                     email = st.text_input("Email")
#                     phone = st.text_input("Phone (optional)")
#                     submitted = st.form_submit_button("Create User")
#                     if submitted:
#                         res = user_manager.add_user(name, email, phone)
#                         if res["Success"]:
#                             st.success("✅ User created successfully!")
#                         else:
#                             st.error(f"❌ {res['Message']}")

#             # List Users
#             users = user_manager.list_users()
#             for u in users:
#                 st.write(f"**{u['name']}** ({u['email']}) - {u.get('phone', 'No phone')}")
#                 with st.expander(f" Edit {u['name']}"):
#                     with st.form(f"Edit User Form {u['id']}"):
#                         name_edit = st.text_input("Name", value=u['name'])
#                         email_edit = st.text_input("Email", value=u['email'])
#                         phone_edit = st.text_input("Phone (optional)", value=u.get('phone', ''))
#                         submitted_edit = st.form_submit_button("Update User")
#                         if submitted_edit:
#                             res = user_manager.complete_user_update(u['id'], {
#                                 "name": name_edit,
#                                 "email": email_edit,
#                                 "phone": phone_edit
#                             })
#                             if res["Success"]:
#                                 st.success("✅ User updated successfully!")
#                             else:
#                                 st.error(f"❌ {res['Message']}")

#                 if st.button(f" Delete {u['name']}"):
#                     res = user_manager.remove_user(u['id'])
#                     if res["Success"]:
#                         st.success("✅ User deleted successfully!")
#                     else:
#                         st.error(f"❌ {res['Message']}")

#         # --- Channels Management ---
#         elif tab_choice == "Channels":
#             st.subheader("Manage Channels")

#             # Add Channel Form
#             with st.expander("➕ Add Channel"):
#                 with st.form("add_channel_form"):
#                     name = st.text_input("Channel Name")
#                     description = st.text_area("Description (optional)")
#                     submitted = st.form_submit_button("Create Channel")
#                     if submitted:
#                         res = channel_manager.add_channel(name, description)
#                         if res["Success"]:
#                             st.success("✅ Channel created successfully!")
#                         else:
#                             st.error(f"❌ {res['Message']}")

#             # Display existing channels
#             channels = channel_manager.list_channels()
#             for c in channels:
#                 st.write(f"**{c['name']}** - {c.get('description', 'No description')}")
#                 with st.expander(f" Edit {c['name']}"):
#                     with st.form(f"edit_channel_form_{c['id']}"):
#                         name_edit = st.text_input("Channel Name", value=c['name'])
#                         desc_edit = st.text_area("Description (optional)", value=c.get('description', ''))
#                         submitted_edit = st.form_submit_button("Update Channel")
#                         if submitted_edit:
#                             res = channel_manager.modify_channel(c['id'], {
#                                 "name": name_edit,
#                                 "description": desc_edit
#                             })
#                             if res["Success"]:
#                                 st.success("✅ Channel updated successfully!")
#                             else:
#                                 st.error(f"❌ {res['Message']}")

#                 if st.button(f" Delete {c['name']}"):
#                     res = channel_manager.remove_channel(c['id'])
#                     if res["Success"]:
#                         st.success("✅ Channel deleted successfully!")
#                     else:
#                         st.error(f"❌ {res['Message']}")

#         # --- Reminders Management ---
#         elif tab_choice == "Reminders":
#             st.subheader("📅 My Reminders")
#             reminders = reminder_manager.list_reminders(user['id'])
#             channels = channel_manager.list_channels()
#             channel_options = {c['name']: c['id'] for c in channels}

#             # Add Reminder Section
#             with st.expander("➕ Add New Reminder"):
#                 with st.form("add_reminder_form"):
#                     recipient_name = st.text_input("Recipient Name")
#                     recipient = st.text_input("Recipient (Email or Phone)")
#                     message = st.text_area("Message")
#                     channel_name = st.selectbox("Channel", list(channel_options.keys()))
#                     event_date = st.date_input("Event Date", value=datetime.now().date())
#                     event_time = st.time_input("Event Time", value=datetime.now().time())
#                     event_datetime_naive = datetime.combine(event_date, event_time)
#                     event_datetime_clean = event_datetime_naive.replace(microsecond=0)
#                     submitted = st.form_submit_button("Create Reminder")
#                     if submitted:
#                         # Convert local IST to UTC
#                         local_tz = pytz.timezone("Asia/Kolkata")
#                         local_dt_ist = local_tz.localize(event_datetime_clean, is_dst=None)
#                         event_time_utc = local_dt_ist.astimezone(pytz.utc).isoformat()
#                         res = reminder_manager.add_reminder(
#                                 user['id'],
#                                 recipient_name,
#                                 recipient,
#                                 message,
#                                 channel_options[channel_name],
#                                 event_time_utc # This is the correctly shifted time
#                         )

#                         if res["Success"]:
#                             st.success("✅ Reminder created successfully!")
#                         else:
#                             st.error(f"❌ {res['Message']}")
                    
                                                

#             st.markdown("---")

#             # Display reminders
#             for r in reminders:
#                 if r['status'] == "pending":
#                     bg_color = "#FFF9C4"
#                 elif r['status'] == "sent":
#                     bg_color = "#C8E6C9"
#                 else:
#                     bg_color = "#FFCDD2"

#                 with st.container():
#                     st.markdown(
#                         f"""
#                         <div style="background-color:{bg_color}; padding:15px; border-radius:10px; margin-bottom:10px;">
#                             <strong>To:</strong> {r['recipient_name']}<br>
#                             <strong>Message:</strong> {r['message']}<br>
#                             <strong>Channel:</strong> {next((c['name'] for c in channels if c['id']==r['channel_id']), 'Unknown')}<br>
#                             <strong>Time:</strong> {format_datetime_local(r['event_time'])}<br>
#                             <strong>Status:</strong> {r['status'].capitalize()}
#                         </div>
#                         """,
#                         unsafe_allow_html=True
#                     )

# # --- Logout ---
# elif choice == "Logout":
#     logout()




import streamlit as st
import sys, os
from datetime import datetime
from dotenv import load_dotenv
import pytz

# Load environment variables
load_dotenv()

# Add src to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Import Managers from logic.py
from src.logic import UserManager, ChannelManager, ReminderManager
from src.utils import format_datetime
from src.auth import login, signup, logout, get_current_user


# Initialize managers
user_manager = UserManager()
channel_manager = ChannelManager()
reminder_manager = ReminderManager()

# Streamlit page config
st.set_page_config(page_title="SmartNotify", layout="wide")

# --- Utility function to format UTC to local IST ---
def format_datetime_local(utc_str):
    utc_dt = datetime.fromisoformat(utc_str)
    if utc_dt.tzinfo is None:
        from datetime import timezone
        utc_dt = utc_dt.replace(tzinfo=timezone.utc)
    ist = pytz.timezone("Asia/Kolkata")
    local_dt = utc_dt.astimezone(ist)
    return local_dt.strftime("%d %b %Y, %I:%M %p")

# --- CSS ---
def add_custom_css():
   st.markdown("""
<style>
/* ---------------- Global Animated Background ---------------- */
@keyframes gradientShift {
    0% {background-position: 0% 50%;}
    50% {background-position: 100% 50%;}
    100% {background-position: 0% 50%;}
}

.stApp {
    background: linear-gradient(135deg, 
        #f8fcff, #f3faff, #eef8ff, #eaf7ff, #e5f5ff, 
        #e0f3ff, #dbf1ff, #d6efff);
    background-size: 2000% 2000%;
    animation: gradientShift 30s ease infinite;
    font-family: 'Poppins', sans-serif !important;
    color: #1f2d3d !important;
}

/* ---------------- Sidebar ---------------- */
[data-testid="stSidebar"] {
    background: linear-gradient(135deg, 
        #e6f4ff, #dcefff, #d2eaff, #c8e5ff, #bee0ff);
    color: #f0f8ff !important;
}
[data-testid="stSidebar"] * {
    color: #37bade !important;
    font-family: 'Poppins', sans-serif !important;
    font-weight: 500 !important;
}

/* ---------------- Headings ---------------- */
h1 {
    color: #007acc !important;
    text-align: center !important;
    font-weight: 800 !important;
}
h2, h3, h4, h5, h6 {
    color: #0091ea !important;
    font-weight: 700 !important;
}

/* ---------------- Text Elements ---------------- */
p, div, span, label, li, .css-16idsys, .css-1n76uvr, .stMarkdown {
    color: #1f2d3d !important;
    font-weight: 500 !important;
}

/* ---------------- Input Fields ---------------- */
input, textarea, select {
    background-color: #ffffff !important;
    color: #37bade !important;
    border: 2px solid #cce7ff !important;
    border-radius: 8px !important;
    padding: 10px !important;
}
textarea:hover, input:hover, select:hover {
    border: 2px solid #99ddff !important;
    box-shadow: 0 0 8px #b3e5fc !important;
}
input:focus, textarea:focus, select:focus {
    border: 2px solid #80cfff !important;
    box-shadow: 0 0 8px #99ddff !important;
}

/* ✅ Only dropdown menu options darker */
div[data-baseweb="popover"] * {
    color: #1f2d3d !important; /* darker text inside options */
    background-color: #f9fcff !important;
}

/* ---------------- Buttons ---------------- */
div.stButton > button {
    background: linear-gradient(to right, #b3e5fc, #81d4fa, #4fc3f7);
    color: #00334d !important;
    border-radius: 10px;
    padding: 0.6em 1.2em;
    font-weight: 600;
    border: none;
    transition: 0.3s ease-in-out;
    box-shadow: 0 3px 10px rgba(100, 200, 255, 0.4);
}
div.stButton > button:hover {
    background: linear-gradient(to right, #4fc3f7, #29b6f6, #03a9f4);
    transform: scale(1.05);
    color: white !important;
    box-shadow: 0 5px 15px rgba(80, 180, 255, 0.6);
}

/* ---------------- Expanders ---------------- */
.streamlit-expanderHeader {
    background-color: #e1f5fe !important;
    color: #01579b !important;
    font-weight: bold;
    border-radius: 6px;
}

/* ---------------- Cards ---------------- */
.custom-card {
    background: #f3faff;
    border-radius: 12px;
    padding: 15px 20px;
    margin-bottom: 15px;
    box-shadow: 0 4px 10px rgba(0,0,0,0.05);
    transition: transform 0.2s, box-shadow 0.2s;
}
.custom-card:hover {
    transform: translateY(-3px);
    box-shadow: 0 6px 14px rgba(0,0,0,0.1);
}
.custom-card h4 {
    margin: 0;
    color: #0277bd;
    font-weight: 600;
}
.custom-card small {
    color: #333;
}

/* ---------------- Reminder States ---------------- */
.reminder-pending {background-color:#e3f2fd;}
.reminder-sent {background-color:#b3e5fc;}
.reminder-failed {background-color:#bbdefb;}

/* ---------------- Footer ---------------- */
footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)





# Apply custom CSS
add_custom_css()

st.title("SmartNotify")

# Sidebar menu
menu = ["Home", "Login", "Sign Up", "Dashboard", "Logout"]
choice = st.sidebar.selectbox("Menu", menu)

# --- Home ---
if choice == "Home":
    st.subheader(" Home")
    st.write("Welcome to **SmartNotify!** Please log in or sign up to continue.")

# --- Login ---
elif choice == "Login":
    st.subheader(" Login")
    login()

# --- Sign Up ---
elif choice == "Sign Up":
    st.subheader(" Sign Up")
    signup()

# --- Dashboard ---
elif choice == "Dashboard":
    user = get_current_user()
    if user:
        st.subheader(f" Welcome, {user['name']}!")
        tabs = ["Users", "Channels", "Reminders"]
        tab_choice = st.sidebar.selectbox("Dashboard Sections", tabs)

        # --- Users Management ---
        if tab_choice == "Users":
            st.subheader(" Manage Users")

            # Add User
            with st.expander("➕ Add User"):
                with st.form("Add User Form"):
                    name = st.text_input("Name")
                    email = st.text_input("Email")
                    phone = st.text_input("Phone (optional)")
                    submitted = st.form_submit_button("Create User")
                    if submitted:
                        res = user_manager.add_user(name, email, phone)
                        if res["Success"]:
                            st.success("✅ User created successfully!")
                        else:
                            st.error(f"❌ {res['Message']}")

            # List Users
            users = user_manager.list_users()
            for u in users:
                st.write(f"**{u['name']}** ({u['email']}) - {u.get('phone', 'No phone')}")
                with st.expander(f"✏️ Edit {u['name']}"):
                    with st.form(f"Edit User Form {u['id']}"):
                        name_edit = st.text_input("Name", value=u['name'])
                        email_edit = st.text_input("Email", value=u['email'])
                        phone_edit = st.text_input("Phone (optional)", value=u.get('phone', ''))
                        submitted_edit = st.form_submit_button("Update User")
                        if submitted_edit:
                            res = user_manager.complete_user_update(u['id'], {
                                "name": name_edit,
                                "email": email_edit,
                                "phone": phone_edit
                            })
                            if res["Success"]:
                                st.success("✅ User updated successfully!")
                            else:
                                st.error(f"❌ {res['Message']}")

                if st.button(f" Delete {u['name']}"):
                    res = user_manager.remove_user(u['id'])
                    if res["Success"]:
                        st.success("✅ User deleted successfully!")
                    else:
                        st.error(f"❌ {res['Message']}")

        # --- Channels Management ---
        elif tab_choice == "Channels":
            st.subheader(" Manage Channels")

            # Add Channel Form
            with st.expander("➕ Add Channel"):
                with st.form("add_channel_form"):
                    name = st.text_input("Channel Name")
                    description = st.text_area("Description (optional)")
                    submitted = st.form_submit_button("Create Channel")
                    if submitted:
                        res = channel_manager.add_channel(name, description)
                        if res["Success"]:
                            st.success("✅ Channel created successfully!")
                        else:
                            st.error(f"❌ {res['Message']}")

            # Display existing channels
            channels = channel_manager.list_channels()
            for c in channels:
                st.write(f"**{c['name']}** - {c.get('description', 'No description')}")
                with st.expander(f" Edit {c['name']}"):
                    with st.form(f"edit_channel_form_{c['id']}"):
                        name_edit = st.text_input("Channel Name", value=c['name'])
                        desc_edit = st.text_area("Description (optional)", value=c.get('description', ''))
                        submitted_edit = st.form_submit_button("Update Channel")
                        if submitted_edit:
                            res = channel_manager.modify_channel(c['id'], {
                                "name": name_edit,
                                "description": desc_edit
                            })
                            if res["Success"]:
                                st.success("✅ Channel updated successfully!")
                            else:
                                st.error(f"❌ {res['Message']}")

                if st.button(f" Delete {c['name']}"):
                    res = channel_manager.remove_channel(c['id'])
                    if res["Success"]:
                        st.success("✅ Channel deleted successfully!")
                    else:
                        st.error(f"❌ {res['Message']}")

        # --- Reminders Management ---
        elif tab_choice == "Reminders":
            st.subheader(" My Reminders")
            reminders = reminder_manager.list_reminders(user['id'])
            channels = channel_manager.list_channels()
            channel_options = {c['name']: c['id'] for c in channels}

            # Add Reminder Section
            with st.expander("➕ Add New Reminder"):
                with st.form("add_reminder_form"):
                    recipient_name = st.text_input("Recipient Name")
                    recipient = st.text_input("Recipient (Email or Phone)")
                    message = st.text_area("Message")
                    channel_name = st.selectbox("Channel", list(channel_options.keys()))

                    # Persistent Date and Time Fix
                    if 'event_date' not in st.session_state:
                        st.session_state.event_date = datetime.now().date()
                    if 'event_time' not in st.session_state:
                        st.session_state.event_time = datetime.now().time().replace(second=0, microsecond=0)

                    col1, col2 = st.columns(2)
                    with col1:
                        event_date = st.date_input(
                            " Select Date",
                            value=st.session_state.event_date,
                            format="DD-MM-YYYY",
                            help="Pick the date for your reminder."
                        )
                    with col2:
                        event_time = st.time_input(
                            " Select Time",
                            value=st.session_state.event_time,
                            step=60,
                            help="Choose the reminder time using the clock picker."
                        )

                    # Update session state whenever user changes them
                    st.session_state.event_date = event_date
                    st.session_state.event_time = event_time

                    event_datetime_naive = datetime.combine(event_date, event_time)
                    event_datetime_clean = event_datetime_naive.replace(microsecond=0)

                    submitted = st.form_submit_button("Create Reminder")
                    if submitted:
                        # Convert local IST to UTC
                        local_tz = pytz.timezone("Asia/Kolkata")
                        local_dt_ist = local_tz.localize(event_datetime_clean, is_dst=None)
                        event_time_utc = local_dt_ist.astimezone(pytz.utc).isoformat()
                        res = reminder_manager.add_reminder(
                            user['id'],
                            recipient_name,
                            recipient,
                            message,
                            channel_options[channel_name],
                            event_time_utc
                        )

                        if res["Success"]:
                            st.success("✅ Reminder created successfully!")
                        else:
                            st.error(f"❌ {res['Message']}")

            st.markdown("---")

            # Display reminders
            for r in reminders:
                if r['status'] == "pending":
                    bg_color = "#FFF9C4"
                elif r['status'] == "sent":
                    bg_color = "#C8E6C9"
                else:
                    bg_color = "#FFCDD2"

                with st.container():
                    st.markdown(
                        f"""
                        <div style="background-color:{bg_color}; padding:15px; border-radius:10px; margin-bottom:10px;">
                            <strong>To:</strong> {r['recipient_name']}<br>
                            <strong>Message:</strong> {r['message']}<br>
                            <strong>Channel:</strong> {next((c['name'] for c in channels if c['id']==r['channel_id']), 'Unknown')}<br>
                            <strong>Time:</strong> {format_datetime_local(r['event_time'])}<br>
                            <strong>Status:</strong> {r['status'].capitalize()}
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

# --- Logout ---
elif choice == "Logout":
    logout()
