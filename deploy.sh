#!/usr/bin/env bash

# Get the directory where this script resides
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Use absolute paths based on the script directory
"$SCRIPT_DIR/enclave/run_proxies.sh"
"$SCRIPT_DIR/enclave/run_enclave.sh"
"$SCRIPT_DIR/host/run_api_proxy.sh"
sleep 1
python3 "$SCRIPT_DIR/host/get_public_key.py"