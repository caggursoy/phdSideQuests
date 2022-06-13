# -*- coding: utf-8 -*-
"""
Created on Mon Jun 13 13:12:14 2022

@author: Cagatay.Guersoy
"""
import requests

r = requests.get('https://pug2022.de/en/programm/tagungsprogramm/', verify=False)
r.content