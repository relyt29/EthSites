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
        'reg_addr',
        type=str,
        help="The address of the registry contract stored on chain.")
    parser.add_argument(
        'filepath',
        type=str,
        help="Path to file upload to check against.")
    parser.add_argument(
        'position',
        type=int,
        help="The position (Entry ID) in the registry of the data to pull down")

    return parser.parse_args()


def main():
    '''
    Main method. Runs the program if it is used standalone (rather than as an exported library).
    '''

    parser = _get_args()
    #prov = Web3.HTTPProvider(parser.rpc_url)
    #w3 = Web3(prov)

    with open('./compiles/Registry.abi','r') as f:
        abi = json.loads(f.read())

    # Compress input with LZ
    with open(parser.filepath, 'r') as f:
        compressor = lzstring.LZString()
        upload_data = f.read()
        compressed_data = compressor.compressToUTF16(upload_data)
        print("Upload Data Length: {} | Compressed Data Length: {}".format(len(upload_data), len(compressed_data)))

    num_chunks = math.ceil(len(compressed_data) / BYTES_PER_CHUNK )
    print("Total length of input {}, Number chunks {}".format(len(upload_data),num_chunks))

    registry = w3.eth.contract(address=parser.reg_addr, abi=abi)

    out_compressed_len = registry.functions.getLen(parser.position).call()
    if out_compressed_len != len(compressed_data):
        print("Error out len does not match what it should {} | {}".format(out_compressed_len, len(compressed_data)))
        return
    print("Lens match, is good")

    reconstructor = ''
    for chunk_index in range(0, num_chunks):
        this_chunk = registry.functions.get(parser.position,chunk_index).call().decode("utf-16")
        reconstructor += this_chunk

    if not (reconstructor == compressed_data):
        print(reconstructor)
        print(compressed_data)
        print("They don't match")
    else:
        print("They match. Success, everything works.")

if __name__ == "__main__":
    main()


