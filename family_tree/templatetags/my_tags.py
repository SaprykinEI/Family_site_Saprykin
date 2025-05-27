from django import template

register = template.Library()

@register.filter()
def person_media(val):
    if val:
        return fr'/media/{val}'
    return ('s'
            'static/img/no-photo.jpg')