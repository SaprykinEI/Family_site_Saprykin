from django import template

register = template.Library()

@register.filter
def file_exists(photo_field):
    if not photo_field:
        return False
    try:
        return photo_field.storage.exists(photo_field.name)
    except Exception:
        return False
