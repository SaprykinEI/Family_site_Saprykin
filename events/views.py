from django.views.generic import ListView, View
from django.http import JsonResponse
from django.utils.dateparse import parse_date

from events.models import Event


class EventListView(ListView):
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