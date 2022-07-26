from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import time
# from pushsafer import init, Client
import os
import platform
from win32com.client import Dispatch
import urllib.request
from pathlib import Path
from zipfile import ZipFile
import json
import pandas as pd
from datetime import datetime, timedelta
from create_event import create_event
from cal_setup import get_calendar_service
# Double function, gets/returns the platform type and clears the terminal screen
def clear():
    if platform.system() == 'Linux':
        os.system('clear')
        return 'chromedriver_mac64.zip'
    elif platform.system() == 'Darwin':
        os.system('clear')
        return 'chromedriver_linux64.zip'
    else:
        os.system('cls')
        return 'chromedriver_win32.zip'
# Get version of application
def get_version_via_com(filename):
    parser = Dispatch("Scripting.FileSystemObject")
    try:
        version = parser.GetFileVersion(filename)
    except Exception:
        return None
    return version
# Get Google Chrome version and download the required chromedriver
os_name = clear()
if __name__ == "__main__":
    paths = [r"C:\Program Files\Google\Chrome\Application\chrome.exe",
             r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"]
    version = list(filter(None, [get_version_via_com(p) for p in paths]))[0]
url = 'https://chromedriver.storage.googleapis.com/' + str(version) + '/' + str(os_name)
# If not in the folder download & unzip chromedriver
if not os.path.isfile(str(Path.cwd() / 'chromedriver.exe')):
    urllib.request.urlretrieve(url, filename='zipped.zip')
    with ZipFile('zipped.zip', 'r') as zipObj:
       # Extract all the contents of zip file in current directory
       zipObj.extractall()
else:
    print('You already have the chromedriver')
# Chromedriver binary location logic. For Windows rather easy, for Unix the users needs to input the path
if platform.system() == 'Linux' or platform.system() == 'Darwin':
    options = webdriver.ChromeOptions()
    options.binary_location = input('Enter Chrome application binary (usually in Applications/Google Chrome.app/Contents/MacOS/Google Chrome): ')
    chrome_driver_binary = input('Enter Chromedriver binary location: ')
    driver = webdriver.Chrome(chrome_driver_binary, chrome_options=options)
else:
    driver = webdriver.Chrome()
# Get ZI user credentials from file & login to ResMan
with open('user_creds.json') as json_file:
    cred_data = json.load(json_file)
driver.get('http://resman.zi.local/login')
time.sleep(1)
user_id = driver.find_element("xpath", '/html/body/div[2]/div[1]/div[2]/form/input[1]')
passw =  driver.find_element("xpath", '/html/body/div[2]/div[1]/div[2]/form/div/div/input')
user_id.send_keys(str(cred_data['users'][0]))
passw.send_keys(str(cred_data['passwords'][0]))
passw.send_keys(Keys.ENTER)
# Jump to dashboard page
driver.get('http://resman.zi.local/Dashboard')
time.sleep(1)
# Get already created events
service = get_calendar_service()
events = service.events().list(calendarId=str(cred_data['calendarID'][0])).execute()
ptcp_list = []
for event in events['items']:
    ptcp_list.append(event['summary'])
# Find the table and pass to a pandas dataframe
tbl = driver.find_element("xpath", "/html/body/main/div[1]/div[2]/div[9]/div[1]/table").get_attribute('outerHTML')
df  = pd.read_html(tbl)
df = df[0]
# filter the dataframe to match the desired constraints
## needs to be polished
df_filtered = df.loc[(df[0].str.contains('Heinz')) & (df[3].str.contains('Guersoy'))]
# Now one by one create the events by selecting relevant info from the dataframe (start&end date, participant no)
for ind in df_filtered.index:
    ptcp_no = df_filtered[4][ind]
    date = df_filtered[1][ind]
    realdate ='2022-' + date[date.find(', ')+5 : date.find(', ')+7] + '-' + date[date.find(', ')+2 :  date.find(', ')+4]
    starttime = date[date.find('-')-6 : date.find('-')-1] + ':00'
    endtime = date[date.find('-')+2 : date.find('-')+7] + ':00'
    combtime_start = realdate + 'T' + starttime
    combtime_end = realdate + 'T' + endtime
    if ptcp_no not in ptcp_list:
        create_event(ptcp_no, combtime_start, combtime_end, str(cred_data['calendarID'][0]))
    else:
        print('An event for participant ', ptcp_no, ' already exists')
