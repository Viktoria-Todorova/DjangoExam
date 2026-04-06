from celery import shared_task
from django.core.files.base import ContentFile
from PIL import Image, ImageOps
from io import BytesIO
import uuid

#this is only for the sake of async operation, claudinary is doing most of this job.
@shared_task(bind=True, autoretry_for=(Exception,), retry_backoff=5, max_retries=3)
def process_grimoire_image(self, grimoire_id):

    from grimoire.models import Grimoire

    try:
        grimoire = Grimoire.objects.get(id=grimoire_id)

        if not grimoire.image:
            return {"status": "error", "message": "No image found"}


        grimoire.image.open()
        img = Image.open(grimoire.image.file)


        img = ImageOps.exif_transpose(img)


        if img.mode in ("RGBA", "LA", "P"):
            img = img.convert("RGB")


        img = ImageOps.fit(img, (800, 600), Image.Resampling.LANCZOS)


        img_io = BytesIO()
        img.save(img_io, format="JPEG", quality=80, optimize=True)
        img_io.seek(0)

        filename = f"grimoire_{grimoire_id}_{uuid.uuid4().hex[:8]}.jpg"


        grimoire.image.save(
            filename,
            ContentFile(img_io.read()),
            save=True
        )


        grimoire.image.close()

        return {
            "status": "success",
            "message": "Image processed successfully"
        }

    except Grimoire.DoesNotExist:
        return {
            "status": "error",
            "message": f"Grimoire {grimoire_id} not found"
        }

    except Exception as e:
        raise e