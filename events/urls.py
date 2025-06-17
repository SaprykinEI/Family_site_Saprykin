from django.urls import path

from events.views import EventListView, EventJsonView

app_name = 'events'

urlpatterns = [
    path('', EventListView.as_view(), name='events_list'),
    path('api/events/', EventJsonView.as_view(), name='events_json'),
]