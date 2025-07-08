import os
from uuid import uuid4
from PIL import Image

def photo_upload_path(instance, filename):
    """ Генерирует путь для сохранения фотографии при загрузке в модель. """
    album_id = instance.album.id if instance.album else 'unknown'
    ext = filename.split('.')[-1]
    new_filename = f"{uuid4().hex}.{ext}"
    return os.path.join(f"album_{album_id}", "photos", new_filename)

def video_upload_path(instance, filename):
    """ Генерирует путь для сохранения видео при загрузке в модель. """
    album_id = instance.album.id if instance.album else 'unknown'
    ext = filename.split('.')[-1]
    new_filename = f"{uuid4().hex}.{ext}"
    return os.path.join(f"album_{album_id}", "videos", new_filename)


def convert_photo_to_webp(photo):
    """ Конвертирует фото в формат WebP и заменяет старое изображение. """
    original_path = photo.image.path
    webp_path = os.path.splitext(original_path)[0] + '.webp'

    with Image.open(original_path) as im:
        im.save(webp_path, 'webp', quality=85)

    # Обновляем поле image в модели
    photo.image.name = photo.image.name.rsplit('.', 1)[0] + '.webp'
    photo.save(update_fields=['image'])

    # Удаляем оригинал
    if os.path.exists(original_path):
        os.remove(original_path)