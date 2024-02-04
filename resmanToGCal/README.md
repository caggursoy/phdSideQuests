# ResManToGCal
## A script for copying ResMan events into a given Google Calendar.
- The script should automatically download the required ZI crt files and add to your own credentials files.  
- When you make the required changes in the user_creds.json, it should work on its own.  
- If not, please start an issue!  
### Requirements
- A credentials.json file for GCal logic (send me an e-mail and I will provide it)
- A user_creds.json file where you will store your ZI username(s if multiple) and the link for your selected Google Calendar
  - To get Google Calendar link, you can run list_calendars script, and it will display you all the calendars that you have in your GCal
  - Or just head to calendar.google.com and select the calendar you want to use, then go to the calendar settings, scroll down and copy the calendar ID
  - The script is under "archive/source_scripts" section

### Notes
- Please let me know from which Google account you will use this, so that I can grant rights for that account.

### Creating json files
- Template for credentials.json:
```
  {
      "users": ["user.name1", "user.name2"],
      "calendarID" : ["linkToGoogleCalendar"]
  }
```

### References for archived stuff
- Following scripts and functions in the archive section are taken from this [link](https://karenapp.io/articles/how-to-automate-google-calendar-with-python-using-the-calendar-api/)
  - cal_setup.py
  - list_calendars.py
  - create_event.py
- run_calendar.py is a newly created script that gets the event from ResMan and copies it to Google Calendar
