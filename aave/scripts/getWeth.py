from . import helper
from brownie import interface, config, network

def getWeth():
    """ 
    Mints weth via depositing eth 
    address and abi of the kovan test weth contract: 
    0xd0A1E359811322d97991E03f863a0C30C2cF029C
    """
    account = helper.get_account()
    weth = interface.IWeth(config['networks'][network.show_active()]['weth_token'])
    tx = weth.deposit({'from': account, 'value': 0.1 * 10 ** 18})
    tx.wait(1)
    print(f'Received 0.1 WETH')
    return tx

def main():
    getWeth()