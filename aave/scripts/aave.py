from . import helper
from brownie import config, network, interface
from . import getWeth as get_weth
from web3 import Web3

DEPOSIT_AMOUNT = Web3.toWei(0.1, 'ether')

def main():
    account = helper.get_account()
    erc20_address = config['networks'][network.show_active()]['weth_token']
    if network.show_active() in ['mainnet-fork']:
        get_weth.getWeth()

    # we need the lending pool contract:
    # https://docs.aave.com/developers/v/1.0/developing-on-aave/the-protocol/lendingpool
    
    lending_pool = get_lending_pool()
    print(lending_pool)

    # approve sending ERC20 tokens

    approve_tx = approve_erc20(lending_pool.address, DEPOSIT_AMOUNT, erc20_address, account)
    print(approve_tx)

    # deposit into aave
    print("Depositing to AAVE..")
    tx = lending_pool.deposit(
        erc20_address, 
        DEPOSIT_AMOUNT,
        account.address,
        0, 
        {'from': account}
    )
    tx.wait(1)
    print("Deposited")
    
    print("Lets Borrow...")
    eth_i_can_borrow, total_debt = get_user_data(lending_pool, account)

    # in order to borrow, we need to know the conversation rate
    dai_eth_price_feed_address = config['networks'][network.show_active()]['dai_price_feed']
    dai_to_eth_price = get_asset_price(dai_eth_price_feed_address)
    amount_dai_to_borrow = (1/dai_to_eth_price) * (eth_i_can_borrow * 0.95)
    print(f'You are going to borrow this much: {amount_dai_to_borrow}')
    dai_address = config['networks'][network.show_active()]['dai_token']
    tx = lending_pool.borrow(
        dai_address, 
        Web3.toWei(amount_dai_to_borrow, 'ether'),
        1, 
        0,
        account.address,
        {'from': account}
    )
    tx.wait(1)
    print(tx)
    print("Borrowing Dai Completed!")
    get_user_data(lending_pool, account)
    repay_all(Web3.toWei(amount_dai_to_borrow, "ether"), lending_pool, account)
    print("You just deposited, borrowed and repayed with AAVE, Brownie and Chainlink")
    get_user_data(lending_pool, account)

def repay_all(amount, lending_pool, account):
    approve_erc20(lending_pool, Web3.toWei(amount, 'ether'), config['networks'][network.show_active()]['dai_token'], account)
    tx = lending_pool.repay(
        config['networks'][network.show_active()]['dai_token'],
        amount,
        1,
        account.address,
        {'from': account}
    )
    tx.wait(1)
    print("REPAYED!!!!")


def get_asset_price(dai_eth_price_feed_address):
    dai_eth_price_feed = interface.IAggregatorV3Interface(dai_eth_price_feed_address)
    latest_price = dai_eth_price_feed.latestRoundData()[1]
    print("DAI/ETH LATEST PRICE: ", Web3.fromWei(latest_price, 'ether'))
    return float(latest_price)



def get_user_data(lending_pool, account):
    (total_collat_eth, total_debt_eth, available_borrow_eth, current_liquidation, ltv, health_factor) = lending_pool.getUserAccountData(account.address)
    available_borrow_eth = Web3.fromWei(available_borrow_eth, 'ether')
    total_collat_eth = Web3.fromWei(total_collat_eth, 'ether')
    total_debt_eth = Web3.fromWei(total_debt_eth, 'ether')

    print(f'You have total this much eth deposited: {total_collat_eth}')
    print(f'You have total this much eth in debt: {total_debt_eth}')
    print("*" * 70)
    print(f'You can borrow total this much eth: {available_borrow_eth}')

    return float(available_borrow_eth), float(total_debt_eth)



def deposit():
    pass


def approve_erc20(spender, amount, erc20_address, account):
    print("Approving ERC20 Token..")
    erc20 = interface.IERC20(erc20_address)
    tx = erc20.approve(spender, amount, {'from': account})
    tx.wait(1)
    print("Approved")
    return tx

def get_lending_pool():
    # we need the lending pool address provider contract to get the lending pool contract address
    lending_pool_addresses_provider = interface.ILendingPoolAddressesProvider(
        config['networks'][network.show_active()]['lending_pool_address_provider']
    )
    lending_pool_address = lending_pool_addresses_provider.getLendingPool()
    lending_pool = interface.ILendingPool(
        lending_pool_address
    )
    return lending_pool