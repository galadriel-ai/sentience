SCRIPT="proxy.py"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

PIDS=$(pgrep -f "$SCRIPT_DIR/$SCRIPT")

if [ -n "$PIDS" ]; then
    echo "Killing existing instance(s) of $SCRIPT..."
    kill $PIDS
    sleep 1
fi