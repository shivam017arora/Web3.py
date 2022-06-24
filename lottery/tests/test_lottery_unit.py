from brownie import Lottery, accounts, network, config, exceptions
from scripts.deploy_lottery import deploy_lottery
from web3 import Web3
from scripts import helper
import pytest

def test_lottery():
    contract = deploy_lottery() #arrange
    entrance_fee = contract.getEntranceFee() #act
    expected = Web3.toWei(0.025, 'ether') / 10 ** 7 #because priceFeed is deployed with 8 decimals
    #assert
    assert entrance_fee == expected, f"Entrance fee is {entrance_fee} but expected {expected}"


def test_cant_enter_unless_started():
    contract = deploy_lottery() #arrange
    with pytest.raises(exceptions.VirtualMachineError): #act / assert
        contract.enter({'from': helper.get_account(), 'value': contract.getEntranceFee()})
        # this line throws error because someone attepts to enter without the lottery being started after deployment

def test_can_start_and_enter_lottery():
    contract = deploy_lottery(_index=2) #arrange
    account = helper.get_account(index=2)
    contract.startLottery({'from': account})
    contract.enter({'from': account, 'value': contract.getEntranceFee()}) #act
    assert contract.players(0) == account, f"Player is {contract.players(0)} but expected {account}" #assert
    
def test_can_end_lottery():
    contract = deploy_lottery(_index=2) #arrange
    account = helper.get_account(index=2)
    contract.startLottery({'from': account}) #act
    contract.enter({'from': account, 'value': contract.getEntranceFee()}) #act
    #fund with LINK
    helper.fund_with_LINK(contract_address=contract.address)
    contract.endLottery({'from': account}) #act
    #assert
    assert contract.lottery_state() == 2

def test_can_pick_winner_correctly():
    contract = deploy_lottery(_index=2) #arrange
    account = helper.get_account(index=2)
    contract.startLottery({'from': account}) #act
    contract.enter({'from': account, 'value': contract.getEntranceFee()}) #act
    contract.enter({'from': helper.get_account(index=5), 'value': contract.getEntranceFee()}) #act
    contract.enter({'from': helper.get_account(index=6), 'value': contract.getEntranceFee()}) #act
    #fund with LINK
    helper.fund_with_LINK(contract_address=contract.address)
    tx = contract.endLottery({'from': account}) #act
    requestId = tx.events['RequestedRandomness']['requestId']
    helper.get_contract('vrf_coordinator').callBackWithRandomness(requestId, 777, contract.address, {'from': account})
    starting_balance = account.balance()
    contract_balance = contract.balance()
    #assert
    assert contract.recentWinner() == account, f"Winner is {contract.recentWinner()} but expected {account}"
    assert contract.balance() == 0, f"Balance is {contract.balance()} but expected 0"
    assert account.balance() == starting_balance + contract_balance, f"Balance is {account.balance} but expected {starting_balance + contract_balance}"

