import datetime
import urllib.request

firstday = input("Enter the first day of the week (1-31): ")
month1 = input("Enter the month (numbers please!): ")
lastday = input("Enter the last day of the week (1-31): ")
month2 = input("Enter the month (numbers please!): ")
wkNo = datetime.date(2020, int(month1), int(firstday)).isocalendar()[1] - 5
dates = ''
##
## months needs to be fixed
if int(firstday) < 10 and int(lastday) < 10 and int(month) < 10:
    dates = '_0' + firstday + '.0' + month1 + '.2020_bis_0' + lastday + '.0' + month2 + '.2020'
elif int(firstday) < 10 and int(lastday) >= 10 and int(month) < 10:
    dates = '_0' + firstday + '.0' + month1 + '.2020_bis_' + lastday + '.0' + month2 + '.2020'
elif int(firstday) < 10 and int(lastday) < 10 and int(month) >= 10:
    dates = '_0' + firstday + '.' + month1 + '.2020_bis_0' + lastday + '.' + month2 + '.2020'
elif int(firstday) < 10 and int(lastday) >= 10 and int(month) >= 10:
    dates = '_0' + firstday + '.' + month1 + '.2020_bis_' + lastday + '.' + month2 + '.2020'
elif int(firstday) >= 10 and int(lastday) >= 10 and int(month) >= 10:
    dates = '_' + firstday + '.' + month1 + '.2020_bis_' + lastday + '.' + month2 + '.2020'
elif int(firstday) >= 10 and int(lastday) >= 10 and int(month) < 10:
    dates = '_' + firstday + '.0' + month1 + '.2020_bis_' + lastday + '.0' + month2 + '.2020'

fullPath = 'https://intranet.zi-mannheim.de/fileadmin/user_upload/cafeteria/Mittagessen/Cafeteria/'
fullPath = fullPath + 'W' + str(wkNo) + '_Mittagessen_Cafeteria_vom' + dates + '.pdf'
print(fullPath)

print('Beginning file download with urllib2...')
urllib.request.urlretrieve(fullPath, 'C:\\Local\\LocalRepos\\phdSideQuests\\cafeteriaPlan\\'+dates+'.pdf')
