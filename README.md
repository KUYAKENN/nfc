# NFC Contact Sharing Application

This application creates an NFC-enabled contact sharing system that allows users to tap an NFC tag and save contact information directly to their phone, complete with a profile picture display.

## Features

- **NFC Contact Sharing**: When users tap an NFC tag, they are directed to a contact page
- **vCard Download**: Automatic download of contact information in vCard format for easy saving to phone contacts
- **Profile Picture Display**: Beautiful contact card with profile image
- **QR Code Generation**: Alternative sharing method via QR code
- **Responsive Design**: Mobile-optimized interface
- **RESTful API**: JSON endpoints for contact information

## Setup Instructions

1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Add Profile Image**:
   - Place your profile image as `static/profile.jpg`
   - The app will automatically display it on the contact page

3. **Configure Contact Information**:
   - Edit `src/contact_service.py` to update your contact details
   - Modify the `ContactInfo` object with your information

4. **Run the Application**:
   ```bash
   python main.py
   ```
   The app will run on `http://localhost:5002`

## NFC Setup

### For NFC Tags:
1. Use an NFC writing app on your phone
2. Write the URL: `http://YOUR_SERVER_IP:5002/nfc/contact`
3. When someone taps the NFC tag, they'll be directed to your contact page

### For Testing:
- Visit `http://localhost:5002/nfc/contact` to see the contact page
- Visit `http://localhost:5002/nfc/contact/vcard` to download the vCard
- Visit `http://localhost:5002/nfc/contact/qr` to see the QR code

## API Endpoints

- `GET /nfc/contact/` - Contact page with profile picture
- `GET /nfc/contact/vcard` - Download vCard file
- `GET /nfc/contact/qr` - Generate QR code for contact URL
- `GET /nfc/contact/info` - JSON contact information
- `POST /nfc/contact/update` - Update contact information
- `POST /nfc/contact/upload-image` - Upload new profile image
- `GET /nfc/static/{filename}` - Serve static files (images)

## How It Works

1. **NFC Tag Interaction**: When someone taps your NFC tag with their phone, they're automatically directed to your contact page
2. **Contact Display**: The page shows a beautiful contact card with your profile picture, name, phone, email, and company information
3. **Save to Contacts**: Users can tap "Save to Contacts" to download a vCard file that automatically adds your information to their phone's contacts
4. **Direct Actions**: Quick action buttons for calling or emailing you directly

## Customization

### Update Contact Information
Edit the `ContactInfo` object in `src/contact_service.py`:

```python
self.contact = ContactInfo(
    first_name="Your First Name",
    last_name="Your Last Name",
    phone_number="+1-555-0123",
    email="your.email@company.com",
    company="Your Company",
    title="Your Title",
    website="https://yourwebsite.com",
    profile_image_path="static/profile.png"
)
```

### Styling
Modify `templates/contact.html` to customize the appearance of your contact page.

## Deployment

For production deployment:
1. Update the host configuration in `main.py`
2. Use a reverse proxy like nginx
3. Enable HTTPS for security
4. Update NFC tags with your production URL

## Troubleshooting

- **Import Errors**: Make sure all dependencies are installed with `pip install -r requirements.txt`
- **Profile Image Not Showing**: Ensure `static/profile.jpg` exists and is accessible
- **Port Conflicts**: The app runs on port 5002 by default. Change the port in `main.py` if needed
