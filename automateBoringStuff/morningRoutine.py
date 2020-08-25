# my lovely morning routine
import shutil
import os
import subprocess
import sys
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
    if f == 'desktop.ini':
        print('here')
        continue
    else:
        pathSource = root + '/' + f
        pathTarget = root + '/Shortcuts/' + f
        shutil.move(pathSource, pathTarget)

# Start Spotify, path = C:\Local\Programs\Spotify\Spotify.exe // C:\Program Files (x86)\Microsoft Office\Office16\OUTLOOK.EXE
cmdList = ['C:\Program Files (x86)\Microsoft Office\Office16\OUTLOOK.EXE', 'C:\Local\Programs\Spotify\Spotify.exe']
for cmd in cmdList:
    proc = subprocess.Popen(cmd, shell=True)
    try:
        proc.wait(timeout=1)
    except subprocess.TimeoutExpired:
        # sys.exit()
        continue
