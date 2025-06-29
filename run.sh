#!/bin/bash
set -e

echo "Starting SFELAPCO Generation Charge Monitor..."

# Get configuration from Home Assistant options
CONFIG_PATH=/data/options.json

# Set defaults if config file doesn't exist
if [ -f "$CONFIG_PATH" ]; then
    echo "Reading configuration from $CONFIG_PATH"
    UPDATE_INTERVAL=$(jq --raw-output '.update_interval // 1.0' $CONFIG_PATH 2>/dev/null || echo "1.0")
    RETAIN_HISTORY=$(jq --raw-output '.retain_history // true' $CONFIG_PATH 2>/dev/null || echo "true")
    MAX_HISTORY_DAYS=$(jq --raw-output '.max_history_days // 365' $CONFIG_PATH 2>/dev/null || echo "365")
else
    echo "No config file found at $CONFIG_PATH, using defaults"
    UPDATE_INTERVAL=1.0
    RETAIN_HISTORY=true
    MAX_HISTORY_DAYS=365
fi

echo "Configuration:"
echo "  Update Interval: ${UPDATE_INTERVAL} days"
echo "  Retain History: ${RETAIN_HISTORY}"
echo "  Max History Days: ${MAX_HISTORY_DAYS}"

# Export configuration as environment variables
export UPDATE_INTERVAL
export RETAIN_HISTORY  
export MAX_HISTORY_DAYS

# Ensure data directory exists
mkdir -p /data

# Check Python installation
echo "Python version: $(python3 --version)"
echo "Python path: $(which python3)"

# Start the Python monitoring service
echo "Starting Python service..."
exec python3 /sfelapco_monitor.py