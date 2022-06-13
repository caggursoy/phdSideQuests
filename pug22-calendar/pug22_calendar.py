# -*- coding: utf-8 -*-
"""
Created on Mon Jun 13 13:12:14 2022

@author: Cagatay.Guersoy
"""
from PyPDF2 import PdfReader

reader = PdfReader("pug-booklet.pdf")
for pg_no in range(8,11):
    page = reader.pages[pg_no]
    page_content = page.extract_text().lstrip().split('\n')
    # print(page_content)
    for line in page_content:
        print(line)
        if 'DONNERSTAG | ' in line:
            date = line[line.find(' | ')+3:line.find(' | ')+13]
            print(date)
        elif 'FREITAG | ' in line:
            date = line[line.find(' | ')+3:line.find(' | ')+13]
            print(date)
        elif 'Samstag | ' in line:
            date = line[line.find(' | ')+3:line.find(' | ')+13]
            print(date)
