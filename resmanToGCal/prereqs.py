import certifi
import urllib.request
from pathlib import Path
###
certf_loc = certifi.where()
certf_file = open(certf_loc, "r")
if not (Path('./ssl-deep-zi.cer').is_file() and Path('./ZI-ZICERT1-CA.crt').is_file()):
    cert1 = 'http://wiki.zi.local/_media/proxy/ssl-deep-zi.cer'
    cert2 = 'http://wiki.zi.local/ZI-ZICERT1-CA.crt'
    urllib.request.urlretrieve(cert1, filename='ssl-deep-zi.cer')
    urllib.request.urlretrieve(cert2, filename='ZI-ZICERT1-CA.crt')
cert1_file = open('./ssl-deep-zi.cer')
cert2_file = open('./ZI-ZICERT1-CA.crt')
if cert1_file in certf_file and cert2_file in certf_file:
    print('ZI certificates are already installed')
else:
    print('Appending ZI certificates')
