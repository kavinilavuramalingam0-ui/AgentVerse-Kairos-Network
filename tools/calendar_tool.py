import os
import datetime
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

SCOPES = ['https://www.googleapis.com/auth/calendar']
CREDENTIALS_FILE = 'credentials.json'

def authenticate_oauth():
    """Authenticates using OAuth2 and saves token.json."""
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
    print("\n[SYSTEM] Agent is checking your calendar for existing conflicts (OAuth2)...")
    try:
        service = authenticate_oauth()
        today = datetime.datetime.today()
        start_of_day = today.replace(hour=0, minute=0, second=0).isoformat() + "+05:30"
        end_of_day = today.replace(hour=23, minute=59, second=59).isoformat() + "+05:30"
        
        events_result = service.events().list(
            calendarId='primary', timeMin=start_of_day, timeMax=end_of_day, 
            singleEvents=True, orderBy='startTime'
        ).execute()
        
        events = events_result.get('items', [])
        if not events:
            return "No events scheduled for today."
            
        formatted_events = "=== EXISTING CALENDAR EVENTS FOR TODAY ===\n"
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
    today_date = datetime.datetime.today().strftime('%Y-%m-%d')
    try:
        start_dt = datetime.datetime.strptime(f"{today_date} {start_str.strip()}", "%Y-%m-%d %I:%M %p")
    except ValueError:
        start_dt = datetime.datetime.today()

    try:
        end_dt = datetime.datetime.strptime(f"{today_date} {end_str.strip()}", "%Y-%m-%d %I:%M %p")
    except ValueError:
        end_dt = start_dt + datetime.timedelta(minutes=30)

    if end_dt <= start_dt:
        end_dt = start_dt + datetime.timedelta(minutes=30)

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