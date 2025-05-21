from django.shortcuts import render

from family_tree.models import Person


def index(request):
    context = {
        'objects_list': Person.objects.all(),
        'title': "<h1>Сайт семьи - Сапрыкины</h1>"
    }
    return render(request, 'family_tree/index.html', context=context)
