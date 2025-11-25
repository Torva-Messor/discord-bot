#!/bin/bash

SERVICE_NAME="discord-bot"
BOT_DIR="$(pwd)"  # assuming deploy.sh is run from the bot directory
PYTHON_BIN="$BOT_DIR/venv/bin/python"

# --- Update bot code ---

echo "Pulling latest code..."
git pull origin main

# --- Update virtualenv packages ---

echo "Activating virtualenv and installing requirements..."
source "$BOT_DIR/venv/bin/activate"
pip install -r requirements.txt

# --- Restart service ---

echo "Restarting $SERVICE_NAME service..."
systemctl --user restart "$SERVICE_NAME.service"

echo "Deployment complete! Use 'journalctl --user -u $SERVICE_NAME.service -f' to view logs."
