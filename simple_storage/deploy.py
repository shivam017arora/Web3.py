from solcx import compile_standard
import json
import os

with open("SimpleStorage.sol") as file:
    contract = file.read()

compiled_sol = compile_standard(
    {
        "language": "Solidity",
        "sources": {"SimpleStorage.sol": {"content": contract}},
        "settings": {"outputSelection": {"*": {"*": ["*"]}}},
    },
    solc_version="0.8.0",
)

with open("contract.json", "w") as file:
    json.dump(compiled_sol, file)

bytecode = compiled_sol['contracts']['SimpleStorage.sol']['SimpleStorage']['evm']['bytecode']['object']

abi = compiled_sol['contracts']['SimpleStorage.sol']['SimpleStorage']['abi']

from web3 import Web3 #deploy but to where?

#connect to ganache
server = 'https://rinkeby.infura.io/v3/231a54f73ded4902b7870eea9ecf4e5b'
chainId = 4
address = '0xA37a0eE21f5964B27fD577002Ed93e75d3357244'
private_key = os.getenv('privatekey')
w3 = Web3(Web3.HTTPProvider(server))
SimpleStorage = w3.eth.contract(abi=abi, bytecode=bytecode)
nonce = w3.eth.getTransactionCount(address)

#make transaction
transaction = SimpleStorage.constructor().buildTransaction({'chainId': chainId, 'from': address, 'nonce': nonce, 'gasPrice': w3.eth.gas_price})
#sign 
signed_transaction = w3.eth.account.signTransaction(transaction, private_key)
#send
tx_hash = w3.eth.sendRawTransaction(signed_transaction.rawTransaction)
#get tx_receipt
tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
#get contract address
contract_address = tx_receipt.contractAddress
print("Contract Address: ", contract_address)

#working with the contract

simple_storage = w3.eth.contract(address=tx_receipt.contractAddress, abi=abi)
print(simple_storage) #contract object

#make transaction to store
#get latest nonce
nonce = w3.eth.getTransactionCount(address)
store_tx = simple_storage.functions.store(15).buildTransaction(
    {
        'chainId': chainId, 
        'from': address, 
        'nonce': nonce, 
        'gasPrice': w3.eth.gas_price
    }
)
#sign
signed_store_tx = w3.eth.account.signTransaction(store_tx, private_key)
#send
sent_store_tx = w3.eth.sendRawTransaction(signed_store_tx.rawTransaction)
#get tx_receipt
store_tx_receipt = w3.eth.wait_for_transaction_receipt(sent_store_tx)

print(simple_storage.functions.retrieve().call()) #call function
