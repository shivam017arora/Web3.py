from brownie import network, AdvanceCollectible
from scripts import helper

dog_metadata_dic = {
    "PUG": "ipfs://Qmd9MCGtdVz2miNumBHDbvj8bigSgTwnr4SbyH6DNnpWdt?filename=0-PUG.json",
    "SHIBA_INU": "ipfs://QmdryoExpgEQQQgJPoruwGJyZmz6SqV4FRTX1i73CT3iXn?filename=1-SHIBA_INU.json",
    "ST_BERNARD": "ipfs://QmbBnUjyHHN7Ytq9xDsYF9sucZdDJLRkWz7vnZfrjMXMxs?filename=2-ST_BERNARD.json",
}

def main():
    print(f"Working on: {network.show_active()}")
    contract = AdvanceCollectible[-1]

    breeds = {
        0: 'PUG',
        1: 'SHIBA_INU',
        2: 'ST_BERNARD'
    }

    for tokenID in range(contract.tokenCounter()):
        breed = breeds[contract.tokenIdToBreed(tokenID)]
        if not contract.tokenURI(tokenID).startswith('https://'):
            print(f"Setting token URI of {tokenID}")
            set_tokenURI(tokenID, contract, dog_metadata_dic[breed])

def set_tokenURI(token_id, nft_contract, token_uri):
    account = helper.get_account()
    tx = nft_contract.setTokenURI(token_id, token_uri, {'from': account})
    tx.wait(1)
    print(f"AWESOME! You can view the nft at: {helper.OPENSEA_FORMAT.format(nft_contract.address, token_id)}")
    print("Please wait upto 20 mins and hit refresh metadata!")
