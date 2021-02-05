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

#imports for delays and waiting
import time

mnemonic = os.getenv("MNEMONIC","""rough pull enemy remove resource toward army okay slender rapid uphold segment""")

# Function to derive children wallets based on mnemonic phrase input

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

# function to obtain the address(public) given the input of private key

def priv_key_to_account (coin,priv_key):
    """
    This function return the address of a wallet
    given its corresponding private key
    """
    if coin==ETH:
        account_address = Account.privateKeyToAccount(priv_key)
    if coin==BTCTEST:
        account_address = PrivateKeyTestnet(priv_key).address
    if coin==BTC:
        account_address = PrivateKey(priv_key).address

    return account_address

# function that creates the transaction for a cold wallet (it only signs the order)
# but doesn't send the order to the network

def create_tx(sender_acc_priv_key,recipient_address,amount,coin):
    if coin==BTCTEST:
        my_key_testnet = PrivateKeyTestnet(sender_acc_priv_key)
        outputs3 = [(recipient_address, amount, 'btc')]
        my_address_to_display = priv_key_to_account(BTCTEST,sender_acc_priv_key)
        print( my_address_to_display)
        wrap_prep_tx = my_key_testnet.prepare_transaction(my_address_to_display,outputs=outputs3)
        tx_hex=my_key_testnet.sign_transaction(wrap_prep_tx)
        return tx_hex

# function to send transactions to the network (it produces a message when send is succesful)


def send_tx(sender_acc_priv_key,recipient_address,amount,coin):
    """
    This function is to send cryptos from cold wallet
    """
    if coin==BTCTEST:
        prep_tx = create_tx(sender_acc_priv_key,recipient_address,amount,coin)
        NetworkAPI.broadcast_tx_testnet(prep_tx)
        sender_address_tx = PrivateKeyTestnet(sender_acc_priv_key).get_transactions()
        
    if coin==ETH:
        tx = create_tx(coin,account,recipient_address, amount)
        signed_tx = account.sign_transaction(tx)
        result = w3.eth.sendRawTransaction(signed_tx.rawTransaction)
        return result.hex()

    send_succ_message = 1
    print(amount, coin, "transaction successful")
    return send_succ_message

# function to send transactions to the network (it prints out the transaction id )


def send_tx_id (sender_acc_priv_key,recipient_address,amount,coin):
    send_message_succ = send_tx(sender_acc_priv_key,recipient_address,amount,coin)
    if send_message_succ==1:
        time.sleep(20)
        sender_address_tx = PrivateKeyTestnet("cNtNRuDWJcJfYxGZ8GCJVjq7xGzQ1gokMkALQuow3Wx3vvs7Z2Az").get_transactions()
        last_transac = sender_address_tx[0]
        return last_transac
    else:
        print("transaction failed")
    