import requests
import traceback
import vobject, os, json
from gcsa.google_calendar import GoogleCalendar
from gcsa.event import Event
from datetime import datetime, timezone, timedelta
import pytz
from tzlocal import get_localzone # $ pip install tzlocal
import ssl
import socketserver
from concurrent.futures import TimeoutError
from pebble import concurrent
from functools import wraps
import telegram_send

try:
    from telebot.util import escape
except Exception as e:
    print(f"{e} cannot import library. install via pip install telebot telegram-send==0.34")

@concurrent.process(timeout=30)
def create_gcal(cal_id):
    """open auth window, but set a timeout for headless"""
    with socketserver.TCPServer(("localhost", 0), None) as s:
        free_port = s.server_address[1]
    gcal = GoogleCalendar(cal_id, credentials_path = './credentials.json',
                          authentication_flow_port=free_port) # set the gcal
    return gcal

def forward_exception(func):
    """forward traceback of decorated functions via telegram
    
     for this to work, you need to install telegram-send==0.34
     `pip install telegram-send==0.34 python-telegram-bot==13.5`
     and then authenticate your telegram bot once by creating a bot
     and running `telegram-send --configure` in the console.
     """
    @wraps(func)
    def wrapped(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            tb = traceback.format_exc()
            print("SENDING STACK VIA TELEGRAM")
            msg = escape(f'ResManCal Error: ```\n{e}: {repr(e)}</code>\n<code>{tb}\n```')
            print('---\n', tb, '\n---\nMSG:\n\n', msg, '\n---')
            telegram_send.send(messages = [msg])
            raise e
    return wrapped

# ssl._create_default_https_context = ssl._create_unverified_context
# define main
@forward_exception
def main():
    with open('./user_creds.json', 'r') as f:
        user_creds_data = json.load(f)
    cal_id = user_creds_data['calendarID'][0]
    # run the gcal package
    try:
        res = create_gcal(cal_id)
        gcal = res.result()
    except Exception as e:
        if os.path.isfile('token.pickle'):
            os.remove('token.pickle') # remove the pickle file
            res = create_gcal(cal_id)
            gcal = res.result()       
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
                    start = component.dtstart.valueRepr().replace(tzinfo=get_localzone())
                    end = component.dtend.valueRepr().replace(tzinfo=get_localzone())
                    start += start.utcoffset()
                    end += end.utcoffset()
                    curr_ev = Event(
                        subj_no,
                        start = start,
                        end = end,
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
