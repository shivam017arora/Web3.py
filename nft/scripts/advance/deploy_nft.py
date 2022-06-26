from scripts import helper
from brownie import AdvanceCollectible, network, config
import time

OPENSEA_FORMAT = helper.OPENSEA_FORMAT

def deploy_and_create():
    account = helper.get_account()
    contract = AdvanceCollectible.deploy(
        helper.get_contract('vrf_cordinator'), # config['networks'][network.show_active()]['vrf_cordinator'],
        helper.get_contract('link_token'), # config['networks'][network.show_active()]['link_token'],
        config['networks'][network.show_active()]['keyhash'],
        config['networks'][network.show_active()]['fee'],
        {'from': account}
    )
    helper.fund_with_LINK(contract.address)
    creating_tx = contract.createCollectible({'from': account})
    creating_tx.wait(1)
    print("TOKEN CREATED")
    return contract, creating_tx

def main():
    deploy_and_create()