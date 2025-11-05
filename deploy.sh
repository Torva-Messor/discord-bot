git pull origin main
source venv/bin/activate
pip install -r requirements.txt
systemctl --user restart bot.service
