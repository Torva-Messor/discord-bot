#!/bin/bash

# --- Variables ---

SERVICE_NAME="discord-bot"
BOT_DIR="/opt/discord-bot"            # Path to your bot directory
BOT_USER="$USER"                       # Current user
BOT_GROUP="$USER"                      # Current group (for user service)
ENV_FILE="$BOT_DIR/.env"               # Environment variables file
PYTHON_BIN="$BOT_DIR/venv/bin/python"  # Path to virtualenv Python
MAIN_FILE="$BOT_DIR/main.py"           # Main bot entry point
SERVICE_PATH="$HOME/.config/systemd/user/$SERVICE_NAME.service"  # User systemd path

# --- Create user service ---

mkdir -p "$(dirname "$SERVICE_PATH")"

cat <<EOF > "$SERVICE_PATH"
[Unit]
Description=Discord Bot Service
After=network.target

[Service]
WorkingDirectory=$BOT_DIR
EnvironmentFile=$ENV_FILE
ExecStart=$PYTHON_BIN $MAIN_FILE
Restart=always
RestartSec=5

[Install]
WantedBy=default.target
EOF

echo "Service file created at $SERVICE_PATH"

# --- Set permissions ---

chmod -R u+rx "$BOT_DIR"
if [ -d "$BOT_DIR/logs" ]; then
chmod -R u+rw "$BOT_DIR/logs"
fi

# --- Reload and start user service ---

systemctl --user daemon-reload
systemctl --user enable "$SERVICE_NAME.service"
systemctl --user start "$SERVICE_NAME.service"

echo "Service $SERVICE_NAME installed and started successfully (user mode)!"
echo "Use: 'journalctl --user -u $SERVICE_NAME.service -f' to view logs."
