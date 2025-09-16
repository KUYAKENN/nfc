#!/bin/bash
# Deployment script for NFC Contact App

echo "🚀 Deploying NFC Contact Application..."

# Create deployment directory
sudo mkdir -p /var/www/nfc-contact
sudo chown $USER:$USER /var/www/nfc-contact

# Copy application files
echo "📂 Copying application files..."
# You would run this from your local machine:
# scp -r ./nfc-app/* user@your-server:/var/www/nfc-contact/

# Install Python dependencies
echo "📦 Installing dependencies..."
cd /var/www/nfc-contact
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Create systemd service
echo "⚙️ Creating systemd service..."
sudo tee /etc/systemd/system/nfc-contact.service > /dev/null <<EOF
[Unit]
Description=NFC Contact Application
After=network.target

[Service]
Type=simple
User=$USER
WorkingDirectory=/var/www/nfc-contact
Environment=PATH=/var/www/nfc-contact/venv/bin
ExecStart=/var/www/nfc-contact/venv/bin/python main.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

# Enable and start service
sudo systemctl daemon-reload
sudo systemctl enable nfc-contact
sudo systemctl start nfc-contact

echo "✅ NFC Contact app deployed and running on port 5002"
echo "🔧 Now configure nginx to route /nfc/ requests to localhost:5002"