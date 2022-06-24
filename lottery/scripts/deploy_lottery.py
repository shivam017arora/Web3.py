from brownie import Lottery, accounts, config, network
from . import helper
import time

def deploy_lottery(_index=None, _id=None):
    if(_index is None):
        account = helper.get_account(id=_id if _id else 'shivam')
    else:
        account = helper.get_account(index=_index)
    contract = Lottery.deploy(helper.get_contract('eth_usd_price_feed').address, 
                                helper.get_contract('vrf_cordinator').address,
                                helper.get_contract('link_token').address,
                                config['networks'][network.show_active()]['fee'],
                                config['networks'][network.show_active()]['keyhash'],
                                {'from': account}, 
                                publish_source=config['networks'][network.show_active()].get('verify', False))
    print("Deployed Lottery Contract..")
    return contract

def start_lottery():
    account = helper.get_account(id='shivam')
    # Start the lottery
    contract = Lottery[-1]
    tx = contract.startLottery({'from': account})
    tx.wait(1)
    print("Lottery has started..")

def enter_lottery():
    account = helper.get_account(index=2)
    contract = Lottery[-1]
    value = contract.getEntranceFee() + 1000000
    tx = contract.enter({'from': account, 'value': value})
    tx.wait(1)
    print("Lottery has been entered..")

def end_lottery():
    # fund the contract with LINK token to call RandomGenerator
    account = helper.get_account(id='shivam')
    contract = Lottery[-1]
    tx = helper.fund_with_LINK(contract.address)
    tx.wait(1)
    # End the lottery
    tx = contract.endLottery({'from': account})
    tx.wait(1)
    time.sleep(60)
    print(f"Lottery Recent Winner: {contract.recentWinner()}")
    print("Lottery has ended..")

def main():
    deploy_lottery()
    start_lottery()
    enter_lottery()
    end_lottery()