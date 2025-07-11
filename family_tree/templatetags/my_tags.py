from django import template

register = template.Library()


@register.filter()
def person_media(val):
    """ Формирует путь к фото человека.
    - Если фото есть, показывает фото
    - Если фото нет, показывает заглушку """
    if val:
        return f'/media/{val}'
    return ('/static/img/no-photo.jpg')


@register.filter()
def user_media(val):
    """ Формирует путь к аватарке человека.
    - Если аватарка есть, показывает аватарку
    - Если аватарки нет, показывает заглушку """
    if val:
        return fr'/media/{val}'
    return ('/static/img/default-avatar.jpg.')
