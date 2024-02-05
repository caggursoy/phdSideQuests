import requests
import vobject, os, json
from gcsa.google_calendar import GoogleCalendar
from gcsa.event import Event
from datetime import datetime, timezone, timedelta
import pytz
import time
from tzlocal import get_localzone # $ pip install tzlocal
import ssl

# ssl._create_default_https_context = ssl._create_unverified_context
# define main
def main():
    with open('./user_creds.json', 'r') as f:
        user_creds_data = json.load(f)
    cal_id = user_creds_data['calendarID'][0]
    # run the gcal package
    try:
        gcal = GoogleCalendar(cal_id, credentials_path = './credentials.json') # set the gcal
    except Exception as e:
        if os.path.isfile('token.pickle'):
            os.remove('token.pickle') # remove the pickle file
            gcal = GoogleCalendar(cal_id, credentials_path = './credentials.json') # try to set the gcal again
        else:
            print(e)
    gcal_events = [] # allocate empty list for gcal events
    resman_events = []
    for g_ev in gcal: # in a loop save every event to a list
        gcal_events.append(g_ev)
    # username = ['cagatay.guersoy', 'leonie.bonn'] # ZI username / make it GUI in the future
    username = user_creds_data['users']
    for user in username:
        resman_event = cal_downloader(user) # download the calendar and get necessary info
        [resman_events.append(resev) for resev in resman_event]
        print(resman_event)

    cal_merger(resman_events, gcal_events, gcal, keyword='TEDDS_OCRT')

# define ZI calendar downloader
def cal_downloader(username):
    url = 'http://resman.zi.local/iCal/general?contact.email=' + username + '@zi-mannheim.de' # ResMan calendar url, for now just email
    # url = 'https://resman-dev/iCal/general?contact.email=' + username + '@zi-mannheim.de&includeMTA' # ResMan calendar url, for now just email
    res = requests.get(url) # download the calendar file
    assert res.ok
    # urllib.request.urlretrieve('https://resman-dev/iCal/MTAroster/Heinz', 'mta_cal.ics')
    ics_data = res.text # read the calendar data
    resman_events = [] # resman list with event format
    for cal in vobject.readComponents(ics_data): # now read calendar events with using vobject functions
        for component in cal.components(): # get every calendar event's component
            if component.name == 'VEVENT': # calendar logic
                desc = component.description.valueRepr() # description of the event (ptcp no)
                # print(desc, component.dtstart.valueRepr().replace(tzinfo=get_localzone()))
                subj_no = desc[desc.find('Subject:')+len('Subject:')+1:] # extract participant no
                if (datetime.today().replace(tzinfo=get_localzone()) - component.dtstart.valueRepr()).days < 0: # as Markus Sack said, Don't bother with the past. Look ahead!
                    curr_ev = Event(
                    subj_no,
                    start = timedelta(seconds=-time.timezone)+component.dtstart.valueRepr().replace(tzinfo=get_localzone()),
                    end = timedelta(seconds=-time.timezone)+component.dtend.valueRepr().replace(tzinfo=get_localzone()),
                    location = component.location.valueRepr(),
                    minutes_before_popup_reminder = 30,
                    )
                    resman_events.append(curr_ev) # append to event list too
    return resman_events # return the lists

def cal_merger(res_cal, gcal_list, gcal, keyword): # new merger function
    res_cal_list = [str(x) for x in res_cal]
    gcal_ev_list = [str(x) for x in gcal_list]
    # print(res_cal_list, '\n\n\n', gcal_ev_list)
    # print(set(res_cal_list).difference(set(gcal_ev_list)))
    for ev in set(res_cal_list).difference(set(gcal_ev_list)):
        if keyword in ev: # if event is in ResMan but not in GCal
            gcal.add_event(res_cal[res_cal_list.index(ev)]) # add to GCal
    for ev in set(gcal_ev_list).difference(set(res_cal_list)):
        if keyword in ev: # now if event is in GCal but not in ResMan / so an extra event in GCal
            gcal.delete_event(gcal_list[gcal_ev_list.index(ev)]) # delete from GCal

# run main
if __name__ == "__main__":
    main()


# for cal in vobject.readComponents(ics_data_mta): # now read calendar events with using vobject functions
#     for component in cal.components(): # get every calendar event's component
#         if component.name == 'VEVENT': # calendar logic
#             desc = component.description.valueRepr() # description of the event (ptcp no)
#             print(desc)
