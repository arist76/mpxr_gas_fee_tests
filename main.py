from web3 import Web3
import json


# Connect to the Ethereum network (replace with your network URL)
provider_url = "https://polygon-amoy.drpc.org"
web3 = Web3(Web3.HTTPProvider(provider_url))

with open("mpxr_abi.json", "r") as json_file:
    contract_abi = json.load(json_file)

contract_address = "0x59F859C266f81349f97F0a1ab1b6CBAa5564DDc6"

contract = web3.eth.contract(address=contract_address, abi=contract_abi)

account = web3.eth.account.from_key(
    "e83bf38a5138f052edd87f895711fb8cd1b4aabd6e0ed0b29c009b0f606ec759"
)


# Function to measure gas for batchTransfer and batchUpdate
def measure_gas(users_count, batch_func_name):
    # Generate dummy users and amounts
    receivers = [
        Web3.to_checksum_address(f"0x{str(i).zfill(40)}")
        for i in range(1, users_count + 1)
    ]
    amounts = [2 * 10**6] * users_count

    # Prepare transaction
    txn = contract.functions[batch_func_name](receivers, amounts).build_transaction(
        {
            "from": account.address,
            "nonce": web3.eth.get_transaction_count(account.address),
            "gas": 8000000,
            "gasPrice": web3.to_wei("20", "gwei"),
        }
    )

    # Sign transaction
    signed_txn = web3.eth.account.sign_transaction(
        txn, private_key=account._private_key
    )

    # Estimate gas
    gas_estimate = web3.eth.estimate_gas(
        {"to": contract_address, "data": txn["data"], "from": account.address}
    )

    return gas_estimate


# Users count to test
users_counts = [1, 5, 10, 20, 50, 100, 500, 1000]

# Measure gas for batchTransfer
for users_count in users_counts:
    gas = measure_gas(users_count, "batchTransfer")
    print(f"Gas for batchTransfer with {users_count} users: {gas}")
