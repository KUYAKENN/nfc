import io
import os
import qrcode
from fastapi import Response, Request, HTTPException
from fastapi.responses import HTMLResponse
from nest.core import Controller, Get
from .contact_service import ContactInfo


@Controller("/nfc/chrisma")
class ChrismaController:
    """Controller for Chrisma Maxwell's NFC contact sharing"""
    
    def __init__(self):
        # Chrisma Maxwell's contact information
        self.contact = ContactInfo(
            first_name="Chrisma",
            last_name="Maxwell",
            phone_number="+63-928-310-5224",
            email="chrisma@quanbyit.com",
            company="QUANBY Solutions, Inc.",
            address="1862-B Dominga Street Pasay City",
            title="Chief Executive Officer",
            website="https://quanbyit.com",
            profile_image_path="static/profile.png"
        )

    @Get("/")
    def get_contact_page(self, request: Request):
        """Serve Chrisma's contact page"""
        base_url = str(request.base_url).rstrip('/')
        
        # Read the HTML template file directly
        try:
            template_path = os.path.join("templates", "contact.html")
            with open(template_path, 'r', encoding='utf-8') as f:
                html_content = f.read()
            
            # Simple template replacement
            html_content = html_content.replace("{{ contact.full_name }}", self.contact.full_name)
            html_content = html_content.replace("{{ contact.phone_number }}", self.contact.phone_number)
            html_content = html_content.replace("{{ contact.email }}", self.contact.email or "")
            html_content = html_content.replace("{{ contact.company }}", self.contact.company or "")
            html_content = html_content.replace("{{ contact.title }}", self.contact.title or "")
            html_content = html_content.replace("{{ contact.address }}", self.contact.address or "")
            html_content = html_content.replace("{{ contact.website }}", self.contact.website or "")
            html_content = html_content.replace("{{ base_url }}", base_url)
            
            # Handle conditional blocks for email
            if self.contact.email:
                # Keep email section
                html_content = html_content.replace("{% if contact.email %}", "")
                html_content = html_content.replace("{% endif %}", "")
            else:
                # Remove email section
                start_marker = "{% if contact.email %}"
                end_marker = "{% endif %}"
                start_idx = html_content.find(start_marker)
                if start_idx != -1:
                    end_idx = html_content.find(end_marker, start_idx) + len(end_marker)
                    html_content = html_content[:start_idx] + html_content[end_idx:]
            
            # Clean up any remaining template syntax
            html_content = html_content.replace("{% endif %}", "")
            
            return HTMLResponse(content=html_content)
            
        except FileNotFoundError:
            return HTMLResponse(content="<h1>Template not found</h1>", status_code=404)
        except Exception as e:
            return HTMLResponse(content=f"<h1>Error loading template: {str(e)}</h1>", status_code=500)

    @Get("/vcard")
    def download_vcard(self):
        """Download Chrisma's vCard file for adding to phone contacts"""
        vcard_content = self.contact.to_vcard()
        
        filename = f"Chrisma_Maxwell_Contact.vcf"
        
        return Response(
            content=vcard_content,
            media_type="text/vcard",
            headers={
                "Content-Disposition": f"attachment; filename={filename}",
                "Content-Type": "text/vcard; charset=utf-8"
            }
        )

    @Get("/qr")
    def get_qr_code(self, request: Request):
        """Generate QR code for Chrisma's contact page URL"""
        try:
            # Create QR code pointing to Chrisma's contact page
            contact_url = f"{str(request.base_url).rstrip('/')}/nfc/chrisma"
            
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=10,
                border=4,
            )
            qr.add_data(contact_url)
            qr.make(fit=True)
            
            # Create QR code image
            qr_img = qr.make_image(fill_color="black", back_color="white")
            
            # Convert to bytes
            img_buffer = io.BytesIO()
            qr_img.save(img_buffer, format='PNG')
            img_buffer.seek(0)
            
            return Response(
                content=img_buffer.getvalue(),
                media_type="image/png",
                headers={"Cache-Control": "public, max-age=3600"}
            )
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error generating QR code: {str(e)}")

    @Get("/info")
    def get_contact_info(self):
        """Get Chrisma's contact information as JSON"""
        return {
            "name": self.contact.full_name,
            "phone": self.contact.phone_number,
            "email": self.contact.email,
            "company": self.contact.company,
            "title": self.contact.title,
            "website": self.contact.website,
            "address": self.contact.address
        }