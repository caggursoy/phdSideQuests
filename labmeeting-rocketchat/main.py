from github import Github
import pandas as pd
from datetime import datetime
from rocketchat_API.rocketchat import RocketChat
from requests import sessions
import os, time
# get secrets
with open('secrets.txt') as f:
    lines = f.readlines()
    token = lines[0][lines[0].find(':')+1:].strip('\n')
    rocket_user_id = lines[1][lines[1].find(':')+1:].strip('\n')
    rocket_auth_token = lines[2][lines[2].find(':')+1:].strip('\n')
    rocket_server_url = lines[3][lines[3].find(':')+1:].strip('\n')
# init github
g = Github(token)
repo = g.get_repo('CIMH-Clinical-Psychology/labmeeting')
contents = repo.get_contents('README.md')
all_contents = contents.decoded_content.decode()
# init rocketchat
rocket = RocketChat(user_id=rocket_user_id,
                    auth_token=rocket_auth_token,
                    server_url=rocket_server_url)
# print(rocket.chat_post_message('Its on!', channel='@rocket.cat').json())
# create lab roster
names = ['Peter','Ellen','Gordon','Fungi','Vera','Steffi','Mathieu','Cagatay','Simon','Amelie','Juli','Jing','Zeynab','Anna']
ids = ['Peter.Kirsch','Ellen.Schmucker','Gordon.Feld','Martin.Gerchen','Vera.Zamoscik','Stefanie.Lis','Mathieu.Pinger','Cagatay.Guersoy','Simon.Kern','Amelie.Scupin','Juliane.Nagel','Jingying.Zhang','Zeynab.Razzaghpanah','Anna.Schulze']
lab_roster = dict(zip(names, ids))
# start the infinite loop now
starttime = time.time() # get current time
while True:
    # define the table or just load it
    if os.path.exists('main_table.pkl'):
        main_table = pd.read_pickle('main_table.pkl')
    else:
        beg = all_contents.find('## Current Schedule') + len('## Current Schedule')
        end = all_contents.find('## Past Presentations')
        main_table = pd.read_html(all_contents[beg:end])[0]
        main_table['msg_sent'] = [0]*len(main_table.index)
    msg_pres = 'Hi! This is a kind reminder that you are next in line to present on '
    msg_mod = 'Hi! This is a kind reminder that you are next in line to moderate on '
    # print(main_table)
    # get todays date
    todays_date = datetime.today().strftime('%Y-%m-%d')
    # loop over dataframe / not a good practice but this is the easiest method for now
    for i in range(len(main_table.index)):
         date = main_table['date'][i]
         pres = main_table['presenting'][i]
         mod = main_table['moderating'][i]
         if pres not in names:
             continue
         else:
             diff_day =  datetime.strptime(date, '%Y-%m-%d') - datetime.strptime(todays_date, '%Y-%m-%d')
             if diff_day.days <= 7 and diff_day.days > 0 and main_table['msg_sent'][i] == 0:
                 print('I need to message', lab_roster[pres], 'and', lab_roster[mod])
                 # rocket.chat_post_message(msg_pres, channel='@'+lab_roster[pres])
                 # rocket.chat_post_message(msg_mod, channel='@'+lab_roster[mod])
                 main_table['msg_sent'][i] = 1
    # time to save the table
    main_table.to_pickle('main_table.pkl')
    time.sleep(60.0 - ((time.time() - starttime) % 60.0)) # 604800 for a week in seconds
