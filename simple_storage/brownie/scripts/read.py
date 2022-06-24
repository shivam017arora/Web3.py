from brownie import accounts, SimpleStorage

def read_simple_storage():
    contract = SimpleStorage[-1] #get the last deployed contract
    value = contract.retrieve()
    print(value)

def main():
    read_simple_storage()