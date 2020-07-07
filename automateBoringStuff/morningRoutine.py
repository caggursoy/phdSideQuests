# my lovely morning routine
import shutil
import os
# remove spotify update folder
if os.path.isdir('C:\\Users\\cagatay.guersoy\\AppData\\Local\\Spotify\\Update'):
    shutil.rmtree('C:\\Users\\cagatay.guersoy\\AppData\\Local\\Spotify\\Update')
print('Removed spotify update folder')
# clean my desktop
walk1 = os.walk('\\zisvfs12\\Home\\cagatay.guersoy\\Desktop')
for root, dirs, files in os.walk('//zisvfs12/Home/cagatay.guersoy/Desktop'):
    print('Cleaning my desktop')
    break
for f in files:
    if f is not 'desktop.ini':
        pathSource = root + '/' + f
        pathTarget = root + '/Shortcuts/' + f
        shutil.move(pathSource, pathTarget)
