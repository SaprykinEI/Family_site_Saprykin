import os
from uuid import uuid4

def photo_upload_path(instance, filename):
    album_id = instance.album.id if instance.album else 'unknown'
    ext = filename.split('.')[-1]
    new_filename = f"{uuid4().hex}.{ext}"
    return os.path.join(f"album_{album_id}", "photos", new_filename)

def video_upload_path(instance, filename):
    album_id = instance.album.id if instance.album else 'unknown'
    ext = filename.split('.')[-1]
    new_filename = f"{uuid4().hex}.{ext}"
    return os.path.join(f"album_{album_id}", "videos", new_filename)
