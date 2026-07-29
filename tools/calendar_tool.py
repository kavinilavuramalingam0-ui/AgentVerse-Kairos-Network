import os
import datetime
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# Scope allows both Reading and Writing to the calendar
SCOPES = ['https://www.googleapis.com/auth/calendar']
CREDENTIALS_FILE = 'credentials.json'

def authenticate_oauth():
    """Authenticates using OAuth2 (browser popup) and saves token.json for future runs."""
    creds = None
    
    # 1. Check if we already logged in previously
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
        
    # 2. If no valid credentials, force log in
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if not os.path.exists(CREDENTIALS_FILE):
                raise FileNotFoundError(f"[CRITICAL ERROR] '{CREDENTIALS_FILE}' is missing. Please download it from Google Cloud Console.")
            
            flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_FILE, SCOPES)
            creds = flow.run_local_server(port=0)
            
        # Save the token for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
            
    return build('calendar', 'v3', credentials=creds)

def get_todays_events() -> str:
    """Fetches all events scheduled for today and returns them as a formatted string."""
    print("\n[SYSTEM] Agent is checking your calendar for existing conflicts (OAuth2)...")
    try:
        service = authenticate_oauth()
        
        today = datetime.datetime.today()
        start_of_day = today.replace(hour=0, minute=0, second=0).isoformat() + "+05:30"
        end_of_day = today.replace(hour=23, minute=59, second=59).isoformat() + "+05:30"
        
        # calendarId='primary' automatically selects the logged-in user's main calendar
        events_result = service.events().list(
            calendarId='primary', 
            timeMin=start_of_day, 
            timeMax=end_of_day, 
            singleEvents=True,
            orderBy='startTime'
        ).execute()
        
        events = events_result.get('items', [])
        
        if not events:
            return "No events scheduled for today. The calendar is completely free."
            
        formatted_events = "=== EXISTING CALENDAR EVENTS FOR TODAY ===\n"
        for event in events:
            start = event['start'].get('dateTime', event['start'].get('date'))
            end = event['end'].get('dateTime', event['end'].get('date'))
            
            start_formatted = datetime.datetime.fromisoformat(start).strftime('%I:%M %p')
            end_formatted = datetime.datetime.fromisoformat(end).strftime('%I:%M %p')
            summary = event.get('summary', 'Busy')
            
            formatted_events += f"- {start_formatted} to {end_formatted}: {summary}\n"
            
        return formatted_events
    except Exception as e:
        print(f"[ERROR] Failed to read calendar via OAuth2: {e}")
        return "Warning: Could not fetch calendar data. Assume standard profile constraints apply."

def parse_and_validate_time_range(start_str: str, end_str: str):
    """Parses start/end times and validates that end_time > start_time to prevent API errors."""
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

    start_iso = start_dt.isoformat() + "+05:30"
    end_iso = end_dt.isoformat() + "+05:30"
    
    return start_iso, end_iso

def add_to_calendar(task_name: str, start_time: str, end_time: str, location: str):
    print(f"[SYSTEM] Accessing Google Calendar for: {task_name}...")
    try:
        service = authenticate_oauth()
        start_iso, end_iso = parse_and_validate_time_range(start_time, end_time)
        
        event = {
            'summary': task_name,
            'location': location,
            'start': {
                'dateTime': start_iso,
                'timeZone': 'Asia/Kolkata',
            },
            'end': {
                'dateTime': end_iso,
                'timeZone': 'Asia/Kolkata',
            },
            'reminders': {'useDefault': True},
        }

        # calendarId='primary' automatically selects the logged-in user's main calendar
        event_result = service.events().insert(calendarId='primary', body=event).execute()
        print(f"[SUCCESS] Event created: {event_result.get('htmlLink')}")
    except Exception as e:
        print(f"[ERROR] Failed to add to calendar via OAuth2: {e}")