from django import forms
from events.models import Event


class EventForm(forms.ModelForm):
    """ Форма для создания и редактирования события (Event).
    - Основана на модели Event.
    - Исключает поля 'slug' и 'owner' — они заполняются автоматически.
    - Настраивает виджеты для удобного ввода данных """
    class Meta:
        model = Event
        fields = '__all__'
        exclude = ['slug', 'owner']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}, format='%Y-%m-%d'),
            'description': forms.Textarea(attrs={'rows': 3}),
            'people': forms.SelectMultiple(attrs={'size': 5}),
            'categories': forms.SelectMultiple(attrs={'size': 5}),
            'album': forms.Select(),
        }

        labels = {
            'title': 'Название',
            'date': 'Дата',
            'repeat': 'Повтор',
            'event_type': 'Тип события',
            'description': 'Описание',
            'people': 'Связанные лица',
            'categories': 'Категории',
            'is_reminder_enabled': 'Напоминание',
            'is_in_timeline': 'Показывать в хронологии',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['date'].input_formats = ['%Y-%m-%d']
