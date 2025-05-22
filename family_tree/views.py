from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse

from family_tree.models import Person
from family_tree.forms import PersonForm


def index_view(request):
    context = {
        'objects_list': Person.objects.all(),
        'title': "<h1>Сайт семьи - Сапрыкины</h1>"
    }
    return render(request, 'family_tree/index.html', context=context)


def persons_list_view(request):
    context = {
        'objects_list': Person.objects.all(),
        'title': "Все члены семьи"
    }
    return render(request, 'family_tree/persons.html', context=context)


def person_create_view(request):
    if request.method == 'POST':
        form = PersonForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('family_tree:persons'))
    context = {
        'title': 'Добавить члена семьи',
        'form': PersonForm
    }
    return render(request, 'family_tree/person_create.html', context=context)