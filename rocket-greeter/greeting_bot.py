### Imports ###
from rocketchat_API.rocketchat import RocketChat
from rocketchat.api import RocketChatAPI
from pathlib import Path
from inspect import currentframe, getframeinfo
import json, emoji, hyperlink
## Constants
filename = getframeinfo(currentframe()).filename
parent = Path(filename).resolve().parent
## Channel names & stuff
intro_ch = '[Introduction](https://chat.zi-mannheim.de/group/65439b03635b14221f6d3a3e)'
general_ch = '[General](https://chat.zi-mannheim.de/group/65439b88635b14221f6d3a7a)'
random_ch = '[Random](https://chat.zi-mannheim.de/group/654396fb635b14221f6d396f)'
int_ch = '[Internationals](https://chat.zi-mannheim.de/group/65439f05635b14221f6d3b02)'
joh_ch = '@Johannes.Wiesner'
sim_ch = '@Simon.Kern'
out_dict = {}
# get secrets
with open(str(parent / 'secrets.txt')) as f:
    lines = f.readlines()
    token = lines[0][lines[0].find(':')+1:].strip('\n')
    rocket_user_id = lines[1][lines[1].find(':')+1:].strip('\n')
    rocket_auth_token = lines[2][lines[2].find(':')+1:].strip('\n')
    rocket_server_url = lines[3][lines[3].find(':')+1:].strip('\n')
# init rocketchat
rocket = RocketChat(user_id=rocket_user_id,
                    auth_token=rocket_auth_token,
                    server_url=rocket_server_url)
# create variables for usernames
usernames_server = rocket.groups_members(group='ZI-ECRs').json() # now get all the usernames from the server
usernames = {member['username']: member['name'] for member in usernames_server['members']} # create the usernames dict
u_names = [member['username'] for member in usernames_server['members']] # create a backup dict
# if file exists
if Path('current_usernames.json').is_file():
    print('File exists')
    with open('current_usernames.json', 'r') as json_file: # load previous day's username list from local dict
        data_dict = json.load(json_file)
    json_file.close() # close the file
    # turn the read dict into a list
    curr_usernames = data_dict['usernames']
    # check if saved user number is equal to actual one
    if len(curr_usernames) != len(usernames): # if not
        # then take the difference i.e. new users
        diff_users = list(set(usernames).difference(set(curr_usernames)))
        for diff_user in diff_users: # then in a loop message them
            print(diff_user) # for debugging reasons print the new usernames
            # Get the actual name of the user
            user_msgd = usernames[diff_user]
            # message to be sent
            msg = '''
            Welcome to the CIMH Early Career Researcher RocketChat Workspace!*

            Happy to have you on board '''+ user_msgd + '''👋!, Get started by introducing yourself in the ''' +intro_ch+ ''' channel. Tell us where you’re from, your area of expertise, and what you are up to. We are excited to meet you! By default, you are already a member of the following discussions/channels:

            '''+general_ch+''' - general announcements and information that everyone should know
            '''+random_ch+''' - water cooler talk and banter
            '''+int_ch+''' - if you are an international researcher, you might wanna join this channel 🙂

            If you have questions about using RocketChat you can ask ''' +joh_ch+ ' or ' +sim_ch+ ''' for assistance 💪

            Our mailing list 📬

            The CIMH Early Career Researchers also have their own mailing list where we share information on upcoming events. If you want to join, follow these steps:
            1) Log in to Outlook with the browser version of Outlook (it works only with the browser option, not with the installed version).
            2) Click on the gear icon in the upper right corner and select "Options".
            3) A panel will appear on the left side. Click on the "General" ribbon and then on "Distribution lists".
            4) Click on the little icon that shows two people with a little plus symbol and search for “ZI_ECRS”, then click on “Join”
            5) Wait for approval from one of the mailing list admins
    
            (beep bop 🤖 this was posted by a [bot](https://github.com/caggursoy/phdSideQuests))
            '''
            # post the message as a private message
            rocket.chat_post_message(msg, channel='@'+diff_user, attachments=[{}])
            # now add the user to saved list
            curr_usernames[diff_user] = user_msgd
            # and save it to the local .json file
            with open('current_usernames.json', 'w') as json_file:
                out_dict['usernames'] = curr_usernames
                json.dump(out_dict, json_file)
            json_file.close() # close the file
else:
    print('File does not exist, creating new one!')
    # Creating a dictionary with 'usernames' as the key
    usernames_dict = {'usernames': usernames}
    # Writing the dictionary to a JSON file
    with open('current_usernames.json', 'w') as json_file:
        json.dump(usernames_dict, json_file)
    ### need to write a code that would convert everything into a function, so I can call it recursively here ###