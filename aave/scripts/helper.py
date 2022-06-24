from brownie import accounts, network, config

FLC = []
LCBE = ['development', 'ganache-local', 'mainnet-fork']

def get_account(index=None, id=None):
    if(index and network.show_active() in LCBE):
        return accounts[index]
    if(id):
        return accounts.load(id);
        
    if(network.show_active() in LCBE or network.show_active() in FLC):
        return accounts[0]
    else:
        return accounts.load('shivam')

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
    
def fund_with_LINK(contract_address, account=None, link_token=None, amount=1 * 10 ** 17):
    account = account if account else get_account()
    link_token = link_token if link_token else get_contract('link_token')
    tx = link_token.transfer(contract_address, amount, {'from': account})
    tx.wait(1)
    print("Funded Contract!")
    return tx