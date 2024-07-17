## certificates.py
# A short way to add the ZI certificates to your system
###
try:
    import certifi, subprocess
    import urllib.request
except:
    try:
        import subprocess, sys
        subprocess.call([sys.executable, '-m', 'pip', '--trusted-host', 'pypi.python.org', 'install', 'certifi'])
    except:
        try:
            import requests, tarfile
            from pathlib import Path
            # variables
            url = 'https://files.pythonhosted.org/packages/c2/02/a95f2b11e207f68bc64d7aae9666fed2e2b3f307748d5123dffb72a1bbea/certifi-2024.7.4.tar.gz'
            download_path = str(Path.cwd() / 'certifi.tar.gz')
            extract_path = str(Path.cwd() / 'certifi')
            # Download the file with SSL verification disabled
            response = requests.get(url, verify=False)
            response.raise_for_status()
            
            # Save the downloaded file to the specified download path
            with open(download_path, 'wb') as file:
                file.write(response.content)
            # Extract the tar.gz file
            with tarfile.open(download_path, 'r:gz') as tar:
                tar.extractall(path=extract_path)
            # Run the extracted file
            command_path = Path.cwd() / 'certifi' / 'certifi-2024.7.4'
            # subprocess.run([sys.executable, str(command_path)], capture_output=True)
            subprocess.run([sys.executable, 'setup.py', 'install'], cwd=command_path, capture_output=True, text=True)
        except requests.exceptions.RequestException as e:
            print(f"Error downloading file: {e}")
        except tarfile.TarError as e:
            print(f"Error extracting file: {e}")
    ##
    import urllib.request
    import certifi
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

##
