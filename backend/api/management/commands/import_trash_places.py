import json
from django.core.management.base import BaseCommand
from django.utils import timezone
from api.models import TrashPlace  

class Command(BaseCommand):
    help = 'Import trash places from JSON file'

    def handle(self, *args, **kwargs):
        file_path = 'example_trash1.json'  

        with open(file_path, 'r') as f:
            trash_places = json.load(f)

        for item in trash_places:
            trash_level = item['scale'] 
            name = item['name']
            latitude = item['latitude']
            longitude = item['longitude']

            TrashPlace.objects.create(
                name=name,
                description=f"Uwaga! {name}",
                latitude=latitude,
                longitude=longitude,
                date_created=timezone.now(),  
                trash_level=trash_level, 
                is_active=True 
            )

        self.stdout.write(self.style.SUCCESS('Dane zostały zaimportowane pomyślnie!'))
