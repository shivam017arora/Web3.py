from brownie import accounts, SimpleStorage

def test_simple_storage():
    #Arrange
    my_account = accounts.load('shivam')
    #Acting
    contract = SimpleStorage.deploy({"from": my_account})
    value = contract.retrieve()
    #Assert
    assert value == 0

def test_store_simple_storage():
    #Arrange
    my_account = accounts.load('shivam')
    #Acting
    contract = SimpleStorage.deploy({"from": my_account})
    transaction = contract.store(15, {"from": my_account})
    value = contract.retrieve()
    #Assert
    assert value == 15

def main():
    test_simple_storage()
    test_store_simple_storage()