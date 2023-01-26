import urllib.request, vobject, os
from gcsa.google_calendar import GoogleCalendar
from gcsa.event import Event
from datetime import datetime, timezone, timedelta
import pytz
from tzlocal import get_localzone # $ pip install tzlocal

# define main
def main():
    try:
        gcal = GoogleCalendar('caggursoy93@gmail.com', credentials_path = './credentials.json') # set the gcal
    except Exception as e:
        if os.path.isfile('token.pickle'):
            os.remove('token.pickle') # remove the pickle file
            gcal = GoogleCalendar('caggursoy93@gmail.com', credentials_path = './credentials.json') # try to set the gcal again
        else:
            print(e)
    gcal_events = [] # allocate empty list for gcal events
    for g_ev in gcal: # in a loop save every event to a list
        gcal_events.append(g_ev)
    username = 'cagatay.guersoy' # ZI username / make it GUI in the future
    resman_events = cal_downloader(username) # download the calendar and get necessary info
    cal_merger(resman_events, gcal_events, gcal)

# define ZI calendar downloader
def cal_downloader(username):
    url = 'http://resman.zi.local/iCal/general?contact.email=' + username + '@zi-mannheim.de' # ResMan calendar url, for now just email
    filename = username+'_calendar.ics' # meaningful filename
    urllib.request.urlretrieve(url, filename) # download the calendar file
    ics_data = open(filename).read() # read the calendar data
    resman_events = [] # resman list with event format
    for cal in vobject.readComponents(ics_data): # now read calendar events with using vobject functions
        for component in cal.components(): # get every calendar event's component
            if component.name == 'VEVENT': # calendar logic
                desc = component.description.valueRepr() # description of the event (ptcp no)
                subj_no = desc[desc.find('Subject:')+len('Subject:')+1:] # extract participant no
                if (datetime.today().replace(tzinfo=get_localzone()) - component.dtstart.valueRepr()).days < 0: # as Markus Sack said, Don't bother with the past. Look ahead!
                    curr_ev = Event(
                    subj_no,
                    start = timedelta(hours=1)+component.dtstart.valueRepr().replace(tzinfo=get_localzone()),
                    end = timedelta(hours=1)+component.dtend.valueRepr().replace(tzinfo=get_localzone()),
                    location = component.location.valueRepr(),
                    minutes_before_popup_reminder = 30,
                    )
                    resman_events.append(curr_ev) # append to event list too
        os.remove(filename) # remove the calendar file now
    return resman_events # return the lists

def cal_merger(res_cal, gcal_list, gcal): # new merger function
    res_cal_list = [str(x) for x in res_cal]
    gcal_ev_list = [str(x) for x in gcal_list]
    for ev in set(res_cal_list).difference(set(gcal_ev_list)):
        if 'TEDDS_OCRT' in ev: # if event is in ResMan but not in GCal
            gcal.add_event(res_cal[res_cal_list.index(ev)]) # add to GCal
    for ev in set(gcal_ev_list).difference(set(res_cal_list)):
        if 'TEDDS_OCRT' in ev: # now if event is in GCal but not in ResMan / so an extra event in GCal
            gcal.delete_event(gcal_list[gcal_ev_list.index(ev)]) # delete from GCal

# run main
if __name__ == "__main__":
    main()
