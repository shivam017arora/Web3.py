from brownie import AdvanceCollectible
from scripts import helper
from web3 import Web3

def main():
    account = helper.get_account()
    contract = AdvanceCollectible[-1]
    helper.fund_with_LINK(contract.address)
    tx = contract.createCollectible({'from': account})
    tx.wait(1)
    print("Collectible created..!!!!")