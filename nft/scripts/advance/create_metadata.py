from brownie import AdvanceCollectible, network
from scripts import helper
from web3 import Web3
from metadata.sample_metadata import metadata_template
from pathlib import Path
import requests
import json


breed_to_image_uri = {
    "PUG": "https://ipfs.io/ipfs/QmSsYRx3LpDAb1GZQm7zZ1AuHZjfbPkD6J7s9r41xu1mf8?filename=pug.png",
    "SHIBA_INU": "https://ipfs.io/ipfs/QmYx6GsYAKnNzZ9A6NvEKV9nf1VaDzJrqDR23Y8YSkebLU?filename=shiba-inu.png",
    "ST_BERNARD": "https://ipfs.io/ipfs/QmUPjADFGEKmfohdTaNcWhp7VGk26h5jXDA7v3VtTnTLcW?filename=st-bernard.png",
}

def main():
    account = helper.get_account()
    contract = AdvanceCollectible[-1]
    number_of_collectibles = contract.tokenCounter()
    print(f"You have created {number_of_collectibles} collectibles")

    breeds = {
        0: 'PUG',
        1: 'SHIBA_INU',
        2: 'ST_BERNARD'
    }

    for token_id in range(number_of_collectibles):
        breed = breeds[contract.tokenIdToBreed(token_id)]
        metadata_filename = f"./metadata/{network.show_active()}/{token_id}-{breed}.json"

        collectible_metadata = metadata_template

        if Path(metadata_filename).exists():
            print(f"{metadata_filename} already exists. Delete it to overwrite!")
        else:
            print(f"creating metadata filename: ", metadata_filename)
            collectible_metadata['name'] = breed
            collectible_metadata['description'] = f"An Adorable {breed} pup!"
            img_file_name = "./img/" + breed.lower().replace("_", "-") + '.png'
            
            imageURL = None
            imageURL = upload_to_ipfs(img_file_name)
            imageURL = imageURL if imageURL is not None else breed_to_image_url[breed]

            collectible_metadata['image'] = imageURL
            with open(metadata_filename, 'w') as file:
                json.dump(collectible_metadata, file)

            upload_to_ipfs(metadata_filename)

def upload_to_ipfs(path):
    with Path(path).open('rb') as fp:
        image_binary = fp.read() #read the binary of the image
        # upload stuff
        ipfs_base_url = 'http://127.0.0.1:5001'
        endpoint = '/api/v0/add'
        response = requests.post(ipfs_base_url + endpoint, files={"file": image_binary})
        ipfs_hash = response.json()['Hash']
        filename = path.split('/')[-1:][0]
        image_uri = f"https://ipfs.io/ipfs/{ipfs_hash}?filename={filename}"
        print("HOSTED AT: ", image_uri)
        return image_uri


        