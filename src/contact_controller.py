import io
import os
import qrcode
from fastapi import Response, Request, HTTPException, UploadFile, File
from fastapi.responses import HTMLResponse, FileResponse
from nest.core import Controller, Get, Post
from .contact_service import ContactService


@Controller("/contact")
class ContactController:
    """Controller for NFC contact sharing functionality"""
    
    def __init__(self, contact_service: ContactService):
        self.contact_service = contact_service

    @Get("/")
    def get_contact_page(self, request: Request):
        """Serve the main contact page with profile picture"""
        contact = self.contact_service.get_contact_info()
        base_url = str(request.base_url).rstrip('/')
        
        # Read the HTML template file directly
        try:
            template_path = os.path.join("templates", "contact.html")
            with open(template_path, 'r', encoding='utf-8') as f:
                html_content = f.read()
            
            # Simple template replacement
            html_content = html_content.replace("{{ contact.full_name }}", contact.full_name)
            html_content = html_content.replace("{{ contact.phone_number }}", contact.phone_number)
            html_content = html_content.replace("{{ contact.email }}", contact.email or "")
            html_content = html_content.replace("{{ contact.company }}", contact.company or "")
            html_content = html_content.replace("{{ contact.title }}", contact.title or "")
            html_content = html_content.replace("{{ contact.website }}", contact.website or "")
            html_content = html_content.replace("{{ base_url }}", base_url)
            
            # Handle conditional blocks for email
            if contact.email:
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
            
            # Handle conditional blocks for title
            if contact.title:
                html_content = html_content.replace("{% if contact.title %}", "")
            else:
                start_marker = "{% if contact.title %}"
                end_marker = "{% endif %}"
                start_idx = html_content.find(start_marker)
                if start_idx != -1:
                    end_idx = html_content.find(end_marker, start_idx) + len(end_marker)
                    html_content = html_content[:start_idx] + html_content[end_idx:]
            
            # Handle conditional blocks for company
            if contact.company:
                html_content = html_content.replace("{% if contact.company %}", "")
            else:
                start_marker = "{% if contact.company %}"
                end_marker = "{% endif %}"
                start_idx = html_content.find(start_marker)
                if start_idx != -1:
                    end_idx = html_content.find(end_marker, start_idx) + len(end_marker)
                    html_content = html_content[:start_idx] + html_content[end_idx:]
            
            # Handle conditional blocks for website
            if contact.website:
                html_content = html_content.replace("{% if contact.website %}", "")
            else:
                start_marker = "{% if contact.website %}"
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
        """Download vCard file for adding to phone contacts"""
        contact = self.contact_service.get_contact_info()
        vcard_content = self.contact_service.get_vcard()
        
        filename = f"{contact.first_name}_{contact.last_name}.vcf"
        
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
        """Generate QR code for the contact page URL"""
        try:
            # Create QR code pointing to the contact page
            contact_url = f"{str(request.base_url).rstrip('/')}/contact"
            
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
        """Get contact information as JSON"""
        contact = self.contact_service.get_contact_info()
        return {
            "name": contact.full_name,
            "phone": contact.phone_number,
            "email": contact.email,
            "company": contact.company,
            "title": contact.title,
            "website": contact.website
        }

    @Post("/update")
    def update_contact(self, contact_data: dict):
        """Update contact information"""
        try:
            updated_contact = self.contact_service.update_contact_info(contact_data)
            return {
                "success": True,
                "message": "Contact updated successfully",
                "contact": {
                    "name": updated_contact.full_name,
                    "phone": updated_contact.phone_number,
                    "email": updated_contact.email,
                    "company": updated_contact.company,
                    "title": updated_contact.title,
                    "website": updated_contact.website
                }
            }
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Error updating contact: {str(e)}")

    @Post("/upload-image")
    async def upload_profile_image(self, file: UploadFile = File(...)):
        """Upload and process profile image"""
        try:
            if not file.content_type.startswith('image/'):
                raise HTTPException(status_code=400, detail="File must be an image")
            
            image_data = await file.read()
            processed_image = self.contact_service.process_profile_image(image_data)
            
            return {
                "success": True,
                "message": "Image uploaded successfully",
                "image_data": processed_image
            }
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Error uploading image: {str(e)}")