from dotenv import load_dotenv
load_dotenv()

import os
import time
from pathlib import Path

from brownie.network import accounts
from brownie.network.account import LocalAccount

from pybundlr import pybundlr
from web3.main import Web3

from ocean_lib.example_config import get_config_dict
from ocean_lib.ocean.ocean import Ocean
from ocean_lib.web3_internal.utils import connect_to_network

def create_ocean_instance(network_name: str) -> Ocean:
    config = get_config_dict(network_name)
    config["BLOCK_CONFIRMATIONS"] = 1  # faster
    connect_to_network(network_name)
    ocean = Ocean(config)
    return ocean

def create_alice_wallet(ocean: Ocean) -> LocalAccount:
    config = ocean.config_dict
    alice_private_key = os.getenv("REMOTE_PRIVATE_KEY")
    alice_wallet = accounts.add(alice_private_key)
    bal = Web3.fromWei(accounts.at(alice_wallet.address).balance(), "ether")
    print(f"alice_wallet.address={alice_wallet.address}. bal={bal}")
    assert bal > 0, f"Alice needs MATIC"
    return alice_wallet

if __name__ == "__main__":
    file_name = "../data/predictions.csv"
    ocean = create_ocean_instance("polygon-test") # change the network name if needed
    alice_wallet = create_alice_wallet(ocean) #you're Alice

    # # this step assumes "matic" currency. You could also use "eth", "ar", etc.
    # url = pybundlr.fund_and_upload(file_name, "matic", alice_wallet.private_key)

    # #e.g. url = "https://arweave.net/qctEbPb3CjvU8LmV3G_mynX74eCxo1domFQIlOBH1xU"
    # print(f"Your csv url: {url}")

    # name = "ETH predictions " + str(time.time()) #time for unique name
    # (data_nft, datatoken, asset) = ocean.assets.create_url_asset(name, url, {"from":alice_wallet}, wait_for_aqua=False)
    # metadata_state = 5
    # data_nft.setMetaDataState(metadata_state, {"from":alice_wallet})
    # print(f"New asset created, with did={asset.did}, and datatoken.address={datatoken.address}")

    # to_address="0xA54ABd42b11B7C97538CAD7C6A2820419ddF703E" # official judges address
    # datatoken.mint(to_address, Web3.toWei(10, "ether"), {"from": alice_wallet})