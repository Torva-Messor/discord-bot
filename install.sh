#!/bin/bash

BOT_ROOT="$HOME/discord-bot"
USER="deploy"
SYSTEMD_PATH="$HOME/.config/systemd/user"

mkdir -p "$SYSTEMD_PATH"
cd "$SYSTEMD_PATH"

cat <<EOF > bot.service
[Unit]
Description=Discord Bot Service
After=network.target

[Service]
User=$USER
WorkingDirectory=$BOT_ROOT
EnvironmentFile=/etc/environment
ExecStart=$BOT_ROOT/venv/bin/python $BOT_ROOT/discord-bot/main.py
Restart=always
RestartSec=5

[Install]
WantedBy=default.target
EOF

systemctl --user daemon-reload
systemctl --user enable bot.service
systemctl --user start bot.service

echo "Service installed and started!"
