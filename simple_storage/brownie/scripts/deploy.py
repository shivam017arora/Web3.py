from brownie import accounts, SimpleStorage

def deploy_simple_storage():
    #need an address and a private key i.e wallet
    my_account = accounts.load('shivam')
    #deploy the contract using this wallet
    print(type(SimpleStorage))
    print(SimpleStorage)
    contract = SimpleStorage.deploy({"from": my_account})
    print(contract)
    value = contract.retrieve()
    print(value)
    transaction = contract.store(15, {"from": my_account})
    print(transaction)
    value = contract.retrieve()
    print(value)

def main():
    deploy_simple_storage()