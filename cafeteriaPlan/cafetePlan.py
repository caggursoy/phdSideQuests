import datetime
import urllib.request
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from io import StringIO
import io
import os
import re
import sys
##
firstday = input("Enter the first day of the week (1-31): ")
month1 = input("Enter the month (numbers please!): ")
lastday = input("Enter the last day of the week (1-31): ")
month2 = input("Enter the month (numbers please!): ")
wkNo = datetime.date(2020, int(month1), int(firstday)).isocalendar()[1] - 5
dates = ''
##
## months needs to be fixed
if int(firstday) < 10 and int(lastday) < 10 and int(month1) < 10:
    dates = '_0' + firstday + '.0' + month1 + '.2020_bis_0' + lastday + '.0' + month2 + '.2020'
elif int(firstday) < 10 and int(lastday) >= 10 and int(month1) < 10:
    dates = '_0' + firstday + '.0' + month1 + '.2020_bis_' + lastday + '.0' + month2 + '.2020'
elif int(firstday) < 10 and int(lastday) < 10 and int(month1) >= 10:
    dates = '_0' + firstday + '.' + month1 + '.2020_bis_0' + lastday + '.' + month2 + '.2020'
elif int(firstday) < 10 and int(lastday) >= 10 and int(month1) >= 10:
    dates = '_0' + firstday + '.' + month1 + '.2020_bis_' + lastday + '.' + month2 + '.2020'
elif int(firstday) >= 10 and int(lastday) >= 10 and int(month1) >= 10:
    dates = '_' + firstday + '.' + month1 + '.2020_bis_' + lastday + '.' + month2 + '.2020'
elif int(firstday) >= 10 and int(lastday) >= 10 and int(month1) < 10:
    dates = '_' + firstday + '.0' + month1 + '.2020_bis_' + lastday + '.0' + month2 + '.2020'

fullPath = 'https://intranet.zi-mannheim.de/fileadmin/user_upload/cafeteria/Mittagessen/Cafeteria/'
fullPath = fullPath + 'W' + str(wkNo) + '_Mittagessen_Cafeteria_vom' + dates + '.pdf'
fullPathPdf =os.path.dirname(os.path.abspath(__file__)) + '//' + dates + '.pdf'
prompt1 = input('Do I need to download the file? Y/N...')
if prompt1.lower() == 'Y'.lower():
    print('Beginning file download...')
    urllib.request.urlretrieve(fullPath, fullPathPdf)
    print('File downloaded...')
elif prompt1.lower() == 'N'.lower():
    pass
else:
    print('You did something wrong! Terminating!')
    sys.exit()
## Function taken from: http://www.blog.pythonlibrary.org/2018/05/03/exporting-data-from-pdfs-with-python/
def extract_text_from_pdf(pdf_path):
    resource_manager = PDFResourceManager()
    fake_file_handle = io.StringIO()
    converter = TextConverter(resource_manager, fake_file_handle)
    page_interpreter = PDFPageInterpreter(resource_manager, converter)

    with open(pdf_path, 'rb') as fh:
        for page in PDFPage.get_pages(fh,
                                      caching=True,
                                      check_extractable=True):
            page_interpreter.process_page(page)

        text = fake_file_handle.getvalue()

    # close open handles
    converter.close()
    fake_file_handle.close()

    if text:
        return text
## Call function to extract text from pdf
xText = extract_text_from_pdf(fullPathPdf)
xTextList = re.split('□',xText)
print(xTextList)

datesStart = dates[1:dates.find("2020")+4] # find starting date of the week and extract it from dates
datesEnd = dates[dates[dates.find("2020")+4:].find("2020")-10:dates[dates.find("2020")+4:].find("2020")] # find starting date of the week and extract it from dates
print(datesStart, '\t', datesEnd)
