from datetime import date

from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.urls import reverse_lazy
from django.views.generic import ListView, View, CreateView, DetailView, UpdateView, DeleteView
from django.http import JsonResponse
from django.utils.dateparse import parse_date

from gallery.models import Photo, Album
from events.models import Event
from events.forms import EventForm
from users.models import UserRoles
from events.constants import EVENT_TYPE_COLORS


class EventListView(LoginRequiredMixin, ListView):
    """ Представление для отображения списка событий в календаре.
    - Пользователь должен быть авторизован (LoginRequiredMixin).
    - Выводит все объекты модели Event. """
    model = Event
    template_name = 'events/calendar.html'
    context_object_name = 'events'


class EventJsonView(View):
    """ API-представление для получения списка событий в формате JSON. """
    def get(self, request, *args, **kwargs):
        events = Event.objects.all()

        start_str = request.GET.get('start')
        end_str = request.GET.get('end')

        if start_str:
            start_date = date.fromisoformat(start_str[:10])
        else:
            start_date = None

        if end_str:
            end_date = date.fromisoformat(end_str[:10])
        else:
            end_date = None

        events_list = []

        for event in events:
            if event.repeat == 'yearly':
                year = start_date.year if start_date else date.today().year
                try:
                    event_date_this_year = date(year, event.date.month, event.date.day)
                except ValueError:
                    continue
                if (start_date is None or event_date_this_year >= start_date) and \
                   (end_date is None or event_date_this_year <= end_date):
                    events_list.append({
                        "id": event.id,
                        "title": event.title,
                        "start": event_date_this_year.isoformat(),
                        "allDay": True,
                        "color": EVENT_TYPE_COLORS.get(event.event_type, '#808080'),
                        "slug": event.slug,
                    })
            else:
                event_date = event.date
                if (start_date is None or event_date >= start_date) and \
                   (end_date is None or event_date <= end_date):
                    events_list.append({
                        "id": event.id,
                        "title": event.title,
                        "start": event_date.isoformat(),
                        "allDay": True,
                        "color": EVENT_TYPE_COLORS.get(event.event_type, '#808080'),
                        "slug": event.slug,
                    })

        return JsonResponse(events_list, safe=False)


class EventCreateView(LoginRequiredMixin, CreateView):
    """ Представление для создания нового события в календаре. """
    model = Event
    form_class = EventForm
    template_name = 'events/create_event_form.html'
    success_url = reverse_lazy('events:events_list')

    def form_valid(self, form):
        """ Владелец события автоматически устанавливается как текущий пользователь. """
        form.instance.owner = self.request.user
        return super().form_valid(form)

    def dispatch(self, request, *args, **kwargs):
        """ Проверка уровней доступа
        - Доступ разрешён только администраторам и модераторам."""
        if request.user.role not in [UserRoles.ADMIN, UserRoles.MODERATOR]:
            raise PermissionDenied("У вас нет прав для добавления событий")
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        """ В контекст шаблона добавляется заголовок страницы. """
        context = super().get_context_data(**kwargs)
        context['title'] = "Добавление события в календарь"
        return context


class EventDetailView(LoginRequiredMixin, DetailView):
    """ Класс-представление для показа детальной страницы одного события
    - Доступ разрешён только авторизованным пользователям.
    - Использует поле slug из URL для поиска события.
    - В шаблон передаётся объект события под именем 'event'"""
    model = Event
    template_name = 'events/event_detail.html'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'
    context_object_name = 'event'

    def get_context_data(self, **kwargs):
        """ Если у события есть связанный альбом, в контекст добавляются
      все фотографии из этого альбома под ключом 'random_photos' """
        context = super().get_context_data(**kwargs)
        event = self.get_object()
        if event.album:
            photos = Photo.objects.filter(album=event.album).distinct()
        else:
            photos = Photo.objects.none()

        context['random_photos'] = photos
        return context


class EventUpdateView(LoginRequiredMixin, UpdateView):
    """ Представление для редактирования события. """
    model = Event
    form_class = EventForm
    template_name = 'events/update_event_form.html'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'

    def get_success_url(self):
        """ После успешного редактирования перенаправляет на страницу детали события. """
        return reverse_lazy('events:event_detail', kwargs={'slug': self.object.slug})

    def dispatch(self, request, *args, **kwargs):
        """ Только для авторизованных пользователей.
             - Администраторы могут редактировать любые события.
             - Модераторы могут редактировать только события, которые создали сами.
             - Остальные пользователи не имеют доступа и получают PermissionDenied."""
        self.object = self.get_object()
        user = request.user.role

        if user == UserRoles.ADMIN:
            return super().dispatch(request, *args, **kwargs)
        elif user == UserRoles.MODERATOR:
            if self.object.owner == self.request.user:
                return super().dispatch(request, *args, **kwargs)
            else:
                raise PermissionDenied ("Вы можете редактировать только свои события")
        else:
            raise PermissionDenied("У вас нет прав на редактирование события")


class EventDeleteView(LoginRequiredMixin, DeleteView):
    """ Представление для удаления события. """
    model = Event
    slug_field = 'slug'
    slug_url_kwarg = 'slug'
    template_name = 'events/event_confirm_delete.html'
    success_url = reverse_lazy('events:events_list')

    def dispatch(self, request, *args, **kwargs):
        """ Только для авторизованных пользователей.
        - Администраторы могут удалять любые события.
        - Модераторы могут удалять только свои собственные события.
        - Остальные пользователи не имеют прав на удаление и получают PermissionDenied. """
        self.object = self.get_object()
        user = request.user.role

        if user == UserRoles.ADMIN:
            return super().dispatch(request, *args, **kwargs)
        elif user == UserRoles.MODERATOR:
            if self.object.owner == self.request.user:
                return super().dispatch(request, *args, **kwargs)
            else:
                raise PermissionDenied("Вы можете удалять только свои события")
        else:
            raise PermissionDenied("У вас нет прав на удаление события")


