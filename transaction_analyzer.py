import time
import json
from web3 import Web3

# Replace with your Infura or other Ethereum node provider URL
INFURA_URL = "https://mainnet.infura.io/v3/YOUR_INFURA_PROJECT_ID"

# Address to monitor
MONITORED_ADDRESS = "0xYourEthereumAddressHere"
# Set a threshold for transaction value in ETH
VALUE_THRESHOLD = 0.1  # 0.1 ETH

# Connect to the Ethereum network
web3 = Web3(Web3.HTTPProvider(INFURA_URL))

# Function to get the latest block number
def get_latest_block():
    return web3.eth.blockNumber

# Function to get all transactions in a block
def get_block_transactions(block_number):
    block = web3.eth.getBlock(block_number, full_transactions=True)
    return block['transactions']

# Function to check if the monitored address is involved in the transaction
def is_address_involved(tx, address):
    return tx['from'].lower() == address.lower() or tx['to'].lower() == address.lower()

# Function to filter transactions by value threshold
def filter_transactions_by_value(tx, threshold):
    value = web3.fromWei(tx['value'], 'ether')
    return value >= threshold

# Function to analyze the transactions in a given block
def analyze_transactions(block_number):
    print(f"Analyzing block {block_number}...")
    transactions = get_block_transactions(block_number)
    for tx in transactions:
        if is_address_involved(tx, MONITORED_ADDRESS):
            value = web3.fromWei(tx['value'], 'ether')
            if value >= VALUE_THRESHOLD:
                print(f"📦 Transaction found:")
                print(f"  From: {tx['from']}")
                print(f"  To: {tx['to']}")
                print(f"  Value: {value} ETH")
                print(f"  Hash: {tx['hash'].hex()}")
                print("-" * 40)

def main():
    print("=== Ethereum Transaction Analyzer ===")
    last_block = get_latest_block()
    
    while True:
        latest_block = get_latest_block()
        
        if latest_block > last_block:
            print(f"New block found: {latest_block}")
            analyze_transactions(latest_block)
            last_block = latest_block
        
        time.sleep(30)  # Check every 30 seconds

if __name__ == "__main__":
    main()
