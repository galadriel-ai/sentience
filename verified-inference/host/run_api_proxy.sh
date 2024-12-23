#!/usr/bin/env bash
SCRIPT="proxy.py"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "Starting $SCRIPT..."
nohup python "$SCRIPT_DIR/$SCRIPT" > "$SCRIPT_DIR/proxy.log" 2>&1 &
echo "Started $SCRIPT with PID $!"