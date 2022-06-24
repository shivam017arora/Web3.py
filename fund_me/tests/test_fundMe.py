from scripts.deploy import deploy_fund_me
from scripts import helper
from scripts.fund_and_withdraw import fund, withdraw
from brownie import network, accounts, exceptions
import pytest

def test_can_fund_and_withdraw():
    account = helper.get_account()
    fundme = deploy_fund_me()
    entrance_fee = fundme.getEntranceFee()
    tx = fundme.fund({'from': account, 'value': entrance_fee})
    tx.wait(1)
    assert fundme.addressToAmountFunded(account.address) == entrance_fee
    tx2 = fundme.withdraw({'from': account})
    tx2.wait(1)
    assert fundme.addressToAmountFunded(account.address) == 0

def test_only_owner_withdraw():
    if(network.show_active() not in helper.LCBE):
        pytest.skip("Only local testing")
    account = helper.get_account()
    fundme = deploy_fund_me()
    entrance_fee = fundme.getEntranceFee()
    bad_actor = accounts.add()
    # fundme.withdraw({'from': bad_actor})
    with pytest.raises(exceptions.VirtualMachineError):
        fundme.withdraw({'from': bad_actor})