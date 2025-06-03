###
# A short way to add the ZI certificates to your system
###

import sys
import subprocess
from pathlib import Path
import ssl
import urllib.request

def install_certifi_fallback():
    """Install certifi with various fallback methods for restricted networks"""
    try:
        import certifi
        return True
    except ImportError:
        pass

    # Method 1: Try pip with trusted hosts and no SSL verification
    try:
        subprocess.check_call([
            sys.executable, '-m', 'pip', 'install', 'certifi',
            '--trusted-host', 'pypi.org',
            '--trusted-host', 'pypi.python.org',
            '--trusted-host', 'files.pythonhosted.org',
            '--disable-pip-version-check'
        ])
        import certifi
        return True
    except (subprocess.CalledProcessError, ImportError):
        print("Failed to install certifi via pip")

    # Method 2: Try downloading and installing manually without SSL verification
    try:
        # Create unverified SSL context
        ssl_context = ssl.create_default_context()
        ssl_context.check_hostname = False
        ssl_context.verify_mode = ssl.CERT_NONE

        # Download certifi manually
        url = 'https://files.pythonhosted.org/packages/c2/02/a95f2b11e207f68bc64d7aae9666fed2e2b3f307748d5123dffb72a1bbea/certifi-2024.7.4.tar.gz'
        download_path = Path.cwd() / 'certifi.tar.gz'

        # Use urllib with unverified context
        with urllib.request.urlopen(url, context=ssl_context) as response:
            with open(download_path, 'wb') as f:
                f.write(response.read())

        # Extract and install
        import tarfile
        extract_path = Path.cwd() / 'certifi'
        with tarfile.open(download_path, 'r:gz') as tar:
            tar.extractall(path=extract_path)

        # Install the package
        setup_path = extract_path / 'certifi-2024.7.4'
        subprocess.check_call([
            sys.executable, 'setup.py', 'install'
        ], cwd=setup_path)

        # Clean up
        download_path.unlink(missing_ok=True)
        import shutil
        shutil.rmtree(extract_path, ignore_errors=True)

        import certifi
        return True

    except Exception as e:
        print(f"Failed to install certifi manually: {e}")
        return False

def download_with_fallback(url, filename):
    """Download file with SSL verification fallbacks"""
    filepath = Path.cwd() / filename

    # Method 1: Try with unverified SSL context
    try:
        ssl_context = ssl.create_default_context()
        ssl_context.check_hostname = False
        ssl_context.verify_mode = ssl.CERT_NONE

        with urllib.request.urlopen(url, context=ssl_context) as response:
            with open(filepath, 'wb') as f:
                f.write(response.read())
        return True
    except Exception as e:
        print(f"Failed to download {filename} with unverified SSL: {e}")

    # Method 2: Try with requests if available (with verify=False)
    try:
        import requests
        response = requests.get(url, verify=False, timeout=30)
        response.raise_for_status()
        with open(filepath, 'wb') as f:
            f.write(response.content)
        return True
    except Exception as e:
        print(f"Failed to download {filename} with requests: {e}")

    # Method 3: Try with curl if available
    try:
        subprocess.check_call([
            'curl', '-k', '-L', '-o', str(filepath), url
        ], timeout=60)
        return True
    except Exception as e:
        print(f"Failed to download {filename} with curl: {e}")

    # Method 4: Try with wget if available
    try:
        subprocess.check_call([
            'wget', '--no-check-certificate', '-O', str(filepath), url
        ], timeout=60)
        return True
    except Exception as e:
        print(f"Failed to download {filename} with wget: {e}")

    return False

def main():
    # Disable SSL warnings
    try:
        import urllib3
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    except ImportError:
        pass

    # Install certifi if needed
    if not install_certifi_fallback():
        print("Could not install certifi. Attempting to continue without it...")
        # Create a basic certificate bundle location
        certs_loc = str(Path.home() / '.local' / 'cacert.pem')
        Path(certs_loc).parent.mkdir(parents=True, exist_ok=True)
        if not Path(certs_loc).exists():
            Path(certs_loc).touch()
    else:
        import certifi
        certs_loc = certifi.where()

    print(f"Using certificate location: {certs_loc}")

    # Read existing certificates
    try:
        with open(certs_loc, "r") as cert_file:
            cert_main = cert_file.read()
    except FileNotFoundError:
        cert_main = ""
        print("Certificate file not found, creating new one...")

    # Download ZI certificates with fallback methods
    zi_cert_urls = {
        'ssl-deep-zi.cer': 'http://wiki.zi.local/_media/proxy/ssl-deep-zi.cer',
        'ZI-ZICERT1-CA.crt': 'http://wiki.zi.local/ZI-ZICERT1-CA.crt'
    }

    downloaded_certs = []
    for cert_name, cert_url in zi_cert_urls.items():
        print(f"Downloading {cert_name}...")
        if download_with_fallback(cert_url, cert_name):
            downloaded_certs.append(cert_name)
            print(f"Successfully downloaded {cert_name}")
        else:
            print(f"Failed to download {cert_name}")

    # Add certificates to the bundle
    with open(certs_loc, "a") as cert_main_file_write:
        for cert_name in downloaded_certs:
            try:
                with open(cert_name, "r") as zi_cert_file:
                    zi_cert_text = zi_cert_file.read()

                if zi_cert_text not in cert_main:
                    print(f'Adding certificate {cert_name}...')
                    cert_main_file_write.write('\n')
                    cert_main_file_write.write(zi_cert_text)
                else:
                    print(f'Certificate {cert_name} already exists')
            except FileNotFoundError:
                print(f"Could not read {cert_name}")

    # Configure conda with SSL verification disabled or custom cert
    try:
        if 'ZI-ZICERT1-CA.crt' in downloaded_certs:
            subprocess.run([
                'conda', 'config', '--set', 'ssl_verify',
                str(Path.cwd() / 'ZI-ZICERT1-CA.crt')
            ], check=True)
        else:
            # Disable SSL verification for conda as fallback
            subprocess.run([
                'conda', 'config', '--set', 'ssl_verify', 'false'
            ], check=True)
        print("Conda SSL configuration updated")
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("Could not configure conda SSL settings")

    # Set environment variables for SSL
    import os
    os.environ['REQUESTS_CA_BUNDLE'] = certs_loc
    os.environ['CURL_CA_BUNDLE'] = certs_loc
    os.environ['SSL_CERT_FILE'] = certs_loc

    print("Certificate installation completed!")
    print(f"Certificate bundle location: {certs_loc}")

if __name__ == "__main__":
    main()