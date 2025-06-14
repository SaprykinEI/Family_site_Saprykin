from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import ListView, FormView, CreateView
from django.db.models import Q, F, Value, CharField
from django.db.models.functions import ExtractYear
from rest_framework.generics import get_object_or_404
from rest_framework.reverse import reverse_lazy

from gallery.models import Album, Category, Tag, Photo
from gallery.forms import AlbumCreateForm, PhotoUploadForm

from family_tree.models import Person


class AlbumListView(ListView):
    model = Album
    template_name = 'gallery/albums_list.html'
    context_object_name = 'albums'
    paginate_by = 12

    def get_queryset(self):
        qs = Album.objects.all().select_related('category').prefetch_related(
            'photos__tags', 'photos__people', 'videos__tags', 'videos__people'
        ).distinct()

        category_ids = self.request.GET.getlist('category')
        years = self.request.GET.getlist('year')
        tag_ids = self.request.GET.getlist('tag')
        person_id = self.request.GET.get('person')  # одно значение
        search = self.request.GET.get('search', '').strip()

        if category_ids:
            qs = qs.filter(category__id__in=category_ids)

        if years:
            years_int = [int(y) for y in years if y.isdigit()]
            if years_int:
                qs = qs.annotate(year=ExtractYear('date')).filter(year__in=years_int)

        if tag_ids:
            qs = qs.filter(
                Q(photos__tags__id__in=tag_ids) | Q(videos__tags__id__in=tag_ids)
            )

        if person_id and person_id.isdigit():
            qs = qs.filter(
                Q(photos__people__id=person_id) | Q(videos__people__id=person_id)
            )

        if search:
            qs = qs.filter(title__icontains=search)

        return qs.distinct()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['categories'] = Category.objects.all()
        context['years'] = Album.objects.dates('date', 'year', order='DESC')
        context['tags'] = Tag.objects.all()
        context['persons'] = Person.objects.all()

        def safe_int_list(param_list):
            return [int(x) for x in param_list if x.isdigit()]

        context['selected_categories'] = safe_int_list(self.request.GET.getlist('category'))
        context['selected_years'] = safe_int_list(self.request.GET.getlist('year'))
        context['selected_tags'] = safe_int_list(self.request.GET.getlist('tag'))
        context['selected_persons'] = safe_int_list(self.request.GET.getlist('person'))
        context['search'] = self.request.GET.get('search', '')

        return context


class AlbumCreateView(CreateView):
    """Класс создания альбома"""

    model = Album
    form_class = AlbumCreateForm
    template_name = 'gallery/album_create.html'

    def form_valid(self, form):
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('gallery:photo_upload', kwargs={'album_id': self.object.id})


class PhotoUploadView(FormView):
    """Класс загрузки фотографий"""
    template_name = 'gallery/photo_upload.html'
    form_class = PhotoUploadForm

    def dispatch(self, request, *args, **kwargs):
        """Получение альбома по id из url"""
        self.album = get_object_or_404(Album, id=kwargs['album_id'])
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        """Сохранение фото, связанного с альбомом"""
        photo = form.save(commit=False)
        photo.album = self.album
        photo.save()
        return redirect('gallery:photo_upload', album_id=self.album.id)

    def get_context_data(self, **kwargs):
        """Добавление альбома в шаблон"""
        context = super().get_context_data(**kwargs)
        context['album'] = self.album
        return context
