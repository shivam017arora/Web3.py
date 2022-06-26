from brownie import accounts, network, config, VRFCoordinatorMock, LinkToken, Contract
from web3 import Web3

FLC = ['mainnet-fork-dev']
LCBE = ['development', 'ganache-local']

OPENSEA_FORMAT = "https://testnets.opensea.io/assets/{}/{}"

def get_account(index=None, id=None):
    if(index and network.show_active() in LCBE):
        return accounts[index]
    if(id):
        return accounts.load(id);
        
    if(network.show_active() in LCBE or network.show_active() in FLC):
        return accounts[0]
    else:
        return accounts.load('shivam')

contractToMock = {
    'vrf_cordinator': VRFCoordinatorMock, 
    'link_token': LinkToken,
}

DECIMALS = 8
STARTING_FUND = 2000000000000000000

def deploy_mocks():
    account = get_account()
    # MockV3Aggregator.deploy(DECIMALS, STARTING_FUND, {'from': account}, publish_source=False)
    link_mock = LinkToken.deploy({'from': account}, publish_source=False)
    VRFCoordinatorMock.deploy(link_mock.address, {'from': account}, publish_source=False)
    

def get_contract(contract_name):
    """
        Will grab the addresses from config otherwise
        Will deploy the mock contract on ganache and return the contract object

        Args:
            contract_name: string
        Returns:
            brownie.network.contract.ProjectContract: The most recently deployed
            Contract of the type specificed by the dictionary. This could be either
            a mock or the 'real' contract on a live network.
    """
    contract_type = contractToMock[contract_name]
    if network.show_active() in LCBE:
        if(len(contract_type) <= 0):
            deploy_mocks()
        contract = contract_type[-1];
    else:
        contract_address = config['networks'][network.show_active()][contract_name]
        contract = Contract.from_abi(contract_type._name, contract_address, contract_type.abi)

    return contract
    
def fund_with_LINK(contract_address, account=None, link_token=None, amount=Web3.toWei(1, 'ether')):
    account = account if account else get_account()
    link_token = link_token if link_token else get_contract('link_token')
    tx = link_token.transfer(contract_address, amount, {'from': account})
    tx.wait(1)
    print("Funded Contract!")
    return tx