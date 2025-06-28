import re
from transliterate import translit
from django.utils.text import slugify

def slug_generator(title):
    if not title:
        return ''
    transliterated_title = translit(title, 'ru', reversed=True)
    slug = re.sub(r'[-\s]+', '-', transliterated_title)
    slug = re.sub(r'[^\w\-]', '', slug)
    slug = slug.lower()
    slug = slugify(slug)
    return slug
