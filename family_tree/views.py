from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.template.loader import render_to_string

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
        'persons': Person.objects.all(),
        'title': "Все члены семьи"
    }
    return render(request, 'family_tree/persons.html', context=context)


@login_required(login_url='users:user_login')
def person_create_view(request):
    if request.method == 'POST':
        form = PersonForm(request.POST, request.FILES)
        if form.is_valid():
            person_object = form.save()
            person_object.creator = request.user
            person_object.save()
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


@login_required(login_url='users:user_login')
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

@login_required(login_url='users:user_login')
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



def tree_view(request, person_id=None):
    if person_id is None:
        person_id = 12  # корень дерева по умолчанию
    root_person = get_object_or_404(Person, pk=person_id)
    return render(request, 'family_tree/tree.html', {'root_person': root_person})

def tree_data_view(request, person_id):
    try:
        root = Person.objects.get(pk=person_id)
    except Person.DoesNotExist:
        return JsonResponse({"error": "Person not found"}, status=404)

    data = build_descendants_tree(root, is_spouse=False)
    return JsonResponse(data)


def spouse_tree_data(request, spouse_id):
    try:
        spouse = Person.objects.get(pk=spouse_id)
    except Person.DoesNotExist:
        return JsonResponse({"error": "Spouse not found"}, status=404)
    data = build_ancestors_tree(spouse)
    return JsonResponse(data)



def build_descendants_tree(person, is_spouse=False):
    spouse = person.spouse
    pair_html = render_to_string('family_tree/includes/inc_card_pair.html', {
        'person': person,
        'spouse': spouse if not is_spouse else None,  # Если это супруг, не показываем супруга (чтобы не зациклить)
    })

    children_nodes = []
    # Если это супруг — не строим детей
    if not is_spouse:
        for child in person.children():
            children_nodes.append(build_descendants_tree(child))

    return {
        "innerHTML": pair_html,
        "children": children_nodes,
        "person_id": person.id,
        "spouse_id": spouse.id if spouse else None
    }


def build_ancestors_tree(person):
    # Рендерим карточку человека и его супруга(и)
    pair_html = render_to_string('family_tree/includes/inc_card_pair.html', {
        'person': person,
        'spouse': person.spouse,  # Супруг(а) отображается, но его родители - нет
    })

    parents_nodes = []

    # Добавляем только родителей текущего человека (жены)
    if person.father:
        parents_nodes.append(build_ancestors_tree(person.father))

    if person.mother:
        parents_nodes.append(build_ancestors_tree(person.mother))

    return {
        "innerHTML": pair_html,
        "children": parents_nodes,
        "person_id": person.id,
        "spouse_id": person.spouse.id if person.spouse else None
    }


