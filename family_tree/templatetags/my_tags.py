from django import template

register = template.Library()

@register.filter()
def person_media(val):
    if val:
        return f'/media/{val}'
    return ('/static/img/no-photo.jpg')


@register.filter()
def user_media(val):
    if val:
        return fr'/media/{val}'
    return ('/static/img/default-avatar.jpg.')