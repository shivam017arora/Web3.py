from scripts import helper
from brownie import SimpleCollectible
import time

sample_token_uri = "ipfs://Qmd9MCGtdVz2miNumBHDbvj8bigSgTwnr4SbyH6DNnpWdt?filename=0-PUG.json"
OPENSEA_FORMAT = helper.OPENSEA_FORMAT

def deploy_and_create():
    account = helper.get_account()
    SimpleCollectible.deploy({'from': account})
    time.sleep(1)
    contract = SimpleCollectible[len(SimpleCollectible) - 1]
    tx = contract.createCollectible(sample_token_uri, {'from': account})
    tx.wait(1)
    print("AWESOME! You can view your NFT at: ", OPENSEA_FORMAT.format(contract.address, contract.tokenCounter() - 1))
    print('Please give up to 20 minutes, and hit the "refresh metadata" button')
    return contract

def main():
    deploy_and_create()