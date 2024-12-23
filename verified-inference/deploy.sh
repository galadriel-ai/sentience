#!/usr/bin/env bash

# Get the directory where this script resides
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Use absolute paths based on the script directory
"$SCRIPT_DIR/host/stop_api_proxy.sh"
"$SCRIPT_DIR/enclave/run_proxies.sh"
"$SCRIPT_DIR/enclave/run_enclave.sh"
sleep 5
"$SCRIPT_DIR/host/run_api_proxy.sh"
sleep 5
python3 "$SCRIPT_DIR/host/check_connectivity.py"