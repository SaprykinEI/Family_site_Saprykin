from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.urls import reverse_lazy
from django.views.generic import ListView, View, CreateView
from django.http import JsonResponse
from django.utils.dateparse import parse_date

from events.models import Event
from events.forms import EventForm
from users.models import UserRoles


class EventListView(LoginRequiredMixin, ListView):
    model = Event
    template_name = 'events/calendar.html'
    context_object_name = 'events'


class EventJsonView(View):
    def get(self, request, *args, **kwargs):
        events = Event.objects.all()

        # Формируем список событий для FullCalendar
        events_list = []
        for event in events:
            events_list.append({
                "id": event.id,
                "title": event.title,
                "start": event.date.isoformat(),  # дата начала
                # если нужна end_date, можно добавить "end": event.end_date.isoformat()
                "allDay": True,
                # Можно добавить дополнительные поля при необходимости
            })
        return JsonResponse(events_list, safe=False)

class EventCreateView(LoginRequiredMixin, CreateView):
    model = Event
    form_class = EventForm
    template_name = 'events/create_event_form.html'
    success_url = reverse_lazy('events:events_list')

    def dispatch(self, request, *args, **kwargs):
        if request.user.role not in [UserRoles.ADMIN, UserRoles.MODERATOR]:
            raise PermissionDenied("У вас нет прав для добавления событий")
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Добавление события в календарь"
        return context