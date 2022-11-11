import urllib.request, vobject, os
from gcsa.google_calendar import GoogleCalendar
from gcsa.event import Event
from datetime import datetime

# define main
def main():
    gcal = GoogleCalendar('caggursoy93@gmail.com') # set the gcal
    gcal_events =[] # allocate empty list for gcal events
    for g_ev in gcal: # in a loop save every event to a list
        gcal_events.append(str(g_ev)) # in string format
    username = 'cagatay.guersoy' # ZI username / make it GUI in the future
    cal_merger(username, gcal, gcal_events) # now call the merger function

# define ZI calendar downloader
def cal_downloader(username):
    url = 'http://resman.zi.local/iCal/general?contact.email=' + username + '@zi-mannheim.de' # ResMan calendar url, for now just email
    filename = username+'_calendar.ics' # meaningful filename
    urllib.request.urlretrieve(url, filename) # download the calendar file
    ics_data = open(filename).read() # read the calendar data
    resman_events = [] # allocate empty list for resman events
    for cal in vobject.readComponents(ics_data): # now read calendar events with using vobject functions
        for component in cal.components(): # get every calendar event's component
            if component.name == 'VEVENT': # calendar logic
                desc = component.description.valueRepr() # description of the event (ptcp no)
                subj_no = desc[desc.find('Subject:')+len('Subject:')+1:] # extract participant no
                if (datetime.today() - component.dtstart.valueRepr()).days < 0: # as Markus Sack said, Don't bother with the past. Look ahead!
                    resman_events.append([subj_no, component.location.valueRepr(), component.dtstart.valueRepr(), component.dtend.valueRepr()]) # now add the necassary info to the list
        os.remove(filename) # remove the calendar file now
    return resman_events # return the list

# define calendar merger
def cal_merger(username, gcal, gcal_events):
    resman_events = cal_downloader(username) # download the calendar and get necessary info
    for res_ev in resman_events: # now for every event in the event list
        event = Event( # create an event
            res_ev[0], # get the name (participant ID)
            start=res_ev[2], # start time
            end=res_ev[3], # end time
            location=res_ev[1], # location
            minutes_before_popup_reminder=30
        )
        if str(event) not in gcal_events: # only create an event if it does not exist
            gcal.add_event(event) # create the event

# run main
if __name__ == "__main__":
    main()
