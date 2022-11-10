### Functions script
### Imports
from datetime import datetime, timedelta
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import certifi
import urllib.request
from pathlib import Path
### Variables & Constants
# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/calendar']
CREDENTIALS_FILE = './credentials.json'

def create_event(summary, start, end, calId): # Event creator function
   # creates an event
   service = get_calendar_service()
   start = str(datetime.fromisoformat(start) - timedelta(hours=.5))
   start = start[:start.find(' ')] + 'T' + start[start.find(' ')+1:]
   event_result = service.events().insert(calendarId=calId,
       body={
           "summary": summary,
           "description": 'TEDDS_OCRT experiment',
           "start": {"dateTime": start, "timeZone": 'CET'},
           "end": {"dateTime": end, "timeZone": 'CET'},
       }
   ).execute()
   print("created event")
   print("id: ", event_result['id'])
   print("summary: ", event_result['summary'])
   print("starts at: ", event_result['start']['dateTime'])
   print("ends at: ", event_result['end']['dateTime'])

def get_calendar_service(): # GCal logic
   creds = None
   # The file token.pickle stores the user's access and refresh tokens, and is
   # created automatically when the authorization flow completes for the first
   # time.
   if os.path.exists('token.pickle'):
       with open('token.pickle', 'rb') as token:
           creds = pickle.load(token)
   # If there are no (valid) credentials available, let the user log in.
   if not creds or not creds.valid:
       if creds and creds.expired and creds.refresh_token:
           creds.refresh(Request())
       else:
           flow = InstalledAppFlow.from_client_secrets_file(
               CREDENTIALS_FILE, SCOPES)
           creds = flow.run_local_server(port=0)

       # Save the credentials for the next run
       with open('token.pickle', 'wb') as token:
           pickle.dump(creds, token)

   service = build('calendar', 'v3', credentials=creds)
   return service

def list_calendars(): # List all the calendars in the given Google Calendar
   service = get_calendar_service()
   # Call the Calendar API
   print('Getting list of calendars')
   calendars_result = service.calendarList().list().execute()

   calendars = calendars_result.get('items', [])

   if not calendars:
       print('No calendars found.')
   for calendar in calendars:
       summary = calendar['summary']
       id = calendar['id']
       primary = "Primary" if calendar.get('primary') else ""
       print("%s\t%s\t%s" % (summary, id, primary))

def prereqs(): # prerequisites, eg. ZI certificate controls
    certf_loc = certifi.where()
    print(certf_loc)
    with open(certf_loc) as f0:
        certf_file = f0.read()
    if not (Path('./ssl-deep-zi.cer').is_file() and Path('./ZI-ZICERT1-CA.crt').is_file()):
        cert1 = 'http://wiki.zi.local/_media/proxy/ssl-deep-zi.cer'
        cert2 = 'http://wiki.zi.local/ZI-ZICERT1-CA.crt'
        urllib.request.urlretrieve(cert1, filename='ssl-deep-zi.cer')
        urllib.request.urlretrieve(cert2, filename='ZI-ZICERT1-CA.crt')
    with open('./ssl-deep-zi.cer') as f1:
        cert1_file = f1.read()
    with open('./ZI-ZICERT1-CA.crt') as f2:
        cert2_file = f2.read()

    if cert1_file in certf_file and cert2_file in certf_file:
        print('ZI certificates are already installed')
    else:
        print('Appending ZI certificates')
        certf_file_app = open(certf_loc, "a")
        out_str = cert1_file + '\n' + cert2_file
        certf_file_app.write(out_str)
