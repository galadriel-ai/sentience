nohup vsock-proxy 8001 api.openai.com 443 \
  --config vsock/vsock_proxy_openai.yaml -w 20 &> vsock_proxy_openai.log &
