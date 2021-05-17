# my lovely morning routine
import shutil
import os
import subprocess
import sys
import psutil
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
        continue
    else:
        pathSource = root + '/' + f
        pathTarget = root + '/Shortcuts/' + f
        try:
            shutil.move(pathSource, pathTarget)
        except shutil.SameFileError:
            os.remove(pathTarget)
            shutil.move(pathSource, pathTarget)

# "someProgram" in (p.name() for p in psutil.process_iter()) Rocket.Chat.exe rstudio.exe Spotify.exe OUTLOOK.EXE
progList = []
for p in psutil.process_iter():
    progList.append(p.name())

# Start Spotify, path = C:\Local\Programs\Spotify\Spotify.exe // C:\Program Files (x86)\Microsoft Office\Office16\OUTLOOK.EXE
cmdList = [r'C:\Program Files (x86)\Microsoft Office\Office16\OUTLOOK.EXE', r'C:\Local\Programs\Spotify\Spotify.exe', r'C:\Users\cagatay.guersoy\AppData\Local\atom\atom.exe',
r'C:\Program Files\RStudio\\bin\\rstudio.exe', r'C:\Users\cagatay.guersoy\AppData\Local\Programs\Rocket.Chat\Rocket.Chat.exe',
r'C:\Program Files (x86)\Zotero\zotero.exe',r'C:\Local\Programs\Telegram\Telegram.exe']

for cmd in cmdList:
    cc = cmd[cmd.rfind('\\')+1:]
    if cc not in progList:
        proc = subprocess.Popen(cmd, shell=True)
        try:
                proc.wait(timeout=1)
        except subprocess.TimeoutExpired:
            # sys.exit()
            continue
    else:
        continue
