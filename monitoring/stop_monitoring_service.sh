#!/bin/bash
if [ ! -f ".pid" ]; then
    echo "Enclave monitoring service not running"
    exit 1
fi
PID=$(cat .pid)
kill $PID
rm .pid
echo "Enclave monitoring service stopped"