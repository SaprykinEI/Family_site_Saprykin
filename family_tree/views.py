from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse

import json

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
        'persons': Person.objects.all(),  # <-- фикс здесь
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
    return render(request, 'family_tree/person_create_update.html', context=context)


def person_detail_view(request, pk):
    person_object = Person.objects.get(pk=pk)
    context = {
        'person': person_object,
        'title': person_object
    }
    return render(request, 'family_tree/person_detail.html', context=context)


def person_update_view(request, pk):
    person_object = get_object_or_404(Person, pk=pk)
    if request.method == 'POST':
        form = PersonForm(request.POST, request.FILES, instance=person_object)
        if form.is_valid():
            person_object = form.save()
            person_object.save()
            return HttpResponseRedirect(reverse('family_tree:person_detail', args={pk: pk}))
    context = {
        'object': person_object,
        'title': 'Редактировать данные',
        'form': PersonForm(instance=person_object)
    }
    return render(request, 'family_tree/person_create_update.html', context=context)


def person_delete_view(request, pk):
    person_object = get_object_or_404(Person, pk=pk)
    if request.method == 'POST':
        person_object.delete()
        return HttpResponseRedirect(reverse('family_tree:persons'))
    context = {
        'object': person_object,
        'title': "Удалить члена семьи"
    }
    return render(request, 'family_tree/person_delete.html', context=context)


