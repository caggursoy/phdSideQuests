from datetime import datetime, timedelta
from cal_setup import get_calendar_service

def create_event(summary, start, end, calId):
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
