#!/bin/bash

SYSTEMD_PATH="$HOME/.config/systemd/user"

mkdir -p "$SYSTEMD_PATH"
cd "$SYSTEMD_PATH"

cat <<EOF > bot.service
[Unit]
Description=Discord Bot Service
After=network.target

[Service]
User=%u
WorkingDirectory=%h/discord-bot/
EnvironmentFile=%h/discord-bot/.env
ExecStart=%h/discord-bot/venv/bin/python %h/discord-bot/main.py
Restart=always
RestartSec=5

[Install]
WantedBy=default.target
EOF

systemctl --user daemon-reload
systemctl --user enable bot.service
systemctl --user start bot.service

echo "Service installed and started!"
