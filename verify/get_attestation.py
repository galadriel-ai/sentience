from web3 import Web3

web3 = Web3(Web3.HTTPProvider("https://testnet.galadriel.com/"))

# Make sure this is the right contract address of the oracle!
contract_address = '0xACB8a1fcC06f1a199C1782414E39BdB4A8238e69'
contract_abi = '[{"constant":true,"inputs":[{"name":"","type":"address"}],"name":"attestations","outputs":[{"name":"","type":"string"}],"payable":false,"stateMutability":"view","type":"function"}]'

contract = web3.eth.contract(address=contract_address, abi=contract_abi)

# Make sure this is the correct oracle address!
attestation_value = contract.functions.attestations("0xc01a943964937A642b223c414A05A707385531Af").call()

with open("attestation_doc_b64.txt", "w") as file:
    file.write(attestation_value)

print("Attestation saved to attestation_doc_b64.txt")
