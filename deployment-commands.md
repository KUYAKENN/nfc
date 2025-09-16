# Quick Commands to Deploy NFC App

# 1. Upload files to your server (run from your local machine)
scp -r ./src ./templates ./static ./main.py ./requirements.txt user@your-server:/var/www/nfc-contact/

# 2. SSH into your server
ssh user@your-server

# 3. Set up the application
cd /var/www/nfc-contact
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# 4. Test the app locally first
python main.py
# Should show: "Uvicorn running on http://0.0.0.0:5002"

# 5. Create systemd service (run once)
sudo nano /etc/systemd/system/nfc-contact.service
# Copy the service configuration from deploy.sh

# 6. Start the service
sudo systemctl daemon-reload
sudo systemctl enable nfc-contact
sudo systemctl start nfc-contact
sudo systemctl status nfc-contact

# 7. Update nginx configuration
sudo nano /etc/nginx/sites-available/recognitionbe.quanbyit.com
# Add the location /nfc/ block

# 8. Test and reload nginx
sudo nginx -t
sudo systemctl reload nginx

# 9. Check if it's working
curl http://localhost:5002/nfc/contact
# Should return HTML content

# 10. Test from outside
curl https://recognitionbe.quanbyit.com/nfc/contact
# Should return the contact page