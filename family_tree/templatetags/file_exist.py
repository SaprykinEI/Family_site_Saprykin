from django import template

register = template.Library()

@register.filter
def file_exists(photo_field):
    """
    Проверяет, существует ли файл, связанный с полем изображения.
    Используется в шаблоне inc_card_tree для проверки наличия фото перед отображением.
     """
    if not photo_field:
        return False
    try:
        return photo_field.storage.exists(photo_field.name)
    except Exception:
        return False
