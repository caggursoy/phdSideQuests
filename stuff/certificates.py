## certificates.py
# A short way to add the ZI certificates to your system
###
import certifi
import urllib.request
# get the main certificate location
certs_loc = certifi.where()
# get what's inside the certificate
cert_main_file = open(certs_loc, "r")
cert_main = cert_main_file.read()
cert_main_file_write = open(certs_loc, "a")
# download ZI certificates
urllib.request.urlretrieve('http://wiki.zi.local/_media/proxy/ssl-deep-zi.cer', 'ssl-deep-zi.cer')
urllib.request.urlretrieve('http://wiki.zi.local/ZI-ZICERT1-CA.crt', 'ZI-ZICERT1-CA.crt')
# now read the certificates
zi_cert_names = ['ssl-deep-zi.cer', 'ZI-ZICERT1-CA.crt']
for zi_cert in zi_cert_names:
    zi_cert_file = open(zi_cert, "r")
    zi_cert_text = zi_cert_file.read()
    zi_cert_file.close()
    if zi_cert_text not in cert_main:
        print('you do not have the certificate', zi_cert, 'included, I am adding the certificate now...')
        cert_main_file_write.write('\n')
        cert_main_file_write.write(zi_cert_text)
    else:
        print('you already have the certificate:', zi_cert)

# close everything
cert_main_file.close()
cert_main_file_write.close()