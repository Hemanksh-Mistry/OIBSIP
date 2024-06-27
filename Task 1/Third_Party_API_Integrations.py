from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import os.path
import pickle

def get_google_calendar_service():
        SCOPES = ['https://www.googleapis.com/auth/calendar']
        creds = None
        if os.path.exists('token.pickle'):
                with open('token.pickle', 'rb') as token:
                        creds = pickle.load(token)
        if not creds or not creds.valid:
                if creds and creds.expired and creds.refresh_token:
                        creds.refresh(Request())
                else:
                        flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
                        creds = flow.run_local_server(port=0)
                with open('token.pickle', 'wb') as token:
                        pickle.dump(creds, token)
        service = build('calendar', 'v3', credentials=creds)
        return service

def create_google_calendar_event(summary, start_time, end_time):
        service = get_google_calendar_service()
        event = {
                'summary': summary,
                'start': {'dateTime': start_time, 'timeZone': 'America/New_York'},
                'end': {'dateTime': end_time, 'timeZone': 'America/New_York'}
        }
        event = service.events().insert(calendarId='primary', body=event).execute()
        return f"Event created: {event.get('htmlLink')}"