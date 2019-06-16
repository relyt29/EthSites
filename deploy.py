#!/usr/bin/env python3

from eth_abi import encode_abi
from eth_account import Account
from eth_utils import (
    encode_hex,
    function_abi_to_4byte_selector,
)
import time, json
#from web3 import Web3
from web3.auto.infura import w3
import argparse
import math
import lzstring
from eth_account import Account

def _get_args():
    '''
    Internal function. Creates an argparser for the main method to use.

    :return: parser: argparse object for parsing program arguments.
    '''
    parser = argparse.ArgumentParser(
        description=
        "Tool to upload/store files to the Ethereum blockchain",
        formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument(
        '-r',
        '--rpc-url',
        required=False,
        type=str,
        default="http://127.0.0.1:8545",
        help="The HTTP RPC Endpoint URL you wish to use.")
    parser.add_argument(
        'key',
        type=str,
        help="The Ethereum raw private key for the address that you wish to use to store with."
             " This address must have enough money to store with.")
    parser.add_argument(
        '--gas-price',
        required=False,
        type=int,
        default=(int(6e9) + 5),  # start gas price (1gwei + epsilon)
        help="Gas price to pay.")
    parser.add_argument(
        '--start-gas',
        required=False,
        type=int,
        default=999000,  # start gas price (1gwei + epsilon)
        help="Amount of Gas to pay in Wei.")

    return parser.parse_args()


def main():
    '''
    Main method. Runs the program if it is used standalone (rather than as an exported library).
    '''

    parser = _get_args()
    #prov = Web3.HTTPProvider(parser.rpc_url) # not necessary if using infura
    #w3 = Web3(prov)

    with open('./compiles/Registry.abi','r') as f:
        abi = json.loads(f.read())
    with open('./compiles/Registry.bin', 'r') as f:
        content = f.read()

    acct = Account.privateKeyToAccount(parser.key)
    pool_addr = acct.address

    tx = {
       'from': pool_addr,
       'gasPrice': 3000000000,
       'gas': 2000000,
       'value': 0,
       'data': content
    }
    tx['nonce'] = w3.eth.getTransactionCount(tx['from'])

    signed_tx = w3.eth.account.signTransaction(tx, parser.key)
    sent = w3.eth.sendRawTransaction(signed_tx.rawTransaction)
    receipt = w3.eth.waitForTransactionReceipt(sent)
    print(receipt)

if __name__ == "__main__":
    main()


