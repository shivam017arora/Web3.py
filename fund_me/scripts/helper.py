from brownie import accounts, network, MockV3Aggregator
from web3 import Web3

DECIMALS = 8
STARTING_FUND = 10068180000000000

FLC = ['mainnet-fork-dev']
LCBE = ['development', 'ganache-local']

def get_account():
    if(network.show_active() in LCBE or network.show_active() in FLC):
        return accounts[0]
    else:
        return accounts.load('shivam')

def deploy_mocks():
    print("Active network is not rinkeby, using local price feed")
    print("Deploying mocks...")
    print("*"*70)
    if(len(MockV3Aggregator) <= 0):
        mock = MockV3Aggregator.deploy(DECIMALS, STARTING_FUND, {'from': get_account()}, publish_source=False)
        print("Deployed contract...")
        print("*"*70)
    else:
        mock = MockV3Aggregator[-1] # get last deployed contract
    print("MockV3Aggragator address: ", mock.address)
    print("*"*70)
    return mock