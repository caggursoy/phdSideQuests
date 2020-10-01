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
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
import time
from pushsafer import init, Client
import platform
##
firstday = input("Enter the first day of the week (1-31): ")
month1 = input("Enter the month (numbers please!): ")
lastday = input("Enter the last day of the week (1-31)(two digit numbers please! (i.e. 05 or 18)): ")
month2 = input("Enter the month (numbers please!): ")
wkNo = datetime.date(2020, int(month1), int(firstday)).isocalendar()[1] - 35
prefix = 'W'+str(wkNo)
pdfStr =  prefix+'_Mittagessen_Cafeteria_vom_'+str(firstday)+'.'+(('0'+str(month1)) if int(month1)<10 else str(month1))+'.'+'2020'+'_bis_'+str(lastday)+'.'+(('0'+str(month2)) if int(month2)<10 else str(month2))+'.'+'2020.pdf'
print(pdfStr)
## clear function
def clear():
    if platform.system() == 'Linux' or platform.system() == 'Darwin':
        os.system('clear')
    else:
        os.system('cls')

# t_ref = int(input('Enter refresh timing in seconds: '))
#
# time.sleep(t_ref)
def downloadPdfIntranet():
    chrome_options = Options()
    chrome_options.add_experimental_option('prefs',  {
        "download.default_directory": os.path.dirname(os.path.realpath(__file__)),
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "plugins.always_open_pdf_externally": True
        }
    )
    driver = webdriver.Chrome(options = chrome_options)
    driver.minimize_window()
    driver.get('https://intranet.zi-mannheim.de/')
    driver.refresh()
    username = driver.find_element_by_id("exampleInputEmail1")
    password = driver.find_element_by_id("pass")
    username.send_keys("intranet")
    pswd = input("Enter the password: ")
    password.send_keys(pswd)
    driver.find_element_by_name("submit").click()
    time.sleep(1)
    driver.get('https://intranet.zi-mannheim.de/zi/cafeteria/wochenspeiseplan/')
    driver.refresh()
    time.sleep(1)
    driver.find_element_by_xpath("/html/body/main/div[3]/div/div[2]/div[3]/p[3]/a").click()
    time.sleep(1)
    driver.close()
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

# Call function to extract text from pdf
downloadFlag = input('Do I need to download the pdf? (Y/N)... ')
if downloadFlag.lower() == 'y':
    downloadPdfIntranet()
xText = extract_text_from_pdf(pdfStr)
xTextList = re.split('□',xText)
clear()
for rows in xTextList:
    print(rows)
