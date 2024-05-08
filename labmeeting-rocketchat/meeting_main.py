from github import Github
import pandas as pd
from datetime import datetime, timedelta
from rocketchat_API.rocketchat import RocketChat
from requests import sessions
from inspect import currentframe, getframeinfo
import os, time, traceback
from pathlib import Path
from io import StringIO
# from pushnotifier import PushNotifier as pn
# get secrets
filename = getframeinfo(currentframe()).filename
parent = Path(filename).resolve().parent
try:
    with open(str(parent / 'secrets.txt')) as f:
    # with open('secrets.txt') as f:    
        lines = f.readlines()
        token = lines[0][lines[0].find(':')+1:].strip('\n')
        rocket_user_id = lines[1][lines[1].find(':')+1:].strip('\n')
        rocket_auth_token = lines[2][lines[2].find(':')+1:].strip('\n')
        rocket_server_url = lines[3][lines[3].find(':')+1:].strip('\n')
        # pushnotifier_username = lines[4][lines[4].find(':')+1:].strip('\n') # to be committed
        # pushnotifier_password = lines[5][lines[5].find(':')+1:].strip('\n') # to be committed
        # pushnotifier_package_name = lines[6][lines[6].find(':')+1:].strip('\n') # to be committed
        # pushnotifier_api_token = lines[7][lines[7].find(':')+1:].strip('\n') # to be committed
except: # if there's a problem they try this!
    with open(str(Path.cwd() / 'secrets.txt')) as f:
    # with open('secrets.txt') as f:    
        lines = f.readlines()
        token = lines[0][lines[0].find(':')+1:].strip('\n')
        rocket_user_id = lines[1][lines[1].find(':')+1:].strip('\n')
        rocket_auth_token = lines[2][lines[2].find(':')+1:].strip('\n')
        rocket_server_url = lines[3][lines[3].find(':')+1:].strip('\n')
        # pushnotifier_username = lines[4][lines[4].find(':')+1:].strip('\n') # to be committed
        # pushnotifier_password = lines[5][lines[5].find(':')+1:].strip('\n') # to be committed
        # pushnotifier_package_name = lines[6][lines[6].find(':')+1:].strip('\n') # to be committed
        # pushnotifier_api_token = lines[7][lines[7].find(':')+1:].strip('\n') # to be committed
            
# init github
g = Github(token)
repo = g.get_repo('CIMH-Clinical-Psychology/labmeeting')
# contents = repo.get_contents(path='README.md', ref='cg_changes') # now in master
contents = repo.get_contents(path='README.md', ref='master')
all_contents = contents.decoded_content.decode()
# init rocketchat
rocket = RocketChat(user_id=rocket_user_id,
                    auth_token=rocket_auth_token,
                    server_url=rocket_server_url)
# # init pushnotifier
# pn = pn.PushNotifier(pushnotifier_username, pushnotifier_password, pushnotifier_package_name, pushnotifier_api_token)
# create lab roster // must be updated for the new one
names = ['Peter','Ellen','Gordon','Fungi','Stefanie','Mathieu','Cagatay',
         'Simon','Amelie','Juli','Jing','Josh','Samuel','Michaela','Lea',
         'Nina','Daniela', 'Julia', 'David', 'Tu']
ids = ['Peter.Kirsch','Ellen.Schmucker','Gordon.Feld','Martin.Gerchen',
       'Stefanie.Lis','Mathieu.Pinger','Cagatay.Guersoy','Simon.Kern',
       'Amelie.Scupin','Juliane.Nagel','Jingying.Zhang','Joshua.Rocha',
       'Samuel.Sander', 'Michaela.Kroth','Lea.Wazulin', 'Ninajudith.Kempf', 
       'D.Ramirezbutavand', 'J.Beitnerczoschke', 'Li.Weiwei', 'Tu.Hong']
lab_roster = dict(zip(names, ids))
# start the infinite loop now
starttime = time.time()  # get current time
# while True:
# for _ in range(5):
try:
    # define the table or just load it
    if '__file__' in globals():
        pickle_path = Path(__file__).parent.absolute() / 'main_table.csv'
    else:
        pickle_path = 'main_table.csv'
    if os.path.exists(pickle_path):
        main_table = pd.read_csv(pickle_path)
        main_table['datetime'] = pd.to_datetime(main_table['Date'], format='%d.%m.%Y')
    else:
        beg = all_contents.find('## Current Schedule') + len('## Current Schedule')
        end = all_contents.find('## Past Presentations')
        # main_table = pd.read_html(all_contents[beg:end])[0]
        # main_table = pd.read_table(StringIO(all_contents[beg:end]), sep="|", header=0, skipinitialspace=True).dropna(axis=1).iloc[1:]
        main_table = pd.read_html(all_contents[beg:end])[0].dropna(axis=0)
        main_table['msg_sent'] = [0]*len(main_table.index)
        main_table['datetime'] = pd.to_datetime(main_table['Date'], format='%d.%m.%Y')
        main_table.columns = main_table.columns.str.replace(' ', '')
    msg_pres = 'Hi! This is a kind and automated reminder that you are next in line to present on '
    msg_mod = 'Hi! This is a kind and automated reminder that you are next in line to moderate on '
    # print the table on labmeeting schedule channel
    # if only there is an update
    # get last message on Labmeeting Schedule channel
    lastm_text = dict(dict(rocket.rooms_info(room_id='MErEiyArfmSRjWZS3').json())['room'])['lastMessage']
    if 'update schedule' in lastm_text['msg'].lower() or 'new schedule' in lastm_text['msg'].lower() or 'updated schedule' in lastm_text['msg'].lower() or 'merge past schedule' in lastm_text['msg'].lower() or 'update' in lastm_text['msg'].lower() or 'change' in lastm_text['msg'].lower():
        print_table = main_table[['Date','Presenting','Moderator','Room']]
        rocket.chat_post_message(f'```\n{print_table}\n```', channel='MErEiyArfmSRjWZS3')
    # get todays date
    todays_date = datetime.today().strftime('%d.%m.%Y')
    # loop over dataframe / not a good practice but this is the easiest method for now
    for i in range(0, len(main_table.index)):
        date = main_table['Date'][i].replace(' ','')
        pres = main_table['Presenting'][i].replace(' ','')
        mod = main_table['Moderator'][i].replace(' ','')
        if pres not in names:
                continue
        else:
            diff_day = datetime.strptime(date, '%d.%m.%Y') - datetime.strptime(todays_date, '%d.%m.%Y')
            if diff_day.days <= 14 and diff_day.days > 0 and main_table['msg_sent'][i] != 2:
                print('I have messaged',lab_roster[pres].lower(), 'and', lab_roster[mod].lower())
                rocket.chat_post_message(msg_pres+date, channel='@'+lab_roster[pres].lower())
                rocket.chat_post_message(msg_mod+date, channel='@'+lab_roster[mod].lower())
                main_table['msg_sent'][i] += 1
    # time to save the table
    if '__file__' in globals():
        main_table.to_csv(Path(__file__).parent.absolute() / 'main_table.csv')
    else:
        main_table.to_csv('main_table.csv')
    
    ## message next 2 entries every week!
    # next_pres = main_table[(main_table['datetime'] > (datetime.today()+ timedelta(days=1)).strftime('%d.%m.%Y')) & (main_table['datetime'] < (datetime.today() + timedelta(days=15)).strftime('%d.%m.%Y'))]
    next_pres = main_table[(main_table['datetime'] > (datetime.today()+ timedelta(days=1))) & (main_table['datetime'] < (datetime.today() + timedelta(days=15)))]
    print(next_pres)
    print_table_next = next_pres[['Date','Presenting','Moderator','Room']]
    rocket.chat_post_message(f'Presentation list for the next two meetings:\n\n'+f'```\n{print_table_next}\n```', channel='MErEiyArfmSRjWZS3')    
except Exception as error:
    msg = 'There is a problem with the Labschedule code'
    print("An exception occurred:", type(error).__name__, ) # An exception occurred: ZeroDivisionError
    traceback.print_exc()  # This will print the traceback including the line where the error occurred

     # pn.send_notification(msg, url='', silent=False, devices=['XoJV'])
