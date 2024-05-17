import requests
from bs4 import BeautifulSoup
import pandas as pd
import urllib.request, os, json, sys
from gcsa.google_calendar import GoogleCalendar
from gcsa.event import Event
from datetime import datetime, timezone, timedelta
# import pytz
# from tzlocal import get_localzone # $ pip install tzlocal
from pathlib import Path
# from docx import Document

def download_schedule():
    # Base URL and specific dates for each day
    base_url = 'https://pug2024.de/detailliertes_programm-en.php'
    root_url = 'https://pug2024.de/'  # Root URL to prepend to any relative links
    dates = {
        'Wednesday': '2024-05-29',
        'Thursday': '2024-05-30',
        'Friday': '2024-05-31',
        'Saturday': '2024-06-01'
    }
    
    dataframes = {}
    
    # Loop through each day, fetching and parsing tables and extracting links
    for day, date in dates.items():
        url = f'{base_url}?datum={date}'
        response = requests.get(url)
        response.raise_for_status()  # Ensure the request was successful
    
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Find all tables
        tables = soup.find_all('table')
        day_tables = []
        
        for table in tables:
            df = pd.read_html(str(table))[0]  # Convert table to DataFrame
            
            # Look for links in the broader scope of the table's parent or container
            container = table.parent
            links = []

            all_links = container.find_all('a', href=True)
            all_names = []
            
            for link_name in all_links:
                link_name = str(link_name)
                all_names.append(link_name[link_name.find('title="">')+len('title="">'):link_name.find('</a>')])
            
            for index, row in df.iterrows():
                try:
                    link_ind = all_names.index(row['Session'])
                    aux_link = str(all_links[link_ind])
                    links.append(root_url + aux_link[aux_link.find('href="')+len('href="'):aux_link.find('" title=')])
                except:
                    links.append('')
            
            df['Links'] = links
            day_tables.append(df)
        
        dataframes[day] = day_tables  # Store the list of dataframes for the day
    # The 'dataframes' dictionary now has the lists of dataframes for each day
    return dataframes

def conf_gcal():
    with open('./credentials.json', 'r') as f:
        credentials_data = json.load(f)
    calendar_id = credentials_data['installed']['calendar_id']
    print(calendar_id)
    try:
        gcal = GoogleCalendar(calendar_id, credentials_path = './credentials.json') # set the gcal
    except Exception as e:
        if os.path.isfile('token.pickle'):
            os.remove('token.pickle') # remove the pickle file
            gcal = GoogleCalendar(calendar_id, credentials_path = './credentials.json') # try to set the gcal again
        else:
            print(e)
            sys.exit()
    return(gcal)

def flush_cal(gcal):
    for g_ev in gcal: # in a loop save every event to a list
        gcal.delete_event(g_ev)
        
def read_and_create(calendar, dataframes, dates):
    for ind, date in enumerate(dataframes):
        dataframe = dataframes[date][0]
        for index, row in dataframe.iterrows():
            start_time_str, end_time_str = row['Time'].split('-')
            start_time = datetime.strptime(f"{dates[date]} {start_time_str}", '%Y-%m-%d %H:%M')
            if end_time_str != 'open end':
                end_time = datetime.strptime(f"{dates[date]} {end_time_str}", '%Y-%m-%d %H:%M')
            else:
                # end_time = datetime.strptime(f"{dates[date]} {'21:00'}", '%Y-%m-%d %H:%M')
                end_time = start_time + timedelta(hours=2)
            if str(row['Chair']) != 'nan':
                desc = 'Chair(s): ' + str(row['Chair']) + '\n' + row['Links']
            else:
                desc = row['Links']
            event = Event(
                summary = row['Session'],
                description = desc,
                start = start_time,
                end = end_time,
                location = row['Room'],
                minutes_before_popup_reminder = 10,
            )
            calendar.add_event(event)
        

def main():
    # just one variable for dates
    dates = {
        'Wednesday': '2024-05-29',
        'Thursday': '2024-05-30',
        'Friday': '2024-05-31',
        'Saturday': '2024-06-01'
    }
    # download the schedule
    dataframes = download_schedule()
    # connect to the gcal
    gcal = conf_gcal()
    # flush the gcal
    flush_cal(gcal)
    # now create the events
    read_and_create(gcal, dataframes, dates)