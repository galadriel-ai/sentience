#!/bin/bash
if [ -f ".pid" ]; then
    echo "Enclave monitoring service already running"
    exit 1
fi
nohup uvicorn monitoring:app --host 0.0.0.0 --port 9101 &
echo $! > .pid
echo "Enclave monitoring service started"