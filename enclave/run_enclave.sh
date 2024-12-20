#!/usr/bin/env bash

# Get the directory of this script regardless of the current working directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Terminate any running enclave
ENCLAVE_ID=$(nitro-cli describe-enclaves | jq -r ".[0].EnclaveID")
[ "$ENCLAVE_ID" != "null" ] && nitro-cli terminate-enclave --enclave-id "${ENCLAVE_ID}"

# Build the Docker image using the directory of the script as build context
docker build \
  --label "org.opencontainers.image.source=https://github.com/galadriel-ai/aws-enclave" \
  --label "org.opencontainers.image.description=AWS Enclave Image" \
  --label "org.opencontainers.image.licenses=MIT" \
  -t "galadriel:latest" \
  "$SCRIPT_DIR"

# Remove the old EIF file if it exists
rm -f "$SCRIPT_DIR/galadriel.eif"

# Build the new EIF file
nitro-cli build-enclave \
  --docker-uri "galadriel:latest" \
  --output-file "$SCRIPT_DIR/galadriel.eif"

# Run the enclave from the absolute path of the EIF file
nitro-cli run-enclave \
  --cpu-count 2 \
  --memory 7000 \
  --eif-path "$SCRIPT_DIR/galadriel.eif"

# Uncomment below line if you want to describe enclaves after starting
# nitro-cli describe-enclaves

