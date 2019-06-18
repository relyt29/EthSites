EthSites: Welcome to the Eth Wide Web
============

This is the code repository for [EthSites.io](https://ethsites.io).

The code basically consists of a Registry contract that holds pointers to the actual websites themselves. The websites (right now) are stored in their own contracts that are deployed by the registry contract on chain. There is also some bootstrapper JavaScript that we have provided unminified in boostrapper.js that goes and gets the actual website data and displays it on the page. The one liner of javascript below in turn loads the bootstrapper code and executes it.

## Uploading a new Site

We have provided a python script you can use to upload your own website to the EthSites registry. You can use `pip install requirements.txt` and then run `python3 ./upload.py -h` for help text. If you have access to a full node, you can tweak the code to point back at your code instead of Infura. If using infura, make sure to `export INFURA_API_KEYS` so the environment is prepopulated before running the script. Here's an example:

```
python upload.py --start-gas 8000000 -r "https://infura.io/v3/<some infura key>:443" "Some raw private key exported from metamask" "some deployed registry contract address such as 0x0e46..." mywebsite.html
```

## Contract Deployment

The existing contract deployments are deployed on mainnet at [0x0e46d03b99aaa8b8cc093ffed5855b92d61f9609](https://etherscan.io/address/0x0e46d03b99aaa8b8cc093ffed5855b92d61f9609) for the Registry contract and [0x4CecEC099a5c8B554e6Ec0cdb7B7623f5016e20b](https://etherscan.io/address/0x4CecEC099a5c8B554e6Ec0cdb7B7623f5016e20b) for the Bootstrapper contract.

The contracts are also on ropsten at [0x1cdb4edd89390a6c62496534de721050e3a00ab5](https://ropsten.etherscan.io/address/0x1cdb4edd89390a6c62496534de721050e3a00ab5) (Registry) and [0x2829e431812cc3947f8471084ae013af0017ecb9](https://ropsten.etherscan.io/address/0x2829e431812cc3947f8471084ae013af0017ecb9) (Bootstrapper).

If you wish to deploy this contract on your own private testnet, see deploy.py.

## License

GPL 3.0 or later.

## Authors

This code was furiously written at the [IC3](https://www.initc3.org) [2019 Blockchain Boot Camp](https://www.initc3.org/events/2019-06-10-IC3-Blockchain-Boot-Camp.html).

Primarily written by [Tyler Kell](https://twitter.com/relyt29) (Cornell Tech, IC3), [Drake Eidukas](https://twitter.com/DrakeEidukas)(University of Illinois, IC3), and [Phil Daian](https://twitter.com/phildaian) (Cornell Tech, IC3)

We offer absolutely no support, guarantees, advice, or other help with this software. If you like it, use it.
