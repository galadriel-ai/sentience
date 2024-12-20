#!/usr/bin/env bash

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

nohup vsock-proxy 8001 api.openai.com 443 \
  --config "$SCRIPT_DIR/vsock/vsock_proxy_openai.yaml" -w 20 \
  &> "$SCRIPT_DIR/vsock_proxy_openai.log" &