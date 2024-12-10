# Enclave client

## Admin

Admin is responsible for:
1. Creating the enclave image
2. Starting the enclave
3. Getting the enclave public key and attestation doc
4. Publishing the enclave public key and attestation doc to the Oracle Contract

Flow:

```shell
python3 client.py --action send_secrets

# Request attestation doc from the enclave
python3 client.py --action get_attestation_doc
# Verify the attestation doc
python3 verify.py <pcr0 of the enclave> 
```

## Extra

Devnet faucet:

```shell
curl --location --request POST '0.0.0.0:9123/gas' \
--header 'Content-Type: application/json' \
--data-raw '{
    "FixedAmountRequest": {
        "recipient": "0x5a1c3cc19acfd04538fd7ae83195eb394d1836e4e3c085ce7b5cae9a74908dbc"
    }
}'

curl --header "Content-Type: application/json" \
  --request POST \
  --data '{"jsonrpc":"2.0","id":1,"method":"suix_getBalance","params":["0x5a1c3cc19acfd04538fd7ae83195eb394d1836e4e3c085ce7b5cae9a74908dbc"]}' \
  https://testnet.galadriel.com
```
