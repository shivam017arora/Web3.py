from scripts.advance import deploy_nft
from scripts import helper
from brownie import network
import pytest

def test_can_create_advanced_collectible():
    if(network.show_active() not in helper.LCBE):
        pytest.skip()

    contract, tx = deploy_nft.deploy_and_create()
    requestID = tx.events["requestedCollectible"]['requestID']
    randomNumber = 888
    # this is what a chainlink node is gonna do when we call requestRandomness
    helper.get_contract('vrf_cordinator').callBackWithRandomness(requestID, randomNumber, contract.address, {'from': helper.get_account()})

    assert contract.tokenCounter() == 1
    assert contract.tokenIdToBreed(0) == randomNumber % 3
