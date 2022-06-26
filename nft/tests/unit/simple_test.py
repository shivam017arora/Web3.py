from scripts import helper
from scripts.simple import deploy_nft
from brownie import network
import pytest


def test_can_create_simple_collectible():
    if(network.show_active() not in helper.LCBE):
        pytest.skip()

    simple_collectible = deploy_nft.deploy_and_create()
    
    assert simple_collectible.ownerOf(0) == helper.get_account()

    