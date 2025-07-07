import re
from transliterate import translit
from django.utils.text import slugify

def slug_generator(title):
    """
       Генерирует slug из переданного текста (например, имени).
       - Транслитерирует русский текст в латиницу.
       - Заменяет пробелы и дефисы на один дефис.
       - Убирает лишние символы.
       - Приводит к нижнему регистру.
       - Пропускает через Django slugify.
    """
    if not title:
        return ''
    transliterated_title = translit(title, 'ru', reversed=True)
    slug = re.sub(r'[-\s]+', '-', transliterated_title)
    slug = re.sub(r'[^\w\-]', '', slug)
    slug = slug.lower()
    slug = slugify(slug)
    return slug
