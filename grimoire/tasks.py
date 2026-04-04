from celery import shared_task
from django.core.files.base import ContentFile
from PIL import Image
from io import BytesIO

#todo may change the converting, but will see
@shared_task
def process_grimoire_image(grimoire_id):
    """
    Process and optimize grimoire image asynchronously.
    - Resize image to standard dimensions
    - Compress for web optimization
    """
    from grimoire.models import Grimoire
    from django.core.files.base import ContentFile
    import requests
    
    try:
        grimoire = Grimoire.objects.get(id=grimoire_id)
        
        if not grimoire.image:
            return {"status": "error", "message": "No image found"}
        
        # Get image URL (works with both local and Cloudinary)
        image_url = grimoire.image.url if hasattr(grimoire.image, 'url') else str(grimoire.image)
        
        # If it's a Cloudinary URL, skip processing (Cloudinary handles optimization)
        if 'cloudinary' in image_url:
            return {"status": "success", "message": "Image stored in Cloudinary (no local processing needed)"}
        
        # Local image processing
        img = Image.open(grimoire.image.path)
        
        # Convert RGBA to RGB if needed
        if img.mode in ('RGBA', 'LA', 'P'):
            rgb_img = Image.new('RGB', img.size, (255, 255, 255))
            rgb_img.paste(img, mask=img.split()[-1] if img.mode == 'RGBA' else None)
            img = rgb_img
        
        # Resize to standard dimensions (800x600)
        img.thumbnail((800, 600), Image.Resampling.LANCZOS)
        
        # Compress and save
        img_io = BytesIO()
        img.save(img_io, format='JPEG', quality=85, optimize=True)
        img_io.seek(0)
        
        # Save processed image
        filename = f"grimoire_{grimoire_id}.jpg"
        grimoire.image.save(filename, ContentFile(img_io.read()), save=True)
        
        return {"status": "success", "message": "Image processed successfully"}
    
    except Grimoire.DoesNotExist:
        return {"status": "error", "message": f"Grimoire {grimoire_id} not found"}
    except Exception as e:
        return {"status": "error", "message": str(e)}
