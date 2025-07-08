from django.core.management.base import BaseCommand
from gallery.models import Photo
from gallery.utils import convert_photo_to_webp

class Command(BaseCommand):
    """ Команда на конвертацию фото """
    help = 'Конвертирует все фото в WebP'

    def handle(self, *args, **options):
        photos = Photo.objects.all()
        self.stdout.write(f'Найдено {photos.count()} фото для конвертации.')

        for photo in photos:
            convert_photo_to_webp(photo)
            self.stdout.write(f'Конвертировано и удалено: {photo.image.name}')
