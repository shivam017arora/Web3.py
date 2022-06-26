from pathlib import Path
import requests
import os

PINATA_BASE_URL = 'https://api.pinata.cloud/'

endpoint = 'pinning/pinFileToIPFS'

filepath = './img/pug.png'

filename = filepath.split('/')[-1:][0]

headers = {
    'pinata_api_key': os.getenv('PINATA_API_KEY'),
    'pinata_secret_api_key': os.getenv('PINATA_SECRET_KEY'),
    'Authorization': f"Bearer {os.getenv('PINATA_JWT')}"
}
def main():
    with Path(filepath).open('rb') as fp:
        image_binary = fp.read()
        try:
            response = requests.post(PINATA_BASE_URL + endpoint, files={
            'file': (filename, image_binary)
            },
            headers=headers
            )
            print(response.json())
        except requests.exceptions.ConnectionError:
             print("Connection refused")