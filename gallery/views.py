from django.shortcuts import render
from django.views.generic import ListView

from gallery.models import Tag, Category, Album, Photo, Video

from family_tree.models import Person

class AlbumListView(ListView):
    model = Album
    template_name = 'gallery/albums_list.html'
    context_object_name = 'albums'
    paginate_by = 12

    def get_queryset(self):
        queryset = Album.objects.all().order_by('-date')
        year = self.request.GET.get('year')
        person = self.request.GET.get('person')
        tag = self.request.GET.get('tag')
        category = self.request.GET.get('category')

        if year:
            queryset = queryset.filter(date__year=year)
        if category:
            queryset = queryset.filter(category_id=category)
        if person:
            queryset = queryset.filter(photos__people=person).distinct()
        if tag:
            queryset = queryset.filter(photos__tags=tag).distinct()

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Получаем уникальные года из всех альбомов
        context['years'] = sorted(set(
            album.date.year for album in Album.objects.all()
            if album.date
        ), reverse=True)
        context['tags'] = Tag.objects.all()
        context['people'] = Person.objects.all()
        context['categories'] = Category.objects.all()
        return context