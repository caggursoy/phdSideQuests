import certifi
import urllib.request
from pathlib import Path
###
certf_loc = certifi.where()
print(certf_loc)
with open(certf_loc) as f0:
    certf_file = f0.read()
if not (Path('./ssl-deep-zi.cer').is_file() and Path('./ZI-ZICERT1-CA.crt').is_file()):
    cert1 = 'http://wiki.zi.local/_media/proxy/ssl-deep-zi.cer'
    cert2 = 'http://wiki.zi.local/ZI-ZICERT1-CA.crt'
    urllib.request.urlretrieve(cert1, filename='ssl-deep-zi.cer')
    urllib.request.urlretrieve(cert2, filename='ZI-ZICERT1-CA.crt')
with open('./ssl-deep-zi.cer') as f1:
    cert1_file = f1.read()
with open('./ZI-ZICERT1-CA.crt') as f2:
    cert2_file = f2.read()

if cert1_file in certf_file and cert2_file in certf_file:
    print('ZI certificates are already installed')
else:
    print('Appending ZI certificates')
    certf_file_app = open(certf_loc, "a")
    out_str = cert1_file + '\n' + cert2_file
    certf_file_app.write(out_str)
