#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug 29 20:37:44 2023

@author: cagatay.guersoy
"""
import glob, os
from pathlib import Path
from inspect import currentframe, getframeinfo
import docx
from datetime import datetime
import pandas as pd
from rocketchat_API.rocketchat import RocketChat
import subprocess
import fitz
import imgbbpy
##
file_location = '/zi/flstorage/Klinische_Psychologie/Projekte/Lab Meeting Protokolle/'
protocols = glob.glob(str(Path(file_location) / '*.docx'))
filename = getframeinfo(currentframe()).filename
parent = Path(filename).resolve().parent
# get secrets
with open(str(parent / 'secrets.txt')) as f:
    lines = f.readlines()
    token = lines[0][lines[0].find(':')+1:].strip('\n')
    rocket_user_id = lines[1][lines[1].find(':')+1:].strip('\n')
    rocket_auth_token = lines[2][lines[2].find(':')+1:].strip('\n')
    rocket_server_url = lines[3][lines[3].find(':')+1:].strip('\n')
    imgbb_key = lines[8][lines[8].find(':')+1:].strip('\n')
# init rocketchat
rocket = RocketChat(user_id=rocket_user_id,
                    auth_token=rocket_auth_token,
                    server_url=rocket_server_url)
for protocol in protocols:
    if '~' not in protocol:
        # f = open(protocol, 'rb')
        # document = Document(f)
        # f.close()
        # print(protocol[protocol.find('Protokolle/')+len('Protokolle/'):protocol.find(' KLips_')])
        file_date = protocol[protocol.find('Protokolle/')+len('Protokolle/'):protocol.find(' KLips_')]
        # get todays date
        todays_date = datetime.today().strftime('%Y-%m-%d')
        # convert file date
        try:
            file_date = datetime.strptime(file_date, '%Y_%m_%d')
            # print(datetime.strptime(file_date, '%Y_%m_%d'))
        except:
            try:
                file_date = datetime.strptime(file_date[:-1], '%Y_%m_%d')
                # print(datetime.strptime(file_date[:-1], '%Y_%m_%d'))
            except:
                # print('not a date')
                continue
        diff_day = datetime.strptime(todays_date, '%Y-%m-%d') - file_date
        # print(diff_day)
        # Initialize empty lists to store table data
        data = []
        if diff_day.days < 7 and diff_day.days >= 0:
            protocol_win = protocol
            out_str = 'This week\'s file is located at:\n\nFor Windows users: ' + protocol.replace('/zi/flstorage/','W:\\').replace('/','\\') + '\n\nFor Unix users: ' + protocol
            rocket.chat_post_message(out_str, channel='64ef390ba7410e24a50c8fbe')
            # docx to pdf first
            output = subprocess.check_output(['libreoffice', '--headless', '--convert-to', 'pdf' , protocol])
            pdf_file = ('.' + protocol[protocol.rfind('/'):]).replace('.docx', '.pdf')
            # pdf to png now
            doc = fitz.open(pdf_file)
            zoom = 4
            mat = fitz.Matrix(zoom, zoom)
            count = 0
            # Count variable is to get the number of pages in the pdf
            for p in doc:
                count += 1
            # activate imgbb client to share the images
            imgbb_client = imgbbpy.SyncClient(imgbb_key)
            # create the png files now
            for i in range(count):
                val = f"./image_{i+1}.png"
                page = doc.load_page(i)
                pix = page.get_pixmap(matrix=mat)
                pix.save(val)
                upload = imgbb_client.upload(file=val, expiration=60*60*24*31)
                # print(upload.url)
                rocket.chat_post_message('Here\'s the png version of the protocol for convenience', channel='64ef390ba7410e24a50c8fbe', attachments=[{"image_url": upload.url}])
                os.remove(val) # remove the png files
            doc.close()
            # now remove the pdf files
            os.remove(pdf_file)
