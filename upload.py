#!/usr/bin/env python3

from eth_abi import encode_abi
from eth_account import Account
from eth_utils import (
    encode_hex,
    function_abi_to_4byte_selector,
)
import time, json
from web3 import Web3
#from web3.auto.infura import w3
import argparse
import math
import lzstring
import pprint

BYTES_PER_CHUNK = 9216

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
        '-t',
        '--timeout',
        required=False,
        type=int,
        default=999999999,
        help="The timeout to wait, in seconds.")
    parser.add_argument(
        'key',
        type=str,
        help="The Ethereum raw private key for the address that you wish to use to store with."
             " This address must have enough money to store with.")
    parser.add_argument(
        'reg_addr',
        type=str,
        help="The address of the registry contract stored on chain.")
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

    parser.add_argument(
        'filepath',
        type=str,
        help="Path to file to upload.")

    return parser.parse_args()


def main():
    '''
    Main method. Runs the program if it is used standalone (rather than as an exported library).
    '''

    parser = _get_args()
    prov = Web3.HTTPProvider(parser.rpc_url) # not necessary if using infura
    w3 = Web3(prov)

    with open('./compiles/Registry.abi','r') as f:
        abi = json.loads(f.read())
    acct = Account.privateKeyToAccount(parser.key)
    pool_addr = acct.address

    pp = pprint.PrettyPrinter(indent=4)

    # Compress input with LZ
    with open(parser.filepath, 'r') as f:
        compressor = lzstring.LZString()
        upload_data = f.read()
        compressed_data = compressor.compressToUTF16(upload_data)
        print("Upload Data Length: {} | Compressed Data Length: {}".format(len(upload_data), len(compressed_data)))

    num_chunks = math.ceil(len(compressed_data) / BYTES_PER_CHUNK )
    print("Total length of input {}, Number chunks {}".format(len(upload_data),num_chunks))

    start_nonce = w3.eth.getTransactionCount(pool_addr)
    curr_nonce = start_nonce

    registry = w3.eth.contract(address=parser.reg_addr, abi=abi)

    addEntry_transaction = registry.functions.addEntry(len(compressed_data)).buildTransaction({
            "nonce": curr_nonce,
            "gas": parser.start_gas, # 1M, 0x1a | 216k 5
            "gasPrice": (parser.gas_price),
    })
    curr_nonce += 1
    signed_transaction = w3.eth.account.signTransaction(addEntry_transaction, private_key=parser.key)
    signed_transaction_hash = signed_transaction.hash.hex()
    txn_sent = w3.eth.sendRawTransaction(signed_transaction.rawTransaction)
    if str(txn_sent.hex()) != signed_transaction_hash:
        raise(Exception("Error hashes not matching {}, {}".format(txn_sent, signed_transaction_hash)))
    receipt = w3.eth.waitForTransactionReceipt(signed_transaction_hash)
    entry_id = int(registry.functions.numEntries().call()) - 1
    print("Added Entry: {}".format(entry_id))

    tx_dict = {}
    for chunk_index in range(0, num_chunks):
        start = chunk_index * BYTES_PER_CHUNK
        if (num_chunks - 1) == chunk_index: # then we are on the last iteration
            finish = len(compressed_data)
        else:
            finish = (chunk_index + 1) * BYTES_PER_CHUNK # careful -1 needed depending on language / slice notation
        chunk_data = compressed_data[start:finish]
        chunk_data = bytes(chunk_data, 'utf-16')
        addChunk_transaction = registry.functions.addChunk(entry_id, chunk_index, chunk_data).buildTransaction({
            "nonce": curr_nonce,
            "gas": parser.start_gas, # 1M, 0x1a | 216k 5
            "gasPrice": parser.gas_price,
        })
        curr_nonce += 1
        signed_transaction = w3.eth.account.signTransaction(addChunk_transaction, private_key=parser.key)
        signed_transaction_hash = signed_transaction.hash.hex()
        tx_dict[signed_transaction_hash] = None
        txn_sent = w3.eth.sendRawTransaction(signed_transaction.rawTransaction)
    pp.pprint(tx_dict)
    count_confirmed = 0
    while count_confirmed < len(tx_dict):
        for ele in tx_dict:
            tx_receipt = w3.eth.getTransaction(ele)
            if tx_receipt is not None and tx_dict[ele] is None:
                tx_dict[ele] = True
                count_confirmed += 1
        print("Confirmed TXs {} out of {} ".format(count_confirmed, num_chunks))
        if (count_confirmed % 5 ) == 0:
            pp.pprint(tx_dict)
    print("finalizing")
    finalize_transaction = registry.functions.finalize(entry_id).buildTransaction({
            "nonce": curr_nonce,
            "gas": parser.start_gas, # 1M, 0x1a | 216k 5
            "gasPrice": (parser.gas_price),
    })
    curr_nonce += 1
    signed_transaction = w3.eth.account.signTransaction(finalize_transaction, private_key=parser.key)
    signed_transaction_hash = signed_transaction.hash.hex()
    txn_sent = w3.eth.sendRawTransaction(signed_transaction.rawTransaction)
    receipt = w3.eth.waitForTransactionReceipt(signed_transaction_hash)
    print("Finalized. File uploaded at entry {}".format(entry_id))


if __name__ == "__main__":
    main()


