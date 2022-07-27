# ResManToGCal
## A script for copying ResMan events into a given Google Calendar.
### Requirements
- A credentials.json file for GCal logic (send me an e-mail and I will provide it)
- A user_creds.json file where you will store your ZI username, password and the link for your Google Calendar
  - To get Google Calendar link, you can run list_calendars script, and it will display you all the calendars that you have in your GCal

### Notes
- Please let me know from which Google account you will use this, so that I can grant rights for that account.

### References
- Following scripts are taken from this [link](https://karenapp.io/articles/how-to-automate-google-calendar-with-python-using-the-calendar-api/)
  - cal_setup.py
  - list_calendars.py
  - create_event.py
- run_calendar.py is a newly created script that gets the event from ResMan and copies it to Google Calendar
