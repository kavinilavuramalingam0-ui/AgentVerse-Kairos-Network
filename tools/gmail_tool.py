import os
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# Must exactly match the scopes in calendar_tool.py
SCOPES = [
    'https://www.googleapis.com/auth/calendar', 
    'https://www.googleapis.com/auth/gmail.modify'
]
CREDENTIALS_FILE = 'credentials.json'

def authenticate_gmail():
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
    return build('gmail', 'v1', credentials=creds)

def fetch_unread_emails():
    """Fetches unread emails, returns their content, and marks them as read."""
    print("[SYSTEM] Pinging Gmail API for new messages...")
    try:
        service = authenticate_gmail()
        
        # Search for unread messages in the inbox
        results = service.users().messages().list(userId='me', labelIds=['INBOX', 'UNREAD'], maxResults=5).execute()
        messages = results.get('messages', [])

        if not messages:
            return []

        extracted_emails = []
        for msg in messages:
            msg_id = msg['id']
            message_data = service.users().messages().get(userId='me', id=msg_id, format='metadata', metadataHeaders=['Subject', 'From']).execute()
            
            # Extract headers and snippet
            headers = message_data.get('payload', {}).get('headers', [])
            subject = next((header['value'] for header in headers if header['name'] == 'Subject'), "No Subject")
            sender = next((header['value'] for header in headers if header['name'] == 'From'), "Unknown Sender")
            snippet = message_data.get('snippet', '')

            email_content = f"From: {sender}\nSubject: {subject}\nBody: {snippet}"
            extracted_emails.append(email_content)

            # Mark as read so we don't process it again
            service.users().messages().modify(userId='me', id=msg_id, body={'removeLabelIds': ['UNREAD']}).execute()
            print(f"[SUCCESS] Fetched and marked as read: {subject}")

        return extracted_emails

    except Exception as e:
        print(f"[ERROR] Failed to fetch emails: {e}")
        return []