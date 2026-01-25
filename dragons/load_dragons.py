import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "LibraryProject.settings")
django.setup()
from dragons.models import Dragon

dragons_data = [
    {"name": "Pyroscale", "description": "A massive fire dragon with glowing red scales and a temper as hot as its breath.", "photo": "Pyroscale.jpg"},
    {"name": "Nightwing", "description": "A sleek, shadow-colored dragon that flies silently through the dark skies.", "photo": "Nightwing.jpg"},
    {"name": "Emberclaw", "description": "Smaller but extremely aggressive, with burning talons that leave scorch marks in stone.", "photo": "Emberclaw.jpg"},
    {"name": "Stormmaw", "description": "A thunder dragon that rides the clouds and breathes lightning instead of fire.", "photo": "Stormmaw.jpg"},
    {"name": "Ashenfyr", "description": "An ancient dragon covered in gray, smoke-stained scales that awakens only in times of war.", "photo": "Ashenfyr.jpg"},
    {"name": "Skylash", "description": "A fast and agile wind dragon known for racing storms and outmaneuvering enemies.", "photo": "Skylash.jpg"},
    {"name": "Frostveil", "description": "A pale blue ice dragon that exhales freezing mist and leaves frozen lakes behind.", "photo": "Frostveil.jpg"},
    {"name": "Dreadflame", "description": "A terrifying black dragon whose dark fire can melt armor and frighten other dragons.", "photo": "Dreadflame.jpg"}
]

for data in dragons_data:
    Dragon.objects.get_or_create(
        name=data["name"],
        defaults={
            "description": data["description"],
            "photo": data["photo"],
            "rider": None
        }
    )

print("✅ Dragons loaded into database")
