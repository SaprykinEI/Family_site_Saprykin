from django.urls import path

from events.views import EventListView, EventJsonView, EventCreateView, EventDetailView

app_name = 'events'

urlpatterns = [
    path('', EventListView.as_view(), name='events_list'),
    path('api/events/', EventJsonView.as_view(), name='events_json'),

    path('create/', EventCreateView.as_view(), name='event_create'),
    path('event/<slug:slug>/', EventDetailView.as_view(), name='event_detail'),
]