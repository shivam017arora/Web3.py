from brownie import FundMe, network, config, MockV3Aggregator
from . import helper


def deploy_fund_me():
    account = helper.get_account() 
    if(network.show_active() not in helper.LCBE):
        priceFeedAddress = config['networks'][network.show_active()]['eth_usd_price_feed']
        contract = FundMe.deploy(priceFeedAddress, {'from': account}, publish_source=False)
    else:
        mock = helper.deploy_mocks()
        priceFeedAddress = mock.address
        contract = FundMe.deploy(priceFeedAddress, {'from': account}, publish_source=False)

    print(f'Deployed contract at {contract.address}')

    return contract

def main():
    deploy_fund_me()