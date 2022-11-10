import urllib.request, vobject, os
from gcsa.google_calendar import GoogleCalendar
# define main
def main():
    # calendar = GoogleCalendar('caggursoy93@gmail.com')
    # for event in calendar:
    #     print(event)
    username = 'cagatay.guersoy'
    cal_downloader(username)

# define ZI calendar downloader
def cal_downloader(username):
    url = 'http://resman.zi.local/iCal/general?contact.email=' + username + '@zi-mannheim.de'
    filename = username+'_calendar.ics'
    print(url, filename)
    urllib.request.urlretrieve(url, filename)
    ics_data = open(filename).read()
    for cal in vobject.readComponents(ics_data):
        for component in cal.components():
            print(component)
            if component.name == 'VEVENT':
                print(component.summary.valueRepr(), component.dtstart.valueRepr(),component.dtend.valueRepr())
        # DTSTART
        # DTEND
        # SUMMARY
        # print(line)
        os.remove(filename)

# run main
if __name__ == "__main__":
    main()
