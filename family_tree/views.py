from django.core.exceptions import PermissionDenied
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from datetime import date

from family_tree.models import Person
from family_tree.forms import PersonForm
from family_tree.services import get_person_cache, get_descendants_tree_cached, get_ancestors_tree_cached
from gallery.models import Album
from events.models import Event
from users.models import UserRoles


class IndexView(ListView):
    '''Представление для отображения главной страницы'''
    model = Person
    template_name = 'family_tree/index.html'
    context_object_name = 'person_list'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        today = date.today()
        this_year = today.year

        context['title'] = "<h1>Сайт семьи - Сапрыкины</h1>"
        context['latest_albums'] = Album.objects.order_by('-created_at')[:4]

        events = Event.objects.all()
        upcoming_events = []

        for event in events:
            # Предположим, event.date — дата первого события (год, месяц, день)
            month = event.date.month
            day = event.date.day

            # Событие в этом году
            event_date_this_year = date(this_year, month, day)

            # Если событие уже прошло в этом году, смотрим на следующий год
            if event_date_this_year < today:
                event_date_this_year = date(this_year + 1, month, day)

            # Добавляем событие в список, если оно попадает в ближайшие 30 дней, например
            if 0 <= (event_date_this_year - today).days <= 360:
                # Посчитаем возраст, если нужно
                age_years = None
                if event.event_type in ['birthday', 'wedding']:
                    age_years = event_date_this_year.year - event.date.year

                upcoming_events.append({
                    'title': event.title,
                    'date': event_date_this_year,
                    'original_date': event.date,
                    'photo_one': event.photo_one.url if event.photo_one else '',
                    'age_years': age_years,
                    'type': event.event_type,
                    'description': event.description,
                })

        # Сортируем по дате и берем первые 4
        upcoming_events.sort(key=lambda x: x['date'])
        context['events'] = upcoming_events[:4]
        return context




class PersonsListView(LoginRequiredMixin, ListView):
    '''Представление-класс для отображения всех членов семьи.'''
    model = Person
    template_name = 'family_tree/persons.html'
    context_object_name = 'persons'

    def get_queryset(self):
        """Получаем список Person с фильтром по поиску."""
        queryset = get_person_cache()
        search_query = self.request.GET.get('search', '').strip()
        if search_query:
            queryset = queryset.filter(
                Q(first_name__icontains=search_query) |
                Q(last_name__icontains=search_query)
            )
        return queryset

    def get_context_data(self, **kwargs):
        ''' Добавляем в контекст дополнительную информацию'''
        context = super().get_context_data(**kwargs)
        context['title'] = "Все члены семьи"
        context['search'] = self.request.GET.get('search', '').strip()
        return context


class PersonCreateView(LoginRequiredMixin, CreateView):
    '''Представление-класс для создания нового члена семьи.'''
    model = Person
    form_class = PersonForm
    template_name = 'family_tree/person_create_update.html'
    success_url = reverse_lazy('family_tree:persons')
    login_url = 'users:user_login'

    def dispatch(self, request, *args, **kwargs):
        if request.user.role not in [UserRoles.ADMIN, UserRoles.MODERATOR]:
            raise PermissionDenied("У вас нет прав для добавления членов семьи.")
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        '''Переопределяем поведение при успешной валидации формы.'''
        form.instance.creator = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        """Добавляем заголовок страницы в контекст шаблона."""
        context = super().get_context_data(**kwargs)
        context['title'] = "Добавить члена семьи"
        return context


class PersonDetailView(LoginRequiredMixin, DetailView):
    '''Представление-класс для отображения подробной информации о человеке'''
    model = Person
    slug_field = 'slug'
    slug_url_kwarg = 'slug'
    template_name = 'family_tree/person_detail.html'
    context_object_name = 'person'

    def get_context_data(self, **kwargs):
        '''Добавляем заголовка в шаблон.'''
        context = super().get_context_data(**kwargs)
        person = self.object

        photos_queryset = person.photos.all()
        random_photos = photos_queryset.order_by('?')[:10]
        context['random_photos'] = random_photos
        context['title'] = self.object
        return context


class PersonUpdateView(LoginRequiredMixin, UpdateView):
    '''Представление-класс для редактирования данных о человеке.'''
    model = Person
    slug_field = 'slug'
    slug_url_kwarg = 'slug'
    form_class = PersonForm
    template_name = 'family_tree/person_create_update.html'
    context_object_name = 'object'
    login_url = 'users:user_login'

    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.user

        if user.role == UserRoles.ADMIN:
            return queryset
        elif user.role == UserRoles.MODERATOR:
            return queryset.filter(creator=user)
        return queryset.none()

    def get_context_data(self, **kwargs):
        """Добавляем заголовок в контекст шаблона."""
        context = super().get_context_data(**kwargs)
        context['title'] = 'Редактировать данные'
        return context

    def get_success_url(self):
        """После успешного сохранения — перейти на страницу детального просмотра."""
        return reverse('family_tree:person_detail', kwargs={'slug': self.object.slug})


class PersonDeleteView(LoginRequiredMixin, DeleteView):
    """Представление-класс для удаления объекта Person с подтверждением."""
    model = Person
    slug_field = 'slug'
    slug_url_kwarg = 'slug'
    template_name = 'family_tree/person_delete.html'
    context_object_name = 'object'
    success_url = reverse_lazy('family_tree:persons')
    login_url = 'users:user_login'

    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.user

        if user.role == UserRoles.ADMIN:
            return queryset
        elif user.role == UserRoles.MODERATOR:
            return queryset.filter(creator=user)
        return queryset.none()


class TreeView(LoginRequiredMixin, DetailView):
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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Семейное дерево"
        context['people'] = Person.objects.all()
        return context


class TreeDataView(APIView):
    """API для получения данных генеалогического дерева потомков человека."""

    def get(self, request, person_id):
        """Это метод, который отвечает на GET-запрос."""
        root = get_object_or_404(Person, pk=person_id)
        data = get_descendants_tree_cached(root, self.build_descendants_tree)
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
        data = get_ancestors_tree_cached(spouse, self.build_ancestors_tree)
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

