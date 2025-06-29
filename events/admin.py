from django.contrib import admin

from events.models import Event


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'date', 'event_type')
    list_filter = ('date', 'event_type', 'categories')
    search_fields = ('title', 'event_type')
    filter_horizontal = ('people', 'categories')
    date_hierarchy = 'date'
    ordering = ("-date",)
    prepopulated_fields = {'slug': ('title', 'date')}
