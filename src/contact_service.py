from dataclasses import dataclass
from typing import Optional
import base64
import io
from PIL import Image
from nest.core import Injectable


@dataclass
class ContactInfo:
    """Data model for contact information"""
    first_name: str
    last_name: str
    phone_number: str
    email: Optional[str] = None
    company: Optional[str] = None
    title: Optional[str] = None
    address: Optional[str] = None
    website: Optional[str] = None
    profile_image_path: Optional[str] = None

    @property
    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name}"

    def to_vcard(self) -> str:
        """Generate vCard format string for the contact"""
        vcard_lines = [
            "BEGIN:VCARD",
            "VERSION:3.0",
            f"FN:{self.full_name}",
            f"N:{self.last_name};{self.first_name};;;",
            f"TEL;TYPE=CELL:{self.phone_number}"
        ]
        
        if self.email:
            vcard_lines.append(f"EMAIL:{self.email}")
        
        if self.company:
            vcard_lines.append(f"ORG:{self.company}")
        
        if self.title:
            vcard_lines.append(f"TITLE:{self.title}")
        
        if self.address:
            vcard_lines.append(f"ADR:;;{self.address};;;;")
        
        if self.website:
            vcard_lines.append(f"URL:{self.website}")
        
        vcard_lines.append("END:VCARD")
        return "\n".join(vcard_lines)


@Injectable
class ContactService:
    """Service to handle contact operations"""
    
    def __init__(self):
        # Default contact information - you can modify this
        self.contact = ContactInfo(
            first_name="Maria Crisma",
            last_name="Maxwell",
            phone_number="+63-928-310-5224",
            email="maria@quanbyit.com",
            company="QUANBY Solutions, Inc.",
            address="1862-B Dominga Street Pasay City",
            title="Chief Executive Officer",
            website="https://quanbyit.com",
            profile_image_path="static/profile.png"
        )
    
    def get_contact_info(self) -> ContactInfo:
        """Get the current contact information"""
        return self.contact
    
    def update_contact_info(self, contact_data: dict) -> ContactInfo:
        """Update contact information"""
        for key, value in contact_data.items():
            if hasattr(self.contact, key):
                setattr(self.contact, key, value)
        return self.contact
    
    def get_vcard(self) -> str:
        """Get vCard format string"""
        return self.contact.to_vcard()
    
    def process_profile_image(self, image_data: bytes, max_size: tuple = (400, 400)) -> str:
        """Process and resize profile image"""
        try:
            image = Image.open(io.BytesIO(image_data))
            
            # Convert to RGB if necessary
            if image.mode in ('RGBA', 'LA', 'P'):
                image = image.convert('RGB')
            
            # Resize image while maintaining aspect ratio
            image.thumbnail(max_size, Image.Resampling.LANCZOS)
            
            # Save processed image
            output = io.BytesIO()
            image.save(output, format='JPEG', quality=85, optimize=True)
            
            return base64.b64encode(output.getvalue()).decode()
        except Exception as e:
            raise ValueError(f"Error processing image: {str(e)}")