from scripts.advance import deploy_nft
from scripts import helper
from brownie import network
import pytest
import time

def test_can_create_advanced_collectible_integration():
    if(network.show_active() in helper.LCBE):
        pytest.skip()

    contract, tx = deploy_nft.deploy_and_create()
    randomNumber = 888

    time.sleep(60) #1 min

    assert contract.tokenCounter() == 1
