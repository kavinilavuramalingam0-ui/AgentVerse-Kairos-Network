import os
import datetime
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

SCOPES = [
    'https://www.googleapis.com/auth/calendar', 
    'https://www.googleapis.com/auth/gmail.modify'
]
CREDENTIALS_FILE = 'credentials.json'

def authenticate_oauth():
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if not os.path.exists(CREDENTIALS_FILE):
                raise FileNotFoundError(f"[ERROR] '{CREDENTIALS_FILE}' is missing.")
            flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_FILE, SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    return build('calendar', 'v3', credentials=creds)

def get_todays_events() -> str:
    print("\n[SYSTEM] Agent is checking the calendar for conflicts (Cross-Midnight Window)...")
    try:
        service = authenticate_oauth()
        now = datetime.datetime.now()
        
        start_of_window = now.isoformat() + "+05:30"
        tomorrow = now + datetime.timedelta(days=1)
        end_of_window = tomorrow.replace(hour=4, minute=0, second=0).isoformat() + "+05:30"
        
        events_result = service.events().list(
            calendarId='primary', timeMin=start_of_window, timeMax=end_of_window, 
            singleEvents=True, orderBy='startTime'
        ).execute()
        
        events = events_result.get('items', [])
        if not events:
            return "No events scheduled for the upcoming window."
            
        formatted_events = "=== EXISTING CALENDAR EVENTS (NEXT 9 HOURS) ===\n"
        for event in events:
            start = event['start'].get('dateTime', event['start'].get('date'))
            end = event['end'].get('dateTime', event['end'].get('date'))
            start_fmt = datetime.datetime.fromisoformat(start).strftime('%I:%M %p')
            end_fmt = datetime.datetime.fromisoformat(end).strftime('%I:%M %p')
            summary = event.get('summary', 'Busy')
            formatted_events += f"- {start_fmt} to {end_fmt}: {summary}\n"
            
        return formatted_events
    except Exception as e:
        print(f"[ERROR] Calendar read failed: {e}")
        return "Warning: Could not fetch calendar data."

def parse_and_validate_time_range(start_str: str, end_str: str):
    now = datetime.datetime.now()
    
    try:
        start_t = datetime.datetime.strptime(start_str.strip(), "%I:%M %p").time()
    except ValueError:
        start_t = now.time()

    try:
        end_t = datetime.datetime.strptime(end_str.strip(), "%I:%M %p").time()
    except ValueError:
        end_t = (datetime.datetime.combine(now.date(), start_t) + datetime.timedelta(minutes=30)).time()

    start_dt = datetime.datetime.combine(now.date(), start_t)
    end_dt = datetime.datetime.combine(now.date(), end_t)

    if now.time() > datetime.time(12, 0) and start_t < datetime.time(6, 0):
        start_dt += datetime.timedelta(days=1)
        
    if end_dt <= start_dt:
        end_dt += datetime.timedelta(days=1)

    return start_dt.isoformat() + "+05:30", end_dt.isoformat() + "+05:30"

def add_to_calendar(task_name: str, start_time: str, end_time: str, location: str):
    print(f"[SYSTEM] Pushing to Calendar: {task_name}...")
    try:
        service = authenticate_oauth()
        start_iso, end_iso = parse_and_validate_time_range(start_time, end_time)
        event = {
            'summary': task_name, 'location': location,
            'start': {'dateTime': start_iso, 'timeZone': 'Asia/Kolkata'},
            'end': {'dateTime': end_iso, 'timeZone': 'Asia/Kolkata'},
            'reminders': {'useDefault': True},
        }
        event_result = service.events().insert(calendarId='primary', body=event).execute()
        print(f"[SUCCESS] Event created: {event_result.get('htmlLink')}")
    except Exception as e:
        print(f"[ERROR] Failed to add event: {e}")