from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView



from family_tree.models import Person
from family_tree.forms import PersonForm
from gallery.models import Album


class IndexView(ListView):
    '''Представление для отображения главной страницы'''
    model = Person
    template_name = 'family_tree/index.html'
    context_object_name = 'person_list'

    def get_context_data(self, **kwargs):
        '''Переопределяем метод, чтобы добавить дополнительный контекст в шаблон.'''
        context = super().get_context_data(**kwargs)
        context['title'] = "<h1>Сайт семьи - Сапрыкины</h1>"
        context['latest_albums'] = Album.objects.order_by('-created_at')[:4]
        return context


class PersonsListView(ListView):
    '''Представление-класс для отображения всех членов семьи.'''
    model = Person
    template_name = 'family_tree/persons.html'
    context_object_name = 'persons'

    def get_context_data(self, **kwargs):
        ''' Добавляем в контекст дополнительную информацию'''
        context = super().get_context_data(**kwargs)
        context['title'] = "Все члены семьи"
        return context


class PersonCreateView(LoginRequiredMixin, CreateView):
    '''Представление-класс для создания нового члена семьи.'''
    model = Person
    form_class = PersonForm
    template_name = 'family_tree/person_create_update.html'
    success_url = reverse_lazy('family_tree:persons')
    login_url = 'users:user_login'

    def form_valid(self, form):
        '''Переопределяем поведение при успешной валидации формы.'''
        form.instance.creator = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        """Добавляем заголовок страницы в контекст шаблона."""
        context = super().get_context_data(**kwargs)
        context['title'] = "Добавить члена семьи"
        return context


class PersonDetailView(DetailView):
    '''Представление-класс для отображения подробной информации о человеке'''
    model = Person
    template_name = 'family_tree/person_detail.html'
    context_object_name = 'person'

    def get_context_data(self, **kwargs):
        '''Добавляем заголовка в шаблон.'''

        context = super().get_context_data(**kwargs)
        context['title'] = self.object
        return context


class PersonUpdateView(LoginRequiredMixin, UpdateView):
    '''Представление-класс для редактирования данных о человеке.'''
    model = Person
    form_class = PersonForm
    template_name = 'family_tree/person_create_update.html'
    context_object_name = 'object'
    login_url = 'users:user_login'

    def get_context_data(self, **kwargs):
        """Добавляем заголовок в контекст шаблона."""
        context = super().get_context_data(**kwargs)
        context['title'] = 'Редактировать данные'
        return context

    def get_success_url(self):
        """После успешного сохранения — перейти на страницу детального просмотра."""
        return reverse('family_tree:person_detail', args=[self.object.pk])


class PersonDeleteView(LoginRequiredMixin, DeleteView):
    """Представление-класс для удаления объекта Person с подтверждением."""
    model = Person
    template_name = 'family_tree/person_delete.html'
    context_object_name = 'object'
    success_url = reverse_lazy('family_tree:persons')
    login_url = 'users:user_login'


class TreeView(DetailView):
    """Класс-представление, показывающее генеалогическое дерево
    с корнем в выбранном человеке."""
    model = Person
    template_name = 'family_tree/tree.html'
    context_object_name = 'root_person'

    def get_object(self, queryset=None):
        """Переопределяем метод, чтобы задать person_id по умолчанию"""
        pk = self.kwargs.get('person_id')
        if pk is None:
            pk = 12
        return get_object_or_404(Person, pk=pk)


class TreeDataView(APIView):
    """API для получения данных генеалогического дерева потомков человека."""

    def get(self, request, person_id):
        """Это метод, который отвечает на GET-запрос."""
        root = get_object_or_404(Person, pk=person_id)
        data = self.build_descendants_tree(root, is_spouse=False)
        return Response(data, status=status.HTTP_200_OK)

    def build_descendants_tree(self, person, is_spouse=False):
        """Метод строит дерево потомков для конкретного человека person."""
        spouse = person.spouse
        pair_html = render_to_string('family_tree/includes/inc_card_pair.html', {
            'person': person,
            'spouse': spouse if not is_spouse else None,
        })

        children_nodes = []
        if not is_spouse:
            for child in person.children():
                children_nodes.append(self.build_descendants_tree(child))

        return {
            'innerHTML': pair_html,
            'children': children_nodes,
            'person_id': person.id,
            'spouse_id': spouse.id if spouse else None,
        }


class SpouseTreeDataView(APIView):
    """API для получения данных генеалогического дерева предков (родителей) супруга/супруги."""

    def get(self, request, spouse_id):
        """Это метод, который отвечает на GET-запрос."""
        spouse = get_object_or_404(Person, pk=spouse_id)
        data = self.build_ancestors_tree(spouse)
        return Response(data, status=status.HTTP_200_OK)

    def build_ancestors_tree(self, person):
        """Функция строит родословную (только вверх: от человека к его родителям)"""
        pair_html = render_to_string('family_tree/includes/inc_card_pair.html', {
            'person': person,
            'spouse': person.spouse,
        })

        parents_nodes = []
        if person.father and person.mother:
            parents_nodes.append(self.build_ancestors_tree(person.father))
        elif person.father:
            parents_nodes.append(self.build_ancestors_tree(person.father))
        elif person.mother:
            parents_nodes.append(self.build_ancestors_tree(person.mother))

        return {
            'innerHTML': pair_html,
            'children': parents_nodes,
            'person_id': person.id,
            'spouse_id': person.spouse.id if person.spouse else None,
        }

