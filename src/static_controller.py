import os
from fastapi import HTTPException
from fastapi.responses import FileResponse
from nest.core import Controller, Get


@Controller("/nfc/static")
class StaticController:
    """Controller for serving static files like images"""
    
    def __init__(self):
        # Use absolute path to ensure we find the static directory
        self.static_dir = os.path.abspath("static")
    
    @Get("/{filename}")
    def serve_static_file(self, filename: str):
        """Serve static files like profile images"""
        file_path = os.path.join(self.static_dir, filename)
        
        if not os.path.exists(file_path):
            # Try current directory as fallback
            fallback_path = os.path.join("static", filename)
            if os.path.exists(fallback_path):
                file_path = fallback_path
            else:
                raise HTTPException(status_code=404, detail=f"File not found")
        
        # Determine media type based on file extension
        _, ext = os.path.splitext(filename)
        media_type_map = {
            '.jpg': 'image/jpeg',
            '.jpeg': 'image/jpeg',
            '.png': 'image/png',
            '.gif': 'image/gif',
            '.webp': 'image/webp'
        }
        
        media_type = media_type_map.get(ext.lower(), 'application/octet-stream')
        
        return FileResponse(
            path=file_path,
            media_type=media_type,
            headers={"Cache-Control": "public, max-age=3600"}
        )