from brownie import FundMe
from . import helper

def fund():
    fundMe = FundMe[-1] # get last deployed contract
    my_account = helper.get_account() # get account
    entrance_fee = fundMe.getEntranceFee() # get entrance fee
    print(f"Entry Fee is: {entrance_fee}")
    print("Funding contract...")
    fundMe.fund({'from': my_account, 'value': entrance_fee}) # calling fund method of the contract! whoa!

def withdraw():
    fundMe = FundMe[-1] # get last deployed contract
    my_account = helper.get_account() # get account
    print("Withdrawing...")
    fundMe.withdraw({'from': my_account}) # calling withdraw method of the contract! whoa!

def main():
    fund()
    withdraw()