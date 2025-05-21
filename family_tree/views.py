from django.shortcuts import render

from family_tree.models import Person


def index_view(request):
    context = {
        'objects_list': Person.objects.all(),
        'title': "<h1>Сайт семьи - Сапрыкины</h1>"
    }
    return render(request, 'family_tree/index.html', context=context)


def persons_list_view(request):
    context = {
        'objects_list': Person.objects.all,
        'title': "Все члены семьи"
    }
    return render(request, 'family_tree/persons_list.html', context=context)