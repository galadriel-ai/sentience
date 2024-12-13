nohup vsock-proxy 8001 api.openai.com 443 \
  --config vsock/vsock_proxy_openai.yaml -w 20 &> vsock_proxy_openai.log &
  nohup vsock-proxy 8002 api.mainnet-beta.solana.com 443 \
  --config vsock/vsock_proxy_solana_mainnet.yaml -w 20 &> vsock_proxy_solana_mainnet.log &
  nohup vsock-proxy 8003 api.devnet.solana.com 443 \
  --config vsock/vsock_proxy_solana_devnet.yaml -w 20 &> vsock_proxy_solana_devnet.log &
