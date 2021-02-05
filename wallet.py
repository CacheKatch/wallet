# import constants
from constants import BTC
from constants import ETH
from constants import BTCTEST
from constants import LTC

# imports needed for env loads
import os
from dotenv import load_dotenv

load_dotenv()

# imports needed for mnemonic phrase wallet derive
import subprocess
import json

#imports for bitcoin and ethereum transactions
from web3 import Web3
from web3.middleware import geth_poa_middleware
from eth_account import Account
from bit import wif_to_key
from bit import PrivateKeyTestnet
from bit import PrivateKey
from bit import Key

#imports to broadcast bitcoins and bit-test
from bit.network import NetworkAPI

#imports to work in pandas
import pandas as pd

mnemonic = os.getenv("MNEMONIC","""rough pull enemy remove resource toward army okay slender rapid uphold segment""")

def derive_wallets(coin_name, mnemonic=mnemonic ,numb_derive=3):
    command = f'php derive -g --mnemonic="{mnemonic}" --cols=address,privkey,pubkey --numderive={numb_derive} --coin={coin_name} --format=json'
    p =subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
    (output, err) =p.communicate()
    p.wait()
    keys = json.loads(output)
    return keys

coins={"eth":derive_wallets(ETH),
    "btc-test":derive_wallets(BTCTEST),
    "btc":derive_wallets(BTC),
    "ltc":derive_wallets(LTC)}

def priv_key_to_account (coin,priv_key):
    """
    This function return the address of a wallet child
    given its corresponding private key
    """
    if coin==ETH:
        return Account.privateKeyToAccount(priv_key)
    if coin==BTCTEST:
        return  PrivateKeyTestnet(priv_key)
    if coin==BTC:
        return PrivateKey(priv_key)
    