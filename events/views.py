from datetime import date

from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.urls import reverse_lazy
from django.views.generic import ListView, View, CreateView, DetailView, UpdateView, DeleteView
from django.http import JsonResponse
from django.utils.dateparse import parse_date

from events.models import Event
from events.forms import EventForm
from users.models import UserRoles
from events.constants import EVENT_TYPE_COLORS


class EventListView(LoginRequiredMixin, ListView):
    model = Event
    template_name = 'events/calendar.html'
    context_object_name = 'events'


class EventJsonView(View):
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
                        "slug": event.slug,  # Добавляем slug
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
                        "slug": event.slug,  # Добавляем slug
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

class EventDetailView(LoginRequiredMixin, DetailView):
    model = Event
    template_name = 'events/event_detail.html'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'
    context_object_name = 'event'

class EventUpdateView(LoginRequiredMixin, UpdateView):
    pass


class EventDeleteView(LoginRequiredMixin, DeleteView):
    pass