from brownie import accounts, network, Contract, config, MockV3Aggregator, VRFCoordinatorMock, LinkToken
from scripts import helper
from scripts.deploy_lottery import deploy_lottery
import pytest

def test_can_pick_winner():
    if(network.show_active() not in helper.LCBE):
        pytest.skip()

    lottery = deploy_lottery(_id='shivam')
    account = helper.get_account(id='shivam')
    lottery.startLottery({'from': account})
    lottery.enter({'from': account, 'value': lottery.getEntranceFee() + 1000000})
    lottery.enter({'from': account, 'value': lottery.getEntranceFee() + 1000000})
    lottery.enter({'from': account, 'value': lottery.getEntranceFee() + 1000000})
    helper.fund_with_LINK(lottery.address)
    lottery.endLottery({'from': account})
    time.sleep(60)
    assert lottery.recentWinner() == account.address