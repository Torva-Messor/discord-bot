#!/bin/bash

# === CONFIGURATION ===
SERVICE_NAME="discord-bot"
BOT_DIR="/opt/discord-bot"
BOT_USER="deploy"
BOT_GROUP="botgroup"   # <-- replace this with your actual group
ENV_FILE="$BOT_DIR/.env"
PYTHON_BIN="$BOT_DIR/venv/bin/python"
MAIN_FILE="$BOT_DIR/main.py"

SERVICE_PATH="/etc/systemd/system/$SERVICE_NAME.service"

# === CREATE SYSTEMD SERVICE ===
cat <<EOF > "$SERVICE_PATH"
[Unit]
Description=Discord Bot Service
After=network.target

[Service]
User=$BOT_USER
Group=$BOT_GROUP
WorkingDirectory=$BOT_DIR
EnvironmentFile=$ENV_FILE
ExecStart=$PYTHON_BIN $MAIN_FILE
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
EOF

echo "Service file created at $SERVICE_PATH"

# === SET DIRECTORY PERMISSIONS ===
echo "Ensuring $BOT_USER is in group $BOT_GROUP..."
usermod -aG "$BOT_GROUP" "$BOT_USER"

echo "Setting permissions for $BOT_DIR..."
chmod -R g+rx "$BOT_DIR"
# Allow writing if there is a logs or data directory
if [ -d "$BOT_DIR/logs" ]; then
    chmod -R g+w "$BOT_DIR/logs"
fi

# === RELOAD AND START SERVICE ===
systemctl daemon-reload
systemctl enable "$SERVICE_NAME.service"
systemctl start "$SERVICE_NAME.service"

echo "Service $SERVICE_NAME installed and started successfully!"
echo "Use: 'journalctl -u $SERVICE_NAME.service -f' to view logs."
